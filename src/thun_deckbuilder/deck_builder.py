from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace

from thun_deckbuilder.burn_strategy import BurnStrategy
from thun_deckbuilder.calibrated_strategies import (
    ArtifactStrategy,
    MillStrategy,
    ShrineStrategy,
)
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.control_strategy import ControlStrategy
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.deck_strategy import DeckStrategy
from thun_deckbuilder.goldfish_simulator import GoldfishSimulator
from thun_deckbuilder.knowledge_base import KnowledgeBase
from thun_deckbuilder.token_strategy import TokenStrategy


STRATEGIES: dict[str, DeckStrategy] = {
    "burn": BurnStrategy(),
    "tokens": TokenStrategy(),
    "artifacts": ArtifactStrategy(),
    "control": ControlStrategy(),
    "shrines": ShrineStrategy(),
    "mill": MillStrategy(),
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

    strategy = STRATEGIES.get(request.archetype)

    if strategy is None:
        supported = ", ".join(sorted(STRATEGIES))
        raise ValueError(
            f"Unbekannter Archetyp: {request.archetype}. "
            f"Unterstützt werden aktuell: {supported}."
        )

    knowledge_base = KnowledgeBase(database)
    knowledge_base.load()

    deck = strategy.generate(
        knowledge_base=knowledge_base,
        request=request,
    )
    goldfish_report = GoldfishSimulator().simulate(
        deck,
        archetype=request.archetype,
    )
    return replace(deck, goldfish_report=goldfish_report)
