import pytest

from thun_deckbuilder.burn_strategy import BurnStrategy
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase


def build_knowledge_base(
    database: CardDatabase,
) -> KnowledgeBase:
    knowledge_base = KnowledgeBase(database)
    knowledge_base.load()

    return knowledge_base


def test_burn_strategy_generates_60_card_deck():
    request = DeckRequest(
        archetype="burn",
        colors=("R",),
    )

    with CardDatabase() as database:
        knowledge_base = build_knowledge_base(database)

        deck = BurnStrategy().generate(
            knowledge_base=knowledge_base,
            request=request,
        )

    spell_count = sum(
        entry.quantity
        for entry in deck.mainboard
    )

    assert spell_count == 36
    assert deck.lands == 24
    assert spell_count + deck.lands == 60


def test_burn_strategy_rejects_multiple_colors():
    request = DeckRequest(
        archetype="burn",
        colors=("R", "W"),
    )

    with CardDatabase() as database:
        knowledge_base = build_knowledge_base(database)

        with pytest.raises(
            ValueError,
            match="nur Mono-Rot",
        ):
            BurnStrategy().generate(
                knowledge_base=knowledge_base,
                request=request,
            )


def test_burn_strategy_rejects_wrong_deck_size():
    request = DeckRequest(
        archetype="burn",
        colors=("R",),
        deck_size=100,
    )

    with CardDatabase() as database:
        knowledge_base = build_knowledge_base(database)

        with pytest.raises(
            ValueError,
            match="nur Decks mit 60 Karten",
        ):
            BurnStrategy().generate(
                knowledge_base=knowledge_base,
                request=request,
            )