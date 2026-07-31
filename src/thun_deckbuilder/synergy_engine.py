from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.candidate_score import ScoreComponent
from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.synergy_tag import SynergyTag


@dataclass(frozen=True)
class SynergyRule:
    candidate_tag: SynergyTag
    deck_tag: SynergyTag
    points_per_card: float
    maximum_bonus: float
    reason: str


DEFAULT_RULES: tuple[SynergyRule, ...] = (
    SynergyRule(SynergyTag.TOKEN_MAKER, SynergyTag.TOKEN_PAYOFF, 1.5, 6.0, "Token maker supports existing token payoffs."),
    SynergyRule(SynergyTag.TOKEN_PAYOFF, SynergyTag.TOKEN_MAKER, 1.0, 8.0, "Token payoff is enabled by existing token makers."),
    SynergyRule(SynergyTag.SPELL, SynergyTag.SPELL_PAYOFF, 1.0, 6.0, "Instant or sorcery supports existing spell payoffs."),
    SynergyRule(SynergyTag.SPELL_PAYOFF, SynergyTag.SPELL, 0.5, 8.0, "Spell payoff is enabled by the deck's instants and sorceries."),
    SynergyRule(SynergyTag.ARTIFACT, SynergyTag.ARTIFACT_PAYOFF, 1.0, 6.0, "Artifact supports existing artifact payoffs."),
    SynergyRule(SynergyTag.ARTIFACT_PAYOFF, SynergyTag.ARTIFACT, 0.5, 8.0, "Artifact payoff is enabled by existing artifacts."),
    SynergyRule(SynergyTag.SACRIFICE_FODDER, SynergyTag.SACRIFICE_OUTLET, 1.0, 6.0, "Sacrifice fodder supports existing sacrifice outlets."),
    SynergyRule(SynergyTag.SACRIFICE_FODDER, SynergyTag.DEATH_TRIGGER, 1.0, 6.0, "Sacrifice fodder supports existing death triggers."),
    SynergyRule(SynergyTag.SACRIFICE_OUTLET, SynergyTag.SACRIFICE_FODDER, 0.6, 8.0, "Sacrifice outlet is enabled by existing fodder."),
    SynergyRule(SynergyTag.DEATH_TRIGGER, SynergyTag.SACRIFICE_FODDER, 0.6, 8.0, "Death trigger is enabled by existing fodder."),
)


class SynergyEngine:
    """Score how well a candidate interacts with the current deck state."""

    def __init__(self, rules: tuple[SynergyRule, ...] = DEFAULT_RULES) -> None:
        self.rules = rules

    def score(
        self,
        contribution: CardContribution,
        state: DeckState,
    ) -> tuple[ScoreComponent, ...]:
        components: list[ScoreComponent] = []
        candidate_tags = contribution.tags

        for rule in self.rules:
            if rule.candidate_tag not in candidate_tags:
                continue
            enabling_cards = state.tag_count(rule.deck_tag)
            if enabling_cards <= 0:
                continue
            bonus = min(rule.maximum_bonus, enabling_cards * rule.points_per_card)
            components.append(
                ScoreComponent(
                    category="synergy",
                    value=bonus,
                    reason=f"{rule.reason} ({enabling_cards} enabling card(s)).",
                )
            )

        shrine_count = state.tag_count(SynergyTag.SHRINE)
        if SynergyTag.SHRINE in candidate_tags and shrine_count > 0:
            components.append(
                ScoreComponent(
                    category="synergy",
                    value=min(12.0, shrine_count * 2.0),
                    reason=f"Shrine scales with {shrine_count} Shrine card(s) already selected.",
                )
            )

        return tuple(components)
