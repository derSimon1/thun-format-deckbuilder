from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, parse_mana_cost
from thun_deckbuilder.knowledge_base import CardKnowledge


@dataclass(frozen=True)
class SideboardRule:
    label: str
    phrases: tuple[str, ...]
    roles: tuple[str, ...] = ()
    priority: float = 1.0


RULES: dict[str, tuple[SideboardRule, ...]] = {
    "burn": (
        SideboardRule("artifact/enchantment answer", ("destroy target artifact", "destroy target enchantment", "exile target artifact", "exile target enchantment"), priority=5),
        SideboardRule("graveyard hate", ("exile all cards from", "cards in graveyards can't"), priority=4),
        SideboardRule("anti-lifegain", ("players can't gain life", "your opponents can't gain life"), priority=5),
        SideboardRule("sweeper", ("damage to each creature",), priority=3),
    ),
    "tokens": (
        SideboardRule("artifact/enchantment answer", ("destroy target artifact", "destroy target enchantment", "exile target artifact", "exile target enchantment"), priority=5),
        SideboardRule("graveyard hate", ("exile all cards from", "cards in graveyards can't"), priority=4),
        SideboardRule("protection", ("creatures you control gain indestructible", "creatures you control gain hexproof"), roles=("protection",), priority=4),
        SideboardRule("sweeper", ("destroy all creatures", "exile all creatures"), priority=3),
    ),
}


class SideboardBuilder:
    """Build a conservative 15-card sideboard from legal, on-colour cards."""

    def build(
        self,
        cards: Iterable[CardKnowledge],
        deck: GeneratedDeck,
        *,
        archetype: str,
        colors: Iterable[str],
        max_copies: int = 3,
        size: int = 15,
    ) -> tuple[DeckEntry, ...]:
        rules = RULES.get(archetype, ())
        allowed_colors = {color.upper() for color in colors}
        main_counts = Counter({entry.name: entry.quantity for entry in deck.mainboard})
        scored: list[tuple[float, CardKnowledge, tuple[str, ...]]] = []

        for knowledge in cards:
            analysis = knowledge.analysis
            if analysis.is_land or not set(analysis.color_identity).issubset(allowed_colors):
                continue
            available = max_copies - main_counts[analysis.name]
            if available <= 0:
                continue
            text = analysis.oracle_text.lower()
            matched: list[str] = []
            score = 0.0
            for rule in rules:
                phrase_match = any(phrase in text for phrase in rule.phrases)
                role_match = any(role in knowledge.roles for role in rule.roles)
                if phrase_match or role_match:
                    matched.append(rule.label)
                    score += rule.priority
            if score <= 0:
                continue
            score -= analysis.mana_value * 0.15
            scored.append((score, knowledge, tuple(matched)))

        scored.sort(key=lambda item: (-item[0], item[1].analysis.mana_value, item[1].analysis.name))
        entries: list[DeckEntry] = []
        remaining = size
        for score, knowledge, reasons in scored:
            if remaining <= 0:
                break
            quantity = min(max_copies - main_counts[knowledge.analysis.name], 3, remaining)
            entries.append(
                DeckEntry(
                    name=knowledge.analysis.name,
                    quantity=quantity,
                    mana_cost=parse_mana_cost(str(knowledge.card.get("mana_cost", ""))),
                    mana_value=knowledge.analysis.mana_value,
                    type_line=knowledge.analysis.type_line,
                    score=score,
                    reasons=tuple(f"Sideboard: {reason}" for reason in reasons),
                    roles=tuple(sorted(str(role) for role in knowledge.roles)),
                )
            )
            remaining -= quantity
        return tuple(entries)
