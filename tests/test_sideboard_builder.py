from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.sideboard_builder import SideboardBuilder


def k(name, text, colors=("R",), roles=()):
    card = {"name": name, "mana_value": 2, "mana_cost": "{1}{R}", "colors": list(colors), "color_identity": list(colors), "type_line": "Instant", "oracle_text": text}
    return CardKnowledge(card, analyze_card(card), frozenset(roles), frozenset())


def test_sideboard_selects_relevant_on_color_cards():
    cards = (
        k("Smash", "Destroy target artifact."),
        k("No Healing", "Players can't gain life this turn."),
        k("Blue Answer", "Destroy target artifact.", colors=("U",)),
    )
    result = SideboardBuilder().build(cards, GeneratedDeck((), 24), archetype="burn", colors=("R",), size=6)
    assert {entry.name for entry in result} == {"Smash", "No Healing"}
    assert sum(entry.quantity for entry in result) == 6


def test_sideboard_respects_combined_copy_limit():
    main = (DeckEntry("Smash", 2, ManaCost("{1}{R}", 1, "R"), 2, "Instant"),)
    result = SideboardBuilder().build((k("Smash", "Destroy target artifact."),), GeneratedDeck(main, 24), archetype="burn", colors=("R",), max_copies=3)
    assert result[0].quantity == 1


def test_sideboard_excludes_off_color_cards():
    result = SideboardBuilder().build((k("Blue", "Destroy target artifact.", colors=("U",)),), GeneratedDeck((), 24), archetype="burn", colors=("R",))
    assert result == ()


def test_sideboard_covers_distinct_categories_before_filling_duplicates():
    artifact_answers = tuple(
        k(f"Artifact Answer {suffix}", "Destroy target artifact.")
        for suffix in "ABCDE"
    )
    cards = artifact_answers + (
        k("Counter", "Counter target spell.", colors=("U",)),
        k("Graveyard", "Exile target card from a graveyard."),
        k(
            "Protection",
            "Target creature you control gains hexproof until end of turn.",
            colors=("U",),
        ),
        k("Interaction", "Deal 2 damage to any target."),
    )

    result = SideboardBuilder().build(
        cards,
        GeneratedDeck((), 20),
        archetype="prowess",
        colors=("U", "R"),
        size=15,
    )

    names = {entry.name for entry in result}
    assert {"Counter", "Graveyard", "Protection", "Interaction"}.issubset(names)
    assert len(names.intersection({entry.analysis.name for entry in artifact_answers})) == 1
    assert sum(entry.quantity for entry in result) == 15
