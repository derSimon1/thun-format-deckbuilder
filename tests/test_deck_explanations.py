from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck


def test_generated_cards_have_score_and_reasons():
    with CardDatabase() as database:
        deck = generate_deck(
            database=database,
            archetype="burn",
            colors=["R"],
        )

    assert deck.mainboard

    for entry in deck.mainboard:
        assert entry.score > 0
        assert entry.reasons