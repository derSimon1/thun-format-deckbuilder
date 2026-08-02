from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase


_GENERIC_ROLES = frozenset({"aggro_creature"})


@dataclass(frozen=True)
class ReplacementCandidate:
    source_name: str
    replacement_name: str
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class TranslationResult:
    source_name: str
    candidates: tuple[ReplacementCandidate, ...]


def _type_families(type_line: str) -> frozenset[str]:
    normalized = type_line.lower()
    families = {
        family
        for family in (
            "creature", "instant", "sorcery", "artifact", "enchantment",
            "planeswalker", "land",
        )
        if family in normalized
    }
    return frozenset(families)


def _rank_candidate(
    source: CardKnowledge,
    candidate: CardKnowledge,
    *,
    colors: frozenset[str],
) -> ReplacementCandidate | None:
    analysis = candidate.analysis
    if analysis.is_land != source.analysis.is_land:
        return None
    if not set(analysis.color_identity).issubset(colors):
        return None

    shared_roles = source.roles.intersection(candidate.roles)
    shared_synergies = source.synergies.intersection(candidate.synergies)
    meaningful_roles = {
        str(role)
        for role in shared_roles
        if str(role) not in _GENERIC_ROLES
    }

    # Card type, mana value and color are similarity signals, not proof that two
    # cards serve the same strategic purpose. Require at least one meaningful
    # shared role or synergy before ranking a replacement.
    if not meaningful_roles and not shared_synergies:
        return None

    score = 0.0
    reasons: list[str] = []

    if shared_roles:
        score += 5.0 * len(shared_roles)
        reasons.append("gleiche Rolle: " + ", ".join(sorted(str(role) for role in shared_roles)))

    if shared_synergies:
        score += 3.0 * len(shared_synergies)
        reasons.append("gleiche Synergie: " + ", ".join(sorted(str(item) for item in shared_synergies)))

    source_types = _type_families(source.analysis.type_line)
    candidate_types = _type_families(analysis.type_line)
    shared_types = source_types.intersection(candidate_types)
    if shared_types:
        score += 3.0
        reasons.append("gleicher Kartentyp")
    elif source_types and candidate_types:
        score -= 2.0

    mana_gap = abs(source.analysis.mana_value - analysis.mana_value)
    score += max(0.0, 4.0 - mana_gap * 1.5)
    if mana_gap <= 1:
        reasons.append("ähnlicher Manawert")

    source_colors = set(source.analysis.color_identity)
    candidate_colors = set(analysis.color_identity)
    if candidate_colors == source_colors:
        score += 2.0
        reasons.append("gleiche Farbidentität")
    elif candidate_colors.issubset(source_colors):
        score += 0.75

    return ReplacementCandidate(
        source_name=source.analysis.name,
        replacement_name=analysis.name,
        score=round(score, 2),
        reasons=tuple(reasons),
    )


def suggest_replacements(
    source: CardKnowledge,
    legal_pool: KnowledgeBase | Iterable[CardKnowledge],
    *,
    colors: Iterable[str],
    limit: int = 5,
) -> TranslationResult:
    """Rank legal Thun-format replacements for one unavailable source card.

    Ranking preserves function before raw power: roles and synergy signals carry
    more weight than type, mana value, and exact color identity.
    """
    if limit <= 0:
        raise ValueError("limit must be positive.")
    cards = legal_pool.cards if isinstance(legal_pool, KnowledgeBase) else tuple(legal_pool)
    allowed_colors = frozenset(color.upper() for color in colors)
    ranked = [
        candidate
        for card in cards
        if card.analysis.name.casefold() != source.analysis.name.casefold()
        for candidate in [_rank_candidate(source, card, colors=allowed_colors)]
        if candidate is not None
    ]
    ranked.sort(key=lambda item: (-item.score, item.replacement_name))
    return TranslationResult(source.analysis.name, tuple(ranked[:limit]))


def translate_core_cards(
    source_cards: Iterable[CardKnowledge],
    legal_pool: KnowledgeBase | Iterable[CardKnowledge],
    *,
    colors: Iterable[str],
    limit_per_card: int = 3,
) -> tuple[TranslationResult, ...]:
    return tuple(
        suggest_replacements(
            source,
            legal_pool,
            colors=colors,
            limit=limit_per_card,
        )
        for source in source_cards
    )
