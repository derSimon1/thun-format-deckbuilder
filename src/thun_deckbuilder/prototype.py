from __future__ import annotations

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_generator import GeneratedDeck, ManaCost
from thun_deckbuilder.deck_profile import BURN_PROFILE, TOKENS_PROFILE
from thun_deckbuilder.deck_validation import validate_deck
from thun_deckbuilder.explanation import format_quality_report, format_selection_trace


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
    explain: bool = False,
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

    lines.append("-" * 88)
    if deck.mana_base is not None and deck.mana_base.lands:
        for land in deck.mana_base.lands:
            lines.append(
                f"{land.quantity:<6}{land.land_name:<38}{'-':>10}{land.color:>10}{'-':>10}"
            )
    else:
        lines.append(
            f"{deck.lands:<6}{basic_land:<38}{'-':>10}{color_label or '-':>10}{'-':>10}"
        )

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

    if deck.mana_quality is not None:
        lines.extend(["", "MANA BASE", "-" * 88])
        for item in deck.mana_quality.colors:
            marker = "OK" if item.sufficient else "LOW"
            lines.append(
                f"  [{marker:<3}] {item.color}: {item.sources} sources / {item.required} required"
            )
        lines.append(
            f"Mana score: {deck.mana_quality.score}/100 "
            f"(lands {deck.mana_quality.land_count}, recommended {deck.mana_quality.recommended_lands})"
        )

    if deck.quality_report is not None:
        lines.extend(["", *format_quality_report(deck.quality_report)])

    if deck.benchmark_report is not None:
        report = deck.benchmark_report
        lines.extend(["", "BENCHMARK CALIBRATION", "-" * 88])
        lines.append(f"Benchmark: {report.name}")
        for item in report.role_items:
            lines.append(f"Role {item.key}: {item.actual}/{item.target} ({item.score}/100)")
        for item in report.curve_items:
            lines.append(f"Curve MV {item.key}: {item.actual}/{item.target} ({item.score}/100)")
        for item in report.signature_items:
            lines.append(f"Core {item.key}: {item.actual}/{item.target} ({item.score}/100)")
        lines.append(f"Lands: {report.land_item.actual}/{report.land_item.target} ({report.land_item.score}/100)")
        lines.append(f"Benchmark score: {report.score}/100")

    if deck.sideboard:
        lines.extend(["", "SIDEBOARD", "-" * 88])
        for entry in deck.sideboard:
            lines.append(f"{entry.quantity:<6}{entry.name:<38}{entry.score:>10.1f}")
            if entry.reasons:
                lines.append("      " + " | ".join(entry.reasons))
        lines.append(f"Sideboard cards: {sum(entry.quantity for entry in deck.sideboard)}/15")

    if explain and deck.selections:
        lines.extend(["", "SELECTION TRACE", "-" * 88])
        for trace in deck.selections:
            lines.extend(format_selection_trace(trace))
            lines.append("")

    lines.extend(["", "=" * 88])
    return "\n".join(lines)


def main() -> None:
    with CardDatabase() as database:
        deck = generate_deck(database=database, archetype="burn", colors=["R"])
    print(format_deck(deck, archetype="burn", colors=("R",)))


if __name__ == "__main__":
    main()
