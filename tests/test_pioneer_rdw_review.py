import json
from pathlib import Path


REVIEW = (
    Path(__file__).resolve().parents[1]
    / "research"
    / "meta"
    / "pioneer_rdw_thun_review_2026-08-05.json"
)


def load_review():
    return json.loads(REVIEW.read_text(encoding="utf-8"))


def test_review_is_read_only_and_does_not_authorize_generator_or_champion_change():
    review = load_review()
    assert review["status"] == "read_only_research"
    assert review["conclusion"]["champion_change_authorized"] is False
    assert review["conclusion"]["generator_change_authorized"] is False


def test_review_records_partial_mainboard_and_complete_sideboard_transfer():
    counts = load_review()["evidence_counts"]
    assert counts["mainboard_core_cards_checked"] == 15
    assert counts["mainboard_core_cards_directly_legal"] == 7
    assert counts["sideboard_cards_checked"] == 6
    assert counts["sideboard_cards_directly_legal"] == 6


def test_review_downgrades_initial_archetype_prior():
    conclusion = load_review()["conclusion"]
    assert conclusion["transfer_score_prior"] == 7.2
    assert conclusion["transfer_band"] == "high_structural_partial_card_level"


def test_direct_transfers_preserve_timing_conditions():
    transfers = {
        item["card"]: item for item in load_review()["direct_transfers"]
    }
    assert transfers["Monastery Swiftspear"]["timing"] == "immediate"
    assert "chapter" in transfers[
        "Kumano Faces Kakkazan // Etching of Kumano"
    ]["timing"]
    assert "kicker" in transfers["Burst Lightning"]["timing"]
    assert "desert_sacrifice" in transfers["Ramunap Ruins"]["timing"]
    assert "tribal_target" in transfers["Rockface Village"]["timing"]


def test_role_compression_losses_are_explicit():
    review = load_review()
    missing = {
        item["missing_original"]: item
        for item in review["functional_replacements"]
    }
    assert missing["Bonecrusher Giant // Stomp"]["classification"] == "split_across_cards"
    assert missing["Screaming Nemesis"]["classification"] == "partial"
    assert any(
        "creature-land" in statement
        for statement in review["non_reproducible_functions"]
    )


def test_three_copy_rule_requires_four_distinct_one_mana_names():
    review = load_review()
    one_mana = review["curated_candidate_core"]["one_mana_or_turn_one"]
    assert len(set(one_mana)) >= 4
    assert any(
        "at least four distinct" in statement
        for statement in review["non_reproducible_functions"]
    )
