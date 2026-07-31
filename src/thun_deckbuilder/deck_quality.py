from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.synergy_tag import SynergyTag


@dataclass(frozen=True)
class RoleQuality:
    role: str
    current: float
    minimum: int
    target: int
    score: float

    @property
    def minimum_met(self) -> bool:
        return self.current >= self.minimum

    @property
    def target_met(self) -> bool:
        return self.current >= self.target


@dataclass(frozen=True)
class CurveQuality:
    label: str
    current: int
    target: int
    score: float

    @property
    def target_met(self) -> bool:
        return self.current >= self.target


@dataclass(frozen=True)
class SynergyQuality:
    label: str
    enablers: int
    payoffs: int
    score: float

    @property
    def active(self) -> bool:
        return self.enablers > 0 and self.payoffs > 0


@dataclass(frozen=True)
class DeckQualityReport:
    profile_name: str
    role_quality: tuple[RoleQuality, ...]
    curve_quality: tuple[CurveQuality, ...]
    role_score: float
    curve_score: float
    overall_score: int
    synergy_quality: tuple[SynergyQuality, ...] = ()
    synergy_score: float = 100.0
    mana_score: float = 100.0

    @property
    def minimums_met(self) -> bool:
        return all(item.minimum_met for item in self.role_quality)


class DeckQualityAnalyzer:
    """Measure profile fulfilment without changing card selection.

    Role targets contribute 70 percent and curve targets 30 percent. Scores are
    capped at 100, so exceeding a target does not hide a weakness elsewhere.
    """

    ROLE_WEIGHT = 0.70
    CURVE_WEIGHT = 0.30

    def analyze(self, state: DeckState, profile: DeckProfile) -> DeckQualityReport:
        roles = tuple(self._role_quality(state, target) for target in profile.role_targets)
        curves = self._curve_quality(state, profile)

        role_score = self._average(tuple(item.score for item in roles), default=100.0)
        curve_score = self._average(tuple(item.score for item in curves), default=100.0)
        synergy_quality = self._synergy_quality(state)
        active_synergy_scores = tuple(
            item.score for item in synergy_quality if item.enablers > 0 or item.payoffs > 0
        )
        synergy_score = self._average(active_synergy_scores, default=100.0)
        overall = round(
            role_score * self.ROLE_WEIGHT + curve_score * self.CURVE_WEIGHT
        )
        return DeckQualityReport(
            profile_name=profile.name,
            role_quality=roles,
            curve_quality=curves,
            role_score=role_score,
            curve_score=curve_score,
            overall_score=max(0, min(100, overall)),
            synergy_quality=synergy_quality,
            synergy_score=synergy_score,
        )

    @staticmethod
    def _role_quality(state: DeckState, target) -> RoleQuality:
        current = state.role_count(target.role)
        score = 100.0 if target.target == 0 else min(100.0, current / target.target * 100.0)
        return RoleQuality(
            role=str(target.role),
            current=current,
            minimum=target.minimum,
            target=target.target,
            score=score,
        )

    @staticmethod
    def _curve_quality(state: DeckState, profile: DeckProfile) -> tuple[CurveQuality, ...]:
        result: list[CurveQuality] = []
        lower = 0.0
        for target in profile.curve_targets:
            current = state.curve_count(target.maximum_mana_value, lower)
            score = 100.0 if target.target == 0 else min(100.0, current / target.target * 100.0)
            result.append(
                CurveQuality(
                    label=f"{lower:g}-{target.maximum_mana_value:g}",
                    current=current,
                    target=target.target,
                    score=score,
                )
            )
            lower = target.maximum_mana_value
        return tuple(result)


    @staticmethod
    def _synergy_quality(state: DeckState) -> tuple[SynergyQuality, ...]:
        pairs = (
            ("Tokens", SynergyTag.TOKEN_MAKER, SynergyTag.TOKEN_PAYOFF),
            ("Spells", SynergyTag.SPELL, SynergyTag.SPELL_PAYOFF),
            ("Artifacts", SynergyTag.ARTIFACT, SynergyTag.ARTIFACT_PAYOFF),
            ("Sacrifice", SynergyTag.SACRIFICE_FODDER, SynergyTag.SACRIFICE_OUTLET),
            ("Death triggers", SynergyTag.SACRIFICE_FODDER, SynergyTag.DEATH_TRIGGER),
        )
        result: list[SynergyQuality] = []
        for label, enabler_tag, payoff_tag in pairs:
            enablers = state.tag_count(enabler_tag)
            payoffs = state.tag_count(payoff_tag)
            if enablers == 0 and payoffs == 0:
                continue
            if enablers > 0 and payoffs > 0:
                score = min(100.0, 50.0 + min(enablers, 8) * 4.0 + min(payoffs, 4) * 4.5)
            else:
                score = 25.0
            result.append(SynergyQuality(label, enablers, payoffs, score))

        shrines = state.tag_count(SynergyTag.SHRINE)
        if shrines > 0:
            result.append(
                SynergyQuality(
                    "Shrines",
                    shrines,
                    max(0, shrines - 1),
                    min(100.0, 25.0 + shrines * 15.0),
                )
            )
        return tuple(result)

    @staticmethod
    def _average(values: tuple[float, ...], *, default: float) -> float:
        return sum(values) / len(values) if values else default


def with_mana_quality(
    report: DeckQualityReport | None,
    mana_quality,
) -> DeckQualityReport | None:
    """Attach mana quality and include it as a conservative 15% score component."""
    if report is None:
        return None
    from dataclasses import replace

    overall = round(
        report.role_score * 0.60
        + report.curve_score * 0.25
        + mana_quality.score * 0.15
    )
    return replace(
        report,
        overall_score=max(0, min(100, overall)),
        mana_score=float(mana_quality.score),
    )
