from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from thun_deckbuilder.deck_quality import DeckQualityReport
    from thun_deckbuilder.selection_trace import SelectionTrace
    from thun_deckbuilder.mana_distribution import ManaDistribution
    from thun_deckbuilder.mana_quality import ManaQualityReport

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.burn_scoring import score_burn_card
from thun_deckbuilder.card_scoring import ScoreBreakdown
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
    return ManaCost(raw=raw_mana_cost, generic=generic, colored=" ".join(colored_parts))


def _is_mono_red(analysis: CardAnalysis) -> bool:
    return set(analysis.color_identity).issubset({"R"})


def _can_damage_opponent(text: str) -> bool:
    return any(
        phrase in text
        for phrase in (
            "any target",
            "target player",
            "target opponent",
            "each opponent",
            "each player",
        )
    )


def _is_reasonable_burn_card(knowledge: CardKnowledge) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()
    if analysis.is_land or not _is_mono_red(analysis) or analysis.mana_value > 4:
        return False
    if not knowledge.roles.intersection({"burn", "aggro_creature", "card_draw"}):
        return False
    bad_phrases = (
        "damage to itself",
        "damage to target creature you control",
        "damage to each creature you control",
        "damage equal to its power to itself",
        "destroy all creatures",
        "exile all creatures",
    )
    if any(phrase in text for phrase in bad_phrases):
        return False

    # Burn cards must either advance the opponent's life-total clock, provide a
    # credible early attacker, or replace themselves. Creature-only removal is
    # useful sideboard material but should not crowd the proactive main deck.
    reaches_opponent = _can_damage_opponent(text)
    aggressive_creature = (
        analysis.is_creature
        and analysis.mana_value <= 2
        and (analysis.power or 0) >= 2
    )
    card_flow = "card_draw" in knowledge.roles
    return reaches_opponent or aggressive_creature or card_flow


def _score_for_composition(knowledge: CardKnowledge) -> tuple[float, tuple[str, ...]]:
    scored = score_burn_card(knowledge.analysis)
    score = scored.score
    reasons = list(scored.reasons)
    role_bonuses = {
        "burn": (2.5, "Direkter Burn-Beitrag"),
        "aggro_creature": (2.0, "Frühe aggressive Kreatur"),
        "card_draw": (1.5, "Kartennachschub"),
    }
    for role, (bonus, reason) in role_bonuses.items():
        if role in knowledge.roles:
            score += bonus
            if reason not in reasons:
                reasons.append(reason)
    return score, tuple(reasons or ["Passt zum Burn-Profil"])


def generate_burn_deck(
    knowledge_base: KnowledgeBase,
    skeleton: DeckSkeleton = BURN_SKELETON,
    max_copies: int = 3,
) -> GeneratedDeck:
    # ``skeleton`` remains in the public API for compatibility. The profile is
    # now the source of truth for composition; custom legacy skeletons retain
    # their land count through a derived profile.
    from thun_deckbuilder.composition_engine import build_composition
    from thun_deckbuilder.deck_profile import BURN_PROFILE, DeckProfile

    profile = BURN_PROFILE
    if skeleton.lands != BURN_PROFILE.lands:
        profile = DeckProfile(
            name=BURN_PROFILE.name,
            lands=skeleton.lands,
            role_targets=BURN_PROFILE.role_targets,
            curve_targets=BURN_PROFILE.curve_targets,
        )
    deck_size = profile.lands + sum(slot.cards for slot in skeleton.curve)
    result = build_composition(
        knowledge_base.cards,
        profile=profile,
        deck_size=deck_size,
        max_copies=max_copies,
        eligible=_is_reasonable_burn_card,
        score_card=_score_for_composition,
    )
    from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
    from thun_deckbuilder.deck_quality import with_mana_quality

    mana = ManaBaseBuilder().build(
        result.entries, total_lands=profile.lands, deck_size=deck_size
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
