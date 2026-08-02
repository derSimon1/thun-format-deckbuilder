from thun_deckbuilder.benchmark import BenchmarkAnalyzer
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost


def entry(name, qty, mv, roles):
    return DeckEntry(name, qty, ManaCost("", 0, ""), mv, "Instant", roles=roles)


def test_benchmark_reports_role_curve_and_land_scores():
    deck = GeneratedDeck(
        mainboard=(entry("Bolt", 24, 1, ("burn",)), entry("Creature", 9, 2, ("aggro_creature",)), entry("Draw", 3, 3, ("card_draw",))),
        lands=24,
    )
    report = BenchmarkAnalyzer().analyze(deck, "burn")
    assert report.land_item.score == 100
    assert report.role_items[0].actual == 24
    assert 0 <= report.score <= 100


def test_benchmark_role_minimums_do_not_penalize_excess():
    deck = GeneratedDeck(
        mainboard=(
            entry("Bolt", 30, 1, ("burn",)),
            entry("Creature", 12, 2, ("aggro_creature",)),
            entry("Draw", 6, 3, ("card_draw",)),
        ),
        lands=24,
    )

    report = BenchmarkAnalyzer().analyze(deck, "burn")

    assert [item.score for item in report.role_items] == [100, 100, 100]


def test_benchmark_rejects_unknown_archetype():
    try:
        BenchmarkAnalyzer().analyze(GeneratedDeck((), 24), "unknown")
    except ValueError as exc:
        assert "No benchmark" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
