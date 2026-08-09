from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from thun_deckbuilder.composition_engine import build_composition
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_profile import CurveTarget, DeckProfile, RoleTarget
from thun_deckbuilder.deck_quality import with_mana_quality
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
from thun_deckbuilder.meta_analyzer import LearnedArchetypeProfile


@dataclass(frozen=True)
class LearnedStrategyConfig:
    name: str
    profile: LearnedArchetypeProfile
    replacement_names: tuple[str, ...] = ()


def profile_from_learning(
    learned: LearnedArchetypeProfile,
    *,
    name: str,
    deck_size: int = 60,
) -> DeckProfile:
    lands = min(deck_size - 1, max(16, round(learned.average_lands)))
    spell_slots = deck_size - lands

    roles: list[RoleTarget] = []
    for role, average in sorted(learned.role_targets, key=lambda item: -item[1]):
        target = min(spell_slots, max(1, round(average)))
        minimum = min(target, max(0, round(average * 0.6)))
        roles.append(RoleTarget(role, minimum=minimum, target=target))

    curve: list[CurveTarget] = []
    assigned = 0
    for band, average in sorted(learned.curve):
        target = max(0, round(average))
        assigned += target
        curve.append(CurveTarget(99 if band >= 5 else band, target))
    if assigned < spell_slots:
        curve.append(CurveTarget(99, spell_slots - assigned))

    return DeckProfile(
        name=name,
        lands=lands,
        role_targets=tuple(roles),
        curve_targets=tuple(curve),
    )


def _adapt_profile_to_legal_pool(
    profile: DeckProfile,
    cards: Iterable[CardKnowledge],
    *,
    allowed_colors: set[str],
    max_copies: int,
) -> DeckProfile:
    eligible_cards = tuple(
        card
        for card in cards
        if not card.analysis.is_land
        and set(card.analysis.color_identity).issubset(allowed_colors)
    )
    adjusted_roles: list[RoleTarget] = []
    for role_target in profile.role_targets:
        capacity = sum(
            max_copies
            for card in eligible_cards
            if role_target.role in card.roles
        )
        minimum = min(role_target.minimum, capacity)
        target = max(minimum, min(role_target.target, capacity))
        adjusted_roles.append(
            RoleTarget(role_target.role, minimum=minimum, target=target)
        )
    return replace(profile, role_targets=tuple(adjusted_roles))


class LearnedArchetypeStrategy:
    """Build a legal deck from a profile learned from external decklists."""

    def __init__(self, config: LearnedStrategyConfig) -> None:
        self.config = config
        self.deck_profile = profile_from_learning(config.profile, name=config.name)

    def generate(
        self,
        knowledge_base: KnowledgeBase,
        *,
        deck_size: int = 60,
        max_copies: int = 3,
    ) -> GeneratedDeck:
        allowed_colors = set(self.config.profile.colors)
        core = {item.name.casefold() for item in self.config.profile.core_cards}
        replacements = {name.casefold() for name in self.config.replacement_names}
        role_weights = dict(self.config.profile.role_targets)
        profile = _adapt_profile_to_legal_pool(
            self.deck_profile,
            knowledge_base.cards,
            allowed_colors=allowed_colors,
            max_copies=max_copies,
        )

        def eligible(card: CardKnowledge) -> bool:
            return (
                not card.analysis.is_land
                and set(card.analysis.color_identity).issubset(allowed_colors)
            )

        def score(card: CardKnowledge) -> tuple[float, tuple[str, ...]]:
            value = 0.0
            reasons: list[str] = []
            for role in card.roles:
                weight = float(role_weights.get(str(role), 0.0))
                if weight:
                    value += 1.0 + min(4.0, weight / 3.0)
                    reasons.append(f"gelernte Rolle {role}")
            name = card.analysis.name.casefold()
            if name in core:
                value += 8.0
                reasons.append("gelernte Kernkarte")
            if name in replacements:
                value += 5.0
                reasons.append("Thun-Ersatz für Kernkarte")
            value += max(0.0, 3.0 - card.analysis.mana_value * 0.35)
            return value, tuple(reasons or ("passt zum gelernten Profil",))

        result = build_composition(
            knowledge_base.cards,
            profile=profile,
            deck_size=deck_size,
            max_copies=max_copies,
            eligible=eligible,
            score_card=score,
        )
        mana = ManaBaseBuilder().build(
            result.entries,
            total_lands=profile.lands,
            deck_size=deck_size,
        )
        return GeneratedDeck(
            mainboard=result.entries,
            lands=profile.lands,
            profile_name=profile.name,
            requested_roles=result.requested_roles,
            fulfilled_roles=result.fulfilled_roles,
            warnings=result.warnings,
            selections=result.selections,
            quality_report=with_mana_quality(result.quality_report, mana.quality),
            mana_base=mana.distribution,
            mana_quality=mana.quality,
        )
