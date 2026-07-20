from __future__ import annotations

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_generator import GeneratedDeck, ManaCost
from thun_deckbuilder.deck_profile import BURN_PROFILE, TOKENS_PROFILE
from thun_deckbuilder.deck_validation import validate_deck


BASIC_LANDS = {"W": "Plains", "U": "Island", "B": "Swamp", "R": "Mountain", "G": "Forest"}
PROFILES = {"burn": BURN_PROFILE, "tokens": TOKENS_PROFILE}


def format_mana_cost(mana_cost: ManaCost) -> str:
    if not mana_cost.raw:
        return "unbekannt"
    return f"{mana_cost.generic} + {mana_cost.colored}" if mana_cost.colored else str(mana_cost.generic)


def format_deck(
    deck: GeneratedDeck,
    *,
    archetype: str = "burn",
    colors: tuple[str, ...] = ("R",),
    include_report: bool = True,
) -> str:
    spell_count = sum(entry.quantity for entry in deck.mainboard)
    normalized_colors = tuple(color.upper() for color in colors)
    color_label = "".join(normalized_colors)
    title = deck.profile_name or f"{color_label} {archetype.title()} – Prototype"
    basic_land = BASIC_LANDS.get(normalized_colors[0], "Basic Land") if len(normalized_colors) == 1 else "Basic Lands"

    lines = [
        "THUN-FORMAT DECKBUILDER", "=" * 88, "", title, "",
        f"Spells: {spell_count}", f"Lands:  {deck.lands}", f"Total:  {spell_count + deck.lands}", "",
        f"{'Anz.':<6}{'Karte':<38}{'Generisch':>10}{'Farbig':>10}{'Score':>10}",
        "-" * 88,
    ]
    for entry in deck.mainboard:
        lines.append(
            f"{entry.quantity:<6}{entry.name:<38}{entry.mana_cost.generic:>10}"
            f"{(entry.mana_cost.colored or '-'):>10}{entry.score:>10.1f}"
        )
        if entry.reasons:
            lines.append("      " + " | ".join(f"✓ {reason}" for reason in entry.reasons))

    lines.extend([
        "-" * 88,
        f"{deck.lands:<6}{basic_land:<38}{'-':>10}{color_label or '-':>10}{'-':>10}",
    ])

    profile = PROFILES.get(archetype)
    if include_report and profile is not None:
        report = validate_deck(deck, profile=profile)
        lines.extend(["", "DECK CHECK", "-" * 88])
        lines.append(f"Status: {'OK' if report.valid else 'FEHLER'}")
        if report.role_counts:
            lines.append("Rollen: " + ", ".join(f"{role}={count}" for role, count in report.role_counts))
        if report.curve_counts:
            lines.append("Kurve:  " + ", ".join(f"MV {band}={count}" for band, count in report.curve_counts))
        for warning in report.warnings:
            lines.append(f"WARNUNG: {warning}")
        for error in report.errors:
            lines.append(f"FEHLER: {error}")

    lines.extend(["", "=" * 88])
    return "\n".join(lines)


def main() -> None:
    with CardDatabase() as database:
        deck = generate_deck(database=database, archetype="burn", colors=["R"])
    print(format_deck(deck, archetype="burn", colors=("R",)))


if __name__ == "__main__":
    main()
