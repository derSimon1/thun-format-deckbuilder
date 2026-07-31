from __future__ import annotations

from thun_deckbuilder.candidate_score import CandidateScore
from thun_deckbuilder.deck_quality import DeckQualityReport
from thun_deckbuilder.selection_trace import SelectionTrace


def format_candidate_score(score: CandidateScore) -> tuple[str, ...]:
    lines = []
    for component in score.components:
        label = component.category.replace("_", " ").title()
        lines.append(f"  {label:<24}{component.value:>7.1f}  {component.reason}")
    lines.append(f"  {'Total':<24}{score.total:>7.1f}")
    return tuple(lines)


def format_selection_trace(trace: SelectionTrace) -> tuple[str, ...]:
    need = trace.primary_need or "general deck quality"
    lines = [
        f"Step {trace.step}: {trace.card_name} (copy {trace.quantity_after_selection})",
        f"  Primary need: {need}",
    ]
    lines.extend(format_candidate_score(trace.score))
    return tuple(lines)


def format_quality_report(report: DeckQualityReport) -> tuple[str, ...]:
    lines = [
        "DECK QUALITY REPORT",
        "-" * 88,
        "Roles",
    ]
    for role in report.role_quality:
        marker = "OK" if role.target_met else ("MIN" if role.minimum_met else "MISS")
        lines.append(
            f"  [{marker:<4}] {role.role:<22}{role.current:>5g}/{role.target:<5}"
            f" score {role.score:>5.1f}"
        )
    if report.curve_quality:
        lines.append("Curve")
        for band in report.curve_quality:
            marker = "OK" if band.target_met else "LOW"
            lines.append(
                f"  [{marker:<4}] MV {band.label:<17}{band.current:>5}/{band.target:<5}"
                f" score {band.score:>5.1f}"
            )
    if report.synergy_quality:
        lines.append("Synergies")
        for synergy in report.synergy_quality:
            marker = "OK" if synergy.active else "ONE"
            lines.append(
                f"  [{marker:<4}] {synergy.label:<22}"
                f" {synergy.enablers:>3} enabler / {synergy.payoffs:<3} payoff"
                f" score {synergy.score:>5.1f}"
            )
    lines.extend(
        [
            f"Role score:  {report.role_score:>5.1f}",
            f"Curve score: {report.curve_score:>5.1f}",
            f"Synergy:     {report.synergy_score:>5.1f}",
            f"Mana:        {report.mana_score:>5.1f}",
            f"Overall:     {report.overall_score:>3}/100",
        ]
    )
    return tuple(lines)
