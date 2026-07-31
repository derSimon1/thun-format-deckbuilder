from __future__ import annotations

from collections import Counter
from dataclasses import replace
from typing import Callable, Iterable

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown
from thun_deckbuilder.deck_generator import DeckEntry, parse_mana_cost
from thun_deckbuilder.knowledge_base import CardKnowledge


Scorer = Callable[[CardAnalysis], ScoreBreakdown]
Eligibility = Callable[[CardKnowledge, tuple[str, ...]], bool]


def _text(analysis: CardAnalysis) -> str:
    return f" {analysis.oracle_text.lower()} "


def _signals(archetype: str, analysis: CardAnalysis) -> frozenset[str]:
    text = _text(analysis)
    type_line = analysis.type_line.lower()
    signals: set[str] = set()

    if archetype == "artifacts":
        if analysis.is_artifact:
            signals.add("core")
        if any(phrase in text for phrase in (
            "affinity for artifacts", "improvise", "metalcraft",
            "whenever an artifact enters", "for each artifact you control",
            "artifacts you control get", "sacrifice an artifact",
        )):
            signals.add("payoff")
        if analysis.mana_value <= 2 and analysis.is_artifact:
            signals.add("enabler")

    elif archetype == "shrines":
        if "shrine" in type_line:
            signals.add("core")
        if "shrine" in text and any(phrase in text for phrase in (
            "for each", "number of shrines", "search your library", "return target",
        )):
            signals.add("payoff")
        if "any color" in text or "any type" in text:
            signals.add("fixing")

    elif archetype == "mill":
        opponent_mill = "target opponent mills" in text or "each opponent mills" in text
        if opponent_mill or "library into their graveyard" in text:
            signals.add("core")
        if opponent_mill and any(phrase in text for phrase in (
            "whenever", "at the beginning", "whenever a land enters",
        )):
            signals.add("engine")
        if any(phrase in text for phrase in (
            "counter target spell", "destroy target creature", "exile target creature",
            "gets -", "return target creature",
        )) and analysis.mana_value <= 3:
            signals.add("interaction")

    return frozenset(signals)


def _targets(archetype: str) -> dict[str, int]:
    return {
        "artifacts": {"core": 24, "payoff": 6, "enabler": 12},
        "shrines": {"core": 12, "payoff": 6, "fixing": 6},
        "mill": {"core": 18, "engine": 6, "interaction": 6},
    }.get(archetype, {})


def _deck_score(
    quantities: Counter[str],
    entries: dict[str, DeckEntry],
    analyses: dict[str, CardAnalysis],
    archetype: str,
) -> float:
    score = sum(entries[name].score * quantity for name, quantity in quantities.items())
    counts: Counter[str] = Counter()
    expensive = 0
    for name, quantity in quantities.items():
        analysis = analyses[name]
        for signal in _signals(archetype, analysis):
            counts[signal] += quantity
        if analysis.mana_value >= 4:
            expensive += quantity

    for signal, target in _targets(archetype).items():
        current = counts[signal]
        score += min(current, target) * 1.25
        if current < target:
            score -= (target - current) * 2.25

    # Pairwise deck synergies. These bonuses only exist when both halves are present.
    if archetype == "artifacts":
        score += min(counts["payoff"], 8) * min(counts["core"], 30) * 0.08
    elif archetype == "shrines":
        score += min(counts["payoff"], 8) * min(counts["core"], 15) * 0.12
        score += min(counts["fixing"], 8) * min(counts["core"], 15) * 0.06
    elif archetype == "mill":
        score += min(counts["engine"], 8) * min(counts["core"], 24) * 0.10
        score += min(counts["interaction"], 8) * min(counts["core"], 24) * 0.04

    score -= expensive * (1.1 if archetype == "mill" else 0.6)
    return score


def optimize_entries(
    entries: tuple[DeckEntry, ...],
    cards: Iterable[CardKnowledge],
    *,
    archetype: str,
    colors: tuple[str, ...],
    scorer: Scorer,
    eligible: Eligibility,
    max_copies: int,
    max_iterations: int = 30,
) -> tuple[DeckEntry, ...]:
    """Improve a completed spell section with deterministic one-copy swaps.

    The optimizer evaluates the deck as a whole. It rewards core-plan density and
    pairwise synergy, then accepts only swaps that increase the total deck score.
    """
    knowledge_by_name = {
        card.analysis.name: card
        for card in cards
        if eligible(card, colors)
    }
    entry_by_name = {entry.name: entry for entry in entries}
    analyses = {name: card.analysis for name, card in knowledge_by_name.items()}

    for name, card in knowledge_by_name.items():
        if name in entry_by_name:
            continue
        result = scorer(card.analysis)
        entry_by_name[name] = DeckEntry(
            name=name,
            quantity=0,
            mana_cost=parse_mana_cost(str(card.card.get("mana_cost", ""))),
            mana_value=card.analysis.mana_value,
            type_line=card.analysis.type_line,
            score=result.score,
            reasons=result.reasons,
            roles=tuple(sorted(str(role) for role in card.roles)),
        )

    quantities = Counter({entry.name: entry.quantity for entry in entries})
    current_score = _deck_score(quantities, entry_by_name, analyses, archetype)

    for _ in range(max_iterations):
        best_swap: tuple[str, str, float] | None = None
        for remove_name, remove_qty in tuple(quantities.items()):
            if remove_qty <= 0:
                continue
            for add_name in sorted(entry_by_name):
                if add_name == remove_name or quantities[add_name] >= max_copies:
                    continue
                trial = quantities.copy()
                trial[remove_name] -= 1
                trial[add_name] += 1
                trial_score = _deck_score(trial, entry_by_name, analyses, archetype)
                if trial_score > current_score + 0.01:
                    if best_swap is None or trial_score > best_swap[2]:
                        best_swap = (remove_name, add_name, trial_score)
        if best_swap is None:
            break
        remove_name, add_name, current_score = best_swap
        quantities[remove_name] -= 1
        quantities[add_name] += 1

    optimized: list[DeckEntry] = []
    for name in sorted((name for name, qty in quantities.items() if qty > 0)):
        optimized.append(replace(entry_by_name[name], quantity=quantities[name]))
    return tuple(optimized)
