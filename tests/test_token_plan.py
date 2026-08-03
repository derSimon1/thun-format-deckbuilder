from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import CardAnalysis, analyze_card
from thun_deckbuilder.token_plan import TokenPlan, detect_token_plan
from thun_deckbuilder.token_scoring import score_token_card


@dataclass(frozen=True)
class Candidate:
    analysis: CardAnalysis
    roles: frozenset[str]


def candidate(
    name: str,
    oracle_text: str,
    roles: tuple[str, ...] = (),
    *,
    mana_value: int = 2,
    type_line: str = "Enchantment",
) -> Candidate:
    raw = {
        "name": name,
        "mana_value": mana_value,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    return Candidate(
        analysis=analyze_card(raw),
        roles=frozenset(roles),
    )


def test_detects_go_wide_from_multiple_makers_and_anthem():
    report = detect_token_plan(
        (
            candidate(
                "Raise the Team",
                "Create three 1/1 white Soldier creature tokens.",
                ("token_maker",),
                type_line="Sorcery",
            ),
            candidate(
                "Battle Anthem",
                "Creature tokens you control get +1/+1.",
                ("token_payoff", "anthem"),
                mana_value=3,
            ),
            candidate(
                "Gather the Squad",
                "Create two 1/1 white Soldier creature tokens.",
                ("token_maker",),
                type_line="Sorcery",
            ),
        )
    )

    assert report.plan is TokenPlan.GO_WIDE
    assert report.score_for(TokenPlan.GO_WIDE) > report.score_for(TokenPlan.VALUE)


def test_detects_value_tokens_from_repeatable_engine_and_card_advantage():
    report = detect_token_plan(
        (
            candidate(
                "End Step Engine",
                "At the beginning of your end step, create a 1/1 white Soldier creature token.",
                ("token_maker",),
                mana_value=3,
            ),
            candidate(
                "Token Mentor",
                "Whenever a token enters under your control, draw a card.",
                ("token_payoff", "card_draw"),
                mana_value=3,
            ),
            candidate(
                "Clue Captain",
                "Whenever one or more creatures attack, investigate.",
                ("card_draw",),
            ),
        )
    )

    assert report.plan is TokenPlan.VALUE
    assert report.confidence > 0.5


def test_detects_aristocrats_only_with_fodder_outlet_and_death_payoff():
    report = detect_token_plan(
        (
            candidate(
                "Fodder",
                "Create two 1/1 white creature tokens.",
                ("token_maker",),
                type_line="Sorcery",
            ),
            candidate(
                "Sacrifice Outlet",
                "Sacrifice another creature: Scry 1.",
                ("sacrifice",),
                type_line="Creature — Cleric",
            ),
            candidate(
                "Death Drain",
                "Whenever another creature dies, each opponent loses 1 life and you gain 1 life.",
                ("token_payoff",),
                mana_value=3,
                type_line="Creature — Cleric",
            ),
        )
    )

    assert report.plan is TokenPlan.ARISTOCRATS
    assert dict(report.support)[TokenPlan.ARISTOCRATS] == 3
    assert report.score_for(TokenPlan.ARISTOCRATS) > report.score_for(TokenPlan.GO_WIDE)


def test_food_and_one_shot_sacrifice_do_not_fabricate_aristocrats():
    report = detect_token_plan(
        (
            candidate(
                "Food Maker",
                "Create a Food token.",
                ("token_maker",),
                type_line="Artifact",
            ),
            candidate(
                "Additional Cost",
                "As an additional cost to cast this spell, sacrifice a creature. Draw two cards.",
                ("sacrifice", "card_draw"),
                type_line="Sorcery",
            ),
            candidate(
                "Self Death",
                "When this creature dies, create a Food token.",
                ("token_maker", "sacrifice"),
                type_line="Creature — Ox",
            ),
            candidate(
                "Real Maker",
                "Create two 1/1 white Soldier creature tokens.",
                ("token_maker",),
                type_line="Sorcery",
            ),
            candidate(
                "Anthem",
                "Creature tokens you control get +1/+1.",
                ("anthem", "token_payoff"),
            ),
        )
    )

    assert report.plan is TokenPlan.GO_WIDE
    assert dict(report.support)[TokenPlan.ARISTOCRATS] == 1
    assert report.score_for(TokenPlan.ARISTOCRATS) < report.score_for(TokenPlan.GO_WIDE)


def test_plan_specific_scoring_rewards_commitment_and_penalizes_mismatch():
    anthem = candidate(
        "Battle Anthem",
        "Creature tokens you control get +1/+1.",
        ("anthem", "token_payoff"),
        mana_value=3,
    ).analysis
    outlet = candidate(
        "Sacrifice Outlet",
        "Sacrifice another creature: Scry 1.",
        ("sacrifice",),
        type_line="Creature — Cleric",
    ).analysis
    value_engine = candidate(
        "Token Mentor",
        "Whenever a token enters under your control, draw a card.",
        ("token_payoff", "card_draw"),
        mana_value=3,
    ).analysis

    assert score_token_card(anthem, TokenPlan.GO_WIDE).score > score_token_card(
        anthem, TokenPlan.ARISTOCRATS
    ).score
    assert score_token_card(outlet, TokenPlan.ARISTOCRATS).score > score_token_card(
        outlet, TokenPlan.GO_WIDE
    ).score
    assert score_token_card(value_engine, TokenPlan.VALUE).score > score_token_card(
        value_engine, TokenPlan.GO_WIDE
    ).score
