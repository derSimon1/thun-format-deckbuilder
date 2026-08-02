from thun_deckbuilder.land_count_optimizer import (
    LandCountCandidate,
    choose_land_count,
    consistency_score,
)
from thun_deckbuilder.opening_hand_simulator import OpeningHandReport


def report(
    *,
    playable,
    lands_ok,
    post_mulligan=None,
    mulligan=20,
    early=90,
    core=80,
    screw=5,
    flood=5,
):
    return OpeningHandReport(
        samples=2000,
        playable_hands_pct=playable,
        playable_after_mulligan_pct=(
            post_mulligan if post_mulligan is not None else min(100, playable + 10)
        ),
        mulligan_to_six_pct=mulligan,
        two_to_four_lands_pct=lands_ok,
        early_play_pct=early,
        core_by_turn_three_pct=core,
        mana_screw_pct=screw,
        mana_flood_pct=flood,
    )


def test_consistency_score_rewards_post_mulligan_playability_and_penalizes_risk():
    stable = report(playable=82, post_mulligan=94, lands_ok=88, mulligan=18, screw=4, flood=5)
    risky = report(playable=70, post_mulligan=82, lands_ok=75, mulligan=30, screw=14, flood=10)
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


def test_low_curve_land_choice_balances_playability_against_turn_three_flood():
    candidates = (
        LandCountCandidate(
            20,
            "twenty",
            report(
                playable=70,
                post_mulligan=92,
                lands_ok=92,
                mulligan=30,
                early=100,
                core=100,
                screw=2,
                flood=18,
            ),
        ),
        LandCountCandidate(
            21,
            "twenty-one",
            report(
                playable=73,
                post_mulligan=94,
                lands_ok=94,
                mulligan=27,
                early=100,
                core=100,
                screw=2,
                flood=21,
            ),
        ),
        LandCountCandidate(
            22,
            "twenty-two",
            report(
                playable=76,
                post_mulligan=95,
                lands_ok=95,
                mulligan=24,
                early=100,
                core=100,
                screw=1,
                flood=25,
            ),
        ),
    )
    chosen = choose_land_count(candidates, preferred_lands=20)
    assert chosen.lands == 21
    assert chosen.payload == "twenty-one"


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
