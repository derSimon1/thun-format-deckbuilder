from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.knowledge_base import KnowledgeBase


def test_knowledge_base_loads_cards():
    with CardDatabase() as database:

        kb = KnowledgeBase(database)

        kb.load()

        assert len(kb.cards) > 0


def test_every_card_has_analysis():
    with CardDatabase() as database:

        kb = KnowledgeBase(database)

        kb.load()

        card = kb.cards[0]

        assert card.analysis.name
        assert card.roles is not None
        assert card.synergies is not None
        assert card.scoring.score >= 0