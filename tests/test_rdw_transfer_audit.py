from thun_deckbuilder.rdw_transfer_audit import assess_rdw_candidate, rank_candidates


def card(name, *, mv, type_line, text, power=None, identity=("R",)):
    return {
        "name": name,
        "mana_value": mv,
        "type_line": type_line,
        "oracle_text": text,
        "power": power,
        "color_identity": list(identity),
    }


def test_swiftspear_is_immediate_one_mana_spell_matter_threat():
    result = assess_rdw_candidate(card(
        "Monastery Swiftspear",
        mv=1,
        type_line="Creature — Human Monk",
        text="Haste\nProwess",
        power="1",
    ))
    assert result is not None
    assert "one_mana_threat" in result.functions
    assert "spell_matter_threat" in result.functions
    assert result.immediate


def test_death_damage_is_not_treated_as_immediate_burn():
    result = assess_rdw_candidate(card(
        "Death Scamp",
        mv=1,
        type_line="Creature — Phyrexian Goblin Warrior",
        text="When Death Scamp dies, it deals damage equal to its power to any target.",
        power="1",
    ))
    assert result is not None
    assert "face_burn" not in result.functions
    assert "death_trigger" in result.timing_caveats


def test_spell_triggered_damage_is_repeatable_reach_not_burn_spell():
    result = assess_rdw_candidate(card(
        "Firebrand Archer",
        mv=2,
        type_line="Creature — Human Archer",
        text="Whenever you cast a noncreature spell, Firebrand Archer deals 1 damage to each opponent.",
        power="2",
    ))
    assert result is not None
    assert "repeatable_reach" in result.functions
    assert "face_burn" not in result.functions


def test_utility_land_activation_is_explicit():
    result = assess_rdw_candidate(card(
        "Ramunap Ruins",
        mv=0,
        type_line="Land — Desert",
        text="{T}: Add {C}.\n{T}, Pay 1 life: Add {R}.\n{2}{R}{R}, {T}, Sacrifice a Desert: Ramunap Ruins deals 2 damage to each opponent.",
        identity=(),
    ))
    assert result is not None
    assert "utility_land" in result.functions
    assert "activated" in result.timing_caveats


def test_ranking_prefers_immediate_threat_over_death_only_threat():
    cards = [
        card("Immediate", mv=1, type_line="Creature", text="Haste", power="1"),
        card("Death Only", mv=1, type_line="Creature", text="When Death Only dies, it deals 1 damage to any target.", power="1"),
    ]
    ranked = rank_candidates(cards)
    assert ranked["one_mana_threat"][0].name == "Immediate"


def test_off_color_card_is_rejected():
    result = assess_rdw_candidate(card(
        "Blue Threat", mv=1, type_line="Creature", text="Prowess", power="1", identity=("U",)
    ))
    assert result is None
