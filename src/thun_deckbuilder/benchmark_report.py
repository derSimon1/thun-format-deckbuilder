from __future__ import annotations

from thun_deckbuilder.benchmark_engine import BenchmarkReport


def format_benchmark_report(report: BenchmarkReport) -> list[str]:
    lines = ["BENCHMARK", "-" * 88, f"Profile: {report.benchmark_name}"]
    for metric in report.role_metrics:
        marker = "OK" if metric.minimum_met else "LOW"
        lines.append(
            f"  [{marker:<3}] {metric.label}: {metric.actual:g} / {metric.target:g} ({metric.score:.0f}%)"
        )
    for metric in report.curve_metrics:
        lines.append(
            f"  [CUR] {metric.label}: {metric.actual:g} / {metric.target:g} ({metric.score:.0f}%)"
        )
    lines.append(
        f"  [LND] Lands: {report.land_metric.actual:g} / {report.land_metric.target:g} ({report.land_metric.score:.0f}%)"
    )
    lines.append(f"Benchmark score: {report.overall_score}/100")
    return lines
