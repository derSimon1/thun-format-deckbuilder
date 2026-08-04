from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.control_signals import analyze_control


def _analysis(name: str, mana_value: int, type_line: str, text: str):
    return analyze_card(
        {
            "name": name,
            "mana_value": mana_value,
            "colors": ["U"],
            "color_identity": ["U"],
            "type_line": type_line,
            "oracle_text": text,
        }
    )


def test_reliable_answer_and_true_card_advantage_get_control_roles():
    answer = _analysis("Counter", 2, "Instant", "Counter target spell.")
    refill = _analysis("Refill", 3, "Sorcery", "Draw two cards.")

    assert analyze_control(answer).reliable_answer
    assert analyze_control(refill).card_advantage


def test_cycling_and_loot_are_selection_not_card_advantage():
    cycling = _analysis(
        "Censor",
        2,
        "Instant",
        "Counter target spell unless its controller pays {1}. Cycling {U}.",
    )
    loot = _analysis(
        "Lair",
        3,
        "Instant",
        "Draw two cards, then discard two cards.",
    )

    assert analyze_control(cycling).selection
    assert not analyze_control(cycling).card_advantage
    assert analyze_control(loot).selection
    assert not analyze_control(loot).card_advantage


def test_graveyard_or_damage_gate_is_conditional_not_reliable():
    for text in (
        "Destroy target creature that was dealt damage this turn.",
        "Counter target spell with mana value less than or equal to the number "
        "of cards in its controller's graveyard.",
    ):
        signals = analyze_control(_analysis("Narrow", 2, "Instant", text))
        assert signals.conditional_answer
        assert not signals.reliable_answer


def test_own_creature_blink_and_graveyard_exile_are_not_control_answers():
    for text in (
        "Exile target creature you control, then return it to the battlefield.",
        "Exile target creature card from a graveyard.",
    ):
        analysis = _analysis("Not Removal", 2, "Instant", text)
        assert not analyze_control(analysis).reliable_answer
