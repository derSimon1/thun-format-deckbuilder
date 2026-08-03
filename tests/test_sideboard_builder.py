from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.control_strategy import ControlStrategy
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.sideboard_builder import SideboardBuilder


def k(name, text, colors=("R",), roles=()):
    card = {
        "name": name,
        "mana_value": 2,
        "mana_cost": "{1}{R}",
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": "Instant",
        "oracle_text": text,
    }
    return CardKnowledge(
        card,
        analyze_card(card),
        frozenset(roles),
        frozenset(),
    )


def test_sideboard_selects_relevant_on_color_cards():
    cards = (
        k("Smash", "Destroy target artifact."),
        k("No Healing", "Players can't gain life this turn."),
        k("Blue Answer", "Destroy target artifact.", colors=("U",)),
    )
    result = SideboardBuilder().build(
        cards,
        GeneratedDeck((), 24),
        archetype="burn",
        colors=("R",),
        size=6,
    )
    assert {entry.name for entry in result} == {"Smash", "No Healing"}
    assert sum(entry.quantity for entry in result) == 6
    assert all(
        any(role.startswith("sideboard_") for role in entry.roles)
        for entry in result
    )


def test_sideboard_encodes_graveyard_hate_as_machine_readable_role():
    result = SideboardBuilder().build(
        (k("Crypt", "Exile all cards from target player's graveyard."),),
        GeneratedDeck((), 24),
        archetype="burn",
        colors=("R",),
        size=3,
    )
    assert result[0].reasons == ("Sideboard: graveyard hate",)
    assert "sideboard_graveyard_hate" in result[0].roles


def test_specific_phrase_prevents_generic_role_double_classification():
    ControlStrategy()
    graveyard_card_with_broad_role = k(
        "Graveyard Device",
        "Exile all cards from target player's graveyard.",
        colors=(),
        roles=("removal",),
    )

    result = SideboardBuilder().build(
        (graveyard_card_with_broad_role,),
        GeneratedDeck((), 25),
        archetype="control",
        colors=("U", "B"),
        size=3,
    )

    assert result[0].reasons == ("Sideboard: graveyard hate",)
    assert "sideboard_graveyard_hate" in result[0].roles
    assert "sideboard_anti_aggro_removal" not in result[0].roles


def test_sideboard_respects_combined_copy_limit():
    main = (
        DeckEntry(
            "Smash",
            2,
            ManaCost("{1}{R}", 1, "R"),
            2,
            "Instant",
        ),
    )
    result = SideboardBuilder().build(
        (k("Smash", "Destroy target artifact."),),
        GeneratedDeck(main, 24),
        archetype="burn",
        colors=("R",),
        max_copies=3,
    )
    assert result[0].quantity == 1


def test_sideboard_excludes_off_color_cards():
    result = SideboardBuilder().build(
        (k("Blue", "Destroy target artifact.", colors=("U",)),),
        GeneratedDeck((), 24),
        archetype="burn",
        colors=("R",),
    )
    assert result == ()


def test_token_sideboard_prioritizes_burn_stabilization():
    cards = (
        k("Life Cleric", "When this enters, you gain 2 life.", colors=("W",)),
        k("Disenchant", "Destroy target artifact or enchantment.", colors=("W",)),
    )
    result = SideboardBuilder().build(
        cards,
        GeneratedDeck((), 24),
        archetype="tokens",
        colors=("W",),
        size=3,
    )
    assert result[0].name == "Life Cleric"
    assert result[0].reasons == ("Sideboard: protection",)
    assert "sideboard_protection" in result[0].roles
