from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.tournament_simulator import BestOfThreeReport


@dataclass(frozen=True)
class CalibrationRecommendation:
    archetype: str
    priority: str
    message: str


def recommend_calibrations(report: BestOfThreeReport) -> tuple[CalibrationRecommendation, ...]:
    recommendations: list[CalibrationRecommendation] = []
    for archetype, opponent, impacts, plan, postboard_win in (
        (report.archetype_a, report.archetype_b, report.impacts_a, report.plan_a, report.postboard.wins_a_pct),
        (report.archetype_b, report.archetype_a, report.impacts_b, report.plan_b, report.postboard.wins_b_pct),
    ):
        if impacts:
            best = max(impacts, key=lambda item: (item.win_rate_delta, item.card_in))
            recommendations.append(CalibrationRecommendation(
                archetype,
                "HIGH" if best.win_rate_delta >= 5 else "MEDIUM",
                f"Gegen {opponent}: {best.card_in} zeigte +{best.win_rate_delta} Prozentpunkte; mehr Kopien oder Mainboard-Einsatz prüfen.",
            ))
            repeated_out = sorted({name for name, qty in plan.cards_out if qty >= 2})
            for name in repeated_out:
                recommendations.append(CalibrationRecommendation(
                    archetype,
                    "MEDIUM",
                    f"{name} wird gegen {opponent} mehrfach ausgeboardet; Score oder Mainboard-Anzahl senken.",
                ))
        else:
            recommendations.append(CalibrationRecommendation(
                archetype,
                "HIGH" if postboard_win < 40 else "LOW",
                f"Gegen {opponent} fand der Optimizer keinen positiven Sideboard-Tausch; neue Hate-Kategorie ergänzen.",
            ))
        if postboard_win < 40:
            recommendations.append(CalibrationRecommendation(
                archetype,
                "HIGH",
                f"Postboard nur {postboard_win}% gegen {opponent}; mindestens drei gezielte Sideboard-Slots hinzufügen.",
            ))
    return tuple(recommendations)


def format_calibration_recommendations(report: BestOfThreeReport) -> str:
    lines = ["CALIBRATION RECOMMENDATIONS", "-" * 72]
    for item in recommend_calibrations(report):
        lines.append(f"[{item.priority}] {item.archetype}: {item.message}")
    return "\n".join(lines)
