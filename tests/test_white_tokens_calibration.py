from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.token_generator import (
    _go_wide_production_adjustment,
    _is_reasonable_token_card,
    _score_for_composition,
)
from thun_deckbuilder.token_scoring import estimated_token_output, score_token_card


def analysis(text: str, *, mana_value: float = 2, type_line: str = "Sorcery"):
    return analyze_card(
        {
            "name": "Test Card",
            "mana_value": mana_value,
            "mana_cost": "{1}{W}",
            "colors": ["W"],
            "color_identity": ["W"],
            "type_line": type_line,
            "oracle_text": text,
            "power": "2" if "Creature" in type_line else None,
            "toughness": "2" if "Creature" in type_line else None,
        }
    )


def knowledge(text: str, roles: tuple[str, ...], *, mana_value: float = 2):
    card_analysis = analysis(text, mana_value=mana_value)
    return CardKnowledge(
        card={"name": "Test Card", "mana_cost": "{1}{W}"},
        analysis=card_analysis,
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def test_estimates_written_token_numbers():
    assert estimated_token_output("Create three 1/1 white Soldier creature tokens.") == 3
    assert estimated_token_output("Create a 1/1 white Soldier creature token.") == 1


def test_variable_token_output_is_marked_as_scaling():
    assert estimated_token_output("Create X 1/1 white Soldier creature tokens.") is None


def test_two_tokens_for_two_mana_outscores_one_token_for_four():
    efficient = score_token_card(analysis("Create two 1/1 white Soldier creature tokens."))
    inefficient = score_token_card(
        analysis("Create a 1/1 white Soldier creature token.", mana_value=4)
    )
    assert efficient.score >= inefficient.score + 6


def test_repeatable_token_source_beats_one_shot_source():
    repeatable = score_token_card(
        analysis(
            "At the beginning of your end step, create a 1/1 white Soldier creature token.",
            mana_value=3,
            type_line="Enchantment",
        )
    )
    one_shot = score_token_card(
        analysis("Create a 1/1 white Soldier creature token.", mana_value=3)
    )
    assert repeatable.score > one_shot.score
    assert "Wiederholbare Token-Quelle" in repeatable.reasons


def test_persistent_anthem_beats_temporary_pump():
    persistent = score_token_card(
        analysis("Creature tokens you control get +1/+1.", mana_value=3, type_line="Enchantment")
    )
    temporary = score_token_card(
        analysis("Creatures you control get +1/+1 until end of turn.", mana_value=3, type_line="Instant")
    )
    assert persistent.score > temporary.score


def test_board_wipe_is_not_eligible_for_go_wide_tokens():
    card = knowledge("Destroy all creatures.", ("removal", "board_wipe"), mana_value=4)
    assert not _is_reasonable_token_card(card)


def test_card_that_only_mentions_tokens_is_not_eligible():
    card = knowledge("Exile target token.", ("removal",), mana_value=1)
    pure_mention = knowledge("Target token gains flying until end of turn.", ("token_maker",), mana_value=1)
    assert _is_reasonable_token_card(card)
    assert not _is_reasonable_token_card(pure_mention)


def test_composition_score_prefers_reliable_multi_body_card():
    multi = knowledge("Create two 1/1 white Soldier creature tokens.", ("token_maker",))
    single = knowledge("Create a 1/1 white Soldier creature token.", ("token_maker",), mana_value=4)
    multi_score, _ = _score_for_composition(multi)
    single_score, _ = _score_for_composition(single)
    assert multi_score > single_score


def test_go_wide_penalizes_death_delayed_production():
    card = knowledge(
        "When this creature dies, create two 1/1 white Soldier creature tokens.",
        ("token_maker",),
    )
    adjustment, reason = _go_wide_production_adjustment(card)
    assert adjustment == -2.5
    assert reason == "Go Wide: Produktion erst nach eigenem Tod"


def test_go_wide_penalizes_conditional_production():
    card = knowledge(
        "If you control an artifact, create two 1/1 white Soldier creature tokens.",
        ("token_maker",),
    )
    adjustment, reason = _go_wide_production_adjustment(card)
    assert adjustment == -1.5
    assert reason == "Go Wide: bedingte Produktion"


def test_go_wide_scales_activated_penalty_with_mana_cost():
    cheap = knowledge("{1}{W}: Create a 1/1 white Soldier creature token.", ("token_maker",))
    expensive = knowledge("{4}{W}: Create a 1/1 white Soldier creature token.", ("token_maker",))
    cheap_adjustment, _ = _go_wide_production_adjustment(cheap)
    expensive_adjustment, reason = _go_wide_production_adjustment(expensive)
    assert cheap_adjustment == -2.0
    assert expensive_adjustment == -3.0
    assert expensive_adjustment < cheap_adjustment
    assert reason == "Go Wide: zusätzliche Aktivierungskosten"
