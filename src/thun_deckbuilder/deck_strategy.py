from __future__ import annotations

from typing import Protocol

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase


class DeckStrategy(Protocol):
    def generate(
        self,
        knowledge_base: KnowledgeBase,
        request: DeckRequest,
    ) -> GeneratedDeck:
        """Erzeugt ein Deck anhand der übergebenen Anfrage."""
        ...