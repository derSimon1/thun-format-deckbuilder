from thun_deckbuilder.card_contribution import CardContribution, RoleContribution
from thun_deckbuilder.deck_needs import DeckNeedsAnalyzer
from thun_deckbuilder.deck_profile import TOKENS_PROFILE
from thun_deckbuilder.deck_state import DeckState


def token_card(name: str) -> CardContribution:
    return CardContribution(
        card_name=name,
        roles=(RoleContribution("token_maker"),),
        tags=frozenset({"creature_token"}),
        mana_value=2,
    )


def test_empty_deck_reports_required_token_need() -> None:
    needs = DeckNeedsAnalyzer().analyze(DeckState(), TOKENS_PROFILE, deck_size=60)

    token_need = next(need for need in needs.role_needs if need.key == "token_maker")
    assert token_need.current == 0
    assert token_need.missing_minimum == 12
    assert token_need.required
    assert token_need.urgency > 0
    assert needs.remaining_spell_slots == 36
    assert needs.remaining_land_slots == 24


def test_need_falls_as_role_is_filled() -> None:
    analyzer = DeckNeedsAnalyzer()
    empty_needs = analyzer.analyze(DeckState(), TOKENS_PROFILE, deck_size=60)
    state = DeckState().with_card(token_card("Token Spell"), 12)
    filled_needs = analyzer.analyze(state, TOKENS_PROFILE, deck_size=60)

    empty = next(need for need in empty_needs.role_needs if need.key == "token_maker")
    filled = next(need for need in filled_needs.role_needs if need.key == "token_maker")
    assert filled.missing_minimum == 0
    assert filled.urgency < empty.urgency
    assert not any(need.key == "token_maker" for need in filled_needs.unmet_required_needs())
