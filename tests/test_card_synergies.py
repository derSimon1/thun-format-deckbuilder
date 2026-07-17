from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_synergies import detect_synergies


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