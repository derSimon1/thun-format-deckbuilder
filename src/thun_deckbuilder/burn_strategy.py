from __future__ import annotations

from thun_deckbuilder.deck_generator import (
    GeneratedDeck,
    generate_burn_deck,
)
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase


class BurnStrategy:
    def generate(
        self,
        knowledge_base: KnowledgeBase,
        request: DeckRequest,
    ) -> GeneratedDeck:
        self._validate_request(request)

        return generate_burn_deck(
            knowledge_base=knowledge_base,
            max_copies=request.max_copies,
        )

    @staticmethod
    def _validate_request(
        request: DeckRequest,
    ) -> None:
        if set(request.colors) != {"R"}:
            raise ValueError(
                "Der Burn-Prototyp unterstützt aktuell nur Mono-Rot."
            )

        if request.deck_size != 60:
            raise ValueError(
                "Der Burn-Prototyp unterstützt aktuell nur "
                "Decks mit 60 Karten."
            )