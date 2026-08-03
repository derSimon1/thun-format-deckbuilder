from __future__ import annotations

from collections import Counter
from dataclasses import replace
from typing import Iterable, Protocol

from thun_deckbuilder.deck_profile import DeckProfile, RoleTarget, TOKENS_PROFILE
from thun_deckbuilder.token_plan import TokenPlan


class RoleCard(Protocol):
    roles: Iterable[str]


_PLAN_ROLE_TARGETS: dict[TokenPlan, tuple[RoleTarget, ...]] = {
    TokenPlan.GO_WIDE: (
        RoleTarget("token_creature_maker", minimum=15, target=20),
        RoleTarget("token_immediate_maker", minimum=9, target=12),
        RoleTarget("token_multi_maker", minimum=6, target=9),
        RoleTarget("anthem", minimum=3, target=6),
        RoleTarget("removal", minimum=0, target=4),
        RoleTarget("card_draw", minimum=0, target=2),
    ),
    TokenPlan.VALUE: (
        RoleTarget("token_creature_maker", minimum=10, target=15),
        RoleTarget("token_repeatable_maker", minimum=6, target=8),
        RoleTarget("token_value_payoff", minimum=0, target=4),
        RoleTarget("card_draw", minimum=0, target=6),
        RoleTarget("removal", minimum=0, target=5),
    ),
    TokenPlan.ARISTOCRATS: (
        RoleTarget("token_creature_maker", minimum=10, target=15),
        RoleTarget("sacrifice_outlet", minimum=3, target=5),
        RoleTarget("death_payoff", minimum=3, target=6),
        RoleTarget("card_draw", minimum=0, target=3),
        RoleTarget("removal", minimum=0, target=4),
    ),
}


def token_profile_for_plan(
    plan: TokenPlan,
    *,
    lands: int = TOKENS_PROFILE.lands,
) -> DeckProfile:
    """Return evidence-backed density targets for one coherent Token plan."""

    return replace(
        TOKENS_PROFILE,
        name=f"{TOKENS_PROFILE.name} — {plan.label}",
        lands=lands,
        role_targets=_PLAN_ROLE_TARGETS[plan],
    )


def capacity_checked_token_profile(
    profile: DeckProfile,
    cards: Iterable[RoleCard],
    *,
    max_copies: int,
    deck_size: int,
) -> tuple[DeckProfile, tuple[str, ...]]:
    """Cap only unreachable role targets for the actual candidate pool.

    The production card pool keeps the configured minimums. Small fixtures and
    sparse legal pools cannot deadlock composition merely because they contain
    fewer copies of one precise package role. Soft targets are also capped to
    avoid reporting an impossible shortfall.
    """

    cards = tuple(cards)
    capacity: Counter[str] = Counter()
    for card in cards:
        for role in {str(role) for role in card.roles}:
            capacity[role] += max_copies

    spell_slots = profile.spell_slots(deck_size)
    adjusted: list[RoleTarget] = []
    warnings: list[str] = []
    for target in profile.role_targets:
        role = str(target.role)
        available = min(capacity[role], spell_slots)
        minimum = min(target.minimum, available)
        desired = max(minimum, min(target.target, available))
        adjusted.append(RoleTarget(role, minimum=minimum, target=desired))
        if minimum != target.minimum or desired != target.target:
            warnings.append(
                f"Pool capacity adjusted '{role}' from "
                f"{target.minimum}/{target.target} to {minimum}/{desired}; "
                f"available={available}."
            )

    return replace(profile, role_targets=tuple(adjusted)), tuple(warnings)
