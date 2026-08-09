from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
MINIMUM_RELIABLE_GAMES = 20
CONTEXTS = frozenset({"game_one", "postboard", "match"})
_HASH = re.compile(r"[0-9a-f]{64}")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_ROOT_FIELDS = frozenset({"schema_version", "observations"})
_OBSERVATION_FIELDS = frozenset(
    {
        "id",
        "archetype_a",
        "archetype_b",
        "deck_hash_a",
        "deck_hash_b",
        "context",
        "games",
        "wins_a",
        "wins_b",
        "draws",
        "observed_at",
        "source",
    }
)


class MatchupObservationError(ValueError):
    """Raised when empirical matchup evidence violates the versioned schema."""


def _require_string(observation: dict[str, object], field: str, index: int) -> str:
    value = observation[field]
    if not isinstance(value, str) or not value.strip():
        raise MatchupObservationError(
            f"observation {index}: {field} must be a non-empty string"
        )
    normalized = value.strip()
    observation[field] = normalized
    return normalized


def _validate_observation(raw: object, index: int) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise MatchupObservationError(f"observation {index}: expected an object")
    fields = frozenset(raw)
    if fields != _OBSERVATION_FIELDS:
        missing = sorted(_OBSERVATION_FIELDS - fields)
        unknown = sorted(fields - _OBSERVATION_FIELDS)
        raise MatchupObservationError(
            f"observation {index}: schema fields differ; missing={missing}, unknown={unknown}"
        )

    observation = dict(raw)
    observation_id = _require_string(observation, "id", index)
    archetype_a = _require_string(observation, "archetype_a", index)
    archetype_b = _require_string(observation, "archetype_b", index)
    if archetype_a == archetype_b:
        raise MatchupObservationError(
            f"observation {index} ({observation_id}): archetypes must differ"
        )

    for field in ("deck_hash_a", "deck_hash_b"):
        value = _require_string(observation, field, index)
        if _HASH.fullmatch(value) is None:
            raise MatchupObservationError(
                f"observation {index} ({observation_id}): {field} must be a lowercase SHA-256"
            )

    context = _require_string(observation, "context", index)
    if context not in CONTEXTS:
        raise MatchupObservationError(
            f"observation {index} ({observation_id}): unsupported context {context!r}"
        )

    counts: dict[str, int] = {}
    for field in ("games", "wins_a", "wins_b", "draws"):
        value = observation[field]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise MatchupObservationError(
                f"observation {index} ({observation_id}): {field} must be a non-negative integer"
            )
        counts[field] = value
    if counts["games"] <= 0:
        raise MatchupObservationError(
            f"observation {index} ({observation_id}): games must be positive"
        )
    if counts["games"] != counts["wins_a"] + counts["wins_b"] + counts["draws"]:
        raise MatchupObservationError(
            f"observation {index} ({observation_id}): games must equal wins_a + wins_b + draws"
        )

    observed_at = _require_string(observation, "observed_at", index)
    if _DATE.fullmatch(observed_at) is None:
        raise MatchupObservationError(
            f"observation {index} ({observation_id}): observed_at must be YYYY-MM-DD"
        )
    try:
        date.fromisoformat(observed_at)
    except ValueError as error:
        raise MatchupObservationError(
            f"observation {index} ({observation_id}): observed_at must be YYYY-MM-DD"
        ) from error
    _require_string(observation, "source", index)
    return observation


