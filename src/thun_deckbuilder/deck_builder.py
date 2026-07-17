from __future__ import annotations

from collections.abc import Iterable

from thun_deckbuilder.burn_strategy import BurnStrategy
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.deck_strategy import DeckStrategy
from thun_deckbuilder.knowledge_base import KnowledgeBase
from thun_deckbuilder.token_strategy import TokenStrategy


STRATEGIES: dict[str, DeckStrategy] = {
    "burn": BurnStrategy(),
    "tokens": TokenStrategy(),
}


def generate_deck(
    database: CardDatabase,
    archetype: str,
    colors: Iterable[str],
    deck_size: int = 60,
    max_copies: int = 3,
) -> GeneratedDeck:
    request = DeckRequest(
        archetype=archetype,
        colors=tuple(colors),
        deck_size=deck_size,
        max_copies=max_copies,
    )

    strategy = STRATEGIES.get(
        request.archetype
    )

    if strategy is None:
        raise ValueError(
            f"Für den Archetyp '{request.archetype}' "
            "ist noch keine Strategie implementiert."
        )

    knowledge_base = KnowledgeBase(database)
    knowledge_base.load()

    return strategy.generate(
        knowledge_base=knowledge_base,
        request=request,
    )