from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.candidate_score import ScoreComponent
from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.knowledge_base import CardKnowledge


@dataclass(frozen=True)
class ArchetypeRules:
    name: str
    preferred_roles: frozenset[str]
    preferred_max_mana_value: float
    role_bonus: float = 2.0
    curve_bonus: float = 2.0
    expensive_penalty: float = -2.0


RULES: dict[str, ArchetypeRules] = {
    "Mono-Red Burn": ArchetypeRules(
        name="Mono-Red Burn",
        preferred_roles=frozenset({"burn", "aggro_creature", "card_draw"}),
        preferred_max_mana_value=2,
        role_bonus=2.5,
        curve_bonus=2.5,
        expensive_penalty=-3.0,
    ),
    "Mono-White Tokens": ArchetypeRules(
        name="Mono-White Tokens",
        preferred_roles=frozenset({"token_maker", "token_payoff", "removal", "protection"}),
        preferred_max_mana_value=3,
        role_bonus=2.5,
        curve_bonus=2.0,
        expensive_penalty=-2.0,
    ),
}


class ArchetypeEvaluator:
    """Apply small, explicit archetype adjustments without replacing base scoring."""

    def score(
        self,
        knowledge: CardKnowledge,
        contribution: CardContribution,
        profile: DeckProfile,
    ) -> tuple[ScoreComponent, ...]:
        rules = RULES.get(profile.name)
        if rules is None:
            return ()

        components: list[ScoreComponent] = []
        matching_roles = sorted(str(role) for role in knowledge.roles if str(role) in rules.preferred_roles)
        if matching_roles:
            components.append(
                ScoreComponent(
                    category="archetype_fit",
                    value=rules.role_bonus,
                    reason=f"Fits {rules.name}: {', '.join(matching_roles)}.",
                )
            )

        mana_value = contribution.mana_value
        if mana_value <= rules.preferred_max_mana_value:
            components.append(
                ScoreComponent(
                    category="archetype_curve",
                    value=rules.curve_bonus,
                    reason=f"Preferred {rules.name} mana range.",
                )
            )
        elif mana_value >= rules.preferred_max_mana_value + 2:
            components.append(
                ScoreComponent(
                    category="archetype_curve",
                    value=rules.expensive_penalty,
                    reason=f"Expensive for {rules.name}." ,
                )
            )
        return tuple(components)
