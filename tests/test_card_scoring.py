from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import score_burn_card


def _burn_card(
    name: str,
    mana_value: float,
    type_line: str,
    oracle_text: str,
    power: str | None = None,
):
    card = {
        "name": name,
        "mana_value": mana_value,
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": type_line,
        "oracle_text": oracle_text,
    }
    if power is not None:
        card["power"] = power
    return analyze_card(card)


def test_score_contains_reasons():
    analysis = _burn_card(
        "Lightning Strike",
        2,
        "Instant",
        "Lightning Strike deals 3 damage to any target.",
    )

    result = score_burn_card(analysis)

    assert result.score > 0
    assert "Instant" in result.reasons
    assert "3 Schaden" in result.reasons


def test_face_burn_beats_creature_only_removal():
    face_burn = score_burn_card(
        _burn_card(
            "Flexible Strike",
            2,
            "Instant",
            "Flexible Strike deals 3 damage to any target.",
        )
    )
    creature_removal = score_burn_card(
        _burn_card(
            "Creature Strike",
            2,
            "Instant",
            "Creature Strike deals 3 damage to target creature.",
        )
    )

    assert face_burn.score > creature_removal.score
    assert "Nur Board-Interaktion" in creature_removal.reasons


def test_same_damage_prefers_lower_mana_value():
    cheap_burn = score_burn_card(
        _burn_card(
            "Cheap Burn",
            1,
            "Sorcery",
            "Cheap Burn deals 3 damage to target opponent.",
        )
    )
    expensive_burn = score_burn_card(
        _burn_card(
            "Expensive Burn",
            4,
            "Sorcery",
            "Expensive Burn deals 3 damage to target opponent.",
        )
    )

    assert cheap_burn.score > expensive_burn.score
    assert "Sehr effizienter Face-Burn" in cheap_burn.reasons
    assert "Hohe Manakosten" in expensive_burn.reasons


def test_conditional_burn_is_penalized():
    unconditional = score_burn_card(
        _burn_card(
            "Clean Burn",
            2,
            "Instant",
            "Clean Burn deals 3 damage to any target.",
        )
    )
    conditional = score_burn_card(
        _burn_card(
            "Conditional Burn",
            2,
            "Instant",
            (
                "Conditional Burn deals 3 damage to any target "
                "if you attacked this turn."
            ),
        )
    )

    assert unconditional.score > conditional.score
    assert (
        "Bedingter oder zusätzlicher Aufwand"
        in conditional.reasons
    )


def test_hasty_efficient_creature_gets_aggro_credit():
    result = score_burn_card(
        _burn_card(
            "Goblin Runner",
            1,
            "Creature — Goblin",
            "Haste",
            power="2",
        )
    )

    assert "Haste" in result.reasons
    assert "Sehr effiziente Aggro-Kreatur" in result.reasons