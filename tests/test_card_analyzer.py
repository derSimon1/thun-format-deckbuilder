from thun_deckbuilder.card_analyzer import (
    analyze_card,
    detect_features,
)


def test_analyzes_creature():
    card = {
        "name": "Test Creature",
        "mana_value": 2,
        "colors": "R",
        "color_identity": "R",
        "type_line": "Creature — Goblin",
        "oracle_text": "Haste",
        "power": "2",
        "toughness": "1",
    }

    result = analyze_card(card)

    assert result.name == "Test Creature"
    assert result.mana_value == 2
    assert result.colors == ("R",)
    assert result.is_creature
    assert not result.is_land
    assert result.power == 2
    assert result.toughness == 1


def test_analyzes_legendary_enchantment_creature():
    card = {
        "name": "Test Shrine",
        "mana_value": 4,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": (
            "Legendary Enchantment Creature — Shrine"
        ),
        "oracle_text": "At the beginning of your end step...",
        "power": "1",
        "toughness": "3",
    }

    result = analyze_card(card)

    assert result.is_legendary
    assert result.is_enchantment
    assert result.is_creature


def test_analyzes_land():
    card = {
        "name": "Test Land",
        "mana_value": 0,
        "colors": [],
        "color_identity": [],
        "type_line": "Basic Land — Forest",
        "oracle_text": "",
    }

    result = analyze_card(card)

    assert result.is_land
    assert not result.is_creature
    assert result.colors == ()


def test_handles_variable_power():
    card = {
        "name": "Variable Creature",
        "mana_value": 3,
        "type_line": "Creature — Elemental",
        "power": "*",
        "toughness": "*",
    }

    result = analyze_card(card)

    assert result.power is None
    assert result.toughness is None


def test_accepts_database_color_strings():
    card = {
        "name": "Multicolor Card",
        "mana_value": 3,
        "colors": "R,W",
        "color_identity": "W,R",
        "type_line": "Instant",
    }

    result = analyze_card(card)

    assert result.colors == ("R", "W")
    assert result.color_identity == ("R", "W")
    assert result.is_instant

    from thun_deckbuilder.card_analyzer import detect_features
def test_detect_damage():

    features = detect_features(
        "Lightning Strike deals 3 damage to any target."
    )

    assert "damage" in features

def test_detect_draw():

    features = detect_features(
        "Draw two cards."
    )

    assert "draw" in features

def test_detect_token():

    features = detect_features(
        "Create a 1/1 white Human creature token."
    )

    assert "token" in features

def test_detect_mana():

    features = detect_features(
        "{T}: Add {G}."
    )

    assert "mana" in features

def test_detect_search():

    features = detect_features(
        "Search your library for a basic land card."
    )

    assert "search_library" in features
    
def test_analyze_card_includes_features():
    card = {
        "name": "Test Bolt",
        "mana_value": 2,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Instant",
        "oracle_text": "Test Bolt deals 3 damage to any target.",
    }

    analysis = analyze_card(card)

    assert "damage" in analysis.features
    assert isinstance(analysis.features, frozenset)