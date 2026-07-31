from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.matchup_simulator import MatchupReport, MatchupSimulator


@dataclass(frozen=True)
class MetaStanding:
    archetype: str
    matches: int
    wins_pct: int
    losses_pct: int
    draws_pct: int
    classification: str


@dataclass(frozen=True)
class MetaMatrixReport:
    standings: tuple[MetaStanding, ...]
    matchups: tuple[MatchupReport, ...]
    warnings: tuple[str, ...]


def _classification(win_rate: float) -> str:
    if win_rate >= 60.0:
        return "OVERPERFORMER"
    if win_rate <= 40.0:
        return "UNDERPERFORMER"
    return "BALANCED"


class MetaMatrixAnalyzer:
    """Run every supplied archetype against every other archetype once."""

    def analyze(
        self,
        decks: Mapping[str, GeneratedDeck],
        *,
        samples_per_matchup: int = 2000,
        seed: int = 71,
    ) -> MetaMatrixReport:
        if len(decks) < 2:
            raise ValueError("At least two archetypes are required.")
        if samples_per_matchup <= 0:
            raise ValueError("samples_per_matchup must be positive.")

        simulator = MatchupSimulator()
        matchups: list[MatchupReport] = []
        totals = {
            archetype: {"wins": 0.0, "losses": 0.0, "draws": 0.0, "matches": 0}
            for archetype in decks
        }

        for index, (archetype_a, archetype_b) in enumerate(combinations(sorted(decks), 2)):
            report = simulator.simulate(
                decks[archetype_a],
                decks[archetype_b],
                archetype_a=archetype_a,
                archetype_b=archetype_b,
                samples=samples_per_matchup,
                seed=seed + index,
            )
            matchups.append(report)
            totals[archetype_a]["wins"] += report.wins_a_pct
            totals[archetype_a]["losses"] += report.wins_b_pct
            totals[archetype_a]["draws"] += report.draws_pct
            totals[archetype_a]["matches"] += 1
            totals[archetype_b]["wins"] += report.wins_b_pct
            totals[archetype_b]["losses"] += report.wins_a_pct
            totals[archetype_b]["draws"] += report.draws_pct
            totals[archetype_b]["matches"] += 1

        standings: list[MetaStanding] = []
        warnings: list[str] = []
        for archetype, values in totals.items():
            matches = int(values["matches"])
            wins = round(values["wins"] / matches)
            losses = round(values["losses"] / matches)
            draws = round(values["draws"] / matches)
            classification = _classification(wins)
            standings.append(
                MetaStanding(
                    archetype=archetype,
                    matches=matches,
                    wins_pct=wins,
                    losses_pct=losses,
                    draws_pct=draws,
                    classification=classification,
                )
            )
            if classification == "OVERPERFORMER":
                warnings.append(f"{archetype} overperforms at {wins}% estimated meta wins.")
            elif classification == "UNDERPERFORMER":
                warnings.append(f"{archetype} underperforms at {wins}% estimated meta wins.")

        standings.sort(key=lambda item: (-item.wins_pct, item.archetype))
        return MetaMatrixReport(
            standings=tuple(standings),
            matchups=tuple(matchups),
            warnings=tuple(warnings),
        )


def format_matchup_report(report: MatchupReport) -> str:
    return "\n".join(
        (
            f"{report.archetype_a} vs. {report.archetype_b}",
            f"{report.archetype_a} wins: {report.wins_a_pct}%",
            f"{report.archetype_b} wins: {report.wins_b_pct}%",
            f"Draws: {report.draws_pct}%",
            f"Scores: {report.average_score_a} / {report.average_score_b}",
        )
    )


def format_meta_matrix(report: MetaMatrixReport) -> str:
    lines = [
        "THUN META MATRIX",
        "=" * 72,
        f"{'Archetype':<18}{'Win':>8}{'Loss':>8}{'Draw':>8}{'Status':>20}",
        "-" * 72,
    ]
    for standing in report.standings:
        lines.append(
            f"{standing.archetype:<18}{standing.wins_pct:>7}%"
            f"{standing.losses_pct:>7}%{standing.draws_pct:>7}%"
            f"{standing.classification:>20}"
        )
    if report.warnings:
        lines.extend(("", "META WARNINGS", "-" * 72))
        lines.extend(f"WARNUNG: {warning}" for warning in report.warnings)
    return "\n".join(lines)
