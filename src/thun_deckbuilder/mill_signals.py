from __future__ import annotations

import re
from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import CardAnalysis


_FIXED_MILL_PATTERN = re.compile(
    r"(?:target opponent|each opponent|target player) mills? (\d+) cards?"
)
_PUT_PATTERN = re.compile(
    r"(?:target opponent|that player|they) puts? the top (\d+) cards? "
    r"of (?:their|that player's) library into (?:their|that player's) graveyard"
)
_SCALING_PHRASES = (
    "half that library",
    "half their library",
    "equal to the number of cards in",
    "for each card in their graveyard",
    "until they reveal",
)
_REPEATABLE_PHRASES = (
    "whenever",
    "at the beginning",
    "each upkeep",
    "each end step",
)


@dataclass(frozen=True)
class MillSignals:
    """Canonical opponent-mill classification shared by all quality systems."""

    source: bool
    engine: bool
    scalable: bool
    fixed_cards: int
    opponent_focused: bool


def analyze_mill(analysis: CardAnalysis) -> MillSignals:
    """Classify real opponent-mill sources without counting self-mill."""

    text = " ".join(analysis.oracle_text.lower().split())
    fixed_values = [int(value) for value in _FIXED_MILL_PATTERN.findall(text)]
    fixed_values.extend(int(value) for value in _PUT_PATTERN.findall(text))
    fixed_cards = max(fixed_values, default=0)

    explicit_opponent = any(
        phrase in text
        for phrase in (
            "target opponent mills",
            "each opponent mills",
            "target player mills",
            "target opponent puts the top",
            "that player puts the top",
            "they put the top",
            "library into their graveyard",
            "library into that player's graveyard",
        )
    )
    scalable = explicit_opponent and any(
        phrase in text for phrase in _SCALING_PHRASES
    )
    source = explicit_opponent and (
        fixed_cards > 0
        or scalable
        or "mills cards" in text
        or "mill that many" in text
    )
    permanent = any(
        card_type in analysis.type_line.lower()
        for card_type in ("creature", "artifact", "enchantment", "planeswalker")
    )
    engine = source and (
        any(phrase in text for phrase in _REPEATABLE_PHRASES)
        or permanent
    )
    return MillSignals(
        source=source,
        engine=engine,
        scalable=scalable,
        fixed_cards=fixed_cards,
        opponent_focused=explicit_opponent,
    )
