from thun_deckbuilder.config import load_config
from thun_deckbuilder.legality import is_card_legal, is_print_legal


def test_common_in_allowed_set_is_legal():
    result = is_print_legal(
        {"set_code": "dmu", "rarity": "common", "digital": False, "games": "paper"},
        load_config(),
    )
    assert result.legal


def test_mythic_is_illegal():
    result = is_print_legal(
        {"set_code": "dmu", "rarity": "mythic", "digital": False, "games": "paper"},
        load_config(),
    )
    assert not result.legal


def test_common_in_non_allowed_set_is_illegal():
    result = is_print_legal(
        {"set_code": "mh3", "rarity": "common", "digital": False, "games": "paper"},
        load_config(),
    )
    assert not result.legal


def test_card_is_legal_when_one_print_is_legal():
    result = is_card_legal(
        [
            {"set_code": "mh3", "rarity": "rare", "digital": False, "games": "paper"},
            {"set_code": "dmu", "rarity": "uncommon", "digital": False, "games": "paper,arena"},
        ],
        load_config(),
    )
    assert result.legal
    assert len(result.legal_prints) == 1


def test_card_without_prints_is_illegal():
    result = is_card_legal([], load_config())
    assert not result.legal
    assert result.reason == "No prints found."
