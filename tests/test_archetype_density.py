from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.calibrated_strategies import (
    ARTIFACT_PROFILE,
    MILL_PROFILE,
    SHRINE_PROFILE,
    _mill_eligible,
    _shrine_eligible,
)
from thun_deckbuilder.knowledge_base import CardKnowledge


def _knowledge(
    name: str,
    mana_value: float,
    colors: list[str],
    type_line: str,
    oracle_text: str,
    roles: set[str],
) -> CardKnowledge:
    card = {
        "name": name,
        "mana_value": mana_value,
        "colors": colors,
        "color_identity": colors,
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    return CardKnowledge(
        card=card,
        analysis=analyze_card(card),
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def test_calibrated_profiles_do_not_force_generic_support():
    for profile in (ARTIFACT_PROFILE, SHRINE_PROFILE, MILL_PROFILE):
        assert all(target.minimum == 0 for target in profile.role_targets)


def test_shrine_allows_core_and_cheap_support_but_rejects_slow_filler():
    shrine = _knowledge(
        "Core Shrine", 3, ["G"], "Legendary Enchantment — Shrine",
        "At the beginning of your upkeep, gain 1 life.", set(),
    )
    cheap_fixing = _knowledge(
        "Fixing", 2, ["G"], "Artifact",
        "Add one mana of any color.", {"ramp"},
    )
    slow_draw = _knowledge(
        "Slow Draw", 5, ["U"], "Sorcery",
        "Draw three cards.", {"card_draw"},
    )

    colors = ("W", "U", "B", "R", "G")
    assert _shrine_eligible(shrine, colors)
    assert _shrine_eligible(cheap_fixing, colors)
    assert not _shrine_eligible(slow_draw, colors)


def test_mill_allows_core_and_compact_interaction_but_rejects_slow_control():
    mill = _knowledge(
        "Mind Cut", 2, ["U"], "Sorcery",
        "Target opponent mills 6 cards.", set(),
    )
    cheap_removal = _knowledge(
        "Compact Answer", 2, ["B"], "Instant",
        "Destroy target creature.", {"removal"},
    )
    slow_removal = _knowledge(
        "Slow Answer", 5, ["B"], "Sorcery",
        "Destroy target creature.", {"removal"},
    )

    colors = ("U", "B")
    assert _mill_eligible(mill, colors)
    assert _mill_eligible(cheap_removal, colors)
    assert not _mill_eligible(slow_removal, colors)
