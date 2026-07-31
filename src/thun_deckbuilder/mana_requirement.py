from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

COLORS = ("W", "U", "B", "R", "G")


@dataclass(frozen=True)
class ManaRequirement:
    """Colored mana demand extracted from one spell or a spell section."""

    pips: tuple[tuple[str, float], ...]
    early_pips: tuple[tuple[str, float], ...] = ()

    def amount(self, color: str) -> float:
        wanted = color.upper()
        return dict(self.pips).get(wanted, 0.0)

    def early_amount(self, color: str) -> float:
        wanted = color.upper()
        return dict(self.early_pips).get(wanted, 0.0)

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


def requirement_for_spells(entries: Iterable[object], *, early_turn: float = 2.0) -> ManaRequirement:
    total = {color: 0.0 for color in COLORS}
    early = {color: 0.0 for color in COLORS}

    for entry in entries:
        quantity = int(getattr(entry, "quantity", 1))
        mana_value = float(getattr(entry, "mana_value", 0.0))
        mana_cost = getattr(getattr(entry, "mana_cost", None), "raw", "")
        pips = parse_colored_pips(str(mana_cost))
        for color, amount in pips.items():
            weighted = amount * quantity
            total[color] += weighted
            if mana_value <= early_turn:
                early[color] += weighted

    return ManaRequirement(
        pips=tuple((color, total[color]) for color in COLORS),
        early_pips=tuple((color, early[color]) for color in COLORS),
    )
