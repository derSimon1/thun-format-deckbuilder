from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

COLORS = ("W", "U", "B", "R", "G", "C")
BASIC_LANDS = {
    "W": "Plains",
    "U": "Island",
    "B": "Swamp",
    "R": "Mountain",
    "G": "Forest",
    "C": "Wastes",
}
WILDCARD_MANA_SOURCE = "*"


@dataclass(frozen=True)
class ManaRequirement:
    """Colored mana demand extracted from one spell or a spell section."""

    pips: tuple[tuple[str, float], ...]
    early_pips: tuple[tuple[str, float], ...] = ()
    minimum_sources: tuple[tuple[str, int], ...] = ()

    def amount(self, color: str) -> float:
        wanted = color.upper()
        return dict(self.pips).get(wanted, 0.0)

    def early_amount(self, color: str) -> float:
        wanted = color.upper()
        return dict(self.early_pips).get(wanted, 0.0)

    def minimum_sources_for(self, color: str) -> int:
        wanted = color.upper()
        return dict(self.minimum_sources).get(wanted, 0)

    @property
    def total(self) -> float:
        return sum(value for _, value in self.pips)

    @property
    def active_colors(self) -> tuple[str, ...]:
        return tuple(color for color, value in self.pips if value > 0)


def _symbol_weights(symbol: str) -> dict[str, float]:
    normalized = symbol.upper().strip()
    if normalized in COLORS:
        return {normalized: 1.0}

    parts = normalized.split("/")
    colored = [part for part in parts if part in COLORS]
    if not colored:
        return {}
    # A hybrid symbol can be paid with either color and therefore contributes
    # one shared pip rather than one full pip to every color.
    share = 1.0 / len(colored)
    return {color: share for color in colored}


def parse_colored_pips(mana_cost: str) -> dict[str, float]:
    result = {color: 0.0 for color in COLORS}
    for symbol in re.findall(r"\{([^}]+)\}", mana_cost or ""):
        for color, weight in _symbol_weights(symbol).items():
            result[color] += weight
    return result


def mana_symbol_requirements(
    mana_cost: str,
    colored_fallback: str = "",
) -> tuple[frozenset[str], ...]:
    """Return colored and true-colorless payment choices for a mana cost."""

    symbols = re.findall(r"\{([^}]+)\}", (mana_cost or "").upper())
    if not symbols and colored_fallback:
        symbols = colored_fallback.upper().split()
    requirements: list[frozenset[str]] = []
    for symbol in symbols:
        normalized = symbol.strip().upper()
        if normalized.isdigit() or normalized in {"X", "Y", "Z", "S"}:
            continue
        options = frozenset(
            part for part in normalized.split("/") if part in COLORS
        )
        if options:
            requirements.append(options)
    return tuple(requirements)


def source_can_pay(options: frozenset[str], source: str) -> bool:
    """Return whether one source pays one symbol; generic sources never pay {C}."""

    normalized = source.upper()
    return normalized in options or (
        normalized == WILDCARD_MANA_SOURCE
        and any(option != "C" for option in options)
    )


def source_types_support(
    requirements: tuple[frozenset[str], ...],
    source_types: Iterable[str],
) -> bool:
    """Check that every symbol has a source type the configured builder can make."""

    available = tuple(str(source).upper() for source in source_types)
    return all(
        any(source_can_pay(options, source) for source in available)
        for options in requirements
    )


def can_pay_mana_requirements(
    requirements: tuple[frozenset[str], ...],
    sources: Iterable[str],
) -> bool:
    """Match actual one-use sources to colored and true-colorless requirements."""

    available = tuple(str(source).upper() for source in sources)
    used = [False] * len(available)

    def assign(index: int) -> bool:
        if index >= len(ordered):
            return True
        options = ordered[index]
        for source_index, source in enumerate(available):
            if used[source_index] or not source_can_pay(options, source):
                continue
            used[source_index] = True
            if assign(index + 1):
                return True
            used[source_index] = False
        return False

    ordered = tuple(sorted(requirements, key=len))
    return assign(0)


def requirement_for_spells(entries: Iterable[object], *, early_turn: float = 2.0) -> ManaRequirement:
    total = {color: 0.0 for color in COLORS}
    early = {color: 0.0 for color in COLORS}
    minimum_sources = {color: 0 for color in COLORS}

    for entry in entries:
        quantity = int(getattr(entry, "quantity", 1))
        mana_value = float(getattr(entry, "mana_value", 0.0))
        mana_cost = getattr(getattr(entry, "mana_cost", None), "raw", "")
        pips = parse_colored_pips(str(mana_cost))
        symbol_requirements = mana_symbol_requirements(str(mana_cost))
        for color, amount in pips.items():
            weighted = amount * quantity
            total[color] += weighted
            if mana_value <= early_turn:
                early[color] += weighted
            required_by_one_spell = sum(
                1 for options in symbol_requirements if options == frozenset({color})
            )
            minimum_sources[color] = max(
                minimum_sources[color],
                required_by_one_spell,
            )

    return ManaRequirement(
        pips=tuple((color, total[color]) for color in COLORS),
        early_pips=tuple((color, early[color]) for color in COLORS),
        minimum_sources=tuple(
            (color, minimum_sources[color]) for color in COLORS
        ),
    )
