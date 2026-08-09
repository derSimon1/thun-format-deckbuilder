from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_synergies import detect_synergies
from thun_deckbuilder.synergy_tag import SynergyTag


def test_lightning_strike_is_spellslinger():
    card = {
        "name": "Lightning Strike",
        "mana_value": 2,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Instant",
        "oracle_text": "Lightning Strike deals 3 damage to any target.",
    }

    analysis = analyze_card(card)
    synergies = detect_synergies(analysis)

    assert "spellslinger" in synergies


def _synergies_for(text: str):
    return detect_synergies(
        analyze_card(
            {
                "name": "Sacrifice Test",
                "mana_value": 2,
                "colors": ["B"],
                "color_identity": ["B"],
                "type_line": "Artifact",
                "oracle_text": text,
            }
        )
    )


def test_only_activated_sacrifice_cost_is_an_outlet_synergy() -> None:
    additional = _synergies_for(
        "As an additional cost to cast this spell, sacrifice a creature. Draw two cards."
    )
    creature_outlet = _synergies_for("Sacrifice another creature: Scry 1.")
    artifact_outlet = _synergies_for("{1}, Sacrifice an artifact: Draw a card.")

    assert SynergyTag.SACRIFICE_OUTLET not in additional
    assert SynergyTag.SACRIFICE_OUTLET in creature_outlet
    assert SynergyTag.SACRIFICE_OUTLET in artifact_outlet
