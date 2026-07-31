from thun_deckbuilder.benchmark_engine import BenchmarkEngine
from thun_deckbuilder.benchmark_loader import BenchmarkDefinition, BenchmarkRoleTarget, BenchmarkCurveTarget
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost


def entry(name: str, quantity: int, mana_value: float, *roles: str) -> DeckEntry:
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("", 0, ""),
        mana_value=mana_value,
        type_line="Creature",
        roles=roles,
    )


def benchmark() -> BenchmarkDefinition:
    return BenchmarkDefinition(
        key="test",
        name="Test",
        archetype="tokens",
        colors=("W",),
        lands=24,
        role_targets=(BenchmarkRoleTarget("token_maker", 12, 9),),
        curve_targets=(BenchmarkCurveTarget(2, 12),),
    )


def test_exact_benchmark_scores_100() -> None:
    deck = GeneratedDeck(mainboard=(entry("Maker", 12, 2, "token_maker"),), lands=24)
    report = BenchmarkEngine().evaluate(deck, benchmark())
    assert report.overall_score == 100
    assert report.minimums_met


def test_benchmark_detects_missing_role_minimum() -> None:
    deck = GeneratedDeck(mainboard=(entry("Maker", 6, 2, "token_maker"),), lands=24)
    report = BenchmarkEngine().evaluate(deck, benchmark())
    assert not report.minimums_met
    assert report.role_metrics[0].score == 50


def test_benchmark_penalizes_overshooting_curve_target() -> None:
    deck = GeneratedDeck(mainboard=(entry("Maker", 18, 2, "token_maker"),), lands=24)
    report = BenchmarkEngine().evaluate(deck, benchmark())
    assert report.curve_metrics[0].score == 50
    assert report.overall_score < 100
