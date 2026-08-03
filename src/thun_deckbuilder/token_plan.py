from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable, Protocol

from thun_deckbuilder.card_analyzer import CardAnalysis


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


_MULTI_TOKEN_PATTERN = re.compile(
    r"create (?:up to )?(?:two|three|four|five|six|[2-9]|\d{2,}) "
    r"[^.\n]*?tokens?"
)


def token_card_signals(
    analysis: CardAnalysis,
    roles: Iterable[str] = (),
) -> TokenCardSignals:
    """Extract plan-level signals without depending on individual card names."""

    text = analysis.oracle_text.lower()
    normalized_roles = {str(role) for role in roles}
    creates_tokens = "create" in text and "token" in text
    creates_multiple = bool(_MULTI_TOKEN_PATTERN.search(text)) or any(
        phrase in text
        for phrase in (
            "create x ",
            "for each",
            "that many tokens",
        )
    )
    repeatable_source = creates_tokens and any(
        phrase in text
        for phrase in (
            "at the beginning of",
            "whenever one or more",
            "whenever another",
            "whenever a creature",
            "whenever you attack",
            "whenever this creature attacks",
            "{t}: create",
        )
    )
    anthem = "anthem" in normalized_roles or any(
        phrase in text
        for phrase in (
            "creatures you control get +",
            "other creatures you control get +",
            "tokens you control get +",
            "creature tokens you control get +",
            "put a +1/+1 counter on each",
        )
    )
    evasion_payoff = any(
        phrase in text
        for phrase in (
            "creatures you control have flying",
            "creature tokens you control have flying",
            "creatures you control can't be blocked",
            "creature tokens you control can't be blocked",
            "creatures you control have menace",
        )
    )
    card_advantage = "card_draw" in normalized_roles or any(
        phrase in text
        for phrase in (
            "draw a card",
            "investigate",
            "exile the top card",
            "return target card",
        )
    )
    token_value_payoff = card_advantage and any(
        phrase in text
        for phrase in (
            "whenever a token enters",
            "whenever one or more tokens",
            "when one or more tokens",
            "for each token you control",
        )
    )
    sacrifice = "sacrifice" in normalized_roles or "sacrifice" in text
    death_payoff = any(
        phrase in text
        for phrase in (
            "whenever another creature dies",
            "whenever a creature you control dies",
            "whenever one or more creatures you control die",
            "when another creature dies",
            "when this creature dies",
        )
    )
    drain_payoff = (death_payoff or sacrifice) and any(
        phrase in text
        for phrase in (
            "each opponent loses",
            "target opponent loses",
            "opponent loses 1 life",
            "you gain 1 life",
        )
    )
    return TokenCardSignals(
        creates_tokens=creates_tokens,
        creates_multiple_tokens=creates_multiple,
        repeatable_source=repeatable_source,
        anthem=anthem,
        evasion_payoff=evasion_payoff,
        card_advantage=card_advantage,
        token_value_payoff=token_value_payoff,
        sacrifice=sacrifice,
        death_payoff=death_payoff,
        drain_payoff=drain_payoff,
    )


def detect_token_plan(cards: Iterable[TokenCardLike]) -> TokenPlanReport:
    """Select one coherent token plan before composition starts.

    The detector uses broad rules and distinct support signals. A plan without
    token material or enough supporting pieces is discounted so one incidental
    wording cannot redirect the complete deck.
    """

    scores = {plan: 0.0 for plan in TokenPlan}
    support = {plan: 0 for plan in TokenPlan}
    maker_count = 0

    for card in cards:
        signals = token_card_signals(card.analysis, card.roles)
        if signals.creates_tokens:
            maker_count += 1
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

        scores[TokenPlan.ARISTOCRATS] += 3.5 * signals.sacrifice
        scores[TokenPlan.ARISTOCRATS] += 4.0 * signals.death_payoff
        scores[TokenPlan.ARISTOCRATS] += 4.0 * signals.drain_payoff
        support[TokenPlan.ARISTOCRATS] += sum(
            (
                signals.sacrifice,
                signals.death_payoff,
                signals.drain_payoff,
            )
        )

    if maker_count == 0:
        scores = {plan: 0.0 for plan in TokenPlan}
    for plan in (TokenPlan.VALUE, TokenPlan.ARISTOCRATS):
        if support[plan] < 2:
            scores[plan] *= 0.25
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
