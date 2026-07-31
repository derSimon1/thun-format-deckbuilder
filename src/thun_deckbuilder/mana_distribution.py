from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.mana_requirement import COLORS, ManaRequirement

BASIC_LANDS = {
    "W": "Plains",
    "U": "Island",
    "B": "Swamp",
    "R": "Mountain",
    "G": "Forest",
}


@dataclass(frozen=True)
class LandAllocation:
    color: str
    land_name: str
    quantity: int


@dataclass(frozen=True)
class ManaDistribution:
    lands: tuple[LandAllocation, ...]
    total_lands: int
    required_sources: tuple[tuple[str, int], ...]

    def sources_for(self, color: str) -> int:
        wanted = color.upper()
        return sum(item.quantity for item in self.lands if item.color == wanted)


def _largest_remainder(weights: dict[str, float], total: int) -> dict[str, int]:
    if total <= 0 or not weights:
        return {color: 0 for color in weights}
    weight_sum = sum(weights.values())
    if weight_sum <= 0:
        even = total / len(weights)
        raw = {color: even for color in weights}
    else:
        raw = {color: total * weight / weight_sum for color, weight in weights.items()}
    result = {color: int(value) for color, value in raw.items()}
    remaining = total - sum(result.values())
    order = sorted(weights, key=lambda color: (raw[color] - result[color], weights[color], color), reverse=True)
    for color in order[:remaining]:
        result[color] += 1
    return result


def distribute_basic_lands(requirement: ManaRequirement, total_lands: int) -> ManaDistribution:
    colors = requirement.active_colors
    if not colors:
        return ManaDistribution((), total_lands, ())

    weights = {
        color: requirement.amount(color) + requirement.early_amount(color) * 0.75
        for color in colors
    }
    quantities = _largest_remainder(weights, total_lands)

    # Every represented color must receive a source. This matters especially
    # for five-color decks with a lightly splashed color.
    zero_colors = [color for color in colors if quantities[color] == 0]
    for color in zero_colors:
        donor = max(colors, key=lambda item: quantities[item])
        if quantities[donor] > 1:
            quantities[donor] -= 1
            quantities[color] += 1

    requirements = tuple(
        (color, max(1, round(total_lands * weights[color] / sum(weights.values()))))
        for color in colors
    )
    lands = tuple(
        LandAllocation(color, BASIC_LANDS[color], quantities[color])
        for color in COLORS
        if color in quantities and quantities[color] > 0
    )
    return ManaDistribution(lands, total_lands, requirements)
