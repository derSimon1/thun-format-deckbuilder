from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from thun_deckbuilder.deck_generator import DeckEntry
from thun_deckbuilder.token_plan import TokenPlan


@dataclass(frozen=True)
class StrategyCommitmentReport:
    """Explain how strongly a generated deck follows its selected plan."""

    plan: str
    commitment_score: float
    committed_cards: int
    conflicting_cards: int
    neutral_cards: int
    role_densities: tuple[tuple[str, int], ...]
    warnings: tuple[str, ...] = ()


_PLAN_ROLES: dict[TokenPlan, frozenset[str]] = {
    TokenPlan.GO_WIDE: frozenset({"token_maker", "token_payoff", "anthem"}),
    TokenPlan.VALUE: frozenset({"token_maker", "token_payoff", "card_draw"}),
    TokenPlan.ARISTOCRATS: frozenset(
        {"token_maker", "token_payoff", "sacrifice"}
    ),
}

_CONFLICTING_ROLES: dict[TokenPlan, frozenset[str]] = {
    TokenPlan.GO_WIDE: frozenset({"sacrifice"}),
    TokenPlan.VALUE: frozenset({"sacrifice"}),
    TokenPlan.ARISTOCRATS: frozenset({"anthem"}),
}


def evaluate_token_commitment(
    entries: Iterable[DeckEntry],
    plan: TokenPlan,
) -> StrategyCommitmentReport:
    """Measure plan adherence without treating utility cards as mismatches.

    Copies that support at least one defining role count as committed. A copy is
    conflicting only when it carries a plan-opposed role and no defining role.
    Removal and protection remain neutral so interaction is not punished.
    """

    role_counts: dict[str, int] = {}
    committed = 0
    conflicting = 0
    neutral = 0
    defining = _PLAN_ROLES[plan]
    opposed = _CONFLICTING_ROLES[plan]

    for entry in entries:
        roles = {str(role) for role in entry.roles}
        for role in roles:
            role_counts[role] = role_counts.get(role, 0) + entry.quantity
        if roles.intersection(defining):
            committed += entry.quantity
        elif roles.intersection(opposed):
            conflicting += entry.quantity
        else:
            neutral += entry.quantity

    strategic_total = committed + conflicting
    score = 1.0 if strategic_total == 0 else committed / strategic_total
    warnings: list[str] = []
    if strategic_total == 0:
        warnings.append("Kein planprägendes Rollenpaket im Deck erkannt.")
    if conflicting:
        warnings.append(
            f"{conflicting} Kartenkopien tragen nur planfremde Rollen für {plan.label}."
        )
    if score < 0.75:
        warnings.append(
            f"Strategy Commitment für {plan.label} ist mit {score:.0%} zu niedrig."
        )

    return StrategyCommitmentReport(
        plan=plan.value,
        commitment_score=score,
        committed_cards=committed,
        conflicting_cards=conflicting,
        neutral_cards=neutral,
        role_densities=tuple(sorted(role_counts.items())),
        warnings=tuple(warnings),
    )
