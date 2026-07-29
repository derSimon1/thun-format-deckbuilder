from __future__ import annotations

from enum import StrEnum


class CardRole(StrEnum):
    """Canonical functional roles used across profiles and deck composition.

    ``StrEnum`` keeps the existing string-based API compatible while preventing
    spelling drift in new code. For example, ``CardRole.BURN == "burn"``.
    """

    AGGRO_CREATURE = "aggro_creature"
    ANTHEM = "anthem"
    BOARD_WIPE = "board_wipe"
    BURN = "burn"
    CARD_DRAW = "card_draw"
    FINISHER = "finisher"
    PROTECTION = "protection"
    RAMP = "ramp"
    REMOVAL = "removal"
    SACRIFICE = "sacrifice"
    TOKEN_MAKER = "token_maker"
    TOKEN_PAYOFF = "token_payoff"


def normalize_role(role: CardRole | str) -> CardRole:
    """Return a canonical role or raise a clear error for unknown values."""

    if isinstance(role, CardRole):
        return role
    try:
        return CardRole(role)
    except ValueError as exc:
        valid = ", ".join(item.value for item in CardRole)
        raise ValueError(f"Unknown card role '{role}'. Valid roles: {valid}.") from exc
