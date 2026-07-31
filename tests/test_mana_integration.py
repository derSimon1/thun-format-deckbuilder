from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.prototype import format_deck


def test_generated_token_deck_contains_mana_base_and_quality():
    with CardDatabase() as database:
        deck = generate_deck(database, "tokens", ["W"])
    assert deck.mana_base is not None
    assert deck.mana_base.sources_for("W") == deck.lands
    assert deck.mana_quality is not None
    assert deck.quality_report is not None
    assert deck.quality_report.mana_score == deck.mana_quality.score
    rendered = format_deck(deck, archetype="tokens", colors=("W",))
    assert "MANA BASE" in rendered
    assert "Plains" in rendered
