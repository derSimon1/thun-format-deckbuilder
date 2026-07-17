from thun_deckbuilder.card_knowledge import build_card_knowledge


def test_build_card_knowledge():
    card = {
        "name": "Test Bolt",
        "mana_value": 2,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Instant",
        "oracle_text": "Test Bolt deals 3 damage to any target.",
    }

    knowledge = build_card_knowledge(card)

    assert knowledge.analysis.name == "Test Bolt"
    assert "damage" in knowledge.analysis.features
    assert "burn" in knowledge.roles