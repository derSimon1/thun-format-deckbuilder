from thun_deckbuilder.candidate_eligibility import CandidateEligibility
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_contribution import contribution_from_knowledge
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.knowledge_base import CardKnowledge


def knowledge(name: str = "Test Spell", mana_cost: str = "{1}{W}") -> CardKnowledge:
    card = {
        "name": name,
        "mana_cost": mana_cost,
        "mana_value": 2,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Instant",
        "oracle_text": "Create a 1/1 white Soldier creature token.",
    }
    return CardKnowledge(card, analyze_card(card), frozenset({"token_maker"}), frozenset())


def test_rejects_candidate_at_copy_limit() -> None:
    card = knowledge()
    contribution = contribution_from_knowledge(card)
    state = DeckState().with_card(contribution, 3)

    result = CandidateEligibility().check(
        card,
        contribution,
        state,
        deck_size=36,
        max_copies=3,
        strategy_eligible=lambda item: True,
    )

    assert not result.eligible
    assert "copy limit" in result.reason.lower()


def test_rejects_strategy_ineligible_candidate() -> None:
    card = knowledge()
    result = CandidateEligibility().check(
        card,
        contribution_from_knowledge(card),
        DeckState(),
        deck_size=36,
        max_copies=3,
        strategy_eligible=lambda item: False,
    )

    assert not result.eligible
    assert "strategy" in result.reason.lower()


def test_rejects_explicit_colorless_cost_without_colorless_source_support() -> None:
    card = knowledge(name="Colorless Spell", mana_cost="{1}{C}")
    result = CandidateEligibility(frozenset({"W", "*"})).check(
        card,
        contribution_from_knowledge(card),
        DeckState(),
        deck_size=36,
        max_copies=3,
        strategy_eligible=lambda item: True,
    )

    assert not result.eligible
    assert "mana source" in result.reason.lower()


def test_accepts_explicit_colorless_cost_when_builder_supports_wastes() -> None:
    card = knowledge(name="Colorless Spell", mana_cost="{1}{C}")
    result = CandidateEligibility().check(
        card,
        contribution_from_knowledge(card),
        DeckState(),
        deck_size=36,
        max_copies=3,
        strategy_eligible=lambda item: True,
    )

    assert result.eligible


def test_non_colorless_candidate_keeps_existing_eligibility_behavior() -> None:
    card = knowledge(mana_cost="{1}{W}")
    result = CandidateEligibility(frozenset({"W"})).check(
        card,
        contribution_from_knowledge(card),
        DeckState(),
        deck_size=36,
        max_copies=3,
        strategy_eligible=lambda item: True,
    )

    assert result.eligible
