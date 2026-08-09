from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.tournament_simulator import BestOfThreeReport, BestOfThreeSimulator


@dataclass(frozen=True)
class ArchetypeAdvice:
    archetype: str
    estimated_match_win_pct: int
    worst_matchup: str
    worst_matchup_win_pct: int
    recommendations: tuple[str, ...]


@dataclass(frozen=True)
class BestOfThreeMetaReport:
    standings: tuple[ArchetypeAdvice, ...]
    matchups: tuple[BestOfThreeReport, ...]


def _recommendations(archetype: str, opponent: str, win_pct: int) -> tuple[str, ...]:
    if win_pct >= 45:
        return ("Keine dringende Anpassung; Sideboard-Verteilung beibehalten.",)
    ideas: list[str] = []
    if opponent in {"burn", "tokens"}:
        ideas.extend(("mehr günstiges Removal", "Lifegain oder Sweeper im Sideboard"))
    elif opponent == "mill":
        ideas.extend(("mehr Countermagic oder Graveyard-Recycling", "schnellere eigenständige Bedrohungen"))
    elif opponent == "artifacts":
        ideas.extend(("mehr Artefakt-Hate", "weniger langsame Karten ohne Boardeinfluss"))
    elif opponent == "shrines":
        ideas.extend(("mehr Enchantment-Hate", "Druck vor Zug 4 erhöhen"))
    if archetype == "shrines":
        ideas.append("zusätzliche frühe Stabilisierung und Manafixing prüfen")
    if archetype == "mill":
        ideas.append("mehr günstige Interaktion gegen frühe Kreaturen prüfen")
    return tuple(dict.fromkeys(ideas))


class BestOfThreeMetaAnalyzer:
    def analyze(
        self,
        decks: dict[str, GeneratedDeck],
        *,
        samples_per_matchup: int = 2000,
    ) -> BestOfThreeMetaReport:
        if len(decks) < 2:
            raise ValueError("At least two decks are required")
        simulator = BestOfThreeSimulator()
        reports: list[BestOfThreeReport] = []
        results: dict[str, list[tuple[str, int]]] = {name: [] for name in decks}
        for archetype_a, archetype_b in combinations(sorted(decks), 2):
            report = simulator.simulate(
                decks[archetype_a],
                decks[archetype_b],
                archetype_a=archetype_a,
                archetype_b=archetype_b,
                samples=samples_per_matchup,
            )
            reports.append(report)
            results[archetype_a].append((archetype_b, report.match_wins_a_pct))
            results[archetype_b].append((archetype_a, report.match_wins_b_pct))

        standings: list[ArchetypeAdvice] = []
        for archetype, matchups in results.items():
            worst_opponent, worst_pct = min(matchups, key=lambda item: (item[1], item[0]))
            average = round(sum(value for _, value in matchups) / len(matchups))
            standings.append(
                ArchetypeAdvice(
                    archetype=archetype,
                    estimated_match_win_pct=average,
                    worst_matchup=worst_opponent,
                    worst_matchup_win_pct=worst_pct,
                    recommendations=_recommendations(archetype, worst_opponent, worst_pct),
                )
            )
        standings.sort(key=lambda item: (-item.estimated_match_win_pct, item.archetype))
        return BestOfThreeMetaReport(tuple(standings), tuple(reports))


def format_meta_advice(report: BestOfThreeMetaReport) -> str:
    lines = [
        "THUN BEST-OF-THREE META ADVISOR",
        "=" * 88,
        f"{'Archetype':<16}{'Match Win':>12}{'Worst Matchup':>20}{'Worst Win':>12}",
        "-" * 88,
    ]
    for item in report.standings:
        lines.append(
            f"{item.archetype:<16}{str(item.estimated_match_win_pct) + '%':>12}"
            f"{item.worst_matchup:>20}{str(item.worst_matchup_win_pct) + '%':>12}"
        )
        for recommendation in item.recommendations:
            lines.append(f"  -> {recommendation}")
    return "\n".join(lines)
