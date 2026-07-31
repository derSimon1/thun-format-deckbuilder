from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.benchmark_loader import BenchmarkDefinition
from thun_deckbuilder.deck_generator import GeneratedDeck


@dataclass(frozen=True)
class BenchmarkMetric:
    label: str
    actual: float
    target: float
    score: float
    minimum: float = 0.0

    @property
    def minimum_met(self) -> bool:
        return self.actual >= self.minimum


@dataclass(frozen=True)
class BenchmarkReport:
    benchmark_key: str
    benchmark_name: str
    role_metrics: tuple[BenchmarkMetric, ...]
    curve_metrics: tuple[BenchmarkMetric, ...]
    land_metric: BenchmarkMetric
    role_score: float
    curve_score: float
    land_score: float
    overall_score: int

    @property
    def minimums_met(self) -> bool:
        return all(metric.minimum_met for metric in self.role_metrics)


class BenchmarkEngine:
    ROLE_WEIGHT = 0.60
    CURVE_WEIGHT = 0.25
    LAND_WEIGHT = 0.15

    def evaluate(self, deck: GeneratedDeck, benchmark: BenchmarkDefinition) -> BenchmarkReport:
        role_metrics = tuple(
            self._metric(target.role, self._role_count(deck, target.role), target.target, target.minimum)
            for target in benchmark.role_targets
        )
        curve_metrics = self._curve_metrics(deck, benchmark)
        land_metric = self._metric("lands", deck.lands, benchmark.lands, benchmark.lands)
        role_score = self._average(tuple(item.score for item in role_metrics))
        curve_score = self._average(tuple(item.score for item in curve_metrics))
        land_score = land_metric.score
        overall = round(
            role_score * self.ROLE_WEIGHT
            + curve_score * self.CURVE_WEIGHT
            + land_score * self.LAND_WEIGHT
        )
        return BenchmarkReport(
            benchmark_key=benchmark.key,
            benchmark_name=benchmark.name,
            role_metrics=role_metrics,
            curve_metrics=curve_metrics,
            land_metric=land_metric,
            role_score=role_score,
            curve_score=curve_score,
            land_score=land_score,
            overall_score=max(0, min(100, overall)),
        )

    @staticmethod
    def _role_count(deck: GeneratedDeck, role: str) -> float:
        return sum(entry.quantity for entry in deck.mainboard if role in entry.roles)

    def _curve_metrics(self, deck: GeneratedDeck, benchmark: BenchmarkDefinition) -> tuple[BenchmarkMetric, ...]:
        result: list[BenchmarkMetric] = []
        previous = -1.0
        for target in benchmark.curve_targets:
            actual = sum(
                entry.quantity
                for entry in deck.mainboard
                if previous < entry.mana_value <= target.maximum_mana_value
            )
            label = f"MV {previous + 1:g}-{target.maximum_mana_value:g}"
            result.append(self._metric(label, actual, target.target))
            previous = target.maximum_mana_value
        return tuple(result)

    @staticmethod
    def _metric(label: str, actual: float, target: float, minimum: float = 0.0) -> BenchmarkMetric:
        if target <= 0:
            score = 100.0 if actual <= 0 else 0.0
        else:
            deviation = abs(actual - target) / target
            score = max(0.0, 100.0 * (1.0 - deviation))
        return BenchmarkMetric(label, actual, target, score, minimum)

    @staticmethod
    def _average(values: tuple[float, ...]) -> float:
        return sum(values) / len(values) if values else 100.0
