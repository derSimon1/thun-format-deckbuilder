from thun_deckbuilder.deck_skeleton import BURN_SKELETON


def test_burn_skeleton_total_cards():
    spells = sum(slot.cards for slot in BURN_SKELETON.curve)

    assert spells == 36
    assert BURN_SKELETON.lands == 24