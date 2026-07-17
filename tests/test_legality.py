from thun_deckbuilder.legality import (
    is_card_legal,
    is_print_legal,
)


def test_common_is_legal():

    result = is_print_legal(
        rarity="common",
        digital=False,
        games="paper",
        set_allowed=True,
    )

    assert result.legal


def test_rare_is_illegal():

    result = is_print_legal(
        rarity="rare",
        digital=False,
        games="paper",
        set_allowed=True,
    )

    assert not result.legal


def test_digital_is_illegal():

    result = is_print_legal(
        rarity="common",
        digital=True,
        games="paper",
        set_allowed=True,
    )

    assert not result.legal


def test_wrong_set_is_illegal():

    result = is_print_legal(
        rarity="common",
        digital=False,
        games="paper",
        set_allowed=False,
    )

    assert not result.legal

def test_card_is_legal_when_one_print_is_legal():
    prints = [
        {
            "set_code": "old",
            "rarity": "rare",
            "digital": False,
            "games": "paper",
            "set_allowed": False,
        },
        {
            "set_code": "dmu",
            "rarity": "uncommon",
            "digital": False,
            "games": "paper,arena",
            "set_allowed": True,
        },
    ]

    result = is_card_legal(prints)

    assert result.legal
    assert len(result.legal_prints) == 1
    assert result.legal_prints[0]["set_code"] == "dmu"


def test_card_is_illegal_when_all_prints_are_illegal():
    prints = [
        {
            "set_code": "old",
            "rarity": "rare",
            "digital": False,
            "games": "paper",
            "set_allowed": True,
        },
        {
            "set_code": "digital",
            "rarity": "common",
            "digital": True,
            "games": "arena",
            "set_allowed": True,
        },
    ]

    result = is_card_legal(prints)

    assert not result.legal
    assert result.legal_prints == []


def test_card_without_prints_is_illegal():
    result = is_card_legal([])

    assert not result.legal
    assert result.reason == "No prints found."


def test_multiple_legal_prints_are_returned():
    prints = [
        {
            "set_code": "woe",
            "rarity": "common",
            "digital": False,
            "games": "paper,arena",
            "set_allowed": True,
        },
        {
            "set_code": "fdn",
            "rarity": "common",
            "digital": False,
            "games": "paper,arena",
            "set_allowed": True,
        },
    ]

    result = is_card_legal(prints)

    assert result.legal
    assert len(result.legal_prints) == 2