from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_profile import DeckProfile


@dataclass(frozen=True)
class DeckValidationReport:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    spell_count: int
    total_cards: int
    role_counts: tuple[tuple[str, int], ...]
    curve_counts: tuple[tuple[str, int], ...]


def validate_deck(
    deck: GeneratedDeck,
    *,
    profile: DeckProfile,
    deck_size: int = 60,
    max_copies: int = 3,
) -> DeckValidationReport:
    errors: list[str] = []
    warnings = list(deck.warnings)
    spell_count = sum(entry.quantity for entry in deck.mainboard)
    total_cards = spell_count + deck.lands

    if total_cards != deck_size:
        errors.append(f"Deck has {total_cards} cards; expected {deck_size}.")
    if deck.lands != profile.lands:
        errors.append(f"Deck has {deck.lands} lands; profile expects {profile.lands}.")

    names: set[str] = set()
    for entry in deck.mainboard:
        if entry.name in names:
            errors.append(f"Duplicate deck entry: {entry.name}.")
        names.add(entry.name)
        if entry.quantity <= 0:
            errors.append(f"Invalid quantity for {entry.name}: {entry.quantity}.")
        if entry.quantity > max_copies:
            errors.append(f"Copy limit exceeded for {entry.name}: {entry.quantity}/{max_copies}.")

    role_counts: dict[str, int] = {target.role: 0 for target in profile.role_targets}
    for entry in deck.mainboard:
        for role in role_counts:
            if role in entry.roles:
                role_counts[role] += entry.quantity

    for target in profile.role_targets:
        count = role_counts[target.role]
        if count < target.minimum:
            errors.append(
                f"Mandatory role '{target.role}' has {count} cards; minimum is {target.minimum}."
            )
        elif count < target.target:
            warning = f"Role '{target.role}' has {count}/{target.target} target cards."
            if warning not in warnings:
                warnings.append(warning)

    curve_counts: list[tuple[str, int]] = []
    lower = 0.0
    for curve_target in profile.curve_targets:
        count = sum(
            entry.quantity
            for entry in deck.mainboard
            if lower < entry.mana_value <= curve_target.maximum_mana_value
        )
        label = f"{lower:g}-{curve_target.maximum_mana_value:g}"
        curve_counts.append((label, count))
        lower = curve_target.maximum_mana_value

    return DeckValidationReport(
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        spell_count=spell_count,
        total_cards=total_cards,
        role_counts=tuple(role_counts.items()),
        curve_counts=tuple(curve_counts),
    )
