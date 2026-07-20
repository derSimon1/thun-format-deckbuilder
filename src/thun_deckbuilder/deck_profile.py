from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoleTarget:
    """Desired number of non-land cards for one strategic role."""

    role: str
    minimum: int
    target: int

    def __post_init__(self) -> None:
        if self.minimum < 0:
            raise ValueError("Role minimum cannot be negative.")
        if self.target < self.minimum:
            raise ValueError("Role target cannot be smaller than its minimum.")


@dataclass(frozen=True)
class CurveTarget:
    """Maximum desired spell count at one mana-value band."""

    maximum_mana_value: float
    target: int


@dataclass(frozen=True)
class DeckProfile:
    name: str
    lands: int
    role_targets: tuple[RoleTarget, ...]
    curve_targets: tuple[CurveTarget, ...] = ()

    def spell_slots(self, deck_size: int) -> int:
        slots = deck_size - self.lands
        if slots <= 0:
            raise ValueError("Deck size must be greater than the land count.")
        return slots


BURN_PROFILE = DeckProfile(
    name="Mono-Red Burn",
    lands=24,
    role_targets=(
        RoleTarget("burn", minimum=18, target=24),
        RoleTarget("aggro_creature", minimum=0, target=9),
        RoleTarget("card_draw", minimum=0, target=3),
    ),
    curve_targets=(
        CurveTarget(1, 12),
        CurveTarget(2, 16),
        CurveTarget(3, 8),
        CurveTarget(99, 2),
    ),
)


TOKENS_PROFILE = DeckProfile(
    name="Mono-White Tokens",
    lands=24,
    role_targets=(
        RoleTarget("token_maker", minimum=12, target=18),
        RoleTarget("token_payoff", minimum=0, target=6),
        RoleTarget("removal", minimum=0, target=6),
        RoleTarget("card_draw", minimum=0, target=3),
    ),
    curve_targets=(
        CurveTarget(1, 8),
        CurveTarget(2, 12),
        CurveTarget(3, 10),
        CurveTarget(4, 4),
        CurveTarget(99, 2),
    ),
)
