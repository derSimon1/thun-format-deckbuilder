from __future__ import annotations

import re
from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import CardAnalysis


_DAMAGE_PATTERN = re.compile(r"(?:deals?|deal)\s+(\d+)\s+damage")
_CONDITIONAL_PHRASES = (
    " if ",
    "unless ",
    "only if ",
    "as an additional cost",
    "sacrifice a",
    "discard a card",
    "coin flip",
)


@dataclass(frozen=True)
class ScoreBreakdown:
    score: float
    reasons: tuple[str, ...]


def _fixed_damage(text: str) -> int:
    amounts = [int(value) for value in _DAMAGE_PATTERN.findall(text)]
    return max(amounts, default=0)


def score_burn_card(
    analysis: CardAnalysis,
) -> ScoreBreakdown:
    score = 0.0
    reasons: list[str] = []

    text = f" {analysis.oracle_text.lower()} "
    mana_value = max(analysis.mana_value, 0.0)

    if mana_value <= 1:
        score += 4.0
        reasons.append("Mana Value ≤ 1")
    elif mana_value == 2:
        score += 3.0
        reasons.append("Mana Value 2")
    elif mana_value == 3:
        score += 1.5
        reasons.append("Mana Value 3")
    elif mana_value >= 4:
        score -= 1.0
        reasons.append("Hohe Manakosten")

    if analysis.is_instant:
        score += 1.5
        reasons.append("Instant")
    elif analysis.is_sorcery:
        score += 0.5
        reasons.append("Sorcery")

    hits_any_target = "any target" in text
    hits_player = any(
        phrase in text
        for phrase in (
            "target player",
            "target opponent",
            "each opponent",
        )
    )
    hits_creature = any(
        phrase in text
        for phrase in (
            "target creature",
            "each creature",
        )
    )

    if hits_any_target:
        score += 4.0
        reasons.append("Any Target")
    elif hits_player:
        score += 3.0
        reasons.append("Kann Spieler treffen")
    elif hits_creature:
        score += 0.5
        reasons.append("Nur Board-Interaktion")

    damage = _fixed_damage(text)
    if damage:
        score += float(damage)
        reasons.append(f"{damage} Schaden")

        efficiency = damage / max(mana_value, 1.0)
        if hits_any_target or hits_player:
            if efficiency >= 2.5:
                score += 2.5
                reasons.append("Sehr effizienter Face-Burn")
            elif efficiency >= 1.5:
                score += 1.5
                reasons.append("Effizienter Face-Burn")
            elif efficiency < 1.0:
                score -= 1.5
                reasons.append("Ineffizienter Burn")
    elif " x damage" in text and (hits_any_target or hits_player):
        score += 1.0
        reasons.append("Skalierbarer Burn")

    if analysis.is_creature:
        if "haste" in text:
            score += 1.5
            reasons.append("Haste")

        if analysis.power is not None and mana_value > 0:
            power_efficiency = analysis.power / mana_value
            if power_efficiency >= 2.0:
                score += 2.0
                reasons.append("Sehr effiziente Aggro-Kreatur")
            elif power_efficiency >= 1.0:
                score += 1.0
                reasons.append("Effiziente Aggro-Kreatur")

        if (
            "whenever you cast" in text
            and ("instant" in text or "noncreature" in text)
        ):
            score += 1.5
            reasons.append("Burn-Synergie")

        if (
            "{t}:" in text
            and "damage" in text
            and (hits_player or hits_any_target)
        ):
            score += 2.0
            reasons.append("Wiederholbarer Schaden")

    if "can't gain life" in text:
        score += 1.0
        reasons.append("Verhindert Lifegain")

    if "exile it instead" in text:
        score += 0.5
        reasons.append("Exile-Effekt")

    conditional_hits = sum(
        phrase in text for phrase in _CONDITIONAL_PHRASES
    )
    if conditional_hits:
        score -= min(3.0, 1.5 * conditional_hits)
        reasons.append("Bedingter oder zusätzlicher Aufwand")

    if "damage to you" in text:
        score -= 2.0
        reasons.append("Eigenschaden")

    return ScoreBreakdown(
        score=score,
        reasons=tuple(reasons),
    )


def score_artifact_card(
    analysis: CardAnalysis,
) -> ScoreBreakdown:
    score = 0.0
    reasons: list[str] = []
    text = f" {analysis.oracle_text.lower()} "
    mana_value = max(analysis.mana_value, 0.0)

    if analysis.is_artifact:
        score += 2.0
        reasons.append("Artefakt")
        if mana_value <= 1:
            score += 3.0
            reasons.append("Sehr günstiger Enabler")
        elif mana_value <= 2:
            score += 2.0
            reasons.append("Günstiger Enabler")
        elif mana_value >= 5:
            score -= 2.0
            reasons.append("Teures Artefakt")

    mechanic_hits = {
        "affinity for artifacts": (4.0, "Affinity-Payoff"),
        "improvise": (3.5, "Improvise-Payoff"),
        "metalcraft": (2.5, "Metalcraft-Payoff"),
        "whenever an artifact enters": (3.5, "Artifactfall-Payoff"),
        "whenever another artifact enters": (3.5, "Artifactfall-Payoff"),
        "for each artifact you control": (3.0, "Artefakt-Skalierung"),
        "artifacts you control get": (3.0, "Artefakt-Anthem"),
        "sacrifice an artifact": (2.5, "Artefakt-Sacrifice-Synergie"),
    }
    for phrase, (bonus, reason) in mechanic_hits.items():
        if phrase in text:
            score += bonus
            reasons.append(reason)

    token_types = tuple(
        token
        for token in ("treasure", "clue", "blood", "powerstone", "food")
        if token in text
    )
    if "create" in text and token_types:
        score += 2.0 + min(1.5, 0.5 * len(token_types))
        reasons.append("Erzeugt Artefakt-Spielsteine")

    if analysis.is_artifact and "draw a card" in text:
        score += 1.5
        reasons.append("Artefakt mit Kartennachschub")

    if analysis.is_creature and analysis.power is not None and mana_value > 0:
        if analysis.power / mana_value >= 1.0:
            score += 1.0
            reasons.append("Effizienter Körper")

    payoff_phrases = (
        "affinity for artifacts",
        "improvise",
        "metalcraft",
        "whenever an artifact enters",
        "whenever another artifact enters",
        "for each artifact you control",
        "artifacts you control get",
        "sacrifice an artifact",
    )
    has_payoff = any(phrase in text for phrase in payoff_phrases)
    has_utility = any(
        phrase in text
        for phrase in (
            "draw a card",
            "create",
            "add {",
            "destroy target",
            "exile target",
        )
    )
    if (
        analysis.is_artifact
        and mana_value >= 4
        and not has_payoff
        and not has_utility
    ):
        score -= 3.0
        reasons.append("Teures Artefakt ohne Synergie")

    return ScoreBreakdown(
        score=score,
        reasons=tuple(reasons),
    )