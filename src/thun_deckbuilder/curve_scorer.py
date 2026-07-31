from __future__ import annotations

from thun_deckbuilder.candidate_score import ScoreComponent
from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_needs import DeckNeeds
from thun_deckbuilder.deck_profile import DeckProfile


class CurveScorer:
    """Reward candidates in a mana-value band that is still below target."""

    def score(
        self,
        contribution: CardContribution,
        needs: DeckNeeds,
        profile: DeckProfile,
    ) -> ScoreComponent | None:
        previous_maximum = -1.0
        for index, target in enumerate(profile.curve_targets):
            if previous_maximum < contribution.mana_value <= target.maximum_mana_value:
                need = needs.curve_needs[index]
                if need.missing_target <= 0:
                    return ScoreComponent(
                        category="curve",
                        value=-2.0,
                        reason=f"Mana-value band up to {target.maximum_mana_value:g} is already filled.",
                    )
                return ScoreComponent(
                    category="curve",
                    value=3.0 + 7.0 * need.urgency,
                    reason=(
                        f"Fits under-filled mana-value band up to "
                        f"{target.maximum_mana_value:g} ({need.current:g}/{need.target})."
                    ),
                )
            previous_maximum = target.maximum_mana_value
        return None
