import pytest

from thun_deckbuilder.card_contribution import CardContribution, RoleContribution
from thun_deckbuilder.deck_state import DeckState


def contribution(
    name: str,
    *,
    mana_value: float = 2,
    roles: tuple[str, ...] = (),
    tags: frozenset[str] = frozenset(),
    pips: tuple[tuple[str, int], ...] = (),
    is_land: bool = False,
) -> CardContribution:
    return CardContribution(
        card_name=name,
        roles=tuple(RoleContribution(role) for role in roles),
        tags=tags,
        mana_value=mana_value,
        color_pips=pips,
        is_land=is_land,
    )


def test_with_card_returns_new_state_and_preserves_original() -> None:
    original = DeckState()
    updated = original.with_card(contribution("Token Spell", roles=("token_maker",)), 3)

    assert original.total_cards == 0
    assert updated.total_cards == 3
    assert updated.role_count("token_maker") == 3


def test_state_aggregates_roles_tags_curve_and_pips() -> None:
    state = DeckState().with_card(
        contribution(
            "Reinforcements",
            roles=("token_maker",),
            tags=frozenset({"creature_token"}),
            pips=(("W", 1),),
        ),
        3,
    )

    assert state.tag_count("creature_token") == 3
    assert state.curve_count(2) == 3
    assert state.color_pip_count("W") == 3


def test_can_add_enforces_deck_size_and_copy_limit() -> None:
    card = contribution("Burn Spell", roles=("burn",))
    state = DeckState().with_card(card, 2)

    assert state.can_add(card, 1, deck_size=60, max_copies=3)
    assert not state.can_add(card, 2, deck_size=60, max_copies=3)
    assert not state.can_add(card, 1, deck_size=2, max_copies=3)


def test_with_card_can_enforce_limits() -> None:
    card = contribution("Burn Spell", roles=("burn",))
    state = DeckState().with_card(card, 3)

    with pytest.raises(ValueError):
        state.with_card(card, 1, deck_size=60, max_copies=3)
