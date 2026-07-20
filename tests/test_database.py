from thun_deckbuilder.card_database import CardDatabase


def test_ocelot_pride_is_not_legal():
    with CardDatabase() as database:
        assert database.get_card_by_name("Ocelot Pride") is not None
        assert not database.is_card_legal_by_name("Ocelot Pride")


def test_uncommon_reprint_makes_card_legal():
    with CardDatabase() as database:
        assert database.is_card_legal_by_name("Rare Then Uncommon")


def test_legal_pool_excludes_ocelot_pride():
    with CardDatabase() as database:
        names = {card["name"] for card in database.get_all_legal_cards()}
    assert "Ocelot Pride" not in names
    assert "Lightning Strike" in names
