import pytest

from thun_deckbuilder.card_role import CardRole, normalize_role


def test_card_role_is_string_compatible() -> None:
    assert CardRole.BURN == "burn"
    assert "burn" in frozenset({CardRole.BURN})


def test_normalize_role_accepts_enum_and_string() -> None:
    assert normalize_role(CardRole.TOKEN_MAKER) is CardRole.TOKEN_MAKER
    assert normalize_role("token_maker") is CardRole.TOKEN_MAKER


def test_normalize_role_rejects_unknown_role() -> None:
    with pytest.raises(ValueError, match="Unknown card role"):
        normalize_role("tokenmaker")
