import pytest

from thun_deckbuilder.calibrated_strategies import ProwessStrategy
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import score_prowess_card
from thun_deckbuilder.cli import ARCHETYPES, DEFAULT_COLORS
from thun_deckbuilder.deck_request import DeckRequest


def _card(name, mana_value, type_line, oracle_text, *, colors=("U", "R"), power=None):
    card = {
        "name": name,
        "mana_value": mana_value,
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    if power is not None:
        card["power"] = str(power)
    return analyze_card(card)


def test_prowess_threat_beats_slow_chip_damage_creature():
    threat = score_prowess_card(_card(
        "Flying Prowess Threat", 2, "Creature — Drake",
        "Flying. Prowess.", power=1,
    ))
    chip = score_prowess_card(_card(
        "Slow Pinger", 2, "Creature — Human Wizard",
        "Whenever you cast a spell, Slow Pinger deals 1 damage to each opponent.", power=1,
    ))
    assert threat.score > chip.score
    assert "Echte Prowess-Bedrohung" in threat.reasons


def test_cheap_cantrip_and_face_burn_are_rewarded():
    cantrip = score_prowess_card(_card(
        "Quick Study", 1, "Instant", "Draw a card.", colors=("U",)
    ))
    burn = score_prowess_card(_card(
        "Quick Bolt", 1, "Instant", "Quick Bolt deals 3 damage to any target.", colors=("R",)
    ))
    assert cantrip.score > 0
    assert burn.score > 0
    assert "Cantrip/Kartennachschub" in cantrip.reasons
    assert "Reichweite zum Gegner" in burn.reasons


def test_expensive_reactive_spell_is_penalized():
    cheap = score_prowess_card(_card(
        "Cheap Counter", 1, "Instant", "Counter target spell unless its controller pays {2}.", colors=("U",)
    ))
    expensive = score_prowess_card(_card(
        "Slow Counter", 4, "Instant", "Counter target spell.", colors=("U",)
    ))
    assert cheap.score > expensive.score


def test_prowess_strategy_requires_exact_izzet_colors():
    strategy = ProwessStrategy()
    valid = DeckRequest(archetype="prowess", colors=("U", "R"), deck_size=60, max_copies=3)
    strategy._validate_request(valid)

    invalid = DeckRequest(archetype="prowess", colors=("R",), deck_size=60, max_copies=3)
    with pytest.raises(ValueError):
        strategy._validate_request(invalid)


def test_cli_registers_prowess_defaults():
    assert "prowess" in ARCHETYPES
    assert DEFAULT_COLORS["prowess"] == ("U", "R")
