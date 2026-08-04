import json

import pytest

from thun_deckbuilder.matchup_calibration import (
    MatchupObservationError,
    build_calibration_report,
    load_observations,
)


HASH_A = "a" * 64
HASH_B = "b" * 64


def _global_report():
    return {
        "archetypes": {
            "tokens": {"opening_hand_plan": {"deck_hash": HASH_A}},
            "artifacts": {"opening_hand_plan": {"deck_hash": HASH_B}},
        },
        "matchups": [
            {
                "archetype_a": "tokens",
                "archetype_b": "artifacts",
                "wins_a_pct": 0,
                "wins_b_pct": 94,
                "draws_pct": 6,
            }
        ],
        "best_of_three": [],
    }


def _observation(**changes):
    result = {
        "id": "league-001",
        "archetype_a": "tokens",
        "archetype_b": "artifacts",
        "deck_hash_a": HASH_A,
        "deck_hash_b": HASH_B,
        "context": "game_one",
        "games": 20,
        "wins_a": 9,
        "wins_b": 10,
        "draws": 1,
        "observed_at": "2026-08-04",
        "source": "signed league sheet 001",
    }
    result.update(changes)
    return result


def _write(tmp_path, observations, *, schema_version=1):
    path = tmp_path / "observations.json"
    path.write_text(
        json.dumps({"schema_version": schema_version, "observations": observations}),
        encoding="utf-8",
    )
    return path


def test_empty_evidence_is_explicit_and_does_not_claim_calibration(tmp_path):
    observations = load_observations(_write(tmp_path, []))
    result = build_calibration_report(_global_report(), observations)

    assert result["status"] == "NO_EMPIRICAL_DATA"
    assert result["read_only"] is True
    assert result["matched_games"] == 0
    assert result["weighted_mean_absolute_error_pct"] is None


def test_hash_matched_evidence_reports_error_without_changing_prediction(tmp_path):
    observations = load_observations(_write(tmp_path, [_observation()]))
    source = _global_report()
    result = build_calibration_report(source, observations)

    assert result["status"] == "CALIBRATION_AVAILABLE"
    assert result["observations_matched"] == 1
    assert result["matched_games"] == 20
    assert result["weighted_mean_absolute_error_pct"] == 30.0
    assert result["entries"][0]["predicted_wins_a_pct"] == 0
    assert result["entries"][0]["observed_wins_b_pct"] == 50.0
    assert result["entries"][0]["observed_draws_pct"] == 5.0
    assert source["matchups"][0]["wins_a_pct"] == 0


def test_reversed_observation_orientation_is_normalized(tmp_path):
    reversed_row = _observation(
        archetype_a="artifacts",
        archetype_b="tokens",
        deck_hash_a=HASH_B,
        deck_hash_b=HASH_A,
        wins_a=10,
        wins_b=9,
    )
    result = build_calibration_report(
        _global_report(), load_observations(_write(tmp_path, [reversed_row]))
    )

    assert result["entries"][0]["observed_wins_a_pct"] == 45.0


def test_stale_deck_hash_is_excluded_from_calibration(tmp_path):
    stale = _observation(deck_hash_a="c" * 64)
    result = build_calibration_report(
        _global_report(), load_observations(_write(tmp_path, [stale]))
    )

    assert result["status"] == "NO_CURRENT_MATCHES"
    assert result["stale_hash_observations"] == 1
    assert result["matched_games"] == 0


def test_less_than_twenty_games_stays_insufficient(tmp_path):
    short = _observation(games=19, wins_a=9, wins_b=9, draws=1)
    result = build_calibration_report(
        _global_report(), load_observations(_write(tmp_path, [short]))
    )

    assert result["status"] == "INSUFFICIENT_DATA"
    assert result["entries"][0]["reliable_sample"] is False


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"games": 21}, "games must equal"),
        ({"deck_hash_a": "A" * 64}, "lowercase SHA-256"),
        ({"context": "casual"}, "unsupported context"),
        ({"observed_at": "04.08.2026"}, "YYYY-MM-DD"),
        ({"observed_at": "20260804"}, "YYYY-MM-DD"),
    ],
)
def test_invalid_evidence_is_rejected(tmp_path, change, message):
    path = _write(tmp_path, [_observation(**change)])

    with pytest.raises(MatchupObservationError, match=message):
        load_observations(path)


def test_unknown_schema_version_is_rejected(tmp_path):
    with pytest.raises(MatchupObservationError, match="unsupported"):
        load_observations(_write(tmp_path, [], schema_version=2))
