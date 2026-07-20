from __future__ import annotations

import re
from dataclasses import dataclass

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


@dataclass(frozen=True)
class GeneratedDeck:
    mainboard: tuple[DeckEntry, ...]
    lands: int


def parse_mana_cost(raw_mana_cost: str) -> ManaCost:
    symbols = re.findall(r"\{([^}]+)\}", raw_mana_cost)

    generic = 0
    colored_parts: list[str] = []

    for symbol in symbols:
        normalized = symbol.upper()

        if normalized.isdigit():
            generic += int(normalized)
            continue

        colored_parts.append(normalized)

    return ManaCost(
        raw=raw_mana_cost,
        generic=generic,
        colored=" ".join(colored_parts),
    )


def _is_mono_red(analysis: CardAnalysis) -> bool:
    return set(analysis.color_identity).issubset({"R"})


def _is_reasonable_burn_card(
    knowledge: CardKnowledge,
) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()

    if analysis.is_land:
        return False

    if "burn" not in knowledge.roles:
        return False

    if not _is_mono_red(analysis):
        return False

    if analysis.mana_value > 4:
        return False

    bad_phrases = (
        "deals damage to you",
        "damage to itself",
        "damage to target creature you control",
        "damage to each creature you control",
        "damage equal to its power to itself",
    )

    if any(phrase in text for phrase in bad_phrases):
        return False

    useful_targets = (
        "any target",
        "target creature",
        "target player",
        "target opponent",
        "each opponent",
        "each player",
        "creature or planeswalker",
    )

    return any(
        target in text
        for target in useful_targets
    )


def _collect_candidates(
    knowledge_base: KnowledgeBase,
) -> list[BurnCandidate]:
    candidates: list[BurnCandidate] = []

    for knowledge in knowledge_base.cards:
        if not _is_reasonable_burn_card(knowledge):
            continue

        raw_mana_cost = str(
            knowledge.card.get("mana_cost", "")
        )

        candidates.append(
            BurnCandidate(
                knowledge=knowledge,
                mana_cost=parse_mana_cost(raw_mana_cost),
                scoring=score_burn_card(knowledge.analysis),
            )
        )

    return candidates


def _select_cards_for_curve_slot(
    candidates: list[BurnCandidate],
    minimum_mana_value: float,
    maximum_mana_value: float,
    cards_needed: int,
    max_copies: int,
    used_names: set[str],
) -> list[DeckEntry]:
    slot_candidates = [
        candidate
        for candidate in candidates
        if minimum_mana_value
        < candidate.knowledge.analysis.mana_value
        <= maximum_mana_value
        and candidate.knowledge.analysis.name not in used_names
    ]

    slot_candidates.sort(
        key=lambda candidate: (
            -candidate.scoring.score,
            candidate.knowledge.analysis.mana_value,
            candidate.knowledge.analysis.name,
        )
    )

    entries: list[DeckEntry] = []
    remaining = cards_needed

    for candidate in slot_candidates:
        if remaining <= 0:
            break

        analysis = candidate.knowledge.analysis
        quantity = min(max_copies, remaining)

        entries.append(
            DeckEntry(
                name=analysis.name,
                quantity=quantity,
                mana_cost=candidate.mana_cost,
                mana_value=analysis.mana_value,
                type_line=analysis.type_line,
                score=candidate.scoring.score,
                reasons=candidate.scoring.reasons,
            )
        )

        used_names.add(analysis.name)
        remaining -= quantity

    if remaining > 0:
        raise ValueError(
            "Nicht genügend Burn-Karten für den Kurvenbereich "
            f">{minimum_mana_value} bis {maximum_mana_value} Mana. "
            f"Es fehlen {remaining} Karten."
        )

    return entries


def generate_burn_deck(
    knowledge_base: KnowledgeBase,
    skeleton: DeckSkeleton = BURN_SKELETON,
    max_copies: int = 3,
) -> GeneratedDeck:
    candidates = _collect_candidates(knowledge_base)

    entries: list[DeckEntry] = []
    used_names: set[str] = set()

    previous_maximum = -1.0

    for slot in skeleton.curve:
        slot_entries = _select_cards_for_curve_slot(
            candidates=candidates,
            minimum_mana_value=previous_maximum,
            maximum_mana_value=slot.max_mana_value,
            cards_needed=slot.cards,
            max_copies=max_copies,
            used_names=used_names,
        )

        entries.extend(slot_entries)
        previous_maximum = float(slot.max_mana_value)

    return GeneratedDeck(
        mainboard=tuple(entries),
        lands=skeleton.lands,
    )