from thun_deckbuilder.benchmark_engine import BenchmarkEngine
from thun_deckbuilder.benchmark_loader import BenchmarkDefinition
from thun_deckbuilder.benchmark_report import format_benchmark_report
from thun_deckbuilder.deck_generator import GeneratedDeck


def test_report_formatter_exposes_score_and_profile() -> None:
    definition = BenchmarkDefinition("empty", "Empty Benchmark", "burn", ("R",), 24, (), ())
    report = BenchmarkEngine().evaluate(GeneratedDeck(mainboard=(), lands=24), definition)
    text = "\n".join(format_benchmark_report(report))
    assert "Empty Benchmark" in text
    assert "Benchmark score: 100/100" in text
