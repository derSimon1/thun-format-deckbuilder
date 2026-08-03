from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from thun_deckbuilder.card_role import CardRole, normalize_role
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.mana_requirement import strict_mana_symbol_count
from thun_deckbuilder.synergy_tag import SynergyTag, normalize_synergy_tag


_COLOR_SYMBOL = re.compile(r"\{([WUBRG])(?:/[^}]*)?\}", re.IGNORECASE)
_METADATA_ROLE_PREFIXES = (
    "token_output_",
    "token_production_",
    "token_activation_mana_",
)


def _is_metadata_role(role: str) -> bool:
    """Return whether a role carries simulation metadata, not deck function."""

    return role.startswith(_METADATA_ROLE_PREFIXES)


@dataclass(frozen=True)
class RoleContribution:
    """How strongly a card contributes to one functional deck role."""

    role: CardRole
    strength: float = 1.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "role", normalize_role(self.role))
        if self.strength <= 0:
            raise ValueError("Role contribution strength must be positive.")


@dataclass(frozen=True)
class CardContribution:
    """Normalized contribution data used by deck-state and scoring systems."""

    card_name: str
    roles: tuple[RoleContribution, ...]
    tags: frozenset[SynergyTag | str]
    mana_value: float
    color_pips: tuple[tuple[str, int], ...] = ()
    is_land: bool = False
    is_legendary: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "tags",
            frozenset(normalize_synergy_tag(tag) for tag in self.tags),
        )

    def strength_for(self, role: CardRole | str) -> float:
        normalized = normalize_role(role)
        return sum(item.strength for item in self.roles if item.role == normalized)

    def pip_count(self, color: str) -> int:
        normalized = color.upper()
        return sum(count for pip_color, count in self.color_pips if pip_color == normalized)

    @property
    def pip_mapping(self) -> Mapping[str, int]:
        return dict(self.color_pips)


def contribution_from_knowledge(knowledge: CardKnowledge) -> CardContribution:
    """Create conservative functional contribution data from existing analysis.

    Machine-readable simulation metadata remains on the resulting ``DeckEntry``
    because the composition engine copies all knowledge roles into the final
    entry. It is deliberately excluded from ``CardContribution`` so dynamic
    markers such as ``token_output_2`` or ``token_activation_mana_4`` cannot
    become structural deck roles.
    """

    mana_cost = str(knowledge.card.get("mana_cost", ""))
    pips: dict[str, int] = {}
    for symbol in _COLOR_SYMBOL.findall(mana_cost):
        color = symbol.upper()
        pips[color] = pips.get(color, 0) + 1
    strict_colorless = strict_mana_symbol_count(mana_cost, "C")
    if strict_colorless:
        pips["C"] = strict_colorless

    functional_roles = tuple(
        role
        for role in sorted(str(role) for role in knowledge.roles)
        if not _is_metadata_role(role)
    )
    return CardContribution(
        card_name=knowledge.analysis.name,
        roles=tuple(RoleContribution(role) for role in functional_roles),
        tags=frozenset(knowledge.synergies),
        mana_value=knowledge.analysis.mana_value,
        color_pips=tuple(sorted(pips.items())),
        is_land=knowledge.analysis.is_land,
        is_legendary=knowledge.analysis.is_legendary,
    )
