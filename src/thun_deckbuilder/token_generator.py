from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.card_scoring import ScoreBreakdown
from thun_deckbuilder.deck_generator import (
    DeckEntry,
    GeneratedDeck,
    ManaCost,
    parse_mana_cost,
)
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.token_scoring import score_token_card


@dataclass(frozen=True)
class TokenCandidate:
    knowledge: CardKnowledge
    mana_cost: ManaCost
    scoring: ScoreBreakdown


def _is_mono_white(
    knowledge: CardKnowledge,
) -> bool:
    color_identity = set(
        knowledge.analysis.color_identity
    )

    return color_identity.issubset({"W"})


def _is_reasonable_token_card(
    knowledge: CardKnowledge,
) -> bool:
    analysis = knowledge.analysis

    if analysis.is_land:
        return False

    if "token_maker" not in knowledge.roles:
        return False

    if not _is_mono_white(knowledge):
        return False

    if analysis.mana_value > 5:
        return False

    text = analysis.oracle_text.lower()

    excluded_phrases = (
        "token that's a copy of target opponent's",
        "token that's a copy of target creature you don't control",
        "create a token that's a copy of target artifact you don't control",
    )

    return not any(
        phrase in text
        for phrase in excluded_phrases
    )


def _collect_candidates(
    knowledge_base: KnowledgeBase,
) -> list[TokenCandidate]:
    candidates: list[TokenCandidate] = []

    for knowledge in knowledge_base.cards:
        if not _is_reasonable_token_card(knowledge):
            continue

        raw_mana_cost = str(
            knowledge.card.get("mana_cost", "")
        )

        candidates.append(
            TokenCandidate(
                knowledge=knowledge,
                mana_cost=parse_mana_cost(raw_mana_cost),
                scoring=score_token_card(
                    knowledge.analysis
                ),
            )
        )

    candidates.sort(
        key=lambda candidate: (
            -candidate.scoring.score,
            candidate.knowledge.analysis.mana_value,
            candidate.knowledge.analysis.name,
        )
    )

    return candidates


def generate_token_deck(
    knowledge_base: KnowledgeBase,
    deck_size: int = 60,
    lands: int = 24,
    max_copies: int = 3,
) -> GeneratedDeck:
    spell_slots = deck_size - lands

    if spell_slots <= 0:
        raise ValueError(
            "Die Deckgröße muss größer als die Länderzahl sein."
        )

    candidates = _collect_candidates(knowledge_base)

    entries: list[DeckEntry] = []
    remaining = spell_slots

    for candidate in candidates:
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

        remaining -= quantity

    if remaining > 0:
        raise ValueError(
            "Nicht genügend passende Mono-White-Tokenkarten "
            f"gefunden. Es fehlen {remaining} Karten."
        )

    return GeneratedDeck(
        mainboard=tuple(entries),
        lands=lands,
    )