from __future__ import annotations

from dataclasses import replace

from thun_deckbuilder.deck_profile import DeckProfile, RoleTarget, TOKENS_PROFILE
from thun_deckbuilder.token_plan import TokenPlan


_PLAN_ROLE_TARGETS: dict[TokenPlan, tuple[RoleTarget, ...]] = {
    TokenPlan.GO_WIDE: (
        RoleTarget("token_maker", minimum=12, target=18),
        RoleTarget("token_payoff", minimum=0, target=7),
        RoleTarget("removal", minimum=0, target=5),
        RoleTarget("card_draw", minimum=0, target=3),
    ),
    TokenPlan.VALUE: (
        RoleTarget("token_maker", minimum=10, target=15),
        RoleTarget("token_payoff", minimum=0, target=6),
        RoleTarget("card_draw", minimum=0, target=6),
        RoleTarget("removal", minimum=0, target=5),
    ),
    TokenPlan.ARISTOCRATS: (
        RoleTarget("token_maker", minimum=10, target=15),
        RoleTarget("sacrifice", minimum=0, target=5),
        RoleTarget("token_payoff", minimum=0, target=7),
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

    Token makers remain the only hard minimum until the legal pool can be
    checked before composition. Plan-defining support roles are soft targets:
    the composition engine should prefer them, but must not deadlock when a
    sparse fixture or legal pool cannot supply enough distinct copies.
    """

    return replace(
        TOKENS_PROFILE,
        name=f"{TOKENS_PROFILE.name} — {plan.label}",
        lands=lands,
        role_targets=_PLAN_ROLE_TARGETS[plan],
    )
