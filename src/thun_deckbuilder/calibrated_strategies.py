from __future__ import annotations

from dataclasses import replace
from typing import Callable

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import (
    ScoreBreakdown,
    score_artifact_card,
    score_shrine_card,
)
from thun_deckbuilder.mill_scoring import score_mill_card
from thun_deckbuilder.composition_engine import build_composition
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_profile import CurveTarget, DeckProfile, RoleTarget
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
from thun_deckbuilder.deck_quality import with_mana_quality
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

    def generate(self, knowledge_base: KnowledgeBase, request: DeckRequest) -> GeneratedDeck:
        self._validate_request(request)
        result = build_composition(
            knowledge_base.cards,
            profile=self.profile,
            deck_size=request.deck_size,
            max_copies=request.max_copies,
            eligible=lambda card: self.eligibility(card, request.colors),
            score_card=lambda card: _score(card, self.scorer),
        )
        mana = ManaBaseBuilder().build(
            result.entries,
            total_lands=self.profile.lands,
            deck_size=request.deck_size,
        )
        deck = GeneratedDeck(
            mainboard=result.entries,
            lands=self.profile.lands,
            profile_name=self.profile.name,
            requested_roles=result.requested_roles,
            fulfilled_roles=result.fulfilled_roles,
            warnings=result.warnings,
            selections=result.selections,
            quality_report=with_mana_quality(result.quality_report, mana.quality),
            mana_base=mana.distribution,
            mana_quality=mana.quality,
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
        super().__init__(
            profile=ARTIFACT_PROFILE,
            scorer=score_artifact_card,
            eligibility=_artifact_eligible,
        )


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
