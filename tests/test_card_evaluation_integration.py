from thun_deckbuilder.candidate_evaluator import CandidateEvaluator
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_contribution import contribution_from_knowledge
from thun_deckbuilder.deck_needs import DeckNeedsAnalyzer
from thun_deckbuilder.deck_profile import TOKENS_PROFILE
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.knowledge_base import CardKnowledge


def make_card(name: str, oracle_text: str, type_line: str = "Sorcery", mana_value: int = 2):
    card = {
        "name": name,
        "mana_cost": "{1}{W}",
        "mana_value": mana_value,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    return CardKnowledge(card, analyze_card(card), frozenset(), frozenset())


def score(card):
    state = DeckState()
    needs = DeckNeedsAnalyzer().analyze(state, TOKENS_PROFILE, deck_size=60)
    return CandidateEvaluator().evaluate(
        card,
        contribution_from_knowledge(card),
        state,
        needs,
        TOKENS_PROFILE,
        score_card=lambda item: (10.0, ("Equal strategy score",)),
    )


def test_intrinsic_quality_breaks_equal_strategy_score_ties() -> None:
    efficient = make_card("Efficient", "Draw a card.", type_line="Instant")
    blank = make_card("Blank", "", mana_value=5)
    efficient_score = score(efficient)
    blank_score = score(blank)
    assert efficient_score.total > blank_score.total
    assert efficient_score.values_for("intrinsic_quality")
