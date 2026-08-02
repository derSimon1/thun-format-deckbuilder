from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator


def entry(name, qty, mv, type_line="Sorcery", reasons=()):
    return DeckEntry(
        name=name,
        quantity=qty,
        mana_cost=ManaCost("", 0, ""),
        mana_value=mv,
        type_line=type_line,
        reasons=reasons,
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


def test_prowess_core_density_increases_turn_three_access():
    dense = GeneratedDeck(
        mainboard=(
            entry(
                "Prowess Threat",
                18,
                2,
                "Creature",
                ("Echte Prowess-Bedrohung",),
            ),
            entry("Support", 20, 1),
        ),
        lands=22,
    )
    thin = GeneratedDeck(
        mainboard=(
            entry(
                "Prowess Threat",
                3,
                2,
                "Creature",
                ("Echte Prowess-Bedrohung",),
            ),
            entry("Support", 35, 1),
        ),
        lands=22,
    )
    simulator = OpeningHandSimulator()
    dense_report = simulator.simulate(dense, archetype="prowess", samples=1000)
    thin_report = simulator.simulate(thin, archetype="prowess", samples=1000)
    assert dense_report.core_by_turn_three_pct > thin_report.core_by_turn_three_pct


def test_land_count_reports_screw_and_flood_risk_after_mulligan():
    low_land = GeneratedDeck(mainboard=(entry("Spell", 44, 2),), lands=16)
    high_land = GeneratedDeck(mainboard=(entry("Spell", 28, 2),), lands=32)
    simulator = OpeningHandSimulator()
    low = simulator.simulate(low_land, archetype="mill", samples=1000)
    high = simulator.simulate(high_land, archetype="mill", samples=1000)
    assert low.mana_screw_pct > high.mana_screw_pct
    assert high.mana_flood_pct > low.mana_flood_pct
