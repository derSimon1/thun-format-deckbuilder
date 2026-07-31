from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from thun_deckbuilder.deck_generator import GeneratedDeck


@dataclass(frozen=True)
class BenchmarkProfile:
    archetype: str
    display_name: str
    role_targets: tuple[tuple[str, int], ...]
    curve_targets: tuple[tuple[str, int], ...]
    lands: int


@dataclass(frozen=True)
class BenchmarkItem:
    key: str
    target: int
    actual: int
    score: int


@dataclass(frozen=True)
class BenchmarkReport:
    name: str
    role_items: tuple[BenchmarkItem, ...]
    curve_items: tuple[BenchmarkItem, ...]
    land_item: BenchmarkItem
    score: int


BENCHMARKS: dict[str, BenchmarkProfile] = {
    "burn": BenchmarkProfile(
        archetype="burn",
        display_name="Mono-Red Burn",
        role_targets=(("burn", 24), ("aggro_creature", 9), ("card_draw", 3)),
        curve_targets=(("1", 12), ("2", 16), ("3", 6), ("4+", 2)),
        lands=24,
    ),
    "tokens": BenchmarkProfile(
        archetype="tokens",
        display_name="Mono-White Tokens",
        role_targets=(("token_maker", 18), ("token_payoff", 6), ("removal", 6), ("card_draw", 3)),
        curve_targets=(("1", 8), ("2", 12), ("3", 10), ("4+", 6)),
        lands=24,
    ),
}


def _closeness(actual: int, target: int) -> int:
    if target <= 0:
        return 100 if actual == 0 else 0
    difference = abs(actual - target)
    return max(0, round(100 * (1 - difference / target)))


def _curve_band(mana_value: float) -> str:
    if mana_value <= 1:
        return "1"
    if mana_value <= 2:
        return "2"
    if mana_value <= 3:
        return "3"
    return "4+"


class BenchmarkAnalyzer:
    def analyze(self, deck: GeneratedDeck, archetype: str) -> BenchmarkReport:
        profile = BENCHMARKS.get(archetype)
        if profile is None:
            raise ValueError(f"No benchmark is defined for archetype '{archetype}'.")

        role_counts: Counter[str] = Counter()
        curve_counts: Counter[str] = Counter()
        for entry in deck.mainboard:
            for role in entry.roles:
                role_counts[str(role)] += entry.quantity
            curve_counts[_curve_band(entry.mana_value)] += entry.quantity

        role_items = tuple(
            BenchmarkItem(role, target, role_counts[role], _closeness(role_counts[role], target))
            for role, target in profile.role_targets
        )
        curve_items = tuple(
            BenchmarkItem(band, target, curve_counts[band], _closeness(curve_counts[band], target))
            for band, target in profile.curve_targets
        )
        land_item = BenchmarkItem("lands", profile.lands, deck.lands, _closeness(deck.lands, profile.lands))
        all_scores = [item.score for item in role_items + curve_items] + [land_item.score]
        score = round(sum(all_scores) / len(all_scores)) if all_scores else 0
        return BenchmarkReport(profile.display_name, role_items, curve_items, land_item, score)
