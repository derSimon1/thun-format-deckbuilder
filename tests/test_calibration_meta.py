from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import (
    score_artifact_card,
    score_burn_card,
    score_mill_card,
    score_shrine_card,
)


def _card(name, mana_value, type_line, oracle_text, *, colors=(), power=None):
    raw = {
        "name": name,
        "mana_value": mana_value,
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    if power is not None:
        raw["power"] = str(power)
    return analyze_card(raw)


def test_burn_prefers_reliable_face_damage_over_removal():
    face = _card(
        "Clean Bolt", 1, "Instant", "Clean Bolt deals 3 damage to any target.",
        colors=("R",),
    )
    removal = _card(
        "Board Bolt", 1, "Instant", "Board Bolt deals 3 damage to target creature.",
        colors=("R",),
    )
    assert score_burn_card(face).score > score_burn_card(removal).score


def test_artifacts_prefer_engine_piece_over_expensive_filler():
    engine = _card(
        "Foundry Engine",
        2,
        "Artifact Creature — Construct",
        "Whenever another artifact enters under your control, put a +1/+1 counter on Foundry Engine.",
        power=2,
    )
    filler = _card(
        "Heavy Statue", 6, "Artifact Creature — Golem", "Vigilance", power=5,
    )
    assert score_artifact_card(engine).score > score_artifact_card(filler).score


def test_shrines_prefer_scaling_shrine_over_unrelated_legend():
    shrine = _card(
        "Sanctum of Pressure",
        3,
        "Legendary Enchantment — Shrine",
        "At the beginning of your upkeep, target opponent mills a card for each Shrine you control.",
        colors=("U",),
    )
    legend = _card(
        "Unrelated Hero", 4, "Legendary Creature — Human", "Vigilance", colors=("W",), power=4,
    )
    assert score_shrine_card(shrine).score > score_shrine_card(legend).score


def test_mill_prefers_opponent_pressure_over_self_mill():
    opponent = _card(
        "Mind Erosion", 2, "Sorcery", "Target opponent mills eight cards.", colors=("U",),
    )
    self_mill = _card(
        "Grave Setup", 2, "Sorcery", "You mill eight cards.", colors=("U",),
    )
    assert score_mill_card(opponent).score > score_mill_card(self_mill).score


def test_each_archetype_rejects_generic_expensive_filler():
    filler = _card("Generic Colossus", 7, "Artifact Creature — Golem", "Trample", power=7)
    assert score_burn_card(filler).score < 1
    assert score_artifact_card(filler).score < 1
    assert score_shrine_card(filler).score <= 0
    assert score_mill_card(filler).score <= 0
