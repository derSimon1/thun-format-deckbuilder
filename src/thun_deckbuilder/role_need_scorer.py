from __future__ import annotations

from thun_deckbuilder.candidate_score import ScoreComponent
from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_needs import DeckNeeds


class RoleNeedScorer:
    """Reward cards that fill currently under-served deck roles."""

    def score(
        self,
        contribution: CardContribution,
        needs: DeckNeeds,
    ) -> tuple[ScoreComponent, ...]:
        components: list[ScoreComponent] = []
        for need in needs.role_needs:
            strength = contribution.strength_for(need.key)
            if strength <= 0 or need.missing_target <= 0:
                continue

            minimum_bonus = 14.0 if need.missing_minimum > 0 else 0.0
            urgency_bonus = 18.0 * need.urgency
            value = strength * (4.0 + minimum_bonus + urgency_bonus)
            components.append(
                ScoreComponent(
                    category="role_need",
                    value=value,
                    reason=(
                        f"Fills role '{need.key}' "
                        f"({need.current:g}/{need.target}, urgency {need.urgency:.2f})."
                    ),
                )
            )
        return tuple(components)
