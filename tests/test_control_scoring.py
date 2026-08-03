from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.control_scoring import score_control_card


def _card(name, mana_value, type_line, oracle_text):
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


def test_cheap_counter_is_recognized_as_early_control_interaction():
    result = score_control_card(
        _card("Hard Answer", 2, "Instant", "Counter target spell.")
    )
    assert "Counter target spell" in result.reasons
    assert "Frühe Countermagic" in result.reasons
    assert result.score >= 8


def test_cheap_removal_scores_above_generic_creature():
    removal = score_control_card(
        _card("Clean Answer", 2, "Instant", "Destroy target creature.")
    )
    creature = score_control_card(
        _card("Vanilla", 2, "Creature", "Vigilance")
    )
    assert "Control removal" in removal.reasons
    assert removal.score > creature.score


def test_sweeper_and_card_advantage_are_control_components():
    sweeper = score_control_card(
        _card("Reset", 4, "Sorcery", "Destroy all creatures.")
    )
    draw = score_control_card(
        _card("Refill", 3, "Instant", "Draw two cards.")
    )
    assert "Sweeper" in sweeper.reasons
    assert "Card advantage engine" in draw.reasons


def test_reasonable_large_threat_is_marked_as_control_finisher():
    result = score_control_card(
        _card("Closing Threat", 6, "Creature", "Flying, ward {2}")
    )
    assert "Control-Finisher" in result.reasons
    assert "Zu teurer Finisher" not in result.reasons
