from __future__ import annotations

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase
from thun_deckbuilder.token_generator import generate_token_deck


class TokenStrategy:
    def generate(
        self,
        knowledge_base: KnowledgeBase,
        request: DeckRequest,
    ) -> GeneratedDeck:
        self._validate_request(request)

        return generate_token_deck(
            knowledge_base=knowledge_base,
            deck_size=request.deck_size,
            lands=24,
            max_copies=request.max_copies,
        )

    @staticmethod
    def _validate_request(
        request: DeckRequest,
    ) -> None:
        if set(request.colors) != {"W"}:
            raise ValueError(
                "Die Token-Strategie unterstützt aktuell "
                "nur Mono-Weiss."
            )

        if request.deck_size != 60:
            raise ValueError(
                "Die Token-Strategie unterstützt aktuell "
                "nur Decks mit 60 Karten."
            )