from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_profile import BURN_PROFILE, TOKENS_PROFILE
from thun_deckbuilder.deck_validation import validate_deck


def test_generated_burn_deck_passes_structural_validation():
    with CardDatabase() as database:
        deck = generate_deck(database, "burn", ["R"])
    report = validate_deck(deck, profile=BURN_PROFILE)
    assert report.valid
    assert report.total_cards == 60
    assert dict(report.role_counts)["burn"] >= 18


def test_generated_token_deck_passes_structural_validation():
    with CardDatabase() as database:
        deck = generate_deck(database, "tokens", ["W"])
    report = validate_deck(deck, profile=TOKENS_PROFILE)
    assert report.valid
    assert report.total_cards == 60
    assert dict(report.role_counts)["token_maker"] >= 12
