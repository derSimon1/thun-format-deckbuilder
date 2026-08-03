from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_contribution import contribution_from_knowledge
from thun_deckbuilder.knowledge_base import CardKnowledge


def knowledge_with_roles(*roles: str) -> CardKnowledge:
    card = {
        "name": "Test Captain",
        "mana_cost": "{1}{W}{W}",
        "mana_value": 3,
        "type_line": "Legendary Creature — Human",
        "oracle_text": "Creatures you control get +1/+1.",
        "color_identity": ["W"],
    }
    return CardKnowledge(
        card=card,
        analysis=analyze_card(card),
        roles=frozenset(roles),
        synergies=frozenset({"go_wide"}),
    )


def test_contribution_uses_existing_roles_synergies_and_mana_pips() -> None:
    contribution = contribution_from_knowledge(
        knowledge_with_roles("anthem", "token_payoff")
    )

    assert contribution.strength_for("anthem") == 1.0
    assert contribution.pip_count("W") == 2
    assert contribution.tags == frozenset({"go_wide"})
    assert contribution.is_legendary


def test_simulation_metadata_is_not_treated_as_functional_role() -> None:
    contribution = contribution_from_knowledge(
        knowledge_with_roles(
            "token_creature_maker",
            "token_output_2",
            "token_production_immediate",
        )
    )

    assert contribution.strength_for("token_creature_maker") == 1.0
    assert tuple(str(item.role) for item in contribution.roles) == (
        "token_creature_maker",
    )
