from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import score_artifact_card


def _artifact_card(
    name: str,
    mana_value: float,
    type_line: str,
    oracle_text: str,
    power: str | None = None,
):
    card = {
        "name": name,
        "mana_value": mana_value,
        "colors": [],
        "color_identity": [],
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    if power is not None:
        card["power"] = power
    return analyze_card(card)


def test_cheap_artifact_beats_expensive_vanilla_artifact():
    cheap = score_artifact_card(
        _artifact_card("Cheap Enabler", 1, "Artifact", "")
    )
    expensive = score_artifact_card(
        _artifact_card(
            "Expensive Golem",
            6,
            "Artifact Creature — Golem",
            "Vigilance",
            power="6",
        )
    )

    assert cheap.score > expensive.score
    assert "Sehr günstiger Enabler" in cheap.reasons
    assert "Teures Artefakt ohne Synergie" in expensive.reasons


def test_affinity_receives_payoff_bonus():
    result = score_artifact_card(
        _artifact_card(
            "Affinity Threat",
            7,
            "Artifact Creature — Construct",
            "Affinity for artifacts",
            power="5",
        )
    )
    assert "Affinity-Payoff" in result.reasons


def test_improvise_receives_payoff_bonus():
    result = score_artifact_card(
        _artifact_card("Improvised Spell", 5, "Sorcery", "Improvise")
    )
    assert "Improvise-Payoff" in result.reasons


def test_improvised_in_card_name_is_not_the_improvise_mechanic():
    result = score_artifact_card(
        _artifact_card(
            "Improvised Weaponry",
            3,
            "Sorcery",
            "Improvised Weaponry deals 2 damage to any target. "
            "Create a Treasure token.",
        )
    )

    assert "Improvise-Payoff" not in result.reasons


def test_artifact_token_producer_is_recognized():
    result = score_artifact_card(
        _artifact_card(
            "Treasure Maker",
            2,
            "Creature — Human Artificer",
            "When this creature enters, create a Treasure token.",
            power="2",
        )
    )
    assert "Erzeugt Artefakt-Spielsteine" in result.reasons


def test_artifact_payoff_beats_unrelated_filler():
    payoff = score_artifact_card(
        _artifact_card(
            "Artifact Payoff",
            3,
            "Creature — Artificer",
            "Whenever an artifact enters, draw a card.",
        )
    )
    filler = score_artifact_card(
        _artifact_card(
            "Generic Creature",
            3,
            "Creature — Soldier",
            "Vigilance",
            power="3",
        )
    )
    assert payoff.score > filler.score
