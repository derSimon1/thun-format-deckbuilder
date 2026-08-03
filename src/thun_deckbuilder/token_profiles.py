from __future__ import annotations

from dataclasses import replace

from thun_deckbuilder.deck_profile import DeckProfile, RoleTarget, TOKENS_PROFILE
from thun_deckbuilder.token_plan import TokenPlan


_PLAN_ROLE_TARGETS: dict[TokenPlan, tuple[RoleTarget, ...]] = {
    TokenPlan.GO_WIDE: (
        RoleTarget("token_creature_maker", minimum=12, target=18),
        RoleTarget("anthem", minimum=3, target=7),
        RoleTarget("removal", minimum=0, target=5),
        RoleTarget("card_draw", minimum=0, target=3),
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
    """Return evidence-backed density targets for one coherent Token plan.

    Run 55 measured ample Mono-White capacity for creature material, repeatable
    makers, outlets, death payoffs and anthems. Hard minimums therefore use the
    precise package roles rather than broad ``token_maker`` or ``sacrifice``
    labels that also included Food and one-shot costs.
    """

    return replace(
        TOKENS_PROFILE,
        name=f"{TOKENS_PROFILE.name} — {plan.label}",
        lands=lands,
        role_targets=_PLAN_ROLE_TARGETS[plan],
    )
