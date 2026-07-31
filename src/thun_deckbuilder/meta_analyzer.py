from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from statistics import mean
from typing import Iterable

from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.moxfield_import import ImportedDeck


@dataclass(frozen=True)
class LearnedCoreCard:
    name: str
    inclusion_rate: float
    average_copies: float


@dataclass(frozen=True)
class LearnedArchetypeProfile:
    deck_count: int
    colors: tuple[str, ...]
    average_lands: float
    average_mana_value: float
    curve: tuple[tuple[int, float], ...]
    role_targets: tuple[tuple[str, float], ...]
    core_cards: tuple[LearnedCoreCard, ...]
    unresolved_cards: tuple[str, ...]


def _curve_band(mana_value: float) -> int:
    if mana_value >= 5:
        return 5
    return max(0, int(mana_value))


def learn_archetype_profile(
    decks: Iterable[ImportedDeck],
    knowledge_base: KnowledgeBase,
    *,
    core_threshold: float = 0.60,
) -> LearnedArchetypeProfile:
    """Derive a reusable archetype profile from multiple deck exports.

    Card legality is intentionally not applied here. This stage learns the source
    archetype; Thun-format translation can later replace unavailable cards while
    preserving the learned curve, role mix, and core concepts.
    """
    samples = tuple(decks)
    if not samples:
        raise ValueError("At least one imported deck is required.")
    if not 0 < core_threshold <= 1:
        raise ValueError("core_threshold must be between 0 and 1.")

    by_name: dict[str, CardKnowledge] = {
        card.analysis.name.casefold(): card for card in knowledge_base.cards
    }
    inclusion: Counter[str] = Counter()
    copies: Counter[str] = Counter()
    unresolved: set[str] = set()
    deck_land_counts: list[int] = []
    deck_average_mvs: list[float] = []
    deck_curves: list[Counter[int]] = []
    deck_roles: list[Counter[str]] = []
    colors: set[str] = set()

    for deck in samples:
        seen: set[str] = set()
        land_count = 0
        nonland_mvs: list[float] = []
        curve: Counter[int] = Counter()
        roles: Counter[str] = Counter()

        for imported in deck.mainboard:
            knowledge = by_name.get(imported.name.casefold())
            if knowledge is None:
                unresolved.add(imported.name)
                continue
            analysis = knowledge.analysis
            canonical_name = analysis.name
            copies[canonical_name] += imported.quantity
            seen.add(canonical_name)
            colors.update(analysis.color_identity)

            if analysis.is_land:
                land_count += imported.quantity
                continue
            nonland_mvs.extend([analysis.mana_value] * imported.quantity)
            curve[_curve_band(analysis.mana_value)] += imported.quantity
            for role in knowledge.roles:
                roles[str(role)] += imported.quantity

        for name in seen:
            inclusion[name] += 1
        deck_land_counts.append(land_count)
        deck_average_mvs.append(mean(nonland_mvs) if nonland_mvs else 0.0)
        deck_curves.append(curve)
        deck_roles.append(roles)

    deck_count = len(samples)
    core_cards = tuple(
        sorted(
            (
                LearnedCoreCard(
                    name=name,
                    inclusion_rate=round(inclusion[name] / deck_count, 3),
                    average_copies=round(copies[name] / inclusion[name], 2),
                )
                for name in inclusion
                if inclusion[name] / deck_count >= core_threshold
            ),
            key=lambda item: (-item.inclusion_rate, -item.average_copies, item.name),
        )
    )

    curve_keys = sorted({key for curve in deck_curves for key in curve})
    learned_curve = tuple(
        (key, round(mean(curve[key] for curve in deck_curves), 2))
        for key in curve_keys
    )
    role_keys = sorted({key for roles in deck_roles for key in roles})
    learned_roles = tuple(
        (key, round(mean(roles[key] for roles in deck_roles), 2))
        for key in role_keys
    )

    return LearnedArchetypeProfile(
        deck_count=deck_count,
        colors=tuple(sorted(colors)),
        average_lands=round(mean(deck_land_counts), 2),
        average_mana_value=round(mean(deck_average_mvs), 2),
        curve=learned_curve,
        role_targets=learned_roles,
        core_cards=core_cards,
        unresolved_cards=tuple(sorted(unresolved)),
    )
