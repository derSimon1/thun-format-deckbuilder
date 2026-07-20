from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_roles import detect_roles


def test_damage_card_is_burn():
    card = {
        "name": "Test Bolt",
        "mana_value": 2,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Instant",
        "oracle_text": "Test Bolt deals 3 damage to any target.",
    }

    analysis = analyze_card(card)
    roles = detect_roles(analysis)

    assert "burn" in roles


def test_draw_card_has_card_draw_role():
    card = {
        "name": "Test Insight",
        "mana_value": 3,
        "colors": ["U"],
        "color_identity": ["U"],
        "type_line": "Sorcery",
        "oracle_text": "Draw two cards.",
    }

    analysis = analyze_card(card)
    roles = detect_roles(analysis)

    assert "card_draw" in roles


def test_mana_card_has_ramp_role():
    card = {
        "name": "Test Druid",
        "mana_value": 1,
        "colors": ["G"],
        "color_identity": ["G"],
        "type_line": "Creature — Elf Druid",
        "oracle_text": "{T}: Add {G}.",
        "power": "1",
        "toughness": "1",
    }

    analysis = analyze_card(card)
    roles = detect_roles(analysis)

    assert "ramp" in roles


def test_token_card_has_token_maker_role():
    card = {
        "name": "Test Recruiter",
        "mana_value": 2,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Creature — Human Soldier",
        "oracle_text": "Create a 1/1 white Human creature token.",
        "power": "2",
        "toughness": "2",
    }

    analysis = analyze_card(card)
    roles = detect_roles(analysis)

    assert "token_maker" in roles


def test_destroy_card_has_removal_role():
    card = {
        "name": "Test Removal",
        "mana_value": 3,
        "colors": ["B"],
        "color_identity": ["B"],
        "type_line": "Instant",
        "oracle_text": "Destroy target creature.",
    }

    analysis = analyze_card(card)
    roles = detect_roles(analysis)

    assert "removal" in roles

def test_detects_token_payoff_and_anthem():
    card = {
        "name": "Test Anthem",
        "mana_value": 2,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Enchantment",
        "oracle_text": "Creature tokens you control get +1/+1.",
    }
    roles = detect_roles(analyze_card(card))
    assert "anthem" in roles
    assert "token_payoff" in roles


def test_detects_early_creature_as_aggro_creature():
    card = {
        "name": "Test Aggro",
        "mana_value": 1,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Creature — Goblin",
        "oracle_text": "Haste",
    }
    assert "aggro_creature" in detect_roles(analyze_card(card))