def load_observations(path: Path) -> tuple[dict[str, object], ...]:
    """Load and strictly validate real, externally recorded matchup results."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise MatchupObservationError(f"cannot load {path}: {error}") from error
    if not isinstance(payload, dict) or frozenset(payload) != _ROOT_FIELDS:
        raise MatchupObservationError(
            "observation root must contain exactly schema_version and observations"
        )
    if payload["schema_version"] != SCHEMA_VERSION:
        raise MatchupObservationError(
            f"unsupported matchup observation schema {payload['schema_version']!r}; expected {SCHEMA_VERSION}"
        )
    observations = payload["observations"]
    if not isinstance(observations, list):
        raise MatchupObservationError("observations must be an array")
    validated = tuple(
        _validate_observation(observation, index)
        for index, observation in enumerate(observations)
    )
    identifiers = [str(observation["id"]) for observation in validated]
    if len(identifiers) != len(set(identifiers)):
        raise MatchupObservationError("observation ids must be unique")
    return validated


def _deck_hashes(report: dict[str, object]) -> dict[str, str]:
    archetypes = report.get("archetypes", {})
    if not isinstance(archetypes, dict):
        return {}
    result: dict[str, str] = {}
    for archetype, raw_metrics in archetypes.items():
        if not isinstance(raw_metrics, dict):
            continue
        hand = raw_metrics.get("opening_hand_plan") or raw_metrics.get("opening_hand")
        if isinstance(hand, dict) and isinstance(hand.get("deck_hash"), str):
            result[str(archetype)] = str(hand["deck_hash"])
    return result


def _predictions(report: dict[str, object]) -> list[dict[str, object]]:
    predictions: list[dict[str, object]] = []
    for raw in report.get("matchups", []):
        if isinstance(raw, dict):
            predictions.append(
                {
                    "archetype_a": raw["archetype_a"],
                    "archetype_b": raw["archetype_b"],
                    "context": "game_one",
                    "wins_a_pct": raw["wins_a_pct"],
                    "wins_b_pct": raw["wins_b_pct"],
                    "draws_pct": raw["draws_pct"],
                }
            )
    for raw in report.get("best_of_three", []):
        if not isinstance(raw, dict):
            continue
        predictions.append(
            {
                "archetype_a": raw["archetype_a"],
                "archetype_b": raw["archetype_b"],
                "context": "match",
                "wins_a_pct": raw["match_wins_a_pct"],
                "wins_b_pct": raw["match_wins_b_pct"],
                "draws_pct": 0,
            }
        )
        postboard = raw.get("postboard")
        if isinstance(postboard, dict):
            predictions.append(
                {
                    "archetype_a": raw["archetype_a"],
                    "archetype_b": raw["archetype_b"],
                    "context": "postboard",
                    "wins_a_pct": postboard["wins_a_pct"],
                    "wins_b_pct": postboard["wins_b_pct"],
                    "draws_pct": postboard["draws_pct"],
                }
            )
    return predictions


def _canonical_pair(archetype_a: str, archetype_b: str) -> tuple[str, str]:
    return tuple(sorted((archetype_a, archetype_b)))  # type: ignore[return-value]


def build_calibration_report(
    global_report: dict[str, object],
    observations: tuple[dict[str, object], ...],
) -> dict[str, object]:
    """Compare current heuristic predictions with hash-matched real evidence.

    This function reports error and coverage only. It never feeds observations
    back into deck selection, scoring or matchup simulation.
    """

    deck_hashes = _deck_hashes(global_report)
    predictions = _predictions(global_report)
    prediction_by_key = {
        (
            *_canonical_pair(
                str(item["archetype_a"]), str(item["archetype_b"])
            ),
            str(item["context"]),
        ): item
        for item in predictions
    }
    grouped: dict[
        tuple[str, str, str], list[tuple[dict[str, object], bool]]
    ] = defaultdict(list)
    stale_hash_observations = 0
    unsupported_observations = 0

    for observation in observations:
        archetype_a = str(observation["archetype_a"])
        archetype_b = str(observation["archetype_b"])
        key = (*_canonical_pair(archetype_a, archetype_b), str(observation["context"]))
        if key not in prediction_by_key:
            unsupported_observations += 1
            continue
        hashes_match = (
            deck_hashes.get(archetype_a) == observation["deck_hash_a"]
            and deck_hashes.get(archetype_b) == observation["deck_hash_b"]
        )
        if not hashes_match:
            stale_hash_observations += 1
            continue
        prediction = prediction_by_key[key]
        reversed_orientation = archetype_a != prediction["archetype_a"]
        grouped[key].append((observation, reversed_orientation))

    entries: list[dict[str, object]] = []
    weighted_error = 0.0
    matched_games = 0
    matched_observations = 0
    for key in sorted(grouped):
        rows = grouped[key]
        prediction = prediction_by_key[key]
        wins_a = wins_b = draws = games = 0
        identifiers: list[str] = []
        for observation, reversed_orientation in rows:
            games += int(observation["games"])
            draws += int(observation["draws"])
            identifiers.append(str(observation["id"]))
            if reversed_orientation:
                wins_a += int(observation["wins_b"])
                wins_b += int(observation["wins_a"])
            else:
                wins_a += int(observation["wins_a"])
                wins_b += int(observation["wins_b"])
        observed_a_pct = wins_a * 100 / games
        observed_b_pct = wins_b * 100 / games
        observed_draws_pct = draws * 100 / games
        outcome_errors = (
            abs(float(prediction["wins_a_pct"]) - observed_a_pct),
            abs(float(prediction["wins_b_pct"]) - observed_b_pct),
            abs(float(prediction["draws_pct"]) - observed_draws_pct),
        )
        absolute_error = sum(outcome_errors) / len(outcome_errors)
        weighted_error += absolute_error * games
        matched_games += games
        matched_observations += len(rows)
        entries.append(
            {
                "archetype_a": prediction["archetype_a"],
                "archetype_b": prediction["archetype_b"],
                "context": prediction["context"],
                "deck_hash_a": deck_hashes.get(str(prediction["archetype_a"])),
                "deck_hash_b": deck_hashes.get(str(prediction["archetype_b"])),
                "observation_ids": sorted(identifiers),
                "games": games,
                "predicted_wins_a_pct": prediction["wins_a_pct"],
                "predicted_wins_b_pct": prediction["wins_b_pct"],
                "predicted_draws_pct": prediction["draws_pct"],
                "observed_wins_a_pct": round(observed_a_pct, 2),
                "observed_wins_b_pct": round(observed_b_pct, 2),
                "observed_draws_pct": round(observed_draws_pct, 2),
                "mean_absolute_outcome_error_pct": round(absolute_error, 2),
                "reliable_sample": games >= MINIMUM_RELIABLE_GAMES,
            }
        )

    if not observations:
        status = "NO_EMPIRICAL_DATA"
    elif matched_games == 0:
        status = "NO_CURRENT_MATCHES"
    elif any(bool(entry["reliable_sample"]) for entry in entries):
        status = "CALIBRATION_AVAILABLE"
    else:
        status = "INSUFFICIENT_DATA"
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "read_only": True,
        "minimum_reliable_games": MINIMUM_RELIABLE_GAMES,
        "predictions_total": len(predictions),
        "observations_total": len(observations),
        "observations_matched": matched_observations,
        "stale_hash_observations": stale_hash_observations,
        "unsupported_observations": unsupported_observations,
        "matched_games": matched_games,
        "prediction_coverage_pct": round(len(entries) * 100 / max(1, len(predictions)), 2),
        "weighted_mean_absolute_error_pct": (
            round(weighted_error / matched_games, 2) if matched_games else None
        ),
        "entries": entries,
    }
