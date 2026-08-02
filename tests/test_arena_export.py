from thun_deckbuilder.arena_export import format_arena_export
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.mana_distribution import LandAllocation, ManaDistribution


def _entry(name: str, quantity: int, mana_value: float = 1) -> DeckEntry:
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost(raw="{R}", generic=0, colored="R"),
        mana_value=mana_value,
        type_line="Instant",
    )


def test_arena_export_contains_deck_lands_and_sideboard():
    deck = GeneratedDeck(
        mainboard=(_entry("Play with Fire", 3), _entry("Sprite Dragon", 3, 2)),
        lands=20,
        mana_base=ManaDistribution(
            lands=(LandAllocation("U", "Island", 9), LandAllocation("R", "Mountain", 11)),
            total_lands=20,
            required_sources=(("U", 9), ("R", 11)),
        ),
        sideboard=(_entry("Negate", 3, 2),),
    )

    result = format_arena_export(deck)

    assert result.startswith("Deck\n")
    assert "3 Play with Fire" in result
    assert "3 Sprite Dragon" in result
    assert "9 Island" in result
    assert "11 Mountain" in result
    assert "\n\nSideboard\n3 Negate" in result


def test_arena_export_is_deterministic():
    deck = GeneratedDeck(
        mainboard=(_entry("Zulu", 1, 2), _entry("Alpha", 1, 1)),
        lands=0,
    )

    assert format_arena_export(deck).splitlines()[1:] == ["1 Alpha", "1 Zulu"]
