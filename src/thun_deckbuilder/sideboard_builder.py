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


ARTIFACT_ENCHANTMENT_ANSWER = SideboardRule(
    "artifact/enchantment answer",
    (
        "destroy target artifact",
        "destroy target enchantment",
        "exile target artifact",
        "exile target enchantment",
    ),
    priority=5,
)
GRAVEYARD_HATE = SideboardRule(
    "graveyard hate",
    (
        "exile all cards from",
        "cards in graveyards can't",
        "exile target player's graveyard",
        "exile target card from a graveyard",
    ),
    priority=4,
)
CREATURE_SWEEPER = SideboardRule(
    "creature sweeper",
    (
        "destroy all creatures",
        "exile all creatures",
        "damage to each creature",
        "-2/-2 until end of turn",
    ),
    priority=4,
)
COUNTERSPELL = SideboardRule(
    "countermagic",
    ("counter target spell", "counter target noncreature spell"),
    priority=3.5,
)


RULES: dict[str, tuple[SideboardRule, ...]] = {
    "burn": (
        ARTIFACT_ENCHANTMENT_ANSWER,
        GRAVEYARD_HATE,
        SideboardRule(
            "anti-lifegain",
            ("players can't gain life", "your opponents can't gain life"),
            priority=5,
        ),
        CREATURE_SWEEPER,
    ),
    "tokens": (
        ARTIFACT_ENCHANTMENT_ANSWER,
        GRAVEYARD_HATE,
        SideboardRule(
            "protection",
            (
                "creatures you control gain indestructible",
                "creatures you control gain hexproof",
            ),
            roles=("protection",),
            priority=4,
        ),
        CREATURE_SWEEPER,
    ),
    "artifacts": (
        GRAVEYARD_HATE,
        CREATURE_SWEEPER,
        COUNTERSPELL,
        SideboardRule(
            "protect artifacts",
            (
                "artifacts you control gain hexproof",
                "target artifact gains hexproof",
                "return target artifact card from your graveyard",
                "return target artifact to its owner's hand",
            ),
            priority=4.5,
        ),
        SideboardRule(
            "answer opposing artifacts",
            (
                "destroy target artifact",
                "exile target artifact",
                "gain control of target artifact",
            ),
            priority=4,
        ),
    ),
    "shrines": (
        GRAVEYARD_HATE,
        CREATURE_SWEEPER,
        COUNTERSPELL,
        SideboardRule(
            "protect enchantments",
            (
                "enchantments you control have hexproof",
                "target enchantment gains hexproof",
                "permanents you control gain hexproof",
                "permanents you control gain indestructible",
            ),
            roles=("protection",),
            priority=5,
        ),
        SideboardRule(
            "enchantment recursion",
            (
                "return target enchantment card from your graveyard",
                "return target permanent card from your graveyard",
            ),
            priority=4,
        ),
        ARTIFACT_ENCHANTMENT_ANSWER,
    ),
    "mill": (
        GRAVEYARD_HATE,
        CREATURE_SWEEPER,
        COUNTERSPELL,
        SideboardRule(
            "anti-aggro removal",
            (
                "destroy target creature",
                "exile target creature",
                "target creature gets -",
            ),
            roles=("removal",),
            priority=4.5,
        ),
        SideboardRule(
            "protect mill plan",
            (
                "target player can't search",
                "cards can't leave graveyards",
                "spells in graveyards can't be cast",
            ),
            priority=4,
        ),
    ),
    "prowess": (
        COUNTERSPELL,
        GRAVEYARD_HATE,
        SideboardRule(
            "protect threats",
            (
                "target creature you control gains hexproof",
                "target creature gains hexproof",
                "return target creature you control to its owner's hand",
                "phase out",
            ),
            roles=("protection",),
            priority=5,
        ),
        SideboardRule(
            "anti-lifegain",
            (
                "players can't gain life",
                "your opponents can't gain life",
                "life can't be gained",
            ),
            priority=5,
        ),
        SideboardRule(
            "cheap creature interaction",
            (
                "damage to target creature",
                "damage to any target",
                "return target creature to its owner's hand",
            ),
            roles=("removal",),
            priority=4.5,
        ),
        ARTIFACT_ENCHANTMENT_ANSWER,
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
                role_match = any(str(role) in rule.roles for role in knowledge.roles)
                if phrase_match or role_match:
                    matched.append(rule.label)
                    score += rule.priority
            if score <= 0:
                continue
            score -= analysis.mana_value * 0.15
            scored.append((score, knowledge, tuple(dict.fromkeys(matched))))

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].analysis.mana_value,
                item[1].analysis.name,
            )
        )
        entries: list[DeckEntry] = []
        remaining = size
        for score, knowledge, reasons in scored:
            if remaining <= 0:
                break
            quantity = min(
                max_copies - main_counts[knowledge.analysis.name],
                3,
                remaining,
            )
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
