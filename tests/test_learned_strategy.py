from types import SimpleNamespace

from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.learned_strategy import (
    LearnedArchetypeStrategy,
    LearnedStrategyConfig,
    profile_from_learning,
)
from thun_deckbuilder.meta_analyzer import LearnedArchetypeProfile, LearnedCoreCard


def card(name, *, mv, colors=("R",), roles=(), type_line="Instant"):
    raw = {
        "name": name,
        "mana_value": mv,
        "mana_cost": "{R}" if colors else "{1}",
        "colors": list(colors),
        "color_identity": list(colors),
        "type_line": type_line,
        "oracle_text": "",
    }
    return CardKnowledge(
        card=raw,
        analysis=analyze_card(raw),
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def learned_profile():
    return LearnedArchetypeProfile(
        deck_count=4,
        colors=("R",),
        average_lands=20.4,
        average_mana_value=1.8,
        curve=((1, 12.0), (2, 18.0), (3, 8.0), (4, 2.0)),
        role_targets=(("burn", 18.0), ("aggro_creature", 12.0)),
        core_cards=(LearnedCoreCard("Core Bolt", 1.0, 3.0),),
        unresolved_cards=(),
    )


def test_profile_from_learning_rounds_land_count_and_roles():
    profile = profile_from_learning(learned_profile(), name="Learned Red")
    assert profile.lands == 20
    assert profile.name == "Learned Red"
    roles = {item.role: item for item in profile.role_targets}
    assert roles["burn"].target == 18
    assert roles["burn"].minimum == 11


def test_learned_strategy_builds_complete_legal_deck_and_prioritizes_core():
    cards = (
        card("Core Bolt", mv=1, roles=("burn",)),
        card("Replacement Bolt", mv=1, roles=("burn",)),
        card("Other Bolt", mv=2, roles=("burn",)),
        card("Fast Creature", mv=1, roles=("aggro_creature",), type_line="Creature"),
        card("Two Drop", mv=2, roles=("aggro_creature",), type_line="Creature"),
        *(card(f"Legal Filler {index}", mv=2 + index % 2, roles=("burn",)) for index in range(12)),
        card("Off Color", mv=1, colors=("U",), roles=("burn",)),
    )
    strategy = LearnedArchetypeStrategy(
        LearnedStrategyConfig(
            name="Learned Red",
            profile=learned_profile(),
            replacement_names=("Replacement Bolt",),
        )
    )
    deck = strategy.generate(SimpleNamespace(cards=cards))

    assert sum(entry.quantity for entry in deck.mainboard) + deck.lands == 60
    assert all(entry.quantity <= 3 for entry in deck.mainboard)
    names = {entry.name for entry in deck.mainboard}
    assert "Core Bolt" in names
    assert "Replacement Bolt" in names
    assert "Off Color" not in names
