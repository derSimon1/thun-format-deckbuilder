from thun_deckbuilder.mana_distribution import distribute_basic_lands
from thun_deckbuilder.mana_requirement import ManaRequirement


def test_mono_color_distribution_uses_only_matching_basic():
    requirement = ManaRequirement((("W", 20.0), ("U", 0.0), ("B", 0.0), ("R", 0.0), ("G", 0.0)))
    result = distribute_basic_lands(requirement, 24)
    assert [(land.land_name, land.quantity) for land in result.lands] == [("Plains", 24)]


def test_two_color_distribution_favors_early_and_heavier_color():
    requirement = ManaRequirement(
        (("W", 20.0), ("U", 8.0), ("B", 0.0), ("R", 0.0), ("G", 0.0)),
        (("W", 10.0), ("U", 1.0), ("B", 0.0), ("R", 0.0), ("G", 0.0)),
    )
    result = distribute_basic_lands(requirement, 24)
    assert result.sources_for("W") > result.sources_for("U")
    assert sum(land.quantity for land in result.lands) == 24


def test_five_color_distribution_keeps_every_color_available():
    requirement = ManaRequirement(tuple((color, value) for color, value in zip("WUBRG", (12, 8, 6, 4, 1))))
    result = distribute_basic_lands(requirement, 24)
    assert all(result.sources_for(color) >= 1 for color in "WUBRG")
