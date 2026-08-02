from __future__ import annotations

from dataclasses import replace
from typing import Callable

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import (
    ScoreBreakdown,
    score_artifact_card,
    score_prowess_card,
    score_shrine_card,
)
from thun_deckbuilder.composition_engine import build_composition
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_optimizer import optimize_entries
from thun_deckbuilder.deck_profile import CurveTarget, DeckProfile, RoleTarget
from thun_deckbuilder.deck_quality import with_mana_quality
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.land_count_optimizer import LandCountCandidate, choose_land_count
from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
from thun_deckbuilder.mill_scoring import score_mill_card
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator
from thun_deckbuilder.sideboard_builder import SideboardBuilder

Scorer = Callable[[CardAnalysis], ScoreBreakdown]

ARTIFACT_PROFILE = DeckProfile(
    name="Artifact Synergy",
    lands=22,
    role_targets=(
        RoleTarget("card_draw", minimum=0, target=4),
        RoleTarget("removal", minimum=0, target=4),
    ),
    curve_targets=(
        CurveTarget(1, 10), CurveTarget(2, 14), CurveTarget(3, 9),
        CurveTarget(4, 4), CurveTarget(99, 1),
    ),
)

SHRINE_PROFILE = DeckProfile(
    name="Five-Color Shrines",
    lands=24,
    role_targets=(
        RoleTarget("ramp", minimum=0, target=6),
        RoleTarget("card_draw", minimum=0, target=4),
        RoleTarget("removal", minimum=0, target=3),
    ),
    curve_targets=(
        CurveTarget(2, 8), CurveTarget(3, 11), CurveTarget(4, 9),
        CurveTarget(5, 5), CurveTarget(99, 3),
    ),
)

MILL_PROFILE = DeckProfile(
    name="Dimir Mill",
    lands=24,
    role_targets=(
        RoleTarget("card_draw", minimum=0, target=6),
        RoleTarget("removal", minimum=0, target=7),
    ),
    curve_targets=(
        CurveTarget(1, 6), CurveTarget(2, 12), CurveTarget(3, 10),
        CurveTarget(4, 6), CurveTarget(99, 2),
    ),
)

PROWESS_PROFILE = DeckProfile(
    name="Izzet Prowess V2",
    lands=20,
    role_targets=(
        RoleTarget("aggro_creature", minimum=10, target=14),
        RoleTarget("burn", minimum=8, target=12),
        RoleTarget("card_draw", minimum=6, target=9),
        RoleTarget("removal", minimum=0, target=4),
    ),
    curve_targets=(
        CurveTarget(1, 16), CurveTarget(2, 17), CurveTarget(3, 6),
        CurveTarget(99, 1),
    ),
)


def _score(knowledge: CardKnowledge, scorer: Scorer) -> tuple[float, tuple[str, ...]]:
    result = scorer(knowledge.analysis)
    return result.score, result.reasons or ("Passt zum Archetyp",)


def _within_colors(analysis: CardAnalysis, colors: tuple[str, ...]) -> bool:
    return set(analysis.color_identity).issubset(set(colors))


def _artifact_eligible(knowledge: CardKnowledge, colors: tuple[str, ...]) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()
    if analysis.is_land or not _within_colors(analysis, colors):
        return False
    return analysis.is_artifact or "artifact" in text or score_artifact_card(analysis).score >= 4


def _shrine_eligible(knowledge: CardKnowledge, colors: tuple[str, ...]) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()
    if analysis.is_land or not _within_colors(analysis, colors):
        return False
    is_core = "shrine" in analysis.type_line.lower() or "shrine" in text
    is_fixing = "any color" in text or "any type" in text
    is_compact_support = analysis.mana_value <= 3 and bool(
        knowledge.roles.intersection({"ramp", "card_draw", "removal"})
    )
    return is_core or is_fixing or is_compact_support


def _mill_eligible(knowledge: CardKnowledge, colors: tuple[str, ...]) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()
    if analysis.is_land or not _within_colors(analysis, colors):
        return False
    is_core = "mill" in text or "library into" in text
    is_compact_support = analysis.mana_value <= 3 and bool(
        knowledge.roles.intersection({"card_draw", "removal"})
    )
    return is_core or is_compact_support


def _prowess_eligible(knowledge: CardKnowledge, colors: tuple[str, ...]) -> bool:
    analysis = knowledge.analysis
    text = analysis.oracle_text.lower()
    if analysis.is_land or not _within_colors(analysis, colors) or analysis.mana_value > 3:
        return False
    has_creature_sacrifice_cost = (
        "as an additional cost" in text
        and "sacrifice a creature" in text
    )
    is_sorcery_speed_self_blink = (
        analysis.is_sorcery
        and "exile target creature you control" in text
        and "return it to the battlefield" in text
    )
    if has_creature_sacrifice_cost or is_sorcery_speed_self_blink:
        return False
    is_threat = analysis.is_creature and any(
        phrase in text
        for phrase in (
            "prowess",
            "whenever you cast a noncreature spell",
            "whenever you cast an instant or sorcery spell",
            "whenever you cast your second spell",
        )
    )
    hits_face = any(
        phrase in text
        for phrase in (
            "any target",
            "target player",
            "target opponent",
            "each opponent",
        )
    )
    is_compact_spell = (analysis.is_instant or analysis.is_sorcery) and analysis.mana_value <= 2 and (
        "draw a card" in text
        or ("damage" in text and hits_face)
        or "scry" in text
        or "surveil" in text
        or "counter target" in text
        or "return target" in text
    )
    return is_threat or is_compact_spell or score_prowess_card(analysis).score >= 5


