from thun_deckbuilder.deck_generator import (
    DeckEntry,
    GeneratedDeck,
    ManaCost,
)
from thun_deckbuilder.prototype import format_deck


def test_format_deck_contains_cards_and_total():
    deck = GeneratedDeck(
        mainboard=(
            DeckEntry(
                name="Lightning Strike",
                quantity=3,
                mana_cost=ManaCost(
                    raw="{1}{R}",
                    generic=1,
                    colored="R",
                ),
                mana_value=2,
                type_line="Instant",
                score=11.0,
                reasons=(
                    "Mana Value 2",
                    "Instant",
                    "Any Target",
                    "3 Schaden",
                ),
            ),
            DeckEntry(
                name="Shock",
                quantity=3,
                mana_cost=ManaCost(
                    raw="{R}",
                    generic=0,
                    colored="R",
                ),
                mana_value=1,
                type_line="Instant",
                score=12.0,
                reasons=(
                    "Mana Value ≤ 1",
                    "Instant",
                    "Any Target",
                    "2 Schaden",
                ),
            ),
        ),
        lands=24,
    )

    output = format_deck(deck)

    assert "Lightning Strike" in output
    assert "Shock" in output
    assert "Mountain" in output
    assert "Total:  30" in output
    assert "Generisch" in output
    assert "Farbig" in output
    assert "11.0" in output
    assert "Instant" in output