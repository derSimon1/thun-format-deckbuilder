from __future__ import annotations

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown


def score_token_card(
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
        score += 3
        reasons.append("Mana Value 3")
    elif analysis.mana_value == 4:
        score += 2
        reasons.append("Mana Value 4")
    elif analysis.mana_value == 5:
        score += 1
        reasons.append("Mana Value 5")

    if "create two" in text:
        score += 3
        reasons.append("Erzeugt mindestens zwei Tokens")
    elif "create three" in text:
        score += 4
        reasons.append("Erzeugt mindestens drei Tokens")
    elif "create a" in text or "create one" in text:
        score += 1
        reasons.append("Erzeugt einen Token")

    if "for each" in text:
        score += 2
        reasons.append("Skaliert mit dem Board")

    if "+1/+1" in text:
        score += 2
        reasons.append("Verstärkt Kreaturen")

    if "creatures you control get" in text:
        score += 3
        reasons.append("Teamweiter Bonus")

    if "lifelink" in text:
        score += 1
        reasons.append("Lifelink")

    if "vigilance" in text:
        score += 1
        reasons.append("Vigilance")

    if analysis.is_instant:
        score += 1
        reasons.append("Instant")

    if analysis.is_creature:
        score += 1
        reasons.append("Kreatur")

    return ScoreBreakdown(
        score=score,
        reasons=tuple(reasons),
    )