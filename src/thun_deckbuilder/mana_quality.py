from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.mana_distribution import ManaDistribution
from thun_deckbuilder.mana_requirement import ManaRequirement


@dataclass(frozen=True)
class ColorSourceQuality:
    color: str
    sources: int
    required: int
    score: float

    @property
    def sufficient(self) -> bool:
        return self.sources >= self.required


@dataclass(frozen=True)
class ManaQualityReport:
    colors: tuple[ColorSourceQuality, ...]
    land_count: int
    recommended_lands: int
    score: int

    @property
    def sufficient(self) -> bool:
        return all(item.sufficient for item in self.colors)


def analyze_mana_quality(
    requirement: ManaRequirement,
    distribution: ManaDistribution,
    *,
    recommended_lands: int,
) -> ManaQualityReport:
    required = dict(distribution.required_sources)
    colors = tuple(
        ColorSourceQuality(
            color=color,
            sources=distribution.sources_for(color),
            required=required[color],
            score=min(100.0, distribution.sources_for(color) / required[color] * 100.0),
        )
        for color in requirement.active_colors
    )
    source_score = sum(item.score for item in colors) / len(colors) if colors else 100.0
    land_delta = abs(distribution.total_lands - recommended_lands)
    land_score = max(0.0, 100.0 - land_delta * 15.0)
    score = round(source_score * 0.8 + land_score * 0.2)
    return ManaQualityReport(colors, distribution.total_lands, recommended_lands, max(0, min(100, score)))
