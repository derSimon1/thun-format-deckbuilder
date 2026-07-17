from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import CardAnalysis, analyze_card
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.card_scoring import ScoreBreakdown, score_burn_card
from thun_deckbuilder.card_synergies import detect_synergies


@dataclass(frozen=True)
class CardKnowledge:
    card: dict
    analysis: CardAnalysis
    roles: frozenset[str]
    synergies: frozenset[str]
    scoring: ScoreBreakdown


class KnowledgeBase:
    def __init__(self, database: CardDatabase):
        self.database = database
        self._cards: list[CardKnowledge] = []

    def load(self) -> None:
        self._cards.clear()

        for card in self.database.get_all_cards():

            analysis = analyze_card(card)

            self._cards.append(
                CardKnowledge(
                    card=card,
                    analysis=analysis,
                    roles=detect_roles(analysis),
                    synergies=detect_synergies(analysis),
                    scoring=score_burn_card(analysis),
                )
            )

    @property
    def cards(self) -> tuple[CardKnowledge, ...]:
        return tuple(self._cards)