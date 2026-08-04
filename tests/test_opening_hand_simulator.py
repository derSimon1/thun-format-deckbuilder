import pytest

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.mana_distribution import LandAllocation, ManaDistribution
from thun_deckbuilder.opening_hand_simulator import (
    HandPlanClassification,
    OpeningHandSimulator,
    _PlanCard,
    _can_cast_with_sources,
    _mana_symbols,
)


def entry(
    name,
    qty,
    mv,
    type_line="Sorcery",
    reasons=(),
    roles=(),
    mana_cost="",
    colored="",
):
    return DeckEntry(
        name=name,
        quantity=qty,
        mana_cost=ManaCost(mana_cost, 0, colored),
        mana_value=mv,
        type_line=type_line,
        reasons=reasons,
        roles=roles,
    )


def deck_with_sources(*entries, lands=24, colors=("W",)):
    allocations = tuple(
        LandAllocation(color, f"Basic {color}", lands // len(colors))
        for color in colors
    )
    allocated = sum(item.quantity for item in allocations)
    if allocated < lands:
        first = allocations[0]
        allocations = (
            LandAllocation(
                first.color,
                first.land_name,
                first.quantity + lands - allocated,
            ),
            *allocations[1:],
        )
    return GeneratedDeck(
        mainboard=tuple(entries),
        lands=lands,
        mana_base=ManaDistribution(allocations, lands, ()),
    )


def test_simulation_is_deterministic():
    deck = GeneratedDeck(
        mainboard=(
            entry("Ruin Crab", 3, 1, "Creature", ("Millt Karten",)),
            entry("Cheap Mill", 15, 2, reasons=("Millt Karten",)),
            entry("Interaction", 18, 2),
        ),
        lands=24,
    )
    first = OpeningHandSimulator().simulate(deck, archetype="mill", samples=500)
    second = OpeningHandSimulator().simulate(deck, archetype="mill", samples=500)
    assert first == second


def test_mulligan_improves_playable_hand_rate():
    deck = GeneratedDeck(
        mainboard=(
            entry("Cheap Mill", 24, 2, reasons=("Millt Karten",)),
            entry("Slow Support", 12, 5),
        ),
        lands=24,
    )
    report = OpeningHandSimulator().simulate(deck, archetype="mill", samples=2000)
    assert report.mulligan_to_six_pct > 0
    assert report.playable_after_mulligan_pct >= report.playable_hands_pct


def test_low_curve_deck_has_more_early_plays_than_slow_deck():
    fast = GeneratedDeck(
        mainboard=(entry("Cheap", 36, 2),),
        lands=24,
    )
    slow = GeneratedDeck(
        mainboard=(entry("Slow", 36, 5),),
        lands=24,
    )
    simulator = OpeningHandSimulator()
    fast_report = simulator.simulate(fast, archetype="mill", samples=1000)
    slow_report = simulator.simulate(slow, archetype="mill", samples=1000)
    assert fast_report.early_play_pct > slow_report.early_play_pct
    assert fast_report.playable_after_mulligan_pct > slow_report.playable_after_mulligan_pct


def test_core_density_increases_turn_three_access():
    dense = GeneratedDeck(
        mainboard=(
            entry("Mill One", 18, 2, reasons=("Millt Karten",)),
            entry("Support", 18, 2),
        ),
        lands=24,
    )
    thin = GeneratedDeck(
        mainboard=(
            entry("Mill One", 3, 2, reasons=("Millt Karten",)),
            entry("Support", 33, 2),
        ),
        lands=24,
    )
    simulator = OpeningHandSimulator()
    dense_report = simulator.simulate(dense, archetype="mill", samples=1000)
    thin_report = simulator.simulate(thin, archetype="mill", samples=1000)
    assert dense_report.core_by_turn_three_pct > thin_report.core_by_turn_three_pct


def test_land_count_reports_screw_and_flood_risk_after_mulligan():
    low_land = GeneratedDeck(mainboard=(entry("Spell", 44, 2),), lands=16)
    high_land = GeneratedDeck(mainboard=(entry("Spell", 28, 2),), lands=32)
    simulator = OpeningHandSimulator()
    low = simulator.simulate(low_land, archetype="mill", samples=1000)
    high = simulator.simulate(high_land, archetype="mill", samples=1000)
    assert low.mana_screw_pct > high.mana_screw_pct
    assert high.mana_flood_pct > low.mana_flood_pct


def test_plan_report_stores_exactly_100_reproducible_raw_hands():
    deck = deck_with_sources(
        entry(
            "Mill Engine",
            12,
            1,
            reasons=("Mill engine",),
            mana_cost="{U}",
            colored="U",
        ),
        entry(
            "Cheap Interaction",
            12,
            2,
            roles=("removal",),
            mana_cost="{1}{U}",
            colored="U",
        ),
        entry("Support", 12, 3, mana_cost="{2}{U}", colored="U"),
        colors=("U",),
    )
    simulator = OpeningHandSimulator()
    first = simulator.simulate_plan(
        deck, archetype="mill", samples=100, seed=1701
    )
    second = simulator.simulate_plan(
        deck, archetype="mill", samples=100, seed=1701
    )
    different = simulator.simulate_plan(
        deck, archetype="mill", samples=100, seed=1702
    )

    assert first == second
    assert first.samples == 100
    assert len(first.hands) == 100
    assert tuple(hand.cards for hand in first.hands) != tuple(
        hand.cards for hand in different.hands
    )
    assert first.deck_hash == different.deck_hash


def test_early_play_is_not_treated_as_plan_capability():
    deck = deck_with_sources(
        entry(
            "Generic Two Drop",
            36,
            2,
            type_line="Creature",
            mana_cost="{1}{W}",
            colored="W",
        ),
        colors=("W",),
    )
    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="tokens",
        plan="go_wide",
        seed=31,
    )

    assert report.early_play_turn_two_pct > report.plan_capable_pct
    assert report.plan_capable_pct == 0
    assert report.missing_enabler_pct == 100


def test_go_wide_needs_a_token_maker_castable_by_turn_two():
    deck = deck_with_sources(
        entry(
            "Generic Two Drop",
            12,
            2,
            type_line="Creature",
            mana_cost="{1}{W}",
            colored="W",
        ),
        entry(
            "Slow Maker",
            12,
            3,
            roles=("token_maker",),
            reasons=("Go Wide: Token-Erzeuger",),
            mana_cost="{2}{W}",
            colored="W",
        ),
        entry(
            "Slow Anthem",
            12,
            3,
            roles=("anthem", "token_payoff"),
            reasons=("Go Wide: Board-Payoff",),
            mana_cost="{2}{W}",
            colored="W",
        ),
    )

    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="tokens",
        plan="go_wide",
        seed=31,
    )

    assert report.early_play_turn_two_pct > 0
    assert report.plan_capable_pct == 0
    assert any(
        "missing_early_token_maker" in hand.failure_reasons
        for hand in report.hands
    )


def test_go_wide_keeps_early_maker_into_scaling_plan_capable():
    deck = deck_with_sources(
        entry(
            "Early Maker",
            18,
            2,
            roles=("token_maker",),
            reasons=("Go Wide: Token-Erzeuger",),
            mana_cost="{1}{W}",
            colored="W",
        ),
        entry(
            "Anthem",
            9,
            3,
            roles=("anthem", "token_payoff"),
            reasons=("Go Wide: Board-Payoff",),
            mana_cost="{2}{W}",
            colored="W",
        ),
        entry(
            "Interaction",
            9,
            2,
            roles=("removal",),
            mana_cost="{1}{W}",
            colored="W",
        ),
    )

    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="tokens",
        plan="go_wide",
        seed=73,
    )

    assert report.plan_capable_pct > 0
    assert all(
        hand.turn_two_plays
        for hand in report.hands
        if hand.classification == HandPlanClassification.PLAN_CAPABLE
    )


@pytest.mark.parametrize(
    ("plan", "entries", "expected_reason"),
    (
        (
            "go_wide",
            (
                entry(
                    "Early Maker",
                    18,
                    2,
                    roles=("token_maker",),
                    reasons=("Go Wide: Token-Erzeuger",),
                    mana_cost="{1}{W}",
                    colored="W",
                ),
                entry(
                    "Anthem",
                    9,
                    3,
                    roles=("anthem", "token_payoff"),
                    reasons=("Go Wide: Board-Payoff",),
                    mana_cost="{2}{W}",
                    colored="W",
                ),
                entry(
                    "Interaction",
                    9,
                    2,
                    roles=("removal",),
                    mana_cost="{1}{W}",
                    colored="W",
                ),
            ),
            "maker_plus_go_wide_scaling",
        ),
        (
            "value_tokens",
            (
                entry(
                    "Repeatable Maker",
                    18,
                    2,
                    roles=("token_maker", "card_draw"),
                    reasons=("Value Tokens: repeatable engine",),
                    mana_cost="{1}{W}",
                    colored="W",
                ),
                entry(
                    "Value Payoff",
                    9,
                    3,
                    roles=("token_payoff", "card_draw"),
                    reasons=("Value Tokens: Kartenvorteil",),
                    mana_cost="{2}{W}",
                    colored="W",
                ),
                entry(
                    "Interaction",
                    9,
                    2,
                    roles=("removal",),
                    mana_cost="{1}{W}",
                    colored="W",
                ),
            ),
            "maker_plus_value_engine",
        ),
        (
            "aristocrats",
            (
                entry(
                    "Sacrifice Material",
                    12,
                    1,
                    roles=("token_maker",),
                    reasons=("Aristocrats: Opfermaterial",),
                    mana_cost="{W}",
                    colored="W",
                ),
                entry(
                    "Sacrifice Outlet",
                    12,
                    2,
                    roles=("sacrifice",),
                    reasons=("Aristocrats: Opfermöglichkeit",),
                    mana_cost="{1}{W}",
                    colored="W",
                ),
                entry(
                    "Death Payoff",
                    12,
                    2,
                    roles=("token_payoff",),
                    reasons=("Aristocrats: Death-Payoff drain",),
                    mana_cost="{1}{W}",
                    colored="W",
                ),
            ),
            "complete_aristocrats_core",
        ),
    ),
)
def test_token_plans_require_their_defining_packages(
    plan,
    entries,
    expected_reason,
):
    report = OpeningHandSimulator().simulate_plan(
        deck_with_sources(*entries),
        archetype="tokens",
        plan=plan,
        seed=73,
    )

    assert report.plan_capable_pct > 0
    assert any(
        expected_reason in hand.reasons
        for hand in report.hands
        if hand.classification == HandPlanClassification.PLAN_CAPABLE
    )


def test_aristocrats_material_without_outlet_or_payoff_is_not_plan_capable():
    deck = deck_with_sources(
        entry(
            "Sacrifice Material",
            36,
            1,
            roles=("token_maker",),
            reasons=("Aristocrats: Opfermaterial",),
            mana_cost="{W}",
            colored="W",
        ),
    )
    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="tokens",
        plan="aristocrats",
        seed=11,
    )

    assert report.plan_capable_pct == 0
    assert report.not_plan_capable_pct > 0
    assert any(
        "incomplete_aristocrats_core" in hand.failure_reasons
        for hand in report.hands
    )


