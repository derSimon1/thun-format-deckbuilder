from __future__ import annotations

import re
from dataclasses import dataclass

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.token_packages import analyze_token_package


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


@dataclass(frozen=True)
class TokenProductionProfile:
    creates_creature_tokens: bool = False
    minimum_output: int = 0
    variable_output: bool = False
    repeatable: bool = False
    delayed_by_death: bool = False
    conditional: bool = False

    @property
    def mode(self) -> str:
        if not self.creates_creature_tokens:
            return "none"
        if self.delayed_by_death:
            return "death"
        if self.conditional:
            return "conditional"
        if self.repeatable:
            return "repeatable"
        return "immediate"


def _sentences(text: str) -> tuple[str, ...]:
    return tuple(
        sentence.strip()
        for sentence in re.split(r"[.\n]", text.lower())
        if sentence.strip()
    )


def _is_creature_token_sentence(sentence: str) -> bool:
    if "create" not in sentence or "token" not in sentence:
        return False
    if "creature token" in sentence:
        return True
    return "token that's a copy" in sentence and "creature" in sentence


def _output_for_sentence(sentence: str) -> tuple[int, bool]:
    variable = any(
        phrase in sentence
        for phrase in (
            "create x ",
            "for each",
            "that many",
            "equal to",
            "where x",
        )
    )
    match = re.search(
        r"create (?:up to )?(a|an|one|two|three|four|five|six|\d+) "
        r"[^.\n]*?(?:creature tokens?|token that's a copy)",
        sentence,
    )
    if match is None:
        return 1, variable
    raw = match.group(1)
    value = _NUMBER_WORDS.get(raw, int(raw) if raw.isdigit() else 1)
    return max(1, value), variable


def _is_named_self_death(sentence: str, analysis: CardAnalysis) -> bool:
    if "dies" not in sentence:
        return False
    front_name = analysis.name.split(" // ", 1)[0].lower()
    return any(
        phrase in sentence
        for phrase in (
            "when this creature dies",
            "whenever this creature dies",
            "when this permanent dies",
            "whenever this permanent dies",
            f"when {front_name} dies",
            f"whenever {front_name} dies",
        )
    )


def analyze_token_production(analysis: CardAnalysis) -> TokenProductionProfile:
    """Classify creature-token production for conservative solitaire play."""

    sentences = tuple(
        sentence
        for sentence in _sentences(analysis.oracle_text)
        if _is_creature_token_sentence(sentence)
    )
    if not sentences:
        return TokenProductionProfile()

    outputs = tuple(_output_for_sentence(sentence) for sentence in sentences)
    package = analyze_token_package(analysis)
    delayed_by_death = any(
        _is_named_self_death(sentence, analysis) for sentence in sentences
    )
    conditional = any(
        any(
            phrase in sentence
            for phrase in (
                "if ",
                "unless ",
                "for each",
                "that many",
                "equal to",
                "where x",
                "target ",
                "its controller",
                "when transformed",
                "whenever",
            )
        )
        for sentence in sentences
    )
    return TokenProductionProfile(
        creates_creature_tokens=True,
        minimum_output=max(value for value, _ in outputs),
        variable_output=any(variable for _, variable in outputs),
        repeatable=package.repeatable_creature_source,
        delayed_by_death=delayed_by_death,
        conditional=conditional,
    )


def token_production_roles(analysis: CardAnalysis) -> tuple[str, ...]:
    """Encode production data as stable DeckEntry role markers."""

    profile = analyze_token_production(analysis)
    if not profile.creates_creature_tokens:
        return ()
    roles = {
        f"token_output_{min(profile.minimum_output, 9)}",
        f"token_production_{profile.mode}",
    }
    if profile.variable_output:
        roles.add("token_output_variable")
    return tuple(sorted(roles))
