from __future__ import annotations

import math
import random
from dataclasses import dataclass

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck
from thun_deckbuilder.goldfish_simulator import GoldfishReport, GoldfishSimulator


@dataclass(frozen=True)
class MatchupReport:
    archetype_a: str
    archetype_b: str
    samples: int
    wins_a_pct: int
    wins_b_pct: int
    draws_pct: int
    average_score_a: float
    average_score_b: float


def _text(entry: DeckEntry) -> str:
    return " ".join((entry.name, entry.type_line, *entry.roles, *entry.reasons)).lower()


def _interaction_density(deck: GeneratedDeck) -> float:
    count = 0
    for entry in deck.mainboard:
        text = _text(entry)
        if any(
            phrase in text
            for phrase in (
                "removal",
                "counter",
                "destroy",
                "exile",
                "gets -",
                "return target creature",
                "damage to target creature",
            )
        ):
            count += entry.quantity
    return count / max(1, sum(item.quantity for item in deck.mainboard))


def _threat_density(deck: GeneratedDeck) -> float:
    count = sum(
        entry.quantity
        for entry in deck.mainboard
        if "creature" in entry.type_line.lower()
        or "shrine" in entry.type_line.lower()
        or "artifact" in entry.type_line.lower()
    )
    return count / max(1, sum(item.quantity for item in deck.mainboard))


def _lethal_race_progress(report: GoldfishReport) -> float:
    """Measure damage-plan pressure with diminishing returns after lethal.

    Damage up to 20 remains linear because it describes reaching lethal. Excess
    damage still signals speed and reach, but receives only logarithmic credit
    so a 40-damage goldfish does not count as twice as successful as a lethal
    20-damage goldfish. Kill rate contributes a smaller consistency bonus.
    """

    ratio = max(0.0, report.average_damage / 20.0)
    if ratio <= 1.0:
        damage_progress = ratio
    else:
        damage_progress = 1.0 + 0.25 * math.log2(ratio)
    kill_consistency = min(1.0, max(0.0, report.kill_by_final_turn_pct / 100.0))
    return damage_progress + 0.2 * kill_consistency


def _base_progress(report: GoldfishReport, archetype: str) -> float:
    if archetype in {"burn", "tokens"}:
        return _lethal_race_progress(report)
    if archetype == "mill":
        return report.average_cards_milled / 53.0
    if archetype == "artifacts":
        return report.average_artifacts_in_play / 5.0
    if archetype == "shrines":
        return report.average_shrines_in_play / 4.0
    return report.average_spells_cast / 7.0


class MatchupSimulator:
    """Compare two generated decks under simplified mutual interaction.

    This is intentionally a deterministic heuristic model rather than a full
    Magic rules engine. Goldfish progress supplies each deck's proactive plan;
    interaction density suppresses opposing progress and threat density helps a
    deck recover from disruption.
    """

    def simulate(
        self,
        deck_a: GeneratedDeck,
        deck_b: GeneratedDeck,
        *,
        archetype_a: str,
        archetype_b: str,
        samples: int = 2000,
        seed: int = 41,
    ) -> MatchupReport:
        if samples <= 0:
            raise ValueError("samples must be positive")

        goldfish = GoldfishSimulator()
        report_a = deck_a.goldfish_report or goldfish.simulate(deck_a, archetype=archetype_a)
        report_b = deck_b.goldfish_report or goldfish.simulate(deck_b, archetype=archetype_b)

        progress_a = _base_progress(report_a, archetype_a)
        progress_b = _base_progress(report_b, archetype_b)
        interaction_a = _interaction_density(deck_a)
        interaction_b = _interaction_density(deck_b)
        threats_a = _threat_density(deck_a)
        threats_b = _threat_density(deck_b)

        rng = random.Random(seed)
        wins_a = wins_b = draws = 0
        total_a = total_b = 0.0
        for _ in range(samples):
            variance_a = rng.uniform(-0.12, 0.12)
            variance_b = rng.uniform(-0.12, 0.12)
            resilience_a = threats_a * 0.18
            resilience_b = threats_b * 0.18
            score_a = progress_a + resilience_a - interaction_b * 0.65 + variance_a
            score_b = progress_b + resilience_b - interaction_a * 0.65 + variance_b
            total_a += score_a
            total_b += score_b
            margin = score_a - score_b
            if margin > 0.025:
                wins_a += 1
            elif margin < -0.025:
                wins_b += 1
            else:
                draws += 1

        pct = lambda value: round(value * 100 / samples)
        return MatchupReport(
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=samples,
            wins_a_pct=pct(wins_a),
            wins_b_pct=pct(wins_b),
            draws_pct=pct(draws),
            average_score_a=round(total_a / samples, 3),
            average_score_b=round(total_b / samples, 3),
        )
