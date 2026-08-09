from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.sideboard_builder import SideboardBuilder


def _knowledge(name, colors, type_line, oracle_text, mana_value=2, roles=()):
    card = {
        "name": name,
        "mana_value": mana_value,
        "mana_cost": "{1}{U}",
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    return CardKnowledge(
        card=card,
        analysis=analyze_card(card),
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def _names(entries):
    return {entry.name for entry in entries}


def test_artifact_sideboard_prioritizes_protection_and_countermagic():
    cards = (
        _knowledge(
            "Artifact Shield",
            ("U",),
            "Instant",
            "Artifacts you control gain hexproof until end of turn.",
        ),
        _knowledge(
            "Negate",
            ("U",),
            "Instant",
            "Counter target noncreature spell.",
        ),
        _knowledge(
            "Off Color Answer",
            ("G",),
            "Instant",
            "Destroy target artifact.",
        ),
    )
    sideboard = SideboardBuilder().build(
        cards,
        GeneratedDeck((), 22),
        archetype="artifacts",
        colors=("U", "R"),
        size=6,
    )

    assert _names(sideboard) == {"Artifact Shield", "Negate"}


def test_shrine_sideboard_prioritizes_protection_and_recursion():
    cards = (
        _knowledge(
            "Sanctum Guard",
            ("W",),
            "Instant",
            "Permanents you control gain hexproof until end of turn.",
            roles=("protection",),
        ),
        _knowledge(
            "Restore Shrine",
            ("G",),
            "Sorcery",
            "Return target enchantment card from your graveyard to your hand.",
        ),
    )
    sideboard = SideboardBuilder().build(
        cards,
        GeneratedDeck((), 24),
        archetype="shrines",
        colors=("W", "U", "B", "R", "G"),
        size=6,
    )

    assert _names(sideboard) == {"Sanctum Guard", "Restore Shrine"}


def test_mill_sideboard_prioritizes_cheap_interaction_and_graveyard_hate():
    cards = (
        _knowledge(
            "Cheap Removal",
            ("B",),
            "Instant",
            "Destroy target creature.",
            roles=("removal",),
        ),
        _knowledge(
            "Graveyard Lock",
            ("U",),
            "Artifact",
            "Cards in graveyards can't be the targets of spells or abilities.",
        ),
        _knowledge(
            "Vanilla Threat",
            ("U",),
            "Creature — Fish",
            "",
        ),
    )
    sideboard = SideboardBuilder().build(
        cards,
        GeneratedDeck((), 24),
        archetype="mill",
        colors=("U", "B"),
        size=6,
    )

    assert _names(sideboard) == {"Cheap Removal", "Graveyard Lock"}


def test_sideboard_respects_mainboard_copy_limit():
    card = _knowledge(
        "Negate",
        ("U",),
        "Instant",
        "Counter target noncreature spell.",
    )
    mainboard_card = type("Entry", (), {"name": "Negate", "quantity": 3})()
    deck = GeneratedDeck((mainboard_card,), 24)

    sideboard = SideboardBuilder().build(
        (card,),
        deck,
        archetype="mill",
        colors=("U", "B"),
    )

    assert sideboard == ()
