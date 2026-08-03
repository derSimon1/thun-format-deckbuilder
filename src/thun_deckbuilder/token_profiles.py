from __future__ import annotations

from dataclasses import replace

from thun_deckbuilder.deck_profile import DeckProfile, RoleTarget, TOKENS_PROFILE
from thun_deckbuilder.token_plan import TokenPlan


_PLAN_ROLE_TARGETS: dict[TokenPlan, tuple[RoleTarget, ...]] = {
    TokenPlan.GO_WIDE: (
        RoleTarget("token_maker", minimum=12, target=18),
        RoleTarget("token_payoff", minimum=4, target=7),
        RoleTarget("removal", minimum=0, target=5),
        RoleTarget("card_draw", minimum=0, target=3),
    ),
    TokenPlan.VALUE: (
        RoleTarget("token_maker", minimum=10, target=15),
        RoleTarget("token_payoff", minimum=3, target=6),
        RoleTarget("card_draw", minimum=3, target=6),
        RoleTarget("removal", minimum=0, target=5),
    ),
    TokenPlan.ARISTOCRATS: (
        RoleTarget("token_maker", minimum=10, target=15),
        RoleTarget("sacrifice", minimum=3, target=5),
        RoleTarget("token_payoff", minimum=3, target=7),
        RoleTarget("card_draw", minimum=0, target=3),
        RoleTarget("removal", minimum=0, target=4),
    ),
}


def token_profile_for_plan(
    plan: TokenPlan,
    *,
    lands: int = TOKENS_PROFILE.lands,
) -> DeckProfile:
    """Return density targets that express one coherent token game plan.

    Minimums are intentionally conservative. They force the defining package
    for each plan without consuming every spell slot, leaving room for curve,
    interaction and protection decisions in the composition engine.
    """

    return replace(
        TOKENS_PROFILE,
        name=f"{TOKENS_PROFILE.name} — {plan.label}",
        lands=lands,
        role_targets=_PLAN_ROLE_TARGETS[plan],
    )
