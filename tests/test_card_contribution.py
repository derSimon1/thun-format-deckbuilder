from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_contribution import contribution_from_knowledge
from thun_deckbuilder.knowledge_base import CardKnowledge


def test_contribution_uses_existing_roles_synergies_and_mana_pips() -> None:
    card = {
        "name": "Test Captain",
        "mana_cost": "{1}{W}{W}",
        "mana_value": 3,
        "type_line": "Legendary Creature — Human",
        "oracle_text": "Creatures you control get +1/+1.",
        "color_identity": ["W"],
    }
    analysis = analyze_card(card)
    knowledge = CardKnowledge(
        card=card,
        analysis=analysis,
        roles=frozenset({"anthem", "token_payoff"}),
        synergies=frozenset({"go_wide"}),
    )

    contribution = contribution_from_knowledge(knowledge)

    assert contribution.strength_for("anthem") == 1.0
    assert contribution.pip_count("W") == 2
    assert contribution.tags == frozenset({"go_wide"})
    assert contribution.is_legendary
