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
        synergies=frozenset(),
    )


def test_food_only_card_loses_broad_token_maker_role_and_is_not_eligible():
    refined = _with_precise_token_roles(
        knowledge("Food", "Create a Food token.", ("token_maker",))
    )
    assert "token_maker" not in refined.roles
    assert "token_creature_maker" not in refined.roles
    assert not _is_reasonable_token_card(refined)


def test_creature_token_card_gains_package_and_production_roles():
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
        "token_output_2",
        "token_production_immediate",
    }.issubset(refined.roles)
    assert _is_reasonable_token_card(refined)


def test_one_shot_sacrifice_loses_outlet_role():
    refined = _with_precise_token_roles(
        knowledge(
            "One Shot",
            "As an additional cost to cast this spell, sacrifice a creature. Draw two cards.",
            ("sacrifice", "card_draw"),
            type_line="Sorcery",
        )
    )
    assert "sacrifice" not in refined.roles
    assert "sacrifice_outlet" not in refined.roles


def test_real_outlet_and_death_payoff_receive_precise_roles():
    outlet = _with_precise_token_roles(
        knowledge(
            "Outlet",
            "Sacrifice another creature: Scry 1.",
            ("sacrifice",),
            type_line="Creature — Cleric",
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
