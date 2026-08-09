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
}


@dataclass(frozen=True)
class ControlSignals:
    reliable_answer: bool
    conditional_answer: bool
    card_advantage: bool
    selection: bool
    sweeper: bool
    finisher: bool


def _number(value: str) -> int:
    return int(value) if value.isdigit() else _NUMBER_WORDS.get(value, 0)


def _draw_delta(segment: str) -> int:
    draws = [
        _number(value)
        for value in re.findall(
            r"draw (a|an|one|two|three|four|five|six|seven|\d+) cards?",
            segment,
        )
    ]
    discards = [
        _number(value)
        for value in re.findall(
            r"discard (a|an|one|two|three|four|five|six|seven|\d+) cards?",
            segment,
        )
    ]
    return max(draws, default=0) - max(discards, default=0)


def analyze_control(analysis: CardAnalysis) -> ControlSignals:
    """Classify control answers, resources, and win conditions conservatively."""

    segments = cast_accessible_effect_segments(analysis)
    text = " ".join(segments)
    sweeper = any(
        phrase in text
        for phrase in (
            "destroy all creatures",
            "exile all creatures",
            "all creatures get -",
            "each creature gets -",
            "return all creatures",
        )
    )
    answer_segments: list[tuple[str, bool]] = []
    for segment in segments:
        counter = "counter target spell" in segment
        removal = any(
            phrase in segment
            for phrase in (
                "destroy target creature",
                "exile target creature",
                "return target creature",
                "target creature gets -",
            )
        )
        if not counter and not removal:
            continue
        invalid_removal = removal and any(
            phrase in segment
            for phrase in (
                "creature you control",
                "creature card from a graveyard",
                "creature card in a graveyard",
            )
        )
        if invalid_removal and not counter:
            continue
        conditional = any(
            phrase in segment
            for phrase in (
                "was dealt damage this turn",
                "less than or equal to the number of cards",
                "with power or toughness 1 or less",
                "counter target sorcery spell",
            )
        )
        answer_segments.append((segment, conditional or invalid_removal))

    reliable_answer = sweeper or any(
        not conditional for _, conditional in answer_segments
    )
    conditional_answer = any(
        conditional for _, conditional in answer_segments
    )
    card_advantage = any(_draw_delta(segment) >= 2 for segment in segments) or (
        "draw a card" in text
        and any(
            phrase in text
            for phrase in ("whenever", "at the beginning of your upkeep")
        )
    )
    selection = any(
        phrase in text
        for phrase in (
            "cycling",
            "surveil",
            "scry",
            "look at the top",
            "draw a card",
        )
    ) or ("draw" in text and "discard" in text)
    finisher = (
        analysis.is_planeswalker
        or (analysis.is_creature and 5 <= analysis.mana_value <= 7)
        or any(
            phrase in text
            for phrase in (
                "create a token at the beginning",
                "whenever an opponent loses life",
            )
        )
    )
    return ControlSignals(
        reliable_answer=reliable_answer,
        conditional_answer=conditional_answer,
        card_advantage=card_advantage,
        selection=selection,
        sweeper=sweeper,
        finisher=finisher,
    )
