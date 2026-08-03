from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.token_production import (
    analyze_token_production,
    token_production_roles,
)


def card(name: str, text: str, *, type_line="Enchantment"):
    return analyze_card(
        {
            "name": name,
            "mana_value": 2,
            "colors": ["W"],
            "color_identity": ["W"],
            "type_line": type_line,
            "oracle_text": text,
        }
    )


def test_immediate_two_token_spell_has_exact_minimum_output():
    profile = analyze_token_production(
        card(
            "Raise",
            "Create two 1/1 white Soldier creature tokens.",
            type_line="Sorcery",
        )
    )
    assert profile.mode == "immediate"
    assert profile.minimum_output == 2
    assert not profile.variable_output
    assert set(token_production_roles(card(
        "Raise",
        "Create two 1/1 white Soldier creature tokens.",
        type_line="Sorcery",
    ))) == {"token_output_2", "token_production_immediate"}


def test_named_self_death_trigger_is_not_immediate_output():
    profile = analyze_token_production(
        card(
            "Garrison Cat",
            "When Garrison Cat dies, create a 1/1 white Human Soldier creature token.",
            type_line="Creature — Cat",
        )
    )
    assert profile.mode == "death"
    assert profile.delayed_by_death
    assert profile.minimum_output == 1


def test_target_dependent_output_is_conditional():
    profile = analyze_token_production(
        card(
            "Replacement",
            "Exile target creature. Its controller creates a 1/1 white Rabbit creature token.",
            type_line="Instant",
        )
    )
    assert profile.mode == "conditional"


def test_variable_for_each_output_is_conditional_and_conservative():
    profile = analyze_token_production(
        card(
            "Chaplain",
            "When Chaplain enters, create a 1/1 white Bird creature token with flying for each creature you control with defender.",
            type_line="Creature — Cleric",
        )
    )
    assert profile.mode == "conditional"
    assert profile.variable_output
    assert profile.minimum_output == 1


def test_unconditional_end_step_engine_is_repeatable():
    profile = analyze_token_production(
        card(
            "Engine",
            "At the beginning of your end step, create a 1/1 white Soldier creature token.",
        )
    )
    assert profile.mode == "repeatable"
    assert profile.repeatable


def test_whenever_trigger_is_not_assumed_to_fire_in_solitaire():
    profile = analyze_token_production(
        card(
            "Cycling Engine",
            "Whenever you cycle another card, create a 1/1 white Human Soldier creature token.",
            type_line="Creature — Human",
        )
    )
    assert profile.repeatable
    assert profile.mode == "conditional"
