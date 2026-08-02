import pytest

from thun_deckbuilder.calibrated_strategies import (
    ProwessStrategy,
    _has_reliable_draw,
    _prowess_eligible,
)
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import score_prowess_card
from thun_deckbuilder.cli import ARCHETYPES, DEFAULT_COLORS
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import CardKnowledge


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


def _knowledge(name, mana_value, type_line, oracle_text, *, colors=("U", "R")):
    card = {
        "name": name,
        "mana_value": mana_value,
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    analysis = analyze_card(card)
    return CardKnowledge(card, analysis, frozenset(), frozenset())


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


def test_prowess_rejects_spells_that_consume_or_blink_its_own_threats():
    sacrifice = _knowledge(
        "Sacrifice Blast",
        1,
        "Sorcery",
        "As an additional cost to cast this spell, sacrifice a creature. "
        "Sacrifice Blast deals damage equal to its power to any target.",
        colors=("R",),
    )
    self_blink = _knowledge(
        "Slow Blink",
        1,
        "Sorcery",
        "Exile target creature you control, then return it to the battlefield "
        "under its owner's control. Draw a card.",
        colors=("U",),
    )

    assert not _prowess_eligible(sacrifice, ("U", "R"))
    assert not _prowess_eligible(self_blink, ("U", "R"))


def test_reliable_draw_excludes_conditional_and_cycling_text():
    assert _has_reliable_draw("Scry 1. Draw a card.")
    assert not _has_reliable_draw("If you do, draw a card.")
    assert not _has_reliable_draw(
        "Cycling {2} ({2}, Discard this card: Draw a card.)"
    )


def test_conditional_draw_does_not_qualify_narrow_prowess_interaction():
    narrow = _knowledge(
        "Narrow Defeat",
        1,
        "Instant",
        "Narrow Defeat deals 5 damage to target red creature. "
        "If that creature was legendary, draw a card.",
        colors=("R",),
    )
    reliable = _knowledge(
        "Flexible Cantrip",
        1,
        "Instant",
        "Flexible Cantrip deals 1 damage to any target. Draw a card.",
        colors=("R",),
    )

    assert not _prowess_eligible(narrow, ("U", "R"))
    assert _prowess_eligible(reliable, ("U", "R"))


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
