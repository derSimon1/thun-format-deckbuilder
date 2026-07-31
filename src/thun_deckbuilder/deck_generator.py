from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from thun_deckbuilder.deck_quality import DeckQualityReport
    from thun_deckbuilder.selection_trace import SelectionTrace
    from thun_deckbuilder.mana_distribution import ManaDistribution
    from thun_deckbuilder.mana_quality import ManaQualityReport
    from thun_deckbuilder.opening_hand_simulator import OpeningHandReport

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown, score_burn_card
from thun_deckbuilder.deck_skeleton import BURN_SKELETON, DeckSkeleton
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase


@dataclass(frozen=True)
class ManaCost:
    raw: str
    generic: int
    colored: str


@dataclass(frozen=True)
class BurnCandidate:
    knowledge: CardKnowledge
    mana_cost: ManaCost
    scoring: ScoreBreakdown


@dataclass(frozen=True)
class DeckEntry:
    name: str
    quantity: int
    mana_cost: ManaCost
    mana_value: float
    type_line: str
    score: float = 0.0
    reasons: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()


@dataclass(frozen=True)
class GeneratedDeck:
    mainboard: tuple[DeckEntry, ...]
    lands: int
    profile_name: str = ""
    requested_roles: tuple[tuple[str, int], ...] = ()
    fulfilled_roles: tuple[tuple[str, int], ...] = ()
    warnings: tuple[str, ...] = ()
    selections: tuple["SelectionTrace", ...] = ()
    quality_report: "DeckQualityReport | None" = None
    mana_base: "ManaDistribution | None" = None
    mana_quality: "ManaQualityReport | None" = None
    sideboard: tuple[DeckEntry, ...] = ()
    benchmark_report: object | None = None
    opening_hand_report: "OpeningHandReport | None" = None


def parse_mana_cost(raw_mana_cost: str) -> ManaCost:
    symbols = re.findall(r"\{([^}]+)\}", raw_mana_cost)
    generic = 0
    colored_parts: list[str] = []
    for symbol in symbols:
        normalized = symbol.upper()
        if normalized.isdigit():
            generic += int(normalized)
        else:
            colored_parts.append(normalized)
    return ManaCost(
        raw=raw_mana_cost,
        generic=generic,
        colored=" ".join(colored_parts),
    )


def _is_mono_red(analysis: CardAnalysis) -> bool:
    return set(analysis.color_identity).issubset({"R"})


def _is_reasonable_burn_card(knowledge: CardKnowledge) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()
    if (
        analysis.is_land
        or not _is_mono_red(analysis)
        or analysis.mana_value > 4
    ):
        return False

    return (
        "damage" in text
        or "haste" in text
        or "prowess" in text
        or "exile the top card" in text
        or "can't gain life" in text
        or "cannot gain life" in text
    )


def _candidate(knowledge: CardKnowledge) -> BurnCandidate:
    return BurnCandidate(
        knowledge=knowledge,
        mana_cost=parse_mana_cost(str(knowledge.card.get("mana_cost", ""))),
        scoring=score_burn_card(knowledge.analysis),
    )


def _copy_count(candidate: BurnCandidate, remaining: int, max_copies: int) -> int:
    score = candidate.scoring.score
    if score >= 7:
        preferred = max_copies
    elif score >= 4:
        preferred = min(2, max_copies)
    else:
        preferred = 1
    return min(preferred, remaining)


def generate_burn_deck(
    knowledge_base: KnowledgeBase,
    *,
    deck_size: int = 60,
    lands: int = 20,
    max_copies: int = 3,
    skeleton: DeckSkeleton = BURN_SKELETON,
) -> GeneratedDeck:
    spell_slots = deck_size - lands
    candidates = sorted(
        (
            _candidate(knowledge)
            for knowledge in knowledge_base.cards
            if _is_reasonable_burn_card(knowledge)
        ),
        key=lambda candidate: (
            -candidate.scoring.score,
            candidate.knowledge.analysis.mana_value,
            candidate.knowledge.analysis.name,
        ),
    )

    entries: list[DeckEntry] = []
    remaining = spell_slots
    for candidate in candidates:
        if remaining <= 0:
            break
        quantity = _copy_count(candidate, remaining, max_copies)
        analysis = candidate.knowledge.analysis
        entries.append(
            DeckEntry(
                name=analysis.name,
                quantity=quantity,
                mana_cost=candidate.mana_cost,
                mana_value=analysis.mana_value,
                type_line=analysis.type_line,
                score=candidate.scoring.score,
                reasons=candidate.scoring.reasons,
                roles=tuple(sorted(str(role) for role in candidate.knowledge.roles)),
            )
        )
        remaining -= quantity

    if remaining > 0:
        raise ValueError(f"Not enough eligible Burn cards; {remaining} spell slots remain.")

    return GeneratedDeck(
        mainboard=tuple(entries),
        lands=lands,
        profile_name=skeleton.name,
    )
