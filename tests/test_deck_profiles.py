from thun_deckbuilder.deck_profile import BURN_PROFILE, TOKENS_PROFILE


def test_profiles_fit_sixty_card_decks():
    assert BURN_PROFILE.spell_slots(60) == 36
    assert TOKENS_PROFILE.spell_slots(60) == 36


def test_profiles_define_core_roles():
    assert BURN_PROFILE.role_targets[0].role == "burn"
    assert TOKENS_PROFILE.role_targets[0].role == "token_maker"
