from __future__ import annotations

import re

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown


_MILL_NUMBER_PATTERN = re.compile(r"mills?\s+(\d+)\s+cards?")


def score_mill_card(analysis: CardAnalysis) -> ScoreBreakdown:
    score = 0.0
    reasons: list[str] = []
    text = f" {analysis.oracle_text.lower()} "
    mana_value = max(analysis.mana_value, 0.0)

    amounts = [int(value) for value in _MILL_NUMBER_PATTERN.findall(text)]
    fixed_mill = max(amounts, default=0)
    targets_opponent = any(
        phrase in text
        for phrase in (
            "target opponent mills",
            "each opponent mills",
            "target player mills",
        )
    )

    if fixed_mill and targets_opponent:
        score += float(fixed_mill)
        reasons.append(f"Millt {fixed_mill} Karten")
        efficiency = fixed_mill / max(mana_value, 1.0)
        if efficiency >= 4.0:
            score += 3.0
            reasons.append("Sehr effizientes Mill")
        elif efficiency >= 2.5:
            score += 2.0
            reasons.append("Effizientes Mill")
        elif efficiency < 1.5:
            score -= 1.5
            reasons.append("Ineffizientes Mill")

    if any(
        phrase in text
        for phrase in (
            "half that library",
            "half their library",
            "until they reveal",
            "for each card in their graveyard",
            "equal to the number of cards in",
        )
    ):
        score += 3.0
        reasons.append("Skalierendes Mill")

    if "whenever" in text and "mills" in text and targets_opponent:
        score += 3.0
        reasons.append("Wiederholbares Mill")
    if "at the beginning" in text and "mills" in text and targets_opponent:
        score += 2.0
        reasons.append("Permanente Mill-Quelle")

    if "draw a card" in text:
        score += 1.5
        reasons.append("Kartennachschub")
    if analysis.is_instant:
        score += 0.75
        reasons.append("Instant")
    if any(phrase in text for phrase in ("destroy target creature", "exile target creature", "counter target spell")):
        score += 1.5
        reasons.append("Defensive Interaktion")

    if "cards in your graveyard" in text or "you mill" in text or "mill yourself" in text:
        score -= 2.5
        reasons.append("Self-Mill statt Gegner-Mill")
    if mana_value >= 5 and not any(reason in reasons for reason in ("Skalierendes Mill", "Wiederholbares Mill", "Permanente Mill-Quelle")):
        score -= 2.0
        reasons.append("Teure Mill-Karte ohne Skalierung")
    if not targets_opponent and "mill" in text:
        score -= 1.0
        reasons.append("Kein zuverlässiges Gegner-Mill")

    return ScoreBreakdown(score=score, reasons=tuple(reasons))
