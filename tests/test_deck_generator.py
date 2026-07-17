from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_generator import generate_burn_deck
from thun_deckbuilder.knowledge_base import KnowledgeBase


def build_test_deck():
    with CardDatabase() as database:
        knowledge_base = KnowledgeBase(database)
        knowledge_base.load()

        return generate_burn_deck(knowledge_base)


def test_generate_burn_deck_has_60_cards():
    deck = build_test_deck()

    spell_count = sum(
        entry.quantity
        for entry in deck.mainboard
    )

    assert spell_count == 36
    assert deck.lands == 24
    assert spell_count + deck.lands == 60


def test_generate_burn_deck_respects_copy_limit():
    deck = build_test_deck()

    assert all(
        entry.quantity <= 3
        for entry in deck.mainboard
    )


def test_generate_burn_deck_contains_no_duplicate_names():
    deck = build_test_deck()

    names = [
        entry.name
        for entry in deck.mainboard
    ]

    assert len(names) == len(set(names))


def test_generate_burn_deck_uses_expected_number_of_spells():
    deck = build_test_deck()

    spell_count = sum(
        entry.quantity
        for entry in deck.mainboard
    )

    assert spell_count == 36