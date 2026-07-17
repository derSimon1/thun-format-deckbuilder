from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ManaCurveSlot:
    max_mana_value: int
    cards: int


@dataclass(frozen=True)
class DeckSkeleton:
    lands: int
    curve: tuple[ManaCurveSlot, ...]


BURN_SKELETON = DeckSkeleton(
    lands=24,
    curve=(
        ManaCurveSlot(1, 12),
        ManaCurveSlot(2, 12),
        ManaCurveSlot(3, 8),
        ManaCurveSlot(99, 4),
    ),
)