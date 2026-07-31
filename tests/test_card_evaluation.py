from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_evaluation import CardEvaluationEngine


def evaluate(**overrides):
    card = {
        "name": "Test Card",
        "mana_value": 2,
        "colors": ["U"],
        "color_identity": ["U"],
        "type_line": "Instant",
        "oracle_text": "Draw a card.",
    }
    card.update(overrides)
    return CardEvaluationEngine().evaluate(analyze_card(card))


def test_cheap_instant_card_draw_scores_positive() -> None:
    result = evaluate()
    assert result.total > 0
    assert any(c.category == "card_advantage" for c in result.components)
    assert any(c.category == "flexibility" for c in result.components)


def test_two_card_draw_is_worth_more_than_one_card_draw() -> None:
    one = evaluate(oracle_text="Draw a card.")
    two = evaluate(oracle_text="Draw two cards.")
    assert two.total > one.total


def test_instant_interaction_scores_more_than_slow_interaction() -> None:
    instant = evaluate(type_line="Instant", oracle_text="Destroy target creature.")
    sorcery = evaluate(type_line="Sorcery", oracle_text="Destroy target creature.")
    assert instant.total > sorcery.total


def test_above_rate_creature_receives_rate_bonus() -> None:
    result = evaluate(
        type_line="Creature — Beast",
        oracle_text="",
        power="4",
        toughness="4",
        mana_value=3,
    )
    assert any(c.category == "creature_rate" and c.value > 0 for c in result.components)


def test_expensive_low_impact_card_is_penalized() -> None:
    cheap = evaluate(type_line="Sorcery", oracle_text="", mana_value=2)
    expensive = evaluate(type_line="Sorcery", oracle_text="", mana_value=6)
    assert expensive.total < cheap.total


def test_lands_are_not_intrinsically_scored() -> None:
    result = evaluate(type_line="Basic Land — Island", mana_value=0, oracle_text="{T}: Add {U}.")
    assert result.total == 0
    assert result.components == ()
