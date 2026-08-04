from thun_deckbuilder.candidate_evaluator import CandidateEvaluator
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_contribution import contribution_from_knowledge
from thun_deckbuilder.deck_needs import DeckNeedsAnalyzer
from thun_deckbuilder.deck_profile import TOKENS_PROFILE
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.knowledge_base import CardKnowledge


def make_card(
    name: str,
    roles: set[str],
    mana_value: int = 2,
    mana_cost: str = "{1}{W}",
) -> CardKnowledge:
    card = {
        "name": name,
        "mana_cost": mana_cost,
        "mana_value": mana_value,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Instant",
        "oracle_text": "Test text.",
    }
    return CardKnowledge(card, analyze_card(card), frozenset(roles), frozenset())


def evaluate(card: CardKnowledge, state: DeckState):
    needs = DeckNeedsAnalyzer().analyze(state, TOKENS_PROFILE, deck_size=60)
    return CandidateEvaluator().evaluate(
        card,
        contribution_from_knowledge(card),
        state,
        needs,
        TOKENS_PROFILE,
        score_card=lambda item: (10.0, ("Static quality",)),
    )


def test_missing_role_increases_candidate_score() -> None:
    token = make_card("Token", {"token_maker"})
    filler = make_card("Filler", {"protection"})

    assert evaluate(token, DeckState()).total > evaluate(filler, DeckState()).total


def test_role_bonus_falls_after_target_is_filled() -> None:
    token = make_card("Token", {"token_maker"})
    contribution = contribution_from_knowledge(token)
    empty_score = evaluate(token, DeckState())
    filled_score = evaluate(token, DeckState().with_card(contribution, 18))

    assert empty_score.total > filled_score.total
    assert empty_score.values_for("role_need")
    assert not filled_score.values_for("role_need")


def test_score_contains_explainable_components() -> None:
    token = make_card("Token", {"token_maker"})
    score = evaluate(token, DeckState())

    assert score.values_for("base_quality")
    assert score.values_for("role_need")
    assert score.values_for("curve")


def test_strict_colorless_cost_has_explainable_source_strain() -> None:
    colorless = make_card("Colorless", {"removal"}, mana_cost="{1}{C}{C}")

    score = evaluate(colorless, DeckState())

    assert tuple(item.value for item in score.values_for("mana_strain")) == (-4.0,)
    assert "dedicated true-colorless" in score.components[-1].reason


def test_cards_without_strict_colorless_cost_have_no_source_strain() -> None:
    colored = make_card("Colored", {"removal"}, mana_cost="{1}{W}")
    hybrid = make_card("Hybrid", {"removal"}, mana_cost="{W/C}")

    assert not evaluate(colored, DeckState()).values_for("mana_strain")
    assert not evaluate(hybrid, DeckState()).values_for("mana_strain")
