from __future__ import annotations

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_generator import GeneratedDeck, ManaCost


def format_mana_cost(mana_cost: ManaCost) -> str:
    if not mana_cost.raw:
        return "unbekannt"

    generic = str(mana_cost.generic)

    if mana_cost.colored:
        return f"{generic} + {mana_cost.colored}"

    return generic


def format_deck(deck: GeneratedDeck) -> str:
    lines: list[str] = []

    spell_count = sum(
        entry.quantity
        for entry in deck.mainboard
    )
    total_count = spell_count + deck.lands

    lines.append("THUN-FORMAT DECKBUILDER")
    lines.append("=" * 88)
    lines.append("")
    lines.append("Mono-Red Burn – Prototype")
    lines.append("")
    lines.append(f"Spells: {spell_count}")
    lines.append(f"Lands:  {deck.lands}")
    lines.append(f"Total:  {total_count}")
    lines.append("")
    lines.append(
        f"{'Anz.':<6}"
        f"{'Karte':<38}"
        f"{'Generisch':>10}"
        f"{'Farbig':>10}"
        f"{'Score':>10}"
    )
    lines.append("-" * 88)

    for entry in deck.mainboard:
        colored = entry.mana_cost.colored or "-"

        lines.append(
            f"{entry.quantity:<6}"
            f"{entry.name:<38}"
            f"{entry.mana_cost.generic:>10}"
            f"{colored:>10}"
            f"{entry.score:>10.1f}"
        )

        if entry.reasons:
            reasons = " | ".join(
                f"✓ {reason}"
                for reason in entry.reasons
            )
            lines.append(f"      {reasons}")

    lines.append("-" * 88)
    lines.append(
        f"{deck.lands:<6}"
        f"{'Mountain':<38}"
        f"{'-':>10}"
        f"{'R':>10}"
        f"{'-':>10}"
    )
    lines.append("")
    lines.append("=" * 88)

    return "\n".join(lines)


def main() -> None:
    with CardDatabase() as database:
        deck = generate_deck(
    database=database,
    archetype="tokens",
    colors=["W"],
)

    print(format_deck(deck))


if __name__ == "__main__":
    main()