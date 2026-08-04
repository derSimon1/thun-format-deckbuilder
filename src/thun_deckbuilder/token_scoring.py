from __future__ import annotations

import re

from thun_deckbuilder.card_analyzer import CardAnalysis, cast_accessible_oracle_text
from thun_deckbuilder.card_scoring import ScoreBreakdown
from thun_deckbuilder.token_plan import TokenPlan, token_card_signals


_NUMBER_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
}


def estimated_token_output(text: str) -> int | None:
    """Return the smallest explicit number of tokens created by the card.

    ``None`` represents variable output (for example ``create X`` or
    ``for each``). The conservative minimum is used because overestimating a
    conditional token card was a recurring source of poor White Tokens picks.
    """

    lowered = text.lower()
    if "create" not in lowered or "token" not in lowered:
        return 0
    if "create x" in lowered or "for each" in lowered:
        return None

    matches = re.findall(
        r"create (?:up to )?(a|an|one|two|three|four|five|six|\d+) "
        r"[^.\n]*?tokens?",
        lowered,
    )
    if not matches:
        return 1

    values = [
        _NUMBER_WORDS.get(token, int(token) if token.isdigit() else 1)
        for token in matches
    ]
    return min(values)


def _is_repeatable_token_source(text: str) -> bool:
    return "create" in text and "token" in text and any(
        phrase in text
        for phrase in (
            "at the beginning of",
            "whenever one or more",
            "whenever another",
            "whenever a creature",
            "whenever you attack",
            "whenever this creature attacks",
            "{t}: create",
        )
    )


def _is_global_anthem(text: str) -> bool:
    return any(
        phrase in text
        for phrase in (
            "creatures you control get +",
            "other creatures you control get +",
            "tokens you control get +",
            "creature tokens you control get +",
        )
    )


def score_token_card(
    analysis: CardAnalysis,
    plan: TokenPlan = TokenPlan.GO_WIDE,
) -> ScoreBreakdown:
    """Score a token card for one explicitly selected strategic plan.

    The shared base rewards efficient board development. Plan-specific signals
    then reward commitment to Go Wide, Value Tokens, or Aristocrats and discount
    packages that pull the deck in a different direction.
    """

    score = 0.0
    reasons: list[str] = []
    text = cast_accessible_oracle_text(analysis).lower()
    mana_value = analysis.mana_value

    curve_scores = {0: 2.0, 1: 5.0, 2: 5.0, 3: 3.5, 4: 1.5, 5: 0.0}
    score += curve_scores.get(int(mana_value), -2.0 if mana_value >= 6 else 0.0)
    if mana_value <= 2:
        reasons.append("Effizienter früher Spielzug")
    elif mana_value == 3:
        reasons.append("Passt in den zentralen Kurvenbereich")
    elif mana_value >= 5:
        reasons.append("Hohe Manakosten")

    token_output = estimated_token_output(text)
    if token_output is None:
        score += 2.0
        reasons.append("Skalierende Token-Erzeugung")
    elif token_output >= 3:
        score += 5.0
        reasons.append("Erzeugt mindestens drei Tokens")
    elif token_output == 2:
        score += 4.0
        reasons.append("Erzeugt zwei Tokens")
    elif token_output == 1:
        score += 1.0
        reasons.append("Erzeugt einen Token")

    if token_output and mana_value > 0:
        token_rate = token_output / mana_value
        if token_rate >= 1:
            score += 2.0
            reasons.append("Gute Token-Ausbeute pro Mana")
        elif mana_value >= 4 and token_output == 1:
            score -= 3.0
            reasons.append("Zu wenig Board-Präsenz für die Manakosten")

    if _is_repeatable_token_source(text):
        score += 4.0
        reasons.append("Wiederholbare Token-Quelle")

    if _is_global_anthem(text):
        if "until end of turn" in text:
            score += 1.0
            reasons.append("Temporärer Team-Bonus")
        else:
            score += 4.0
            reasons.append("Dauerhafter Team-Bonus")

    if "put a +1/+1 counter on each" in text:
        score += 3.5
        reasons.append("Dauerhafte Verstärkung des gesamten Boards")

    if any(
        phrase in text
        for phrase in (
            "whenever a token enters",
            "whenever one or more tokens",
            "for each token you control",
            "creature tokens you control have",
        )
    ):
        score += 3.0
        reasons.append("Direkter Token-Payoff")

    if "draw a card" in text and any(
        phrase in text for phrase in ("whenever", "when one or more", "for each")
    ):
        score += 2.5
        reasons.append("Wiederholbarer Kartennachschub")

    if analysis.is_instant:
        score += 0.5
        reasons.append("Instant-Geschwindigkeit")
    if analysis.is_creature:
        score += 1.0
        reasons.append("Zusätzlicher Körper")

    if any(phrase in text for phrase in ("destroy all creatures", "exile all creatures")):
        score -= 7.0
        reasons.append("Widerspricht dem eigenen Token-Spielplan")

    if "token that's a copy" in text and any(
        phrase in text
        for phrase in ("opponent", "you don't control", "target creature")
    ):
        score -= 5.0
        reasons.append("Unzuverlässiger gegnerabhängiger Kopiereffekt")

    if "sacrifice a creature" in text and "create" not in text:
        score -= 2.0
        reasons.append("Verbraucht das eigene Board ohne Token-Ersatz")

    signals = token_card_signals(analysis)
    if plan is TokenPlan.GO_WIDE:
        if signals.creates_multiple_tokens:
            score += 1.5
            reasons.append("Go Wide: mehrere Körper")
        if signals.anthem or signals.evasion_payoff:
            score += 2.0
            reasons.append("Go Wide: Team-Finisher")
        if signals.sacrifice and not signals.creates_tokens:
            score -= 2.0
            reasons.append("Go Wide: planfremdes Opferpaket")
    elif plan is TokenPlan.VALUE:
        if signals.repeatable_source:
            score += 3.0
            reasons.append("Value Tokens: wiederholbare Engine")
        if signals.card_advantage:
            score += 2.5
            reasons.append("Value Tokens: Kartenvorteil")
        if signals.token_value_payoff:
            score += 2.0
            reasons.append("Value Tokens: Token-Value-Payoff")
        if signals.sacrifice and not signals.death_payoff:
            score -= 1.0
            reasons.append("Value Tokens: ungestütztes Opferpaket")
    else:
        if signals.sacrifice:
            score += 5.0
            reasons.append("Aristocrats: Opfermöglichkeit")
        if signals.death_payoff:
            score += 4.0
            reasons.append("Aristocrats: Todestrigger")
        if signals.drain_payoff:
            score += 3.0
            reasons.append("Aristocrats: Drain-Finisher")
        if signals.anthem and not signals.death_payoff:
            score -= 1.5
            reasons.append("Aristocrats: planfremder Anthem-Payoff")

    return ScoreBreakdown(score=score, reasons=tuple(reasons))
