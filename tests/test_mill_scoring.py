from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.mill_scoring import score_mill_card


def _card(name, mana_value, type_line, oracle_text):
    return analyze_card({
        "name": name,
        "mana_value": mana_value,
        "colors": ["U"],
        "color_identity": ["U"],
        "type_line": type_line,
        "oracle_text": oracle_text,
    })


def test_efficient_opponent_mill_scores_highly():
    result = score_mill_card(_card("Mind Burst", 2, "Sorcery", "Target opponent mills 8 cards."))
    assert "Millt 8 Karten" in result.reasons
    assert "Sehr effizientes Mill" in result.reasons


def test_repeatable_mill_gets_bonus():
    result = score_mill_card(_card("Crab", 1, "Creature", "Whenever a land enters under your control, target opponent mills 3 cards."))
    assert "Wiederholbares Mill" in result.reasons


def test_interactive_mill_card_gets_defensive_credit():
    result = score_mill_card(_card("Drown", 2, "Instant", "Counter target spell. Target opponent mills 2 cards."))
    assert "Defensive Interaktion" in result.reasons
    assert "Instant" in result.reasons


def test_self_mill_is_penalized():
    opponent = score_mill_card(_card("Opponent Mill", 2, "Sorcery", "Target opponent mills 5 cards."))
    self_mill = score_mill_card(_card("Self Mill", 2, "Sorcery", "You mill 5 cards."))
    assert opponent.score > self_mill.score
    assert "Self-Mill statt Gegner-Mill" in self_mill.reasons


def test_expensive_flat_mill_is_penalized():
    result = score_mill_card(_card("Slow Mill", 6, "Sorcery", "Target opponent mills 5 cards."))
    assert "Teure Mill-Karte ohne Skalierung" in result.reasons
