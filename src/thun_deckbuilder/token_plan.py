from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable, Protocol

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.token_packages import analyze_token_package


class TokenPlan(StrEnum):
    """Coherent strategic plans supported by the token builder."""

    GO_WIDE = "go_wide"
    VALUE = "value_tokens"
    ARISTOCRATS = "aristocrats"

    @property
    def label(self) -> str:
        return {
            TokenPlan.GO_WIDE: "Go Wide",
            TokenPlan.VALUE: "Value Tokens",
            TokenPlan.ARISTOCRATS: "Aristocrats",
        }[self]


@dataclass(frozen=True)
class TokenCardSignals:
    creates_tokens: bool = False
    creates_multiple_tokens: bool = False
    repeatable_source: bool = False
    anthem: bool = False
    evasion_payoff: bool = False
    card_advantage: bool = False
    token_value_payoff: bool = False
    sacrifice: bool = False
    death_payoff: bool = False
    drain_payoff: bool = False


@dataclass(frozen=True)
class TokenPlanReport:
    plan: TokenPlan
    scores: tuple[tuple[TokenPlan, float], ...]
    support: tuple[tuple[TokenPlan, int], ...]
    confidence: float

    def score_for(self, plan: TokenPlan) -> float:
        return dict(self.scores)[plan]


class TokenCardLike(Protocol):
    analysis: CardAnalysis
    roles: Iterable[str]


def token_card_signals(
    analysis: CardAnalysis,
    roles: Iterable[str] = (),
) -> TokenCardSignals:
    """Extract plan-level signals from the shared Token package definition."""

    normalized_roles = {str(role) for role in roles}
    package = analyze_token_package(analysis)
    text = analysis.oracle_text.lower()
    card_advantage = "card_draw" in normalized_roles or any(
        phrase in text
        for phrase in (
            "draw a card",
            "investigate",
            "exile the top card",
            "return target card",
        )
    )
    return TokenCardSignals(
        creates_tokens=package.creates_creature_tokens,
        creates_multiple_tokens=package.creates_multiple_creature_tokens,
        repeatable_source=package.repeatable_creature_source,
        anthem=package.anthem,
        evasion_payoff=package.evasion_payoff,
        card_advantage=card_advantage,
        token_value_payoff=package.token_value_payoff,
        sacrifice=package.sacrifice_outlet,
        death_payoff=package.death_payoff,
        drain_payoff=package.drain_payoff,
    )


def detect_token_plan(cards: Iterable[TokenCardLike]) -> TokenPlanReport:
    """Select one coherent Token plan before composition starts.

    Aristocrats is only a valid candidate when the legal pool contains all
    three independent package components: creature material, a reusable outlet
    and an other-creature death payoff. A single card with several related
    phrases cannot fabricate that support by itself.
    """

    scores = {plan: 0.0 for plan in TokenPlan}
    support = {plan: 0 for plan in TokenPlan}
    maker_count = 0
    aristocrats_components: set[str] = set()

    for card in cards:
        signals = token_card_signals(card.analysis, card.roles)
        if signals.creates_tokens:
            maker_count += 1
            aristocrats_components.add("material")
            for plan in TokenPlan:
                scores[plan] += 1.0

        scores[TokenPlan.GO_WIDE] += 3.0 * signals.creates_multiple_tokens
        scores[TokenPlan.GO_WIDE] += 3.0 * signals.anthem
        scores[TokenPlan.GO_WIDE] += 2.0 * signals.evasion_payoff
        support[TokenPlan.GO_WIDE] += sum(
            (
                signals.creates_multiple_tokens,
                signals.anthem,
                signals.evasion_payoff,
            )
        )

        scores[TokenPlan.VALUE] += 4.0 * signals.repeatable_source
        scores[TokenPlan.VALUE] += 2.5 * signals.card_advantage
        scores[TokenPlan.VALUE] += 3.0 * signals.token_value_payoff
        support[TokenPlan.VALUE] += sum(
            (
                signals.repeatable_source,
                signals.card_advantage,
                signals.token_value_payoff,
            )
        )

        if signals.sacrifice:
            aristocrats_components.add("outlet")
        if signals.death_payoff:
            aristocrats_components.add("death_payoff")
        scores[TokenPlan.ARISTOCRATS] += 3.5 * signals.sacrifice
        scores[TokenPlan.ARISTOCRATS] += 4.0 * signals.death_payoff
        scores[TokenPlan.ARISTOCRATS] += 2.0 * signals.drain_payoff

    support[TokenPlan.ARISTOCRATS] = len(aristocrats_components)
    if maker_count == 0:
        scores = {plan: 0.0 for plan in TokenPlan}
    if support[TokenPlan.VALUE] < 2:
        scores[TokenPlan.VALUE] *= 0.25
    if aristocrats_components != {"material", "outlet", "death_payoff"}:
        scores[TokenPlan.ARISTOCRATS] *= 0.15
    if support[TokenPlan.GO_WIDE] == 0:
        scores[TokenPlan.GO_WIDE] *= 0.5

    tie_order = {
        TokenPlan.GO_WIDE: 2,
        TokenPlan.VALUE: 1,
        TokenPlan.ARISTOCRATS: 0,
    }
    selected = max(
        TokenPlan,
        key=lambda plan: (scores[plan], tie_order[plan]),
    )
    ordered_scores = sorted(scores.values(), reverse=True)
    best = ordered_scores[0]
    second = ordered_scores[1] if len(ordered_scores) > 1 else 0.0
    confidence = (
        0.0
        if best <= 0
        else max(0.0, min(1.0, (best - second) / best))
    )
    return TokenPlanReport(
        plan=selected,
        scores=tuple((plan, scores[plan]) for plan in TokenPlan),
        support=tuple((plan, support[plan]) for plan in TokenPlan),
        confidence=confidence,
    )
