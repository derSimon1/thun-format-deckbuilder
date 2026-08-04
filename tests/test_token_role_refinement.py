from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.token_generator import (
    _composition_candidates,
    _is_reasonable_token_card,
    _with_precise_token_roles,
)


def knowledge(
    name: str,
    text: str,
    roles: tuple[str, ...],
    *,
    type_line="Artifact",
    mana_value=2,
    synergies: tuple[str, ...] = (),
):
    raw = {
        "name": name,
        "mana_value": mana_value,
        "mana_cost": "{1}{W}",
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": type_line,
        "oracle_text": text,
    }
    return CardKnowledge(
        card=raw,
        analysis=analyze_card(raw),
        roles=frozenset(roles),
        synergies=frozenset(synergies),
    )


def test_food_only_card_loses_broad_token_maker_role_and_is_not_eligible():
    refined = _with_precise_token_roles(
        knowledge("Food", "Create a Food token.", ("token_maker",))
    )
    assert "token_maker" not in refined.roles
    assert "token_creature_maker" not in refined.roles
    assert not _is_reasonable_token_card(refined)


def test_immediate_multi_token_card_gains_reliable_go_wide_roles():
    refined = _with_precise_token_roles(
        knowledge(
            "Soldiers",
            "Create two 1/1 white Soldier creature tokens.",
            ("token_maker",),
            type_line="Sorcery",
        )
    )
    assert {
        "token_maker",
        "token_creature_maker",
        "token_immediate_maker",
        "token_multi_maker",
        "token_output_2",
        "token_production_immediate",
    }.issubset(refined.roles)
    assert _is_reasonable_token_card(refined)


def test_transform_gated_back_face_loses_broad_token_and_anthem_roles():
    refined = _with_precise_token_roles(
        knowledge(
            "Front // Back",
            "Craft with artifact {5}{W}{W}. Return this card transformed. // "
            "When this artifact enters, create two 1/1 creature tokens. "
            "Creatures you control get +1/+1.",
            ("token_maker", "token_payoff", "anthem"),
            type_line="Artifact // Artifact",
        )
    )

    assert "token_maker" not in refined.roles
    assert "token_payoff" not in refined.roles
    assert "anthem" not in refined.roles
    assert not _is_reasonable_token_card(refined)


def test_activated_maker_is_not_an_automatic_or_immediate_maker():
    refined = _with_precise_token_roles(
        knowledge(
            "Whirlermaker",
            "{4}, {T}: Create a 1/1 colorless Thopter artifact creature token with flying.",
            ("token_maker",),
            type_line="Artifact",
            mana_value=3,
        )
    )
    assert "token_creature_maker" in refined.roles
    assert "token_production_activated" in refined.roles
    assert "token_repeatable_maker" not in refined.roles
    assert "token_immediate_maker" not in refined.roles
    assert "token_multi_maker" not in refined.roles


def test_automatic_end_step_engine_gets_repeatable_role_only():
    refined = _with_precise_token_roles(
        knowledge(
            "Call",
            "At the beginning of your end step, create a 1/1 white Soldier creature token.",
            ("token_maker",),
            type_line="Enchantment",
            mana_value=3,
        )
    )
    assert "token_repeatable_maker" in refined.roles
    assert "token_immediate_maker" not in refined.roles


def test_one_shot_sacrifice_loses_outlet_role():
    refined = _with_precise_token_roles(
        knowledge(
            "One Shot",
            "As an additional cost to cast this spell, sacrifice a creature. Draw two cards.",
            ("sacrifice", "card_draw"),
            type_line="Sorcery",
            synergies=("sacrifice_outlet",),
        )
    )
    assert "sacrifice" not in refined.roles
    assert "sacrifice_outlet" not in refined.roles
    assert "cast_additional_creature_sacrifice_1" in refined.roles
    assert "sacrifice_outlet" not in refined.synergies


def test_real_outlet_and_death_payoff_receive_precise_roles():
    outlet = _with_precise_token_roles(
        knowledge(
            "Outlet",
            "Sacrifice another creature: Scry 1.",
            ("sacrifice",),
            type_line="Creature — Cleric",
            synergies=("sacrifice_outlet",),
        )
    )
    payoff = _with_precise_token_roles(
        knowledge(
            "Drain",
            "Whenever another creature dies, each opponent loses 1 life and you gain 1 life.",
            (),
            type_line="Creature — Cleric",
        )
    )
    assert {"sacrifice", "sacrifice_outlet"}.issubset(outlet.roles)
    assert "sacrifice_outlet" in outlet.synergies
    assert {"death_payoff", "drain_payoff", "token_payoff"}.issubset(
        payoff.roles
    )
    assert _is_reasonable_token_card(outlet)
    assert _is_reasonable_token_card(payoff)


def test_neutral_fillers_are_excluded_when_plan_capacity_is_sufficient():
    maker = _with_precise_token_roles(
        knowledge(
            "Maker",
            "Create a 1/1 white Soldier creature token.",
            ("token_maker",),
            type_line="Sorcery",
        )
    )
    filler = _with_precise_token_roles(
        knowledge(
            "Vanilla",
            "Vigilance.",
            (),
            type_line="Creature — Soldier",
        )
    )
    selected = _composition_candidates(
        (maker, filler),
        (maker,),
        spell_slots=3,
        max_copies=3,
    )
    assert selected == (maker,)


def test_neutral_fillers_are_added_only_for_a_real_sparse_pool_gap():
    maker = _with_precise_token_roles(
        knowledge(
            "Maker",
            "Create a 1/1 white Soldier creature token.",
            ("token_maker",),
            type_line="Sorcery",
        )
    )
    filler = _with_precise_token_roles(
        knowledge(
            "Vanilla",
            "Vigilance.",
            (),
            type_line="Creature — Soldier",
        )
    )
    selected = _composition_candidates(
        (maker, filler),
        (maker,),
        spell_slots=4,
        max_copies=3,
    )
    assert selected == (maker, filler)
