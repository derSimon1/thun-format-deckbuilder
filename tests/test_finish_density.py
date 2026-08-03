from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.deck_generator import DeckEntry, ManaCost
from thun_deckbuilder.finish_density import evaluate_token_finish_density
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.token_plan import TokenPlan


def entry(name: str, quantity: int) -> DeckEntry:
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost(raw="{1}{W}", generic=1, colored="W"),
        mana_value=2,
        type_line="Enchantment",
        roles=(),
    )


def knowledge(name: str, text: str) -> CardKnowledge:
    card = {
        "name": name,
        "mana_value": 2,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Enchantment",
        "oracle_text": text,
    }
    return CardKnowledge(
        card=card,
        analysis=analyze_card(card),
        roles=frozenset(),
        synergies=frozenset(),
    )


def test_go_wide_anthem_and_evasion_copy_counts_once():
    report = evaluate_token_finish_density(
        (
            entry("Battle Standard", 3),
            entry("Raise the Team", 9),
        ),
        (
            knowledge(
                "Battle Standard",
                "Creatures you control get +1/+1. "
                "Creature tokens you control have flying.",
            ),
            knowledge(
                "Raise the Team",
                "Create two 1/1 white Soldier creature tokens.",
            ),
        ),
        TokenPlan.GO_WIDE,
    )

    assert report.finish_copies == 3
    assert report.spell_copies == 12
    assert report.finish_density == 0.25
    assert report.finish_modes == ("anthem", "evasion")


def test_one_shot_token_maker_is_not_a_finish():
    report = evaluate_token_finish_density(
        (entry("Raise the Team", 12),),
        (
            knowledge(
                "Raise the Team",
                "Create two 1/1 white Soldier creature tokens.",
            ),
        ),
        TokenPlan.GO_WIDE,
    )

    assert report.finish_copies == 0
    assert any("Kein klarer Abschlussweg" in item for item in report.warnings)


def test_finish_detection_is_plan_dependent():
    cards = (
        knowledge(
            "Token Mentor",
            "Whenever one or more tokens enter under your control, draw a card.",
        ),
        knowledge(
            "Drain Priest",
            "Whenever another creature dies, each opponent loses 1 life.",
        ),
    )
    entries = (
        entry("Token Mentor", 3),
        entry("Drain Priest", 3),
    )

    value = evaluate_token_finish_density(entries, cards, TokenPlan.VALUE)
    aristocrats = evaluate_token_finish_density(
        entries,
        cards,
        TokenPlan.ARISTOCRATS,
    )
    go_wide = evaluate_token_finish_density(entries, cards, TokenPlan.GO_WIDE)

    assert value.finish_names == ("Token Mentor",)
    assert aristocrats.finish_names == ("Drain Priest",)
    assert go_wide.finish_copies == 0
