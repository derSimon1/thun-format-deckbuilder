from thun_deckbuilder.card_contribution import CardContribution, RoleContribution
from thun_deckbuilder.deck_profile import CurveTarget, DeckProfile, RoleTarget
from thun_deckbuilder.deck_quality import DeckQualityAnalyzer
from thun_deckbuilder.deck_state import DeckState


def contribution(name: str, role: str, mana_value: float) -> CardContribution:
    return CardContribution(
        card_name=name,
        mana_value=mana_value,
        is_land=False,
        roles=(RoleContribution(role, 1.0),),
        tags=frozenset(),
    )


def test_quality_report_scores_complete_profile_at_100() -> None:
    profile = DeckProfile(
        name="Complete",
        lands=0,
        role_targets=(RoleTarget("burn", minimum=2, target=2),),
        curve_targets=(CurveTarget(1, 2),),
    )
    state = DeckState().with_card(contribution("Bolt", "burn", 1), 2)

    report = DeckQualityAnalyzer().analyze(state, profile)

    assert report.overall_score == 100
    assert report.minimums_met
    assert report.role_quality[0].target_met
    assert report.curve_quality[0].target_met


def test_quality_report_exposes_missing_mandatory_role() -> None:
    profile = DeckProfile(
        name="Incomplete",
        lands=0,
        role_targets=(RoleTarget("removal", minimum=2, target=4),),
    )
    state = DeckState().with_card(contribution("Answer", "removal", 2), 1)

    report = DeckQualityAnalyzer().analyze(state, profile)

    assert not report.minimums_met
    assert report.role_quality[0].current == 1
    assert report.role_quality[0].score == 25
    assert report.overall_score == 48


def test_quality_score_is_capped_when_target_is_exceeded() -> None:
    profile = DeckProfile(
        name="Capped",
        lands=0,
        role_targets=(RoleTarget("card_draw", minimum=0, target=1),),
    )
    state = DeckState().with_card(contribution("Draw", "card_draw", 2), 3)

    report = DeckQualityAnalyzer().analyze(state, profile)

    assert report.role_quality[0].score == 100
    assert report.overall_score == 100
