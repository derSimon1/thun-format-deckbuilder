from types import SimpleNamespace

from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.meta_analyzer import learn_archetype_profile
from thun_deckbuilder.moxfield_import import parse_moxfield_text


def knowledge(name, *, mv, type_line, colors=(), text="", roles=()):
    card = {
        "name": name,
        "mana_value": mv,
        "mana_cost": "",
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": text,
    }
    return CardKnowledge(
        card=card,
        analysis=analyze_card(card),
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def test_moxfield_import_parses_sections_and_set_suffixes():
    deck = parse_moxfield_text(
        """
        4 Monastery Swiftspear (BRO) 144
        4 Lightning Strike

        Sideboard
        3 Lithomantic Barrage (MOM) 152
        """
    )

    assert deck.mainboard_size == 8
    assert [(card.name, card.quantity) for card in deck.mainboard] == [
        ("Monastery Swiftspear", 4),
        ("Lightning Strike", 4),
    ]
    assert deck.sideboard[0].name == "Lithomantic Barrage"


def test_meta_analyzer_learns_curve_roles_colors_and_core_cards():
    cards = (
        knowledge("Mountain", mv=0, type_line="Basic Land — Mountain"),
        knowledge(
            "Monastery Swiftspear",
            mv=1,
            type_line="Creature — Human Monk",
            colors=("R",),
            roles=("aggro_creature",),
        ),
        knowledge(
            "Lightning Strike",
            mv=2,
            type_line="Instant",
            colors=("R",),
            roles=("burn",),
        ),
        knowledge(
            "Play with Fire",
            mv=1,
            type_line="Instant",
            colors=("R",),
            roles=("burn",),
        ),
    )
    knowledge_base = SimpleNamespace(cards=cards)
    decks = (
        parse_moxfield_text(
            "20 Mountain\n4 Monastery Swiftspear\n4 Lightning Strike\n4 Play with Fire"
        ),
        parse_moxfield_text(
            "19 Mountain\n4 Monastery Swiftspear\n4 Lightning Strike\n2 Play with Fire"
        ),
    )

    profile = learn_archetype_profile(decks, knowledge_base)

    assert profile.deck_count == 2
    assert profile.colors == ("R",)
    assert profile.average_lands == 19.5
    assert dict(profile.curve)[1] == 7.0
    assert dict(profile.curve)[2] == 4.0
    assert dict(profile.role_targets)["burn"] == 7.0
    assert [card.name for card in profile.core_cards] == [
        "Lightning Strike",
        "Monastery Swiftspear",
        "Play with Fire",
    ]


def test_meta_analyzer_reports_unknown_cards_without_failing():
    knowledge_base = SimpleNamespace(
        cards=(knowledge("Island", mv=0, type_line="Basic Land — Island"),)
    )
    profile = learn_archetype_profile(
        (parse_moxfield_text("20 Island\n4 Unknown Meta Card"),),
        knowledge_base,
    )

    assert profile.unresolved_cards == ("Unknown Meta Card",)
