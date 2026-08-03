from thun_deckbuilder.token_plan import TokenPlan
from thun_deckbuilder.token_profiles import token_profile_for_plan


def targets(profile):
    return {str(item.role): (item.minimum, item.target) for item in profile.role_targets}


def test_go_wide_profile_requires_creature_material_and_real_payoffs():
    profile = token_profile_for_plan(TokenPlan.GO_WIDE)
    role_targets = targets(profile)

    assert profile.name.endswith("Go Wide")
    assert role_targets["token_creature_maker"] == (12, 18)
    assert role_targets["anthem"] == (3, 7)
    assert "sacrifice_outlet" not in role_targets
    assert "token_maker" not in role_targets


def test_value_profile_requires_repeatable_creature_sources():
    profile = token_profile_for_plan(TokenPlan.VALUE)
    role_targets = targets(profile)

    assert profile.name.endswith("Value Tokens")
    assert role_targets["token_creature_maker"] == (10, 15)
    assert role_targets["token_repeatable_maker"] == (6, 8)
    assert role_targets["card_draw"] == (0, 6)


def test_aristocrats_profile_requires_all_three_package_components():
    profile = token_profile_for_plan(TokenPlan.ARISTOCRATS)
    role_targets = targets(profile)

    assert profile.name.endswith("Aristocrats")
    assert role_targets["token_creature_maker"] == (10, 15)
    assert role_targets["sacrifice_outlet"] == (3, 5)
    assert role_targets["death_payoff"] == (3, 6)
    assert "sacrifice" not in role_targets


def test_custom_land_count_preserves_plan_targets():
    profile = token_profile_for_plan(TokenPlan.VALUE, lands=22)

    assert profile.lands == 22
    assert targets(profile)["token_repeatable_maker"] == (6, 8)


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

    assert go_wide == {"token_creature_maker", "anthem"}
    assert value == {"token_creature_maker", "token_repeatable_maker"}
    assert aristocrats == {
        "token_creature_maker",
        "sacrifice_outlet",
        "death_payoff",
    }
