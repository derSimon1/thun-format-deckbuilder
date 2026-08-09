from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from thun_deckbuilder.deck_generator import DeckEntry
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.token_plan import TokenPlan, token_card_signals


@dataclass(frozen=True)
class EngineDensityReport:
    """Measure repeatable, plan-relevant engines in a generated token deck."""

    plan: str
    engine_copies: int
    spell_copies: int
    engine_density: float
    distinct_engines: int
    engine_names: tuple[str, ...]
    engine_required: bool
    warnings: tuple[str, ...] = ()


def _supports_engine_plan(card: CardKnowledge, plan: TokenPlan) -> bool:
    signals = token_card_signals(card.analysis, card.roles)
    if plan is TokenPlan.GO_WIDE:
        return signals.repeatable_source or (
            signals.anthem and card.analysis.is_creature
        )
    if plan is TokenPlan.VALUE:
        return signals.repeatable_source or signals.token_value_payoff
    return signals.death_payoff or signals.drain_payoff or (
        signals.sacrifice
        and any(
            marker in card.analysis.oracle_text.lower()
            for marker in ("whenever", "at the beginning", "draw a card")
        )
    )


def evaluate_token_engine_density(
    entries: Iterable[DeckEntry],
    cards: Iterable[CardKnowledge],
    plan: TokenPlan,
) -> EngineDensityReport:
    """Return a copy-weighted engine density without inventing card values.

    One-shot token makers are material, not engines. Engines must provide a
    repeatable or triggered effect that advances the selected plan. Unknown
    entries remain part of the denominator and therefore cannot inflate the
    result.
    """

    knowledge_by_name = {
        card.analysis.name.casefold(): card
        for card in cards
    }
    engine_copies = 0
    spell_copies = 0
    engine_names: list[str] = []

    for entry in entries:
        spell_copies += entry.quantity
        knowledge = knowledge_by_name.get(entry.name.casefold())
        if knowledge is None or not _supports_engine_plan(knowledge, plan):
            continue
        engine_copies += entry.quantity
        engine_names.append(entry.name)

    density = 0.0 if spell_copies == 0 else engine_copies / spell_copies
    distinct = len(set(engine_names))
    warnings: list[str] = []
    engine_required = plan.requires_engine
    if engine_copies == 0 and engine_required:
        warnings.append(
            f"Keine wiederholbare Engine für {plan.label} im Deck erkannt."
        )
    elif distinct == 1:
        warnings.append(
            f"Engine-Paket für {plan.label} hängt nur von einer Karte ab."
        )

    return EngineDensityReport(
        plan=plan.value,
        engine_copies=engine_copies,
        spell_copies=spell_copies,
        engine_density=density,
        distinct_engines=distinct,
        engine_names=tuple(sorted(set(engine_names))),
        engine_required=engine_required,
        warnings=tuple(warnings),
    )
