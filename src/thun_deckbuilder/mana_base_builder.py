from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.mana_distribution import ManaDistribution, distribute_basic_lands
from thun_deckbuilder.mana_quality import ManaQualityReport, analyze_mana_quality
from thun_deckbuilder.mana_requirement import ManaRequirement, requirement_for_spells


@dataclass(frozen=True)
class ManaBaseResult:
    distribution: ManaDistribution
    requirement: ManaRequirement
    quality: ManaQualityReport


class ManaBaseBuilder:
    """Build a conservative basic-land mana base for an existing spell section."""

    def recommend_land_count(self, entries: tuple[object, ...], deck_size: int = 60) -> int:
        spell_count = sum(int(getattr(entry, "quantity", 1)) for entry in entries)
        if spell_count == 0:
            return round(deck_size * 0.4)
        average_mv = sum(
            float(getattr(entry, "mana_value", 0.0)) * int(getattr(entry, "quantity", 1))
            for entry in entries
        ) / spell_count
        base = round(deck_size * 0.4)
        if average_mv <= 2.0:
            base -= 2
        elif average_mv <= 2.5:
            base -= 1
        elif average_mv >= 3.5:
            base += 2
        elif average_mv >= 3.0:
            base += 1
        return max(round(deck_size * 0.33), min(round(deck_size * 0.47), base))

    def build(
        self,
        entries: tuple[object, ...],
        *,
        total_lands: int | None = None,
        deck_size: int = 60,
    ) -> ManaBaseResult:
        requirement = requirement_for_spells(entries)
        recommended = self.recommend_land_count(entries, deck_size)
        land_count = recommended if total_lands is None else total_lands
        distribution = distribute_basic_lands(requirement, land_count)
        quality = analyze_mana_quality(
            requirement,
            distribution,
            recommended_lands=recommended,
        )
        return ManaBaseResult(distribution, requirement, quality)
