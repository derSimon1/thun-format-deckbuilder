from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.mill_signals import analyze_mill
from thun_deckbuilder.mill_signals import simulation_metadata_roles


def _analysis(name, mana_value, type_line, oracle_text):
    return analyze_card(
        {
            "name": name,
            "mana_value": mana_value,
            "colors": ["U"],
            "color_identity": ["U"],
            "type_line": type_line,
            "oracle_text": oracle_text,
        }
    )


def test_fixed_opponent_mill_is_a_source_but_not_automatically_an_engine():
    analysis = _analysis(
        "Mind Burst",
        2,
        "Sorcery",
        "Target opponent mills 8 cards.",
    )

    signals = analyze_mill(analysis)

    assert signals.source
    assert signals.fixed_cards == 8
    assert signals.immediate_cards == 8
    assert signals.repeatable_cards == 0
    assert signals.conditional_cards == 0
    assert not signals.engine


def test_repeatable_permanent_mill_is_an_engine():
    analysis = _analysis(
        "Archive Crab",
        1,
        "Creature — Crab",
        "Whenever a land enters under your control, target opponent mills 3 cards.",
    )

    signals = analyze_mill(analysis)
    roles = detect_roles(analysis)

    assert signals.source
    assert signals.engine
    assert signals.immediate_cards == 0
    assert signals.repeatable_cards == 3
    assert "mill_source" in roles
    assert "mill_engine" in roles


def test_self_mill_is_not_an_opponent_mill_source():
    analysis = _analysis(
        "Private Study",
        2,
        "Sorcery",
        "You mill five cards, then draw a card.",
    )

    signals = analyze_mill(analysis)
    roles = detect_roles(analysis)

    assert not signals.source
    assert "mill_source" not in roles


def test_library_to_their_graveyard_wording_is_supported():
    analysis = _analysis(
        "Memory Erosion",
        3,
        "Enchantment",
        "Whenever an opponent casts a spell, that player puts the top two cards "
        "of their library into their graveyard.",
    )

    signals = analyze_mill(analysis)

    assert signals.source
    assert signals.engine
    assert signals.fixed_cards == 2


def test_one_shot_permanent_and_adventure_are_not_mill_engines():
    enters = _analysis(
        "Wall of Memories",
        2,
        "Creature — Wall",
        "When this creature enters, target player mills four cards.",
    )
    adventure = _analysis(
        "Keeper // Deeper",
        1,
        "Creature // Sorcery — Adventure",
        " // Target player mills four cards.",
    )

    for analysis in (enters, adventure):
        signals = analyze_mill(analysis)
        assert signals.source
        assert not signals.engine
        assert signals.immediate_cards == 4
        assert signals.repeatable_cards == 0
        assert "mill_engine" not in detect_roles(analysis)


def test_reusable_activation_is_engine_but_self_sacrifice_is_not():
    millstone = _analysis(
        "Millstone",
        2,
        "Artifact",
        "{2}, {T}: Target player mills two cards.",
    )
    vessel = _analysis(
        "Memory Vessel",
        2,
        "Enchantment",
        "{U}, Sacrifice this enchantment: Target player mills three cards.",
    )

    assert analyze_mill(millstone).engine
    assert simulation_metadata_roles(millstone) == ("mill_repeatable_2",)
    assert not analyze_mill(vessel).engine
    assert analyze_mill(vessel).immediate_cards == 0
    assert analyze_mill(vessel).conditional_cards == 3
    assert simulation_metadata_roles(vessel) == ("mill_conditional_3",)


def test_multi_permanent_activation_is_not_intrinsic_engine_throughput():
    petitioners = _analysis(
        "Persistent Petitioners",
        2,
        "Creature — Human Advisor",
        (
            "{1}, {T}: Target player mills a card.\n"
            "Tap four untapped Advisors you control: "
            "Target player mills twelve cards."
        ),
    )

    signals = analyze_mill(petitioners)
    assert signals.engine
    assert signals.repeatable_cards == 1
    assert simulation_metadata_roles(petitioners) == (
        "mill_repeatable_1",
        "mill_conditional_12",
    )
