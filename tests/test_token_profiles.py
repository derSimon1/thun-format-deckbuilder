from dataclasses import dataclass

from thun_deckbuilder.token_plan import TokenPlan
from thun_deckbuilder.token_profiles import (
    capacity_checked_token_profile,
    token_profile_for_plan,
)


def targets(profile):
    return {str(item.role): (item.minimum, item.target) for item in profile.role_targets}


def test_go_wide_profile_requires_reliable_production_and_real_payoffs():
    role_targets = targets(token_profile_for_plan(TokenPlan.GO_WIDE))
    assert role_targets["token_creature_maker"] == (15, 20)
    assert role_targets["token_immediate_maker"] == (9, 12)
    assert role_targets["token_multi_maker"] == (6, 9)
    assert role_targets["anthem"] == (3, 6)
    assert "sacrifice_outlet" not in role_targets


def test_value_profile_requires_repeatable_creature_sources():
    role_targets = targets(token_profile_for_plan(TokenPlan.VALUE))
    assert role_targets["token_creature_maker"] == (10, 15)
    assert role_targets["token_repeatable_maker"] == (6, 8)
    assert role_targets["card_draw"] == (0, 6)


def test_aristocrats_profile_requires_all_three_package_components():
    role_targets = targets(token_profile_for_plan(TokenPlan.ARISTOCRATS))
    assert role_targets["token_creature_maker"] == (10, 15)
    assert role_targets["sacrifice_outlet"] == (3, 5)
    assert role_targets["death_payoff"] == (3, 6)
    assert "sacrifice" not in role_targets


def test_custom_land_count_preserves_plan_targets():
    profile = token_profile_for_plan(TokenPlan.GO_WIDE, lands=22)
    assert profile.lands == 22
    assert targets(profile)["token_immediate_maker"] == (9, 12)


def test_hard_requirements_are_plan_specific_and_capacity_checked():
    go_wide = {
        str(item.role)
        for item in token_profile_for_plan(TokenPlan.GO_WIDE).role_targets
        if item.minimum > 0
    }
    value = {
        str(item.role)
        for item in token_profile_for_plan(TokenPlan.VALUE).role_targets
        if item.minimum > 0
    }
    aristocrats = {
        str(item.role)
        for item in token_profile_for_plan(TokenPlan.ARISTOCRATS).role_targets
        if item.minimum > 0
    }
    assert go_wide == {
        "token_creature_maker",
        "token_immediate_maker",
        "token_multi_maker",
        "anthem",
    }
    assert value == {"token_creature_maker", "token_repeatable_maker"}
    assert aristocrats == {
        "token_creature_maker",
        "sacrifice_outlet",
        "death_payoff",
    }


@dataclass(frozen=True)
class FixtureCard:
    roles: tuple[str, ...]


def test_capacity_check_only_caps_unreachable_sparse_pool_targets():
    profile = token_profile_for_plan(TokenPlan.VALUE)
    sparse_cards = (
        FixtureCard(("token_creature_maker",)),
        FixtureCard(("token_repeatable_maker", "token_creature_maker")),
    )
    adjusted, warnings = capacity_checked_token_profile(
        profile,
        sparse_cards,
        max_copies=3,
        deck_size=60,
    )
    adjusted_targets = targets(adjusted)

    assert adjusted_targets["token_creature_maker"] == (6, 6)
    assert adjusted_targets["token_repeatable_maker"] == (3, 3)
    assert adjusted_targets["token_value_payoff"] == (0, 0)
    assert warnings


def test_capacity_check_preserves_reachable_hard_go_wide_targets():
    profile = token_profile_for_plan(TokenPlan.GO_WIDE)
    cards = tuple(
        FixtureCard(
            (
                "token_creature_maker",
                "token_immediate_maker",
                "token_multi_maker",
                "anthem",
            )
        )
        for _ in range(7)
    )
    adjusted, warnings = capacity_checked_token_profile(
        profile,
        cards,
        max_copies=3,
        deck_size=60,
    )

    adjusted_targets = targets(adjusted)
    assert adjusted_targets["token_creature_maker"] == (15, 20)
    assert adjusted_targets["token_immediate_maker"] == (9, 12)
    assert adjusted_targets["token_multi_maker"] == (6, 9)
    assert adjusted_targets["anthem"] == (3, 6)
    assert not any(
        role in warning
        for warning in warnings
        for role in (
            "token_creature_maker",
            "token_immediate_maker",
            "token_multi_maker",
            "anthem",
        )
    )
    assert any("removal" in warning for warning in warnings)
