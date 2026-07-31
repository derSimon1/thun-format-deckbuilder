from thun_deckbuilder.archetype_intelligence import ArchetypeEvaluator
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_contribution import contribution_from_knowledge
from thun_deckbuilder.deck_profile import BURN_PROFILE, TOKENS_PROFILE
from thun_deckbuilder.knowledge_base import CardKnowledge


def knowledge(name="Card", mv=2, roles=("burn",), text="Deal 3 damage to any target."):
    card = {"name": name, "mana_value": mv, "mana_cost": "{1}{R}", "colors": ["R"], "color_identity": ["R"], "type_line": "Instant", "oracle_text": text}
    return CardKnowledge(card, analyze_card(card), frozenset(roles), frozenset())


def test_burn_rewards_preferred_role_and_curve():
    card = knowledge()
    parts = ArchetypeEvaluator().score(card, contribution_from_knowledge(card), BURN_PROFILE)
    assert sum(part.value for part in parts) > 0
    assert {part.category for part in parts} == {"archetype_fit", "archetype_curve"}


def test_burn_penalizes_expensive_card():
    card = knowledge(mv=5)
    parts = ArchetypeEvaluator().score(card, contribution_from_knowledge(card), BURN_PROFILE)
    assert any(part.value < 0 for part in parts)


def test_tokens_recognizes_token_role():
    card = knowledge(roles=("token_maker",), text="Create two 1/1 white Soldier creature tokens.")
    parts = ArchetypeEvaluator().score(card, contribution_from_knowledge(card), TOKENS_PROFILE)
    assert any("Mono-White Tokens" in part.reason for part in parts)
