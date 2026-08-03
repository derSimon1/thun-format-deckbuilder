from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.mill_signals import analyze_mill


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
