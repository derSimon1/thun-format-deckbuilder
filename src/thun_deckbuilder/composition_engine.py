from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from thun_deckbuilder.candidate_eligibility import CandidateEligibility
from thun_deckbuilder.candidate_evaluator import CandidateEvaluator
from thun_deckbuilder.candidate_score import CandidateScore
from thun_deckbuilder.card_contribution import CardContribution, contribution_from_knowledge
from thun_deckbuilder.card_analyzer import simulation_metadata_roles
from thun_deckbuilder.deck_generator import DeckEntry, parse_mana_cost
from thun_deckbuilder.deck_needs import DeckNeedsAnalyzer
from thun_deckbuilder.deck_quality import DeckQualityAnalyzer, DeckQualityReport
from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.selection_trace import SelectionTrace


@dataclass(frozen=True)
class CompositionCandidate:
    knowledge: CardKnowledge
    contribution: CardContribution

    @property
    def name(self) -> str:
        return self.knowledge.analysis.name


@dataclass(frozen=True)
class CompositionResult:
    entries: tuple[DeckEntry, ...]
    requested_roles: tuple[tuple[str, int], ...]
    fulfilled_roles: tuple[tuple[str, int], ...]
    warnings: tuple[str, ...]
    selections: tuple[SelectionTrace, ...] = ()
    quality_report: DeckQualityReport | None = None


ScoreFunction = Callable[[CardKnowledge], tuple[float, tuple[str, ...]]]
EligibilityFunction = Callable[[CardKnowledge], bool]


def _entry(
    candidate: CompositionCandidate,
    quantity: int,
    score: CandidateScore,
) -> DeckEntry:
    analysis = candidate.knowledge.analysis
    mana_cost = parse_mana_cost(str(candidate.knowledge.card.get("mana_cost", "")))
    return DeckEntry(
        name=analysis.name,
        quantity=quantity,
        mana_cost=mana_cost,
        mana_value=analysis.mana_value,
        type_line=analysis.type_line,
        score=score.total,
        reasons=tuple(component.reason for component in score.components),
        roles=tuple(
            sorted(
                {
                    *(str(role) for role in candidate.knowledge.roles),
                    *simulation_metadata_roles(analysis),
                }
            )
        ),
    )


def _primary_need(needs) -> str | None:
    active = [need for need in needs.role_needs if need.missing_target > 0]
    if not active:
        return None
    return max(active, key=lambda need: (need.urgency, need.missing_minimum, need.missing_target)).key


def build_composition(
    cards: Iterable[CardKnowledge],
    *,
    profile: DeckProfile,
    deck_size: int,
    max_copies: int,
    eligible: EligibilityFunction,
    score_card: ScoreFunction,
) -> CompositionResult:
    """Build the spell section iteratively from current deck needs.

    Every selected copy updates ``DeckState``. The same candidate can therefore
    receive a different score later as role and curve targets become filled.
    """

    spell_slots = profile.spell_slots(deck_size)
    candidates = tuple(
        CompositionCandidate(card, contribution_from_knowledge(card))
        for card in cards
    )
    state = DeckState()
    needs_analyzer = DeckNeedsAnalyzer()
    eligibility = CandidateEligibility()
    evaluator = CandidateEvaluator()
    traces: list[SelectionTrace] = []
    latest_scores: dict[str, CandidateScore] = {}
    candidate_by_name = {candidate.name: candidate for candidate in candidates}

    while state.spell_count < spell_slots:
        needs = needs_analyzer.analyze(state, profile, deck_size=deck_size)
        scored: list[tuple[CompositionCandidate, CandidateScore]] = []

        unmet_required = needs.unmet_required_needs()
        missing_required = sum(int(need.missing_minimum + 0.999999) for need in unmet_required)
        reserve_required_slots = missing_required >= needs.remaining_spell_slots

        for candidate in candidates:
            check = eligibility.check(
                candidate.knowledge,
                candidate.contribution,
                state,
                deck_size=spell_slots,
                max_copies=max_copies,
                strategy_eligible=eligible,
            )
            if not check.eligible:
                continue
            if reserve_required_slots and not any(
                candidate.contribution.strength_for(need.key) > 0
                for need in unmet_required
            ):
                continue
            score = evaluator.evaluate(
                candidate.knowledge,
                candidate.contribution,
                state,
                needs,
                profile,
                score_card=score_card,
            )
            scored.append((candidate, score))

        if not scored:
            raise ValueError(
                f"Not enough eligible cards; {spell_slots - state.spell_count} spell slots remain."
            )

        candidate, score = max(
            scored,
            key=lambda item: (
                item[1].total,
                -item[0].knowledge.analysis.mana_value,
                item[0].name,
            ),
        )
        state = state.with_card(
            candidate.contribution,
            1,
            deck_size=spell_slots,
            max_copies=max_copies,
        )
        latest_scores[candidate.name] = score
        traces.append(
            SelectionTrace(
                step=len(traces) + 1,
                card_name=candidate.name,
                quantity_after_selection=state.quantity_of(candidate.name),
                score=score,
                primary_need=_primary_need(needs),
            )
        )

    final_needs = needs_analyzer.analyze(state, profile, deck_size=deck_size)
    unmet = final_needs.unmet_required_needs()
    if unmet:
        details = ", ".join(
            f"{need.key}: {need.current:g}/{need.minimum}" for need in unmet
        )
        raise ValueError(f"Mandatory role minimums were not met: {details}.")

    warnings = tuple(
        f"Role '{need.key}' reached {need.current:g}/{need.target}; target not fully met."
        for need in final_needs.role_needs
        if need.missing_target > 0
    )
    entries = tuple(
        _entry(
            candidate_by_name[entry.card_name],
            entry.quantity,
            latest_scores[entry.card_name],
        )
        for entry in state.entries
    )
    fulfilled = tuple(
        (target.role, int(state.role_count(target.role)))
        for target in profile.role_targets
    )
    quality_report = DeckQualityAnalyzer().analyze(state, profile)
    return CompositionResult(
        entries=entries,
        requested_roles=tuple((target.role, target.target) for target in profile.role_targets),
        fulfilled_roles=fulfilled,
        warnings=warnings,
        selections=tuple(traces),
        quality_report=quality_report,
    )


class CompositionEngine:
    """Object-oriented facade for iterative deck composition."""

    def build(
        self,
        cards: Iterable[CardKnowledge],
        *,
        profile: DeckProfile,
        deck_size: int,
        max_copies: int,
        eligible: EligibilityFunction,
        score_card: ScoreFunction,
    ) -> CompositionResult:
        return build_composition(
            cards,
            profile=profile,
            deck_size=deck_size,
            max_copies=max_copies,
            eligible=eligible,
            score_card=score_card,
        )
