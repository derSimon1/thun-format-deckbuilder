from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.token_production import (
    analyze_token_production,
    build_token_production_capacity,
    token_production_roles,
)


def raw_card(
    name: str,
    text: str,
    *,
    type_line="Enchantment",
    colors=("W",),
    mana_value=2,
):
    return {
        "name": name,
        "mana_value": mana_value,
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": text,
    }


def card(name: str, text: str, *, type_line="Enchantment"):
    return analyze_card(raw_card(name, text, type_line=type_line))


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
    assert set(
        token_production_roles(
            card(
                "Raise",
                "Create two 1/1 white Soldier creature tokens.",
                type_line="Sorcery",
            )
        )
    ) == {"token_output_2", "token_production_immediate"}


def test_transform_gated_back_face_is_not_immediate_production():
    analysis = analyze_card(
        raw_card(
            "Front // Back",
            "Craft with artifact {5}{W}{W}. Return this card transformed. // "
            "When this artifact enters, create two 1/1 creature tokens.",
            type_line="Artifact // Artifact",
        )
    )

    profile = analyze_token_production(analysis)

    assert profile.mode == "none"
    assert token_production_roles(analysis) == ()


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
    assert not profile.activated


def test_activated_token_maker_is_not_an_automatic_repeatable_trigger():
    analysis = card(
        "Whirlermaker",
        "{4}, {T}: Create a 1/1 colorless Thopter artifact creature token with flying.",
        type_line="Artifact",
    )
    profile = analyze_token_production(analysis)
    assert profile.mode == "activated"
    assert profile.activated
    assert profile.activation_mana == 4
    assert not profile.repeatable
    assert set(token_production_roles(analysis)) == {
        "token_activation_mana_4",
        "token_output_1",
        "token_production_activated",
    }


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


def test_follow_up_reminder_sentence_inherits_attack_and_payment_condition():
    analysis = card(
        "Descendant",
        "Whenever this creature attacks, you may pay {1}{W}. If you do, it "
        "endures 1. (Put a +1/+1 counter on it or create a 1/1 white Spirit "
        "creature token.)",
        type_line="Creature — Spirit",
    )

    profile = analyze_token_production(analysis)

    assert profile.mode == "conditional"
    assert profile.conditional
    assert "token_production_immediate" not in token_production_roles(analysis)


def test_later_saga_chapter_is_delayed_without_read_ahead():
    profile = analyze_token_production(
        card(
            "Slow Saga",
            "I — Scry 1.\nII — Create a 1/1 white Bird creature token.",
            type_line="Enchantment — Saga",
        )
    )

    assert profile.mode == "conditional"


def test_read_ahead_can_make_a_later_saga_chapter_immediate():
    profile = analyze_token_production(
        card(
            "Read-Ahead Saga",
            "Read ahead (Choose a chapter and start with that many lore "
            "counters.)\nI — Scry 1.\nII — Create a 1/1 white Bird creature "
            "token.",
            type_line="Enchantment — Saga",
        )
    )

    assert profile.mode == "immediate"


def test_modal_bullet_inherits_landfall_trigger_but_plain_choice_does_not():
    landfall = analyze_token_production(
        card(
            "Retreat",
            "Landfall — Whenever a land you control enters, choose one —\n"
            "• Create a 1/1 white Ally creature token.\n"
            "• Creatures you control get +1/+1 until end of turn.",
        )
    )
    plain_choice = analyze_token_production(
        card(
            "Menu",
            "Choose one —\n• Create a 1/1 white Knight creature token.\n"
            "• You gain 4 life.",
            type_line="Instant",
        )
    )

    assert landfall.mode == "conditional"
    assert plain_choice.mode == "immediate"


def test_non_entry_when_trigger_is_conditional_but_self_entry_is_immediate():
    leaves = analyze_token_production(
        card(
            "Valor",
            "When enchanted creature leaves the battlefield, create a 1/1 "
            "white Spirit creature token.",
            type_line="Enchantment — Aura",
        )
    )
    enters = analyze_token_production(
        card(
            "Captain",
            "When this creature enters, create a 1/1 white Soldier creature "
            "token.",
            type_line="Creature — Human",
        )
    )

    assert leaves.mode == "conditional"
    assert enters.mode == "immediate"


def test_short_legend_name_and_token_rules_text_do_not_hide_immediate_etb():
    legendary = analyze_token_production(
        card(
            "Okoye, Leader",
            "When Okoye enters, create two 1/1 white Soldier creature tokens.",
            type_line="Legendary Creature — Human",
        )
    )
    rules_text = analyze_token_production(
        card(
            "Attendant",
            'When this creature enters, create a 1/1 blue Wizard creature token '
            'with "{1}, Sacrifice this token: Counter target noncreature spell."',
            type_line="Creature — Human",
        )
    )

    assert legendary.mode == "immediate"
    assert legendary.minimum_output == 2
    assert rules_text.mode == "immediate"


def test_capacity_groups_modes_and_filters_duplicates_off_color_and_lands():
    cards = (
        raw_card(
            "Raise",
            "Create two 1/1 white Soldier creature tokens.",
            type_line="Sorcery",
        ),
        raw_card(
            "Raise",
            "Create two 1/1 white Soldier creature tokens.",
            type_line="Sorcery",
        ),
        raw_card(
            "Engine",
            "At the beginning of your end step, create a 1/1 white Soldier creature token.",
        ),
        raw_card(
            "Whirlermaker",
            "{4}, {T}: Create a 1/1 colorless Thopter artifact creature token with flying.",
            type_line="Artifact",
        ),
        raw_card(
            "Death Cat",
            "When Death Cat dies, create a 1/1 white Soldier creature token.",
            type_line="Creature — Cat",
        ),
        raw_card(
            "Blue Maker",
            "Create a 1/1 blue Bird creature token.",
            colors=("U",),
        ),
        raw_card(
            "Token Land",
            "Create a 1/1 white Soldier creature token.",
            type_line="Land",
            mana_value=0,
        ),
    )

    capacity = build_token_production_capacity(cards)

    assert capacity["distinct_cards"] == 4
    assert capacity["distinct_by_mode"] == {
        "activated": 1,
        "death": 1,
        "immediate": 1,
        "repeatable": 1,
    }
    assert capacity["maximum_copies_by_mode"] == {
        "activated": 3,
        "death": 3,
        "immediate": 3,
        "repeatable": 3,
    }
    assert capacity["minimum_output_capacity_by_mode"]["immediate"] == 6
