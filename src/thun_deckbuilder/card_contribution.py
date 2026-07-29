from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from thun_deckbuilder.knowledge_base import CardKnowledge


_COLOR_SYMBOL = re.compile(r"\{([WUBRG])(?:/[^}]*)?\}", re.IGNORECASE)


@dataclass(frozen=True)
class RoleContribution:
    """How strongly a card contributes to one functional deck role."""

    role: str
    strength: float = 1.0

    def __post_init__(self) -> None:
        if not self.role:
            raise ValueError("Role name cannot be empty.")
        if self.strength <= 0:
            raise ValueError("Role contribution strength must be positive.")


@dataclass(frozen=True)
class CardContribution:
    """Normalized contribution data used by deck-state and scoring systems."""

    card_name: str
    roles: tuple[RoleContribution, ...]
    tags: frozenset[str]
    mana_value: float
    color_pips: tuple[tuple[str, int], ...] = ()
    is_land: bool = False
    is_legendary: bool = False

    def strength_for(self, role: str) -> float:
        return sum(item.strength for item in self.roles if item.role == role)

    def pip_count(self, color: str) -> int:
        normalized = color.upper()
        return sum(count for pip_color, count in self.color_pips if pip_color == normalized)

    @property
    def pip_mapping(self) -> Mapping[str, int]:
        return dict(self.color_pips)


def contribution_from_knowledge(knowledge: CardKnowledge) -> CardContribution:
    """Create a conservative v1 contribution model from existing analysis.

    Role strength intentionally starts at 1.0. More nuanced strengths can be
    introduced later without changing the public data model.
    """

    mana_cost = str(knowledge.card.get("mana_cost", ""))
    pips: dict[str, int] = {}
    for symbol in _COLOR_SYMBOL.findall(mana_cost):
        color = symbol.upper()
        pips[color] = pips.get(color, 0) + 1

    return CardContribution(
        card_name=knowledge.analysis.name,
        roles=tuple(RoleContribution(role) for role in sorted(knowledge.roles)),
        tags=frozenset(knowledge.synergies),
        mana_value=knowledge.analysis.mana_value,
        color_pips=tuple(sorted(pips.items())),
        is_land=knowledge.analysis.is_land,
        is_legendary=knowledge.analysis.is_legendary,
    )
