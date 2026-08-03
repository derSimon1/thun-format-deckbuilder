from __future__ import annotations

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown
from thun_deckbuilder.mill_signals import analyze_mill


def score_mill_card(analysis: CardAnalysis) -> ScoreBreakdown:
    score = 0.0
    reasons: list[str] = []
    text = f" {analysis.oracle_text.lower()} "
    mana_value = max(analysis.mana_value, 0.0)
    signals = analyze_mill(analysis)

    if signals.fixed_cards and signals.opponent_focused:
        score += float(signals.fixed_cards)
        reasons.append(f"Millt {signals.fixed_cards} Karten")
        efficiency = signals.fixed_cards / max(mana_value, 1.0)
        if efficiency >= 4.0:
            score += 3.0
            reasons.append("Sehr effizientes Mill")
        elif efficiency >= 2.5:
            score += 2.0
            reasons.append("Effizientes Mill")
        elif efficiency < 1.5:
            score -= 1.5
            reasons.append("Ineffizientes Mill")

    if signals.scalable:
        score += 3.0
        reasons.append("Skalierendes Mill")

    if signals.engine:
        score += 3.0
        reasons.append("Wiederholbares Mill")

    if "draw a card" in text:
        score += 1.5
        reasons.append("Kartennachschub")
    if analysis.is_instant:
        score += 0.75
        reasons.append("Instant")
    if any(
        phrase in text
        for phrase in (
            "destroy target creature",
            "exile target creature",
            "counter target spell",
        )
    ):
        score += 1.5
        reasons.append("Defensive Interaktion")

    if "cards in your graveyard" in text or "you mill" in text or "mill yourself" in text:
        score -= 2.5
        reasons.append("Self-Mill statt Gegner-Mill")
    if mana_value >= 5 and signals.source and not signals.scalable and not signals.engine:
        score -= 2.0
        reasons.append("Teure Mill-Karte ohne Skalierung")
    if "mill" in text and not signals.source:
        score -= 1.0
        reasons.append("Kein zuverlässiges Gegner-Mill")

    return ScoreBreakdown(score=score, reasons=tuple(reasons))
