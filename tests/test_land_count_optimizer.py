from thun_deckbuilder.land_count_optimizer import (
    LandCountCandidate,
    choose_land_count,
    consistency_score,
)
from thun_deckbuilder.opening_hand_simulator import OpeningHandReport


def report(*, playable, lands_ok, early=90, core=80, screw=5, flood=5):
    return OpeningHandReport(
        samples=2000,
        playable_hands_pct=playable,
        two_to_four_lands_pct=lands_ok,
        early_play_pct=early,
        core_by_turn_three_pct=core,
        mana_screw_pct=screw,
        mana_flood_pct=flood,
    )


def test_consistency_score_rewards_playable_hands_and_penalizes_mana_risk():
    stable = report(playable=82, lands_ok=88, screw=4, flood=5)
    risky = report(playable=70, lands_ok=75, screw=14, flood=10)
    assert consistency_score(stable) > consistency_score(risky)


def test_choose_land_count_uses_simulation_score():
    candidates = (
        LandCountCandidate(22, "low", report(playable=73, lands_ok=79, screw=12, flood=3)),
        LandCountCandidate(23, "best", report(playable=82, lands_ok=88, screw=5, flood=5)),
        LandCountCandidate(24, "high", report(playable=78, lands_ok=85, screw=3, flood=11)),
    )
    chosen = choose_land_count(candidates, preferred_lands=24)
    assert chosen.lands == 23
    assert chosen.payload == "best"


def test_choose_land_count_prefers_profile_land_count_on_equal_reports():
    same = report(playable=80, lands_ok=86)
    candidates = (
        LandCountCandidate(23, "near", same),
        LandCountCandidate(24, "preferred", same),
        LandCountCandidate(25, "near-high", same),
    )
    assert choose_land_count(candidates, preferred_lands=24).lands == 24


def test_choose_land_count_rejects_empty_candidates():
    try:
        choose_land_count((), preferred_lands=24)
    except ValueError as exc:
        assert "At least one" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
