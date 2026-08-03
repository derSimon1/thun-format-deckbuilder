from __future__ import annotations

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown


def score_control_card(analysis: CardAnalysis) -> ScoreBreakdown:
    """Score cards for a conservative Dimir control reference plan."""

    score = 0.0
    reasons: list[str] = []
    text = analysis.oracle_text.lower()
    mana_value = max(analysis.mana_value, 0.0)

    is_counter = "counter target" in text
    is_targeted_removal = any(
        phrase in text
        for phrase in (
            "destroy target",
            "exile target",
            "return target creature",
            "target creature gets -",
        )
    )
    is_sweeper = any(
        phrase in text
        for phrase in (
            "destroy all creatures",
            "exile all creatures",
            "all creatures get -",
            "each creature gets -",
            "return all creatures",
        )
    )
    is_card_advantage = "draw two" in text or "draw three" in text or (
        "draw a card" in text
        and any(
            phrase in text
            for phrase in (
                "whenever",
                "at the beginning",
                "enters",
                "for each",
            )
        )
    )
    is_selection = any(phrase in text for phrase in ("surveil", "scry", "look at the top"))
    is_finisher = (
        analysis.is_creature and 5 <= mana_value <= 7
    ) or analysis.is_planeswalker or any(
        phrase in text
        for phrase in (
            "create a token at the beginning",
            "whenever you draw",
            "whenever an opponent",
        )
    )

    if is_counter:
        score += 7.0
        reasons.append("Counter target spell")
        if mana_value <= 2:
            score += 2.0
            reasons.append("Frühe Countermagic")
        elif mana_value >= 4:
            score -= 2.0
            reasons.append("Teure Countermagic")

    if is_targeted_removal:
        score += 6.0
        reasons.append("Control removal")
        if mana_value <= 2:
            score += 2.0
            reasons.append("Frühes Removal")
        elif mana_value >= 4:
            score -= 1.5
            reasons.append("Teures Removal")

    if is_sweeper:
        score += 8.0
        reasons.append("Sweeper")
        if 3 <= mana_value <= 5:
            score += 1.5
            reasons.append("Realistisches Stabilisierungsfenster")

    if is_card_advantage:
        score += 5.0
        reasons.append("Card advantage engine")
    elif "draw a card" in text:
        score += 2.0
        reasons.append("Card selection")

    if is_selection:
        score += 1.5
        reasons.append("Card selection")

    if analysis.is_instant and (is_counter or is_targeted_removal or "draw" in text):
        score += 1.0
        reasons.append("Instant-Speed")

    if is_finisher:
        score += 4.0
        reasons.append("Control-Finisher")
        if mana_value >= 8:
            score -= 3.0
            reasons.append("Zu teurer Finisher")

    if analysis.is_creature and mana_value <= 3 and not any(
        (is_targeted_removal, is_card_advantage, is_selection)
    ):
        score -= 4.0
        reasons.append("Generische frühe Kreatur ohne Control-Funktion")

    if mana_value >= 6 and not is_finisher and not is_sweeper:
        score -= 3.0
        reasons.append("Teure Karte ohne Abschluss- oder Stabilisierungseffekt")

    if not any(
        (
            is_counter,
            is_targeted_removal,
            is_sweeper,
            is_card_advantage,
            is_selection,
            is_finisher,
        )
    ):
        score -= 2.0
        reasons.append("Keine erkennbare Control-Funktion")

    return ScoreBreakdown(score=score, reasons=tuple(reasons))
