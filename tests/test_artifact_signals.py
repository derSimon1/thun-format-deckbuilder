from thun_deckbuilder.artifact_signals import analyze_artifact, artifact_roles
from thun_deckbuilder.card_analyzer import analyze_card


def _analysis(name: str, mana_value: int, type_line: str, text: str):
    return analyze_card(
        {
            "name": name,
            "mana_value": mana_value,
            "colors": [],
            "color_identity": [],
            "type_line": type_line,
            "oracle_text": text,
        }
    )


def test_artifact_permanent_is_an_enabler_but_a_text_mention_is_not():
    relic = analyze_artifact(_analysis("Relic", 1, "Artifact", "{T}: Add {C}."))
    answer = analyze_artifact(
        _analysis("Shatter", 2, "Instant", "Destroy target artifact.")
    )

    assert relic.enabler
    assert relic.immediate_artifacts == 1
    assert not answer.enabler
    assert not answer.payoff


def test_immediate_investigate_counts_the_card_and_clue():
    analysis = _analysis(
        "Geardrake",
        2,
        "Artifact Creature",
        "Flying\nWhen this creature enters, investigate. "
        "(Create a Clue token. It's an artifact with "
        "\"{2}, Sacrifice this token: Draw a card.\")",
    )
    signals = analyze_artifact(analysis)

    assert signals.enabler
    assert signals.immediate_artifacts == 2
    assert "artifact_immediate_2" in artifact_roles(analysis)


def test_death_treasure_is_conditional_not_an_immediate_enabler():
    signals = analyze_artifact(
        _analysis(
            "Requisitioner",
            2,
            "Creature",
            "When this creature dies, create a Treasure token.",
        )
    )

    assert not signals.enabler
    assert signals.immediate_artifacts == 0
    assert signals.conditional_artifacts == 1
    assert "artifact_producer" in artifact_roles(
        _analysis(
            "Requisitioner",
            2,
            "Creature",
            "When this creature dies, create a Treasure token.",
        )
    )


def test_repeatable_producer_and_artifactfall_are_engines():
    saheeli = analyze_artifact(
        _analysis(
            "Saheeli",
            3,
            "Legendary Planeswalker",
            "Whenever you cast a noncreature spell, create a 1/1 colorless "
            "Servo artifact creature token.",
        )
    )
    payoff = analyze_artifact(
        _analysis(
            "Payoff",
            2,
            "Creature",
            "Whenever an artifact enters, draw a card.",
        )
    )

    assert saheeli.engine
    assert saheeli.repeatable_artifacts == 1
    assert not saheeli.enabler
    assert payoff.payoff
    assert payoff.engine


def test_card_name_improvised_does_not_satisfy_improvise_mechanic():
    signals = analyze_artifact(
        _analysis(
            "Improvised Weaponry",
            3,
            "Sorcery",
            "Improvised Weaponry deals 2 damage to any target. "
            "Create a Treasure token.",
        )
    )

    assert signals.enabler
    assert signals.immediate_artifacts == 1
    assert not signals.payoff
    assert not signals.engine


def test_named_only_scaling_is_not_a_general_artifact_payoff():
    signals = analyze_artifact(
        _analysis(
            "Powerstone Shard",
            3,
            "Artifact",
            "{T}: Add {C} for each artifact you control named Powerstone Shard.",
        )
    )

    assert signals.enabler
    assert not signals.payoff
    assert not signals.engine


def test_alternative_food_outputs_use_the_guaranteed_minimum():
    signals = analyze_artifact(
        _analysis(
            "Oven",
            1,
            "Artifact",
            "{T}, Sacrifice a creature: Create a Food token. If the sacrificed "
            "creature's toughness was 4 or greater, create two Food tokens instead.",
        )
    )

    assert signals.repeatable_artifacts == 1


def test_dice_table_inherits_the_activated_self_sacrifice_gate():
    signals = analyze_artifact(
        _analysis(
            "Pit Trap",
            1,
            "Artifact",
            "{5}, {T}, Sacrifice this artifact: Choose target creature, then roll a d20.\n"
            "1—9 | This artifact deals 5 damage to that creature.\n"
            "10—20 | This artifact deals 5 damage to that creature. Create a Treasure token.",
        )
    )

    assert signals.immediate_artifacts == 1
    assert signals.conditional_artifacts == 1
    assert signals.repeatable_artifacts == 0


def test_transformed_artifact_back_face_is_not_a_cast_artifact_permanent():
    signals = analyze_artifact(
        _analysis(
            "Invasion // Vehicle",
            2,
            "Battle — Siege // Legendary Artifact — Vehicle",
            "When this Siege enters, create a 1/1 colorless Thopter artifact "
            "creature token. // Flying",
        )
    )

    assert not signals.artifact_card
    assert signals.immediate_artifacts == 1
