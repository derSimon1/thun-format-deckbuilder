from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import CardAnalysis


@dataclass(frozen=True)
class ScoreBreakdown:
    score: float
    reasons: tuple[str, ...]


def score_burn_card(
    analysis: CardAnalysis,
) -> ScoreBreakdown:
    score = 0.0
    reasons: list[str] = []

    text = analysis.oracle_text.lower()

    if analysis.mana_value <= 1:
        score += 5
        reasons.append("Mana Value ≤ 1")

    elif analysis.mana_value == 2:
        score += 4
        reasons.append("Mana Value 2")

    elif analysis.mana_value == 3:
        score += 2
        reasons.append("Mana Value 3")

    if analysis.is_instant:
        score += 2
        reasons.append("Instant")

    if "any target" in text:
        score += 3
        reasons.append("Any Target")

    if (
        "target player" in text
        or "target opponent" in text
    ):
        score += 2
        reasons.append("Kann Spieler treffen")

    if "target creature" in text:
        score += 1
        reasons.append("Kann Kreaturen treffen")

    if "4 damage" in text:
        score += 3
        reasons.append("4 Schaden")

    elif "3 damage" in text:
        score += 2
        reasons.append("3 Schaden")

    elif "2 damage" in text:
        score += 1
        reasons.append("2 Schaden")

    if "can't gain life" in text:
        score += 1
        reasons.append("Verhindert Lifegain")

    return ScoreBreakdown(
        score=score,
        reasons=tuple(reasons),
    )