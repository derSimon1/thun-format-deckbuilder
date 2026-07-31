from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import score_shrine_card


def _card(name, mana_value, type_line, oracle_text, colors=None):
    return analyze_card({
        "name": name,
        "mana_value": mana_value,
        "colors": colors or [],
        "color_identity": colors or [],
        "type_line": type_line,
        "oracle_text": oracle_text,
    })


def test_shrine_type_gets_core_bonus():
    result = score_shrine_card(_card("Sanctum", 2, "Legendary Enchantment — Shrine", "At the beginning of your upkeep, gain 1 life."))
    assert result.score > 0
    assert "Schrein" in result.reasons


def test_scaling_shrine_beats_non_scaling_shrine():
    scaling = score_shrine_card(_card("Scaling Shrine", 3, "Legendary Enchantment — Shrine", "At the beginning of your upkeep, draw a card for each Shrine you control."))
    plain = score_shrine_card(_card("Plain Shrine", 3, "Legendary Enchantment — Shrine", "At the beginning of your upkeep, draw a card."))
    assert scaling.score > plain.score
    assert "Skaliert mit Schreinen" in scaling.reasons


def test_shrine_tutor_gets_bonus():
    result = score_shrine_card(_card("Journey", 3, "Sorcery", "Search your library for a Shrine card, reveal it, put it into your hand, then shuffle."))
    assert "Schrein-Tutor" in result.reasons


def test_five_color_fixing_gets_bonus():
    result = score_shrine_card(_card("Temple Guide", 2, "Creature", "{T}: Add one mana of any color."))
    assert "Fünffarben-Fixing" in result.reasons


def test_expensive_non_scaling_shrine_is_penalized():
    result = score_shrine_card(_card("Slow Shrine", 6, "Legendary Enchantment — Shrine", "At the beginning of your upkeep, scry 1."))
    assert "Teurer Schrein" in result.reasons
    assert "Teurer Schrein ohne Skalierung" in result.reasons
