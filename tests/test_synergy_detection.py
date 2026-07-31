from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_synergies import detect_synergies
from thun_deckbuilder.synergy_tag import SynergyTag


def test_token_maker_and_spell_tags_are_detected() -> None:
    analysis = analyze_card(
        {
            "name": "Reinforcements",
            "mana_value": 2,
            "type_line": "Instant",
            "oracle_text": "Create two 1/1 white Soldier creature tokens.",
        }
    )

    tags = detect_synergies(analysis)

    assert SynergyTag.SPELL in tags
    assert SynergyTag.TOKEN_MAKER in tags
    assert SynergyTag.SACRIFICE_FODDER in tags


def test_artifact_payoff_is_detected_from_oracle_text() -> None:
    analysis = analyze_card(
        {
            "name": "Foundry Captain",
            "mana_value": 3,
            "type_line": "Creature — Human Artificer",
            "oracle_text": "Artifacts you control get +1/+1.",
        }
    )

    assert SynergyTag.ARTIFACT_PAYOFF in detect_synergies(analysis)