@pytest.mark.parametrize(
    ("archetype", "entries", "colors"),
    (
        (
            "artifacts",
            (
                entry(
                    "Cheap Artifact",
                    18,
                    1,
                    type_line="Artifact",
                    reasons=("Günstiger Artifact Enabler",),
                    mana_cost="{1}",
                ),
                entry(
                    "Affinity Payoff",
                    9,
                    3,
                    reasons=("Affinity payoff",),
                    mana_cost="{2}{U}",
                    colored="U",
                ),
                entry(
                    "Interaction",
                    9,
                    2,
                    roles=("removal",),
                    mana_cost="{1}{U}",
                    colored="U",
                ),
            ),
            ("U",),
        ),
        (
            "mill",
            (
                entry(
                    "Mill Engine",
                    18,
                    1,
                    type_line="Creature",
                    reasons=("Repeatable mill engine",),
                    mana_cost="{U}",
                    colored="U",
                ),
                entry(
                    "Interaction",
                    12,
                    2,
                    roles=("removal",),
                    mana_cost="{1}{U}",
                    colored="U",
                ),
                entry(
                    "Card Draw",
                    6,
                    2,
                    roles=("card_draw",),
                    mana_cost="{1}{U}",
                    colored="U",
                ),
            ),
            ("U",),
        ),
        (
            "control",
            (
                entry(
                    "Early Answer",
                    15,
                    2,
                    roles=("removal",),
                    reasons=("Relevant interaction",),
                    mana_cost="{1}{U}",
                    colored="U",
                ),
                entry(
                    "Card Advantage",
                    12,
                    3,
                    roles=("card_draw",),
                    reasons=("Card advantage engine",),
                    mana_cost="{2}{U}",
                    colored="U",
                ),
                entry(
                    "Finisher",
                    9,
                    5,
                    type_line="Creature",
                    roles=("finisher",),
                    mana_cost="{4}{U}",
                    colored="U",
                ),
            ),
            ("U",),
        ),
    ),
)
def test_non_token_archetypes_have_plan_capable_fixture_hands(
    archetype,
    entries,
    colors,
):
    report = OpeningHandSimulator().simulate_plan(
        deck_with_sources(*entries, colors=colors),
        archetype=archetype,
        seed=91,
    )

    assert report.plan_capable_pct > 0
    assert report.samples == 100


def test_color_mismatch_is_reported_separately_from_land_count():
    deck = deck_with_sources(
        entry(
            "Blue Mill Engine",
            24,
            1,
            reasons=("Mill engine",),
            mana_cost="{U}",
            colored="U",
        ),
        entry(
            "Support",
            12,
            2,
            mana_cost="{1}{U}",
            colored="U",
        ),
        colors=("W",),
    )
    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="mill",
        seed=7,
    )

    assert report.color_error_pct > 0
    assert report.mana_error_pct < 100
    assert any(
        "color_mismatch" in hand.failure_reasons for hand in report.hands
    )


def test_true_colorless_spell_requires_real_colorless_source():
    card = _PlanCard(
        "Colorless Spell",
        "spell",
        mana_value=2,
        color_requirements=_mana_symbols("{1}{C}", "C"),
    )

    assert _can_cast_with_sources(card, ("W", "C"), turn=2)
    assert not _can_cast_with_sources(card, ("W", "W"), turn=2)
    assert not _can_cast_with_sources(card, ("W", "*"), turn=2)


def test_regular_colored_spell_keeps_wildcard_source_behavior():
    card = _PlanCard(
        "White Spell",
        "spell",
        mana_value=2,
        color_requirements=_mana_symbols("{1}{W}", "W"),
    )

    assert _can_cast_with_sources(card, ("W", "*"), turn=2)


def test_mana_error_hands_are_never_classified_as_plan_capable():
    deck = deck_with_sources(
        entry(
            "Sacrifice Material",
            12,
            1,
            roles=("token_maker",),
            reasons=("Aristocrats: Opfermaterial",),
            mana_cost="{W}",
            colored="W",
        ),
        entry(
            "Sacrifice Outlet",
            12,
            2,
            roles=("sacrifice",),
            reasons=("Aristocrats: Opfermöglichkeit",),
            mana_cost="{1}{W}",
            colored="W",
        ),
        entry(
            "Death Payoff",
            12,
            2,
            roles=("token_payoff",),
            reasons=("Aristocrats: Death-Payoff drain",),
            mana_cost="{1}{W}",
            colored="W",
        ),
        lands=12,
    )
    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="tokens",
        plan="aristocrats",
        seed=1701,
    )

    assert any(hand.mana_error for hand in report.hands)
    assert all(
        hand.classification != HandPlanClassification.PLAN_CAPABLE
        for hand in report.hands
        if hand.mana_error
    )
