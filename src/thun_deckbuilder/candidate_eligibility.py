from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.knowledge_base import CardKnowledge


EligibilityFunction = Callable[[CardKnowledge], bool]


@dataclass(frozen=True)
class EligibilityResult:
    eligible: bool
    reason: str | None = None


class CandidateEligibility:
    """Apply hard constraints before a card is scored.

    Strategy-specific eligibility remains injectable. Generic construction
    constraints live here so every archetype handles them consistently.
    """

    def check(
        self,
        knowledge: CardKnowledge,
        contribution: CardContribution,
        state: DeckState,
        *,
        deck_size: int,
        max_copies: int,
        strategy_eligible: EligibilityFunction,
    ) -> EligibilityResult:
        if contribution.is_land:
            return EligibilityResult(False, "Lands are added after spell composition.")
        if state.total_cards >= deck_size:
            return EligibilityResult(False, "The deck is already full.")
        if state.quantity_of(contribution.card_name) >= max_copies:
            return EligibilityResult(False, "The copy limit has been reached.")
        if not strategy_eligible(knowledge):
            return EligibilityResult(False, "The card does not satisfy the strategy constraints.")
        return EligibilityResult(True)
