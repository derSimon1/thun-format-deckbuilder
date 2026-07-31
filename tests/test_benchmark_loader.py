import pytest

from thun_deckbuilder.benchmark_loader import BenchmarkLoader


def test_loader_lists_packaged_benchmarks() -> None:
    available = BenchmarkLoader().available()
    assert "white_tokens" in available
    assert "mono_red_burn" in available
    assert "five_color_shrines" in available


def test_loader_reads_white_tokens_definition() -> None:
    benchmark = BenchmarkLoader().load("white-tokens")
    assert benchmark.name == "White Tokens"
    assert benchmark.colors == ("W",)
    assert benchmark.role_targets[0].minimum == 12


def test_loader_rejects_unknown_benchmark() -> None:
    with pytest.raises(KeyError):
        BenchmarkLoader().load("not-real")
