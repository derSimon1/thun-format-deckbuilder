from __future__ import annotations

import re
from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import (
    CardAnalysis,
    cast_accessible_effect_segments,
)


_NUMBER_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}
_AMOUNT = r"([a-z]+|\d+)"
_FIXED_MILL_PATTERN = re.compile(
    rf"(?:target opponent|each opponent|target player) mills? {_AMOUNT} cards?"
)
_PUT_PATTERN = re.compile(
    rf"(?:target opponent|that player|they) puts? the top {_AMOUNT} cards? "
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
    immediate_cards: int
    repeatable_cards: int
    conditional_cards: int


def _amount(value: str) -> int:
    if value.isdigit():
        return int(value)
    return _NUMBER_WORDS.get(value, 0)


def _fixed_mill_cards(text: str) -> int:
    values = [_amount(value) for value in _FIXED_MILL_PATTERN.findall(text)]
    values.extend(_amount(value) for value in _PUT_PATTERN.findall(text))
    return max(values, default=0)


def _reusable_activation(segment: str) -> bool:
    for match in re.finditer(r":", segment):
        effect = segment[match.end() :]
        if not (_FIXED_MILL_PATTERN.search(effect) or _PUT_PATTERN.search(effect)):
            continue
        cost = segment[: match.start()].rsplit(".", 1)[-1]
        if (
            "sacrifice" in cost
            or "pay {e}" in cost
            or re.search(
                r"tap (?:two|three|four|five|\d+) untapped", cost
            )
        ):
            continue
        return True
    return False


def _has_mill_activation(segment: str) -> bool:
    return any(
        _FIXED_MILL_PATTERN.search(segment[match.end() :])
        or _PUT_PATTERN.search(segment[match.end() :])
        for match in re.finditer(r":", segment)
    )


def analyze_mill(analysis: CardAnalysis) -> MillSignals:
    """Classify real opponent-mill sources without counting self-mill."""

    segments = cast_accessible_effect_segments(analysis)
    text = " ".join(" ".join(segments).split())
    fixed_cards = _fixed_mill_cards(text)

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
    immediate_cards = 0
    repeatable_cards = 0
    conditional_cards = 0
    for segment in segments:
        amount = _fixed_mill_cards(segment)
        if amount <= 0:
            continue
        repeatable = any(
            phrase in segment for phrase in _REPEATABLE_PHRASES
        ) or _reusable_activation(segment)
        if repeatable:
            repeatable_cards = max(repeatable_cards, amount)
        elif _has_mill_activation(segment):
            conditional_cards = max(conditional_cards, amount)
        else:
            immediate_cards = max(immediate_cards, amount)
    engine = source and repeatable_cards > 0
    return MillSignals(
        source=source,
        engine=engine,
        scalable=scalable,
        fixed_cards=fixed_cards,
        opponent_focused=explicit_opponent,
        immediate_cards=immediate_cards,
        repeatable_cards=repeatable_cards,
        conditional_cards=conditional_cards,
    )


def simulation_metadata_roles(analysis: CardAnalysis) -> tuple[str, ...]:
    """Return mill throughput metadata for deterministic simulation."""

    signals = analyze_mill(analysis)
    roles: list[str] = []
    if signals.immediate_cards:
        roles.append(f"mill_immediate_{signals.immediate_cards}")
    if signals.repeatable_cards:
        roles.append(f"mill_repeatable_{signals.repeatable_cards}")
    if signals.conditional_cards:
        roles.append(f"mill_conditional_{signals.conditional_cards}")
    return tuple(roles)
