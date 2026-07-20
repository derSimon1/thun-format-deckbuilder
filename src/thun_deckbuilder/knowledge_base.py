from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from thun_deckbuilder.card_analyzer import CardAnalysis, analyze_card
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.card_synergies import detect_synergies
from thun_deckbuilder.config import AppConfig, load_config


@dataclass(frozen=True)
class CardKnowledge:
    card: dict[str, Any]
    analysis: CardAnalysis
    roles: frozenset[str]
    synergies: frozenset[str]


class KnowledgeBase:
    """Analyzed knowledge built exclusively from the legal card pool."""

    def __init__(
        self,
        database: CardDatabase,
        config: AppConfig | None = None,
    ) -> None:
        self.database = database
        self.config = config or load_config()
        self._cards: list[CardKnowledge] = []

    def load(self) -> None:
        self._cards = []
        for card in self.database.get_all_legal_cards(self.config):
            analysis = analyze_card(card)
            self._cards.append(
                CardKnowledge(
                    card=card,
                    analysis=analysis,
                    roles=detect_roles(analysis),
                    synergies=detect_synergies(analysis),
                )
            )

    @property
    def cards(self) -> tuple[CardKnowledge, ...]:
        return tuple(self._cards)
