from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.card_analyzer import analyze_card


def test_lightning_strike_analysis():

    db = CardDatabase()

    card = db.get_card_by_name("Lightning Strike")

    assert card is not None

    analysis = analyze_card(card)

    assert analysis.name == "Lightning Strike"

    assert analysis.is_instant

    assert analysis.mana_value == 2

    assert analysis.colors == ("R",)

    assert "damage" in analysis.features