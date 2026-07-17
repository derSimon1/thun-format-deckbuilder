import pytest

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck


def test_generate_deck_builds_mono_red_burn():
    with CardDatabase() as database:
        deck = generate_deck(
            database=database,
            archetype="burn",
            colors=["R"],
        )

    spell_count = sum(
        entry.quantity
        for entry in deck.mainboard
    )

    assert spell_count == 36
    assert deck.lands == 24
    assert spell_count + deck.lands == 60


def test_generate_deck_normalizes_input():
    with CardDatabase() as database:
        deck = generate_deck(
            database=database,
            archetype=" Burn ",
            colors=["r"],
        )

    assert sum(
        entry.quantity
        for entry in deck.mainboard
    ) == 36


def test_generate_deck_rejects_unknown_archetype():
    with CardDatabase() as database:
        with pytest.raises(
            ValueError,
            match="Unbekannter Archetyp",
        ):
            generate_deck(
                database=database,
                archetype="control",
                colors=["U"],
            )


def test_generate_deck_rejects_invalid_color():
    with CardDatabase() as database:
        with pytest.raises(
            ValueError,
            match="Ungültige Farbe",
        ):
            generate_deck(
                database=database,
                archetype="burn",
                colors=["X"],
            )


def test_generate_deck_rejects_non_red_burn():
    with CardDatabase() as database:
        with pytest.raises(
            ValueError,
            match="nur Mono-Rot",
        ):
            generate_deck(
                database=database,
                archetype="burn",
                colors=["R", "W"],
            )


def test_generate_deck_rejects_unsupported_deck_size():
    with CardDatabase() as database:
        with pytest.raises(
            ValueError,
            match="nur Decks mit 60 Karten",
        ):
            generate_deck(
                database=database,
                archetype="burn",
                colors=["R"],
                deck_size=100,
            )