from thun_deckbuilder.token_plan import TokenPlan
from thun_deckbuilder.token_profiles import token_profile_for_plan


def targets(profile):
    return {str(item.role): (item.minimum, item.target) for item in profile.role_targets}


def test_go_wide_profile_requires_board_development_and_targets_payoffs():
    profile = token_profile_for_plan(TokenPlan.GO_WIDE)
    role_targets = targets(profile)

    assert profile.name.endswith("Go Wide")
    assert role_targets["token_maker"] == (12, 18)
    assert role_targets["token_payoff"] == (0, 7)
    assert "sacrifice" not in role_targets


def test_value_profile_targets_card_advantage_without_hard_deadlock():
    profile = token_profile_for_plan(TokenPlan.VALUE)
    role_targets = targets(profile)

    assert profile.name.endswith("Value Tokens")
    assert role_targets["card_draw"] == (0, 6)
    assert role_targets["token_maker"][0] < targets(
        token_profile_for_plan(TokenPlan.GO_WIDE)
    )["token_maker"][0]


def test_aristocrats_profile_targets_outlet_and_payoff_without_requiring_sparse_roles():
    profile = token_profile_for_plan(TokenPlan.ARISTOCRATS)
    role_targets = targets(profile)

    assert profile.name.endswith("Aristocrats")
    assert role_targets["token_maker"][0] >= 10
    assert role_targets["sacrifice"] == (0, 5)
    assert role_targets["token_payoff"] == (0, 7)


def test_custom_land_count_preserves_plan_targets():
    profile = token_profile_for_plan(TokenPlan.VALUE, lands=22)

    assert profile.lands == 22
    assert targets(profile)["card_draw"] == (0, 6)


def test_only_broadly_available_token_makers_are_hard_requirements():
    for plan in TokenPlan:
        profile = token_profile_for_plan(plan)
        hard_roles = {
            str(item.role) for item in profile.role_targets if item.minimum > 0
        }
        assert hard_roles == {"token_maker"}
