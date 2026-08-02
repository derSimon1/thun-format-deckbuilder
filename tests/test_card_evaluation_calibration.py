from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_evaluation import CardEvaluationEngine


def evaluate(**overrides):
    card = {
        "name": "Calibration Card",
        "mana_value": 2,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Sorcery",
        "oracle_text": "",
    }
    card.update(overrides)
    return CardEvaluationEngine().evaluate(analyze_card(card))


def component(result, category):
    return sum(item.value for item in result.components if item.category == category)


def test_exile_removal_scores_above_destroy_removal() -> None:
    exile = evaluate(type_line="Instant", oracle_text="Exile target creature.")
    destroy = evaluate(type_line="Instant", oracle_text="Destroy target creature.")
    assert component(exile, "interaction") > component(destroy, "interaction")


def test_cheap_removal_scores_above_expensive_removal() -> None:
    cheap = evaluate(mana_value=2, type_line="Instant", oracle_text="Destroy target creature.")
    expensive = evaluate(mana_value=5, type_line="Instant", oracle_text="Destroy target creature.")
    assert component(cheap, "interaction") > component(expensive, "interaction")


def test_damage_plus_creature_tap_receives_additional_tempo_value() -> None:
    plain_burn = evaluate(
        colors=["R"],
        color_identity=["R"],
        type_line="Instant",
        oracle_text="Plain Burn deals 3 damage to any target.",
    )
    vibrant_outburst = evaluate(
        name="Vibrant Outburst",
        colors=["U", "R"],
        color_identity=["U", "R"],
        type_line="Instant",
        oracle_text=(
            "Vibrant Outburst deals 3 damage to any target. "
            "Tap up to one target creature."
        ),
    )

    assert component(vibrant_outburst, "tempo") > 0
    assert vibrant_outburst.total > plain_burn.total


def test_cantrip_is_not_treated_as_true_card_advantage() -> None:
    cantrip = evaluate(type_line="Instant", oracle_text="Draw a card.")
    divination = evaluate(mana_value=3, colors=["U"], type_line="Sorcery", oracle_text="Draw two cards.")
    assert 0 < component(cantrip, "card_advantage") < component(divination, "card_advantage")


def test_looting_is_card_selection_not_card_advantage() -> None:
    result = evaluate(type_line="Sorcery", oracle_text="Draw a card, then discard a card.")
    assert component(result, "card_selection") > 0
    assert component(result, "card_advantage") == 0


def test_repeatable_draw_engine_receives_repeatable_value() -> None:
    result = evaluate(
        mana_value=3,
        type_line="Enchantment",
        oracle_text="At the beginning of your upkeep, draw a card.",
    )
    assert component(result, "repeatable_value") > 0


def test_etb_removal_creature_gets_immediate_value() -> None:
    result = evaluate(
        mana_value=4,
        type_line="Creature — Human",
        oracle_text="When this creature enters, exile target creature an opponent controls.",
        power="2",
        toughness="2",
    )
    assert component(result, "immediate_value") >= 1.5
    assert component(result, "interaction") > 0


def test_vanilla_below_rate_creature_is_penalized() -> None:
    result = evaluate(
        mana_value=4,
        type_line="Creature — Beast",
        oracle_text="",
        power="2",
        toughness="2",
    )
    assert component(result, "creature_rate") < 0
    assert component(result, "vanilla_penalty") < 0


def test_relevant_keywords_improve_creature_score() -> None:
    plain = evaluate(mana_value=3, type_line="Creature — Bird", oracle_text="", power="2", toughness="2")
    evasive = evaluate(mana_value=3, type_line="Creature — Bird", oracle_text="Flying, lifelink", power="2", toughness="2")
    assert evasive.total > plain.total
    assert component(evasive, "creature_keywords") > 0


def test_combat_trick_is_penalized_as_situational() -> None:
    result = evaluate(
        mana_value=1,
        type_line="Instant",
        oracle_text="Target creature you control gets +3/+3 until end of turn.",
    )
    assert component(result, "situational") < 0


def test_cantripping_combat_trick_is_penalized_less() -> None:
    plain = evaluate(
        mana_value=1,
        type_line="Instant",
        oracle_text="Target creature you control gets +2/+2 until end of turn.",
    )
    cantrip = evaluate(
        mana_value=1,
        type_line="Instant",
        oracle_text="Target creature you control gets +2/+2 until end of turn. Draw a card.",
    )
    assert component(cantrip, "situational") > component(plain, "situational")
    assert cantrip.total > plain.total


def test_repeated_token_source_scores_above_one_shot_single_token() -> None:
    one_shot = evaluate(mana_value=2, oracle_text="Create a 1/1 white Soldier creature token.")
    repeatable = evaluate(
        mana_value=2,
        type_line="Enchantment",
        oracle_text="At the beginning of your end step, create a 1/1 white Soldier creature token.",
    )
    assert repeatable.total > one_shot.total


def test_expensive_card_with_real_impact_avoids_full_low_impact_penalty() -> None:
    finisher = evaluate(
        mana_value=6,
        type_line="Creature — Dragon",
        oracle_text="Flying, haste. When this creature enters, it deals 4 damage to any target.",
        power="5",
        toughness="5",
    )
    blank = evaluate(mana_value=6, type_line="Creature — Beast", oracle_text="", power="5", toughness="5")
    assert finisher.total > blank.total
    assert component(finisher, "expensive_low_impact") >= component(blank, "expensive_low_impact")