class CalibratedStrategy:
    def __init__(
        self,
        *,
        profile: DeckProfile,
        scorer: Scorer,
        eligibility: Callable[[CardKnowledge, tuple[str, ...]], bool],
        required_colors: frozenset[str] | None = None,
    ) -> None:
        self.profile = profile
        self.scorer = scorer
        self.eligibility = eligibility
        self.required_colors = required_colors

    def _build_candidate(
        self,
        knowledge_base: KnowledgeBase,
        request: DeckRequest,
        lands: int,
    ) -> LandCountCandidate[tuple]:
        profile = replace(self.profile, lands=lands)
        result = build_composition(
            knowledge_base.cards,
            profile=profile,
            deck_size=request.deck_size,
            max_copies=request.max_copies,
            eligible=lambda card: self.eligibility(card, request.colors),
            score_card=lambda card: _score(card, self.scorer),
        )
        optimized_entries = optimize_entries(
            result.entries,
            knowledge_base.cards,
            archetype=request.archetype,
            colors=request.colors,
            scorer=self.scorer,
            eligible=self.eligibility,
            max_copies=request.max_copies,
        )
        provisional = GeneratedDeck(mainboard=optimized_entries, lands=lands)
        report = OpeningHandSimulator().simulate(
            provisional,
            archetype=request.archetype,
        )
        return LandCountCandidate(
            lands=lands,
            payload=(profile, result, optimized_entries),
            report=report,
        )

    def generate(self, knowledge_base: KnowledgeBase, request: DeckRequest) -> GeneratedDeck:
        self._validate_request(request)
        land_options = range(
            max(18, self.profile.lands - 2),
            min(27, self.profile.lands + 2) + 1,
        )
        candidates = tuple(
            self._build_candidate(knowledge_base, request, lands)
            for lands in land_options
        )
        chosen = choose_land_count(candidates, preferred_lands=self.profile.lands)
        profile, result, optimized_entries = chosen.payload

        mana = ManaBaseBuilder().build(
            optimized_entries,
            total_lands=chosen.lands,
            deck_size=request.deck_size,
        )
        deck = GeneratedDeck(
            mainboard=optimized_entries,
            lands=chosen.lands,
            profile_name=profile.name,
            requested_roles=result.requested_roles,
            fulfilled_roles=result.fulfilled_roles,
            warnings=result.warnings,
            selections=result.selections,
            quality_report=with_mana_quality(result.quality_report, mana.quality),
            mana_base=mana.distribution,
            mana_quality=mana.quality,
            opening_hand_report=chosen.report,
        )
        sideboard = SideboardBuilder().build(
            knowledge_base.cards,
            deck,
            archetype=request.archetype,
            colors=request.colors,
            max_copies=request.max_copies,
        )
        return replace(deck, sideboard=sideboard)

    def _validate_request(self, request: DeckRequest) -> None:
        if request.deck_size != 60:
            raise ValueError("Kalibrierte Strategien unterstützen aktuell nur 60 Karten.")
        if self.required_colors is not None and set(request.colors) != self.required_colors:
            colors = "".join(sorted(self.required_colors))
            raise ValueError(f"Diese Strategie benötigt exakt die Farben {colors}.")


class ArtifactStrategy(CalibratedStrategy):
    def __init__(self) -> None:
        super().__init__(profile=ARTIFACT_PROFILE, scorer=score_artifact_card, eligibility=_artifact_eligible)


class ShrineStrategy(CalibratedStrategy):
    def __init__(self) -> None:
        super().__init__(
            profile=SHRINE_PROFILE,
            scorer=score_shrine_card,
            eligibility=_shrine_eligible,
            required_colors=frozenset({"W", "U", "B", "R", "G"}),
        )


class MillStrategy(CalibratedStrategy):
    def __init__(self) -> None:
        super().__init__(
            profile=MILL_PROFILE,
            scorer=score_mill_card,
            eligibility=_mill_eligible,
            required_colors=frozenset({"U", "B"}),
        )


class ProwessStrategy(CalibratedStrategy):
    def __init__(self) -> None:
        super().__init__(
            profile=PROWESS_PROFILE,
            scorer=score_prowess_card,
            eligibility=_prowess_eligible,
            required_colors=frozenset({"U", "R"}),
        )
