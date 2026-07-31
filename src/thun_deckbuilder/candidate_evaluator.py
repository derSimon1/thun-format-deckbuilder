from __future__ import annotations

from typing import Callable

from thun_deckbuilder.candidate_score import CandidateScore, ScoreComponent
from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.card_evaluation import CardEvaluationEngine
from thun_deckbuilder.curve_scorer import CurveScorer
from thun_deckbuilder.deck_needs import DeckNeeds
from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.role_need_scorer import RoleNeedScorer
from thun_deckbuilder.synergy_engine import SynergyEngine
from thun_deckbuilder.archetype_intelligence import ArchetypeEvaluator


ScoreFunction = Callable[[CardKnowledge], tuple[float, tuple[str, ...]]]


class CandidateEvaluator:
    """Combine static card quality with dynamic deck-state needs."""

    def __init__(
        self,
        role_scorer: RoleNeedScorer | None = None,
        curve_scorer: CurveScorer | None = None,
        synergy_engine: SynergyEngine | None = None,
        card_evaluation_engine: CardEvaluationEngine | None = None,
        archetype_evaluator: ArchetypeEvaluator | None = None,
    ) -> None:
        self.role_scorer = role_scorer or RoleNeedScorer()
        self.curve_scorer = curve_scorer or CurveScorer()
        self.synergy_engine = synergy_engine or SynergyEngine()
        self.card_evaluation_engine = card_evaluation_engine or CardEvaluationEngine()
        self.archetype_evaluator = archetype_evaluator or ArchetypeEvaluator()

    def evaluate(
        self,
        knowledge: CardKnowledge,
        contribution: CardContribution,
        state: DeckState,
        needs: DeckNeeds,
        profile: DeckProfile,
        *,
        score_card: ScoreFunction,
    ) -> CandidateScore:
        base_score, reasons = score_card(knowledge)
        components: list[ScoreComponent] = [
            ScoreComponent(
                category="base_quality",
                value=base_score,
                reason="; ".join(reasons) if reasons else "Base strategy quality.",
            )
        ]
        intrinsic = self.card_evaluation_engine.evaluate(knowledge.analysis)
        components.extend(
            ScoreComponent(
                category="intrinsic_quality",
                value=component.value,
                reason=component.reason,
            )
            for component in intrinsic.components
        )
        components.extend(self.role_scorer.score(contribution, needs))
        curve_component = self.curve_scorer.score(contribution, needs, profile)
        if curve_component is not None:
            components.append(curve_component)
        components.extend(self.synergy_engine.score(contribution, state))
        components.extend(self.archetype_evaluator.score(knowledge, contribution, profile))
        return CandidateScore(card_name=contribution.card_name, components=tuple(components))
