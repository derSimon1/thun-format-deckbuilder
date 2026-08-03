from __future__ import annotations

from enum import StrEnum


class CardRole(StrEnum):
    """Canonical functional roles used across profiles and deck composition.

    ``StrEnum`` keeps the existing string-based API compatible while preventing
    spelling drift in new code. Broad roles remain available for general deck
    reports; precise Token roles prevent conditional or noncreature-token text
    from satisfying reliable Go-Wide package requirements.
    """

    AGGRO_CREATURE = "aggro_creature"
    ANTHEM = "anthem"
    BOARD_WIPE = "board_wipe"
    BURN = "burn"
    CARD_DRAW = "card_draw"
    DEATH_PAYOFF = "death_payoff"
    DRAIN_PAYOFF = "drain_payoff"
    FINISHER = "finisher"
    MILL_ENGINE = "mill_engine"
    MILL_SOURCE = "mill_source"
    PROTECTION = "protection"
    RAMP = "ramp"
    REMOVAL = "removal"
    SACRIFICE = "sacrifice"
    SACRIFICE_OUTLET = "sacrifice_outlet"
    TOKEN_CREATURE_MAKER = "token_creature_maker"
    TOKEN_IMMEDIATE_MAKER = "token_immediate_maker"
    TOKEN_MAKER = "token_maker"
    TOKEN_MULTI_MAKER = "token_multi_maker"
    TOKEN_PAYOFF = "token_payoff"
    TOKEN_REPEATABLE_MAKER = "token_repeatable_maker"
    TOKEN_VALUE_PAYOFF = "token_value_payoff"


def normalize_role(role: CardRole | str) -> CardRole:
    """Return a canonical role or raise a clear error for unknown values."""

    if isinstance(role, CardRole):
        return role
    try:
        return CardRole(role)
    except ValueError as exc:
        valid = ", ".join(item.value for item in CardRole)
        raise ValueError(f"Unknown card role '{role}'. Valid roles: {valid}.") from exc
