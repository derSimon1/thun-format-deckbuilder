from __future__ import annotations

from thun_deckbuilder.deck_generator import GeneratedDeck


def format_arena_export(deck: GeneratedDeck) -> str:
    """Return an MTG Arena compatible plain-text deck list."""
    lines = ["Deck"]
    for entry in sorted(deck.mainboard, key=lambda item: (item.mana_value, item.name)):
        lines.append(f"{entry.quantity} {entry.name}")

    if deck.mana_base is not None and deck.mana_base.lands:
        for land in deck.mana_base.lands:
            lines.append(f"{land.quantity} {land.land_name}")
    elif deck.lands:
        lines.append(f"{deck.lands} Basic Land")

    if deck.sideboard:
        lines.extend(["", "Sideboard"])
        for entry in sorted(deck.sideboard, key=lambda item: (item.mana_value, item.name)):
            lines.append(f"{entry.quantity} {entry.name}")

    return "\n".join(lines)
