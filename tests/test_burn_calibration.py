from thun_deckbuilder.burn_scoring import estimated_direct_damage, score_burn_card
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.deck_generator import _is_reasonable_burn_card, _score_for_composition
from thun_deckbuilder.knowledge_base import CardKnowledge


def analysis(
    text: str,
    *,
    mana_value: float = 2,
    type_line: str = "Instant",
    power: str | None = None,
    toughness: str | None = None,
):
    return analyze_card(
        {
            "name": "Test Card",
            "mana_value": mana_value,
            "mana_cost": "{1}{R}",
            "colors": ["R"],
            "color_identity": ["R"],
            "type_line": type_line,
            "oracle_text": text,
            "power": power,
            "toughness": toughness,
        }
    )


def knowledge(
    text: str,
    roles: tuple[str, ...],
    *,
    mana_value: float = 2,
    type_line: str = "Instant",
    power: str | None = None,
):
    card_analysis = analysis(
        text,
        mana_value=mana_value,
        type_line=type_line,
        power=power,
        toughness=power,
    )
    return CardKnowledge(
        card={"name": "Test Card", "mana_cost": "{1}{R}"},
        analysis=card_analysis,
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def test_estimates_written_and_numeric_damage():
    assert estimated_direct_damage("This spell deals three damage to any target.") == 3
    assert estimated_direct_damage("This spell deals 2 damage to target opponent.") == 2


def test_variable_damage_is_marked_as_scaling():
    assert estimated_direct_damage("This spell deals X damage to any target.") is None


def test_one_mana_three_damage_outscores_three_mana_two_damage():
    efficient = score_burn_card(
        analysis("This spell deals 3 damage to any target.", mana_value=1)
    )
    inefficient = score_burn_card(
        analysis("This spell deals 2 damage to any target.", mana_value=3)
    )
    assert efficient.score >= inefficient.score + 6


def test_face_damage_outscores_creature_only_removal():
    face = score_burn_card(
        analysis("This spell deals 3 damage to any target.", mana_value=2)
    )
    removal = score_burn_card(
        analysis("This spell deals 3 damage to target creature.", mana_value=2)
    )
    assert face.score > removal.score
    assert "Kann den Gegner direkt treffen" in face.reasons
    assert "Nur Board-Interaktion, kein Reach" in removal.reasons


def test_repeatable_face_damage_gets_bonus():
    repeatable = score_burn_card(
        analysis(
            "At the beginning of your upkeep, this enchantment deals 1 damage to each opponent.",
            mana_value=2,
            type_line="Enchantment",
        )
    )
    one_shot = score_burn_card(
        analysis("This spell deals 1 damage to target opponent.", mana_value=2)
    )
    assert repeatable.score > one_shot.score
    assert "Wiederholbarer Schaden" in repeatable.reasons


def test_creature_only_removal_is_not_main_deck_eligible():
    card = knowledge(
        "This spell deals 3 damage to target creature.",
        ("burn",),
        mana_value=2,
    )
    assert not _is_reasonable_burn_card(card)


def test_efficient_aggressive_creature_is_eligible():
    card = knowledge(
        "Haste",
        ("aggro_creature",),
        mana_value=1,
        type_line="Creature — Goblin",
        power="2",
    )
    assert _is_reasonable_burn_card(card)


def test_composition_prefers_reliable_reach():
    face = knowledge(
        "This spell deals 3 damage to any target.",
        ("burn",),
        mana_value=2,
    )
    conditional = knowledge(
        "If a creature died this turn, this spell deals 3 damage to target opponent.",
        ("burn",),
        mana_value=2,
    )
    face_score, _ = _score_for_composition(face)
    conditional_score, _ = _score_for_composition(conditional)
    assert face_score > conditional_score
