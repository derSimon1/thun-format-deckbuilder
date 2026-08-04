from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.deck_generator import DeckEntry, ManaCost
from thun_deckbuilder.engine_density import evaluate_token_engine_density
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.token_plan import TokenPlan


def entry(name: str, quantity: int, roles: tuple[str, ...]) -> DeckEntry:
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost(raw="{1}{W}", generic=1, colored="W"),
        mana_value=2,
        type_line="Creature",
        roles=roles,
    )


def knowledge(
    name: str,
    text: str,
    roles: tuple[str, ...],
    type_line: str = "Creature",
) -> CardKnowledge:
    card = {
        "name": name,
        "mana_value": 2,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": type_line,
        "oracle_text": text,
    }
    return CardKnowledge(
        card=card,
        analysis=analyze_card(card),
        roles=frozenset(roles),
        synergies=frozenset(),
    )


def test_one_shot_token_maker_is_material_not_engine():
    report = evaluate_token_engine_density(
        (entry("Raise the Team", 12, ("token_maker",)),),
        (
            knowledge(
                "Raise the Team",
                "When this creature enters, create two 1/1 creature tokens.",
                ("token_maker",),
            ),
        ),
        TokenPlan.GO_WIDE,
    )

    assert report.engine_copies == 0
    assert report.engine_density == 0
    assert not report.engine_required
    assert not report.warnings


def test_value_plan_without_engine_keeps_actionable_warning():
    report = evaluate_token_engine_density(
        (entry("Raise the Team", 12, ("token_maker",)),),
        (
            knowledge(
                "Raise the Team",
                "When this creature enters, create two 1/1 creature tokens.",
                ("token_maker",),
            ),
        ),
        TokenPlan.VALUE,
    )

    assert report.engine_required
    assert any("Keine wiederholbare Engine" in item for item in report.warnings)


def test_repeatable_token_source_counts_by_copies():
    report = evaluate_token_engine_density(
        (
            entry("Steady Recruiter", 3, ("token_maker",)),
            entry("Raise the Team", 9, ("token_maker",)),
        ),
        (
            knowledge(
                "Steady Recruiter",
                "At the beginning of your end step, create a 1/1 creature token.",
                ("token_maker",),
                "Enchantment",
            ),
            knowledge(
                "Raise the Team",
                "When this creature enters, create two 1/1 creature tokens.",
                ("token_maker",),
            ),
        ),
        TokenPlan.VALUE,
    )

    assert report.engine_copies == 3
    assert report.spell_copies == 12
    assert report.engine_density == 0.25
    assert report.distinct_engines == 1
    assert any("nur von einer Karte" in item for item in report.warnings)


def test_aristocrats_death_payoff_is_plan_engine():
    report = evaluate_token_engine_density(
        (
            entry("Drain Priest", 3, ("token_payoff",)),
            entry("Fodder", 9, ("token_maker",)),
        ),
        (
            knowledge(
                "Drain Priest",
                "Whenever another creature dies, each opponent loses 1 life and you gain 1 life.",
                ("token_payoff",),
            ),
            knowledge(
                "Fodder",
                "When this creature enters, create a 1/1 creature token.",
                ("token_maker",),
            ),
        ),
        TokenPlan.ARISTOCRATS,
    )

    assert report.engine_copies == 3
    assert report.engine_names == ("Drain Priest",)
