from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.card_synergies import detect_synergies
from thun_deckbuilder.card_translator import suggest_replacements
from thun_deckbuilder.knowledge_base import CardKnowledge


def knowledge(name, mv, colors, type_line, text):
    card = {
        "name": name,
        "mana_value": mv,
        "mana_cost": "",
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": text,
    }
    analysis = analyze_card(card)
    return CardKnowledge(
        card=card,
        analysis=analysis,
        roles=detect_roles(analysis),
        synergies=detect_synergies(analysis),
    )


def test_replacement_prefers_shared_function_over_generic_card():
    source = knowledge(
        "Premium Burn", 1, "R", "Instant",
        "Premium Burn deals 3 damage to any target.",
    )
    functional = knowledge(
        "Legal Bolt", 2, "R", "Instant",
        "Legal Bolt deals 3 damage to any target.",
    )
    generic = knowledge(
        "Cheap Creature", 1, "R", "Creature — Goblin",
        "Haste",
    )

    result = suggest_replacements(source, (generic, functional), colors=("R",))

    assert result.candidates[0].replacement_name == "Legal Bolt"
    assert "gleiche Rolle" in " ".join(result.candidates[0].reasons)


def test_replacement_respects_archetype_colors():
    source = knowledge(
        "Blue Draw", 2, "U", "Instant",
        "Draw two cards.",
    )
    legal_blue = knowledge("Blue Option", 2, "U", "Instant", "Draw two cards.")
    illegal_green = knowledge("Green Option", 2, "G", "Instant", "Draw two cards.")

    result = suggest_replacements(
        source,
        (illegal_green, legal_blue),
        colors=("U",),
    )

    assert [item.replacement_name for item in result.candidates] == ["Blue Option"]


def test_replacement_prefers_similar_mana_value_and_type_on_equal_roles():
    source = knowledge(
        "Source Removal", 2, "B", "Instant",
        "Destroy target creature.",
    )
    close = knowledge(
        "Close Removal", 2, "B", "Instant",
        "Destroy target creature.",
    )
    slow = knowledge(
        "Slow Removal", 5, "B", "Sorcery",
        "Destroy target creature.",
    )

    result = suggest_replacements(source, (slow, close), colors=("B",))

    assert result.candidates[0].replacement_name == "Close Removal"


def test_replacement_rejects_unrelated_cards():
    source = knowledge(
        "Artifact Payoff", 2, "U", "Creature",
        "Whenever an artifact enters, draw a card.",
    )
    unrelated = knowledge(
        "Vanilla Creature", 2, "U", "Creature",
        "Vigilance",
    )

    result = suggest_replacements(source, (unrelated,), colors=("U",))

    assert result.candidates == ()


def test_limit_is_enforced_and_validated():
    source = knowledge("Draw Source", 2, "U", "Instant", "Draw two cards.")
    options = tuple(
        knowledge(f"Draw {index}", 2, "U", "Instant", "Draw two cards.")
        for index in range(4)
    )
    result = suggest_replacements(source, options, colors=("U",), limit=2)
    assert len(result.candidates) == 2

    try:
        suggest_replacements(source, options, colors=("U",), limit=0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
