from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping

from thun_deckbuilder.card_analyzer import (
    CardAnalysis,
    analyze_card,
    cast_accessible_oracle_text,
)
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
    activated: bool = False
    activation_mana: int = 0
    delayed_by_death: bool = False
    conditional: bool = False

    @property
    def mode(self) -> str:
        if not self.creates_creature_tokens:
            return "none"
        if self.delayed_by_death:
            return "death"
        if self.activated:
            return "activated"
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


def _activated_mana_cost(sentence: str) -> int | None:
    """Return a conservative mana cost for a token-producing activated ability."""

    if ":" not in sentence:
        return None
    cost, effect = sentence.split(":", 1)
    if not _is_creature_token_sentence(effect):
        return None
    mana = 0
    for symbol in re.findall(r"\{([^}]+)\}", cost.upper()):
        if symbol.isdigit():
            mana += int(symbol)
        elif symbol in {"T", "Q", "X"}:
            continue
        elif any(color in symbol.split("/") for color in "WUBRGC"):
            mana += 1
    return mana


def analyze_token_production(analysis: CardAnalysis) -> TokenProductionProfile:
    """Classify creature-token production for conservative solitaire play."""

    sentences = tuple(
        sentence
        for sentence in _sentences(cast_accessible_oracle_text(analysis))
        if _is_creature_token_sentence(sentence)
    )
    if not sentences:
        return TokenProductionProfile()

    outputs = tuple(_output_for_sentence(sentence) for sentence in sentences)
    package = analyze_token_package(analysis)
    activated_costs = tuple(
        cost
        for sentence in sentences
        if (cost := _activated_mana_cost(sentence)) is not None
    )
    activated = bool(activated_costs)
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
        repeatable=package.repeatable_creature_source and not activated,
        activated=activated,
        activation_mana=min(activated_costs, default=0),
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
    if profile.activated:
        roles.add(f"token_activation_mana_{min(profile.activation_mana, 9)}")
    return tuple(sorted(roles))


def build_token_production_capacity(
    raw_cards: Iterable[Mapping[str, object]],
    *,
    allowed_colors: frozenset[str] = frozenset({"W"}),
    max_copies: int = 3,
    max_mana_value: float = 6,
) -> dict[str, object]:
    """Measure legal production capacity before imposing production targets."""

    cards: list[dict[str, object]] = []
    distinct_by_mode: Counter[str] = Counter()
    minimum_output_by_mode: Counter[str] = Counter()
    seen: set[str] = set()

    for raw in raw_cards:
        analysis = analyze_card(dict(raw))
        key = analysis.name.casefold()
        if key in seen:
            continue
        seen.add(key)
        if analysis.is_land or analysis.mana_value > max_mana_value:
            continue
        if not set(analysis.color_identity).issubset(allowed_colors):
            continue
        profile = analyze_token_production(analysis)
        if not profile.creates_creature_tokens:
            continue
        distinct_by_mode[profile.mode] += 1
        minimum_output_by_mode[profile.mode] += profile.minimum_output
        cards.append(
            {
                "name": analysis.name,
                "mana_value": analysis.mana_value,
                "mode": profile.mode,
                "profile": asdict(profile),
            }
        )

    cards.sort(
        key=lambda item: (
            str(item["mode"]),
            float(item["mana_value"]),
            str(item["name"]),
        )
    )
    return {
        "distinct_cards": len(cards),
        "max_copies": max_copies,
        "distinct_by_mode": dict(sorted(distinct_by_mode.items())),
        "maximum_copies_by_mode": {
            mode: count * max_copies
            for mode, count in sorted(distinct_by_mode.items())
        },
        "minimum_output_capacity_by_mode": {
            mode: output * max_copies
            for mode, output in sorted(minimum_output_by_mode.items())
        },
        "cards": cards,
    }
