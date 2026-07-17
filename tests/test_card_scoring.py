from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import score_burn_card


def test_score_contains_reasons():
    card = {
        "name": "Lightning Strike",
        "mana_value": 2,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Instant",
        "oracle_text": (
            "Lightning Strike deals "
            "3 damage to any target."
        ),
    }

    analysis = analyze_card(card)
    result = score_burn_card(analysis)

    assert result.score > 0
    assert "Instant" in result.reasons
    assert "3 Schaden" in result.reasons