from __future__ import annotations

import re

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_scoring import ScoreBreakdown


_DAMAGE_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
}


def estimated_direct_damage(text: str) -> int | None:
    """Estimate the smallest explicit amount of direct damage dealt.

    ``None`` denotes scalable damage such as X damage or damage based on another
    game value.  Zero means that no direct-damage sentence was detected.
    """

    lowered = text.lower()
    if "deal" not in lowered or "damage" not in lowered:
        return 0
    if any(
        phrase in lowered
        for phrase in (
            "deals x damage",
            "damage equal to",
            "damage for each",
            "damage where x is",
        )
    ):
        return None

    matches = re.findall(
        r"deals? (one|two|three|four|five|six|\d+) damage",
        lowered,
    )
    if not matches:
        return 0
    values = [
        _DAMAGE_WORDS.get(token, int(token) if token.isdigit() else 0)
        for token in matches
    ]
    return min(values)


def _can_hit_opponent(text: str) -> bool:
    return any(
        phrase in text
        for phrase in (
            "any target",
            "target player",
            "target opponent",
            "each opponent",
            "each player",
        )
    )


def _is_repeatable_damage(text: str) -> bool:
    return "damage" in text and any(
        phrase in text
        for phrase in (
            "at the beginning of",
            "whenever",
            "{t}:",
            "you may pay",
        )
    )


def score_burn_card(analysis: CardAnalysis) -> ScoreBreakdown:
    """Score a card for a proactive mono-red Burn deck.

    The calibration rewards efficient, reliable face damage and early pressure.
    Creature-only removal, symmetrical damage, slow conditional effects and
    expensive low-impact cards are deliberately discounted.
    """

    score = 0.0
    reasons: list[str] = []
    text = analysis.oracle_text.lower()
    mana_value = analysis.mana_value

    curve_scores = {0: 1.0, 1: 5.0, 2: 4.0, 3: 1.5}
    score += curve_scores.get(int(mana_value), -3.0 if mana_value >= 4 else 0.0)
    if mana_value <= 1:
        reasons.append("Sehr effizienter früher Spielzug")
    elif mana_value == 2:
        reasons.append("Effizienter Burn-Kurvenpunkt")
    elif mana_value >= 4:
        reasons.append("Zu hohe Manakosten für Burn")

    damage = estimated_direct_damage(text)
    hits_opponent = _can_hit_opponent(text)
    if damage is None:
        score += 2.0 if hits_opponent else 0.5
        reasons.append("Skalierbarer Schaden")
    elif damage > 0:
        rate = damage / max(mana_value, 1)
        score += min(6.0, float(damage))
        if rate >= 2:
            score += 3.0
            reasons.append("Hervorragende Schadensrate")
        elif rate >= 1.5:
            score += 2.0
            reasons.append("Gute Schadensrate")
        elif rate < 1 and mana_value >= 3:
            score -= 3.0
            reasons.append("Schwache Schadensrate")

    if hits_opponent:
        score += 4.0
        reasons.append("Kann den Gegner direkt treffen")
    elif "target creature" in text or "target planeswalker" in text:
        score -= 2.5
        reasons.append("Nur Board-Interaktion, kein Reach")

    if "any target" in text:
        score += 1.5
        reasons.append("Flexible Zielwahl")
    if analysis.is_instant:
        score += 1.5
        reasons.append("Instant-Geschwindigkeit")
    if _is_repeatable_damage(text) and hits_opponent:
        score += 3.0
        reasons.append("Wiederholbarer Schaden")

    if analysis.is_creature:
        power = analysis.power or 0
        if mana_value <= 2 and power >= 2:
            score += 3.0
            reasons.append("Früher aggressiver Körper")
        elif mana_value >= 3 and power <= mana_value:
            score -= 2.0
            reasons.append("Zu wenig Druck für die Manakosten")
        if any(keyword in text for keyword in ("haste", "menace", "first strike")):
            score += 1.5
            reasons.append("Aggressives Kreaturen-Keyword")

    if "draw a card" in text or "exile the top card" in text:
        score += 1.5
        reasons.append("Kartennachschub")
    if "can't gain life" in text or "players can't gain life" in text:
        score += 2.0
        reasons.append("Stoppt Lifegain")

    if any(
        phrase in text
        for phrase in (
            "deals damage to you",
            "deals that much damage to you",
            "damage to each player",
            "damage to each creature and each player",
        )
    ):
        score -= 3.0
        reasons.append("Symmetrischer oder eigener Schaden")

    if any(
        phrase in text
        for phrase in (
            "if a creature died this turn",
            "if you've cast another spell",
            "unless that player",
            "only if",
        )
    ):
        score -= 1.5
        reasons.append("Bedingter Effekt")

    if "sacrifice a creature" in text and not hits_opponent:
        score -= 2.0
        reasons.append("Zusätzliche Ressourcenkosten ohne sicheren Reach")

    return ScoreBreakdown(score=score, reasons=tuple(reasons))
