from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from thun_deckbuilder.deck_generator import DeckEntry
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.token_packages import analyze_token_package
from thun_deckbuilder.token_plan import TokenPlan


@dataclass(frozen=True)
class FinishDensityReport:
    """Measure copy-weighted, plan-relevant closing cards in a token deck."""

    plan: str
    finish_copies: int
    spell_copies: int
    finish_density: float
    distinct_finishers: int
    finish_names: tuple[str, ...]
    finish_modes: tuple[str, ...]
    warnings: tuple[str, ...] = ()


def _finish_modes(card: CardKnowledge, plan: TokenPlan) -> tuple[str, ...]:
    signals = analyze_token_package(card.analysis)
    if plan is TokenPlan.GO_WIDE:
        modes = []
        if signals.anthem:
            modes.append("anthem")
        if signals.evasion_payoff:
            modes.append("evasion")
        return tuple(modes)
    if plan is TokenPlan.VALUE:
        return ("value",) if signals.token_value_payoff else ()
    return ("drain",) if signals.drain_payoff else ()


def evaluate_token_finish_density(
    entries: Iterable[DeckEntry],
    cards: Iterable[CardKnowledge],
    plan: TokenPlan,
) -> FinishDensityReport:
    """Return finish density without double-counting multi-mode finishers.

    A card copy counts at most once even when it supplies more than one closing
    mode. One-shot token makers and generic role labels are not finishes.
    Unknown entries stay in the denominator and cannot inflate the result.
    """

    knowledge_by_name = {
        card.analysis.name.casefold(): card
        for card in cards
    }
    finish_copies = 0
    spell_copies = 0
    finish_names: set[str] = set()
    finish_modes: set[str] = set()

    for entry in entries:
        spell_copies += entry.quantity
        knowledge = knowledge_by_name.get(entry.name.casefold())
        if knowledge is None:
            continue
        modes = _finish_modes(knowledge, plan)
        if not modes:
            continue
        finish_copies += entry.quantity
        finish_names.add(entry.name)
        finish_modes.update(modes)

    density = 0.0 if spell_copies == 0 else finish_copies / spell_copies
    warnings: list[str] = []
    if finish_copies == 0:
        warnings.append(f"Kein klarer Abschlussweg für {plan.label} erkannt.")
    elif len(finish_names) == 1:
        warnings.append(
            f"Abschlussweg für {plan.label} hängt nur von einer Karte ab."
        )

    return FinishDensityReport(
        plan=plan.value,
        finish_copies=finish_copies,
        spell_copies=spell_copies,
        finish_density=density,
        distinct_finishers=len(finish_names),
        finish_names=tuple(sorted(finish_names)),
        finish_modes=tuple(sorted(finish_modes)),
        warnings=tuple(warnings),
    )
