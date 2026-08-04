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
}
_ARTIFACT_TOKEN_TYPES = (
    "blood",
    "clue",
    "food",
    "gold",
    "map",
    "powerstone",
    "servo",
    "thopter",
    "treasure",
)
_PAYOFF_PATTERNS = (
    "affinity for artifacts",
    "metalcraft",
    "for each artifact you control",
    "artifacts you control get",
    "whenever an artifact enters",
    "whenever another artifact enters",
    "whenever you sacrifice an artifact",
    "sacrifice an artifact:",
)


@dataclass(frozen=True)
class ArtifactSignals:
    artifact_card: bool
    enabler: bool
    payoff: bool
    engine: bool
    immediate_artifacts: int
    conditional_artifacts: int
    repeatable_artifacts: int


def _number(raw: str) -> int:
    return int(raw) if raw.isdigit() else _NUMBER_WORDS.get(raw, 1)


def _artifact_token_output(segment: str) -> int:
    investigate_output = (
        segment.count("investigate")
        if "create a clue token" not in segment
        else 0
    )
    outputs: list[int] = []
    token_types = "|".join(_ARTIFACT_TOKEN_TYPES)
    for match in re.finditer(
        rf"create (?:up to )?(a|an|one|two|three|four|five|six|\d+) "
        rf"[^.\n]*?(?:{token_types})(?: artifact)?(?: creature)? tokens?",
        segment,
    ):
        outputs.append(_number(match.group(1)))
    if " instead" in segment and outputs:
        return investigate_output + min(outputs)
    return investigate_output + sum(outputs)


def _is_payoff(segment: str) -> bool:
    named_only = (
        "for each artifact you control" in segment
        and "artifact you control named" in segment
    )
    return bool(
        re.search(r"\bimprovise\b", segment)
        or any(
            pattern in segment
            for pattern in _PAYOFF_PATTERNS
            if pattern != "for each artifact you control" or not named_only
        )
    )


def _production_mode(segment: str, effect_index: int) -> str:
    prefix = segment[:effect_index]
    if re.search(r"when this [^.\n]{0,50} enters", prefix):
        return "immediate"
    if "dies" in prefix or "is put into a graveyard" in prefix:
        return "conditional"
    if ":" in prefix and "sacrifice this artifact" in prefix:
        return "conditional"
    if "combat damage" in prefix:
        return "conditional"
    if ":" in prefix or "whenever" in prefix or "at the beginning" in prefix:
        return "repeatable"
    if any(marker in prefix for marker in ("if ", "when ", "combat damage")):
        return "conditional"
    return "immediate"


def analyze_artifact(analysis: CardAnalysis) -> ArtifactSignals:
    """Return the shared Artifact enabler, engine, and payoff semantics."""

    front_type_line = analysis.type_line.split(" // ", 1)[0].lower()
    artifact_card = "artifact" in front_type_line
    immediate = 1 if artifact_card else 0
    conditional = repeatable = 0
    payoff = False
    repeatable_payoff = False
    segments = cast_accessible_effect_segments(analysis)
    for index, segment in enumerate(segments):
        payoff_hit = _is_payoff(segment)
        payoff = payoff or payoff_hit
        repeatable_payoff = repeatable_payoff or (
            payoff_hit and ("whenever" in segment or ":" in segment)
        )
        output = _artifact_token_output(segment)
        if not output:
            continue
        effect_positions = tuple(
            position
            for marker in ("create", "investigate")
            if (position := segment.find(marker)) >= 0
        )
        mode_segment = segment
        effect_index = min(effect_positions, default=0)
        table_result = re.match(r"^\d+[—-]\d+\s*\|", segment)
        activation_context = next(
            (prior for prior in reversed(segments[:index]) if ":" in prior),
            "",
        )
        if table_result and activation_context:
            mode_segment = f"{activation_context} {segment}"
            effect_index += len(activation_context) + 1
        mode = _production_mode(mode_segment, effect_index)
        if mode == "immediate":
            immediate += output
        elif mode == "repeatable":
            repeatable += output
        else:
            conditional += output

    return ArtifactSignals(
        artifact_card=artifact_card,
        enabler=immediate > 0,
        payoff=payoff,
        engine=repeatable > 0 or repeatable_payoff,
        immediate_artifacts=immediate,
        conditional_artifacts=conditional,
        repeatable_artifacts=repeatable,
    )


def artifact_roles(analysis: CardAnalysis) -> tuple[str, ...]:
    signals = analyze_artifact(analysis)
    roles: set[str] = set()
    if signals.enabler:
        roles.add("artifact_enabler")
    if signals.payoff:
        roles.add("artifact_payoff")
    if signals.engine:
        roles.add("artifact_engine")
    produced_tokens = (
        signals.immediate_artifacts - int(signals.artifact_card)
        + signals.conditional_artifacts
        + signals.repeatable_artifacts
    )
    if produced_tokens > 0:
        roles.add("artifact_producer")
    for prefix, value in (
        ("artifact_immediate_", signals.immediate_artifacts),
        ("artifact_conditional_", signals.conditional_artifacts),
        ("artifact_repeatable_", signals.repeatable_artifacts),
    ):
        if value:
            roles.add(f"{prefix}{min(value, 9)}")
    return tuple(sorted(roles))


def artifact_functional_roles(analysis: CardAnalysis) -> tuple[str, ...]:
    return tuple(role for role in artifact_roles(analysis) if not role[-1:].isdigit())


def artifact_metadata_roles(analysis: CardAnalysis) -> tuple[str, ...]:
    return tuple(role for role in artifact_roles(analysis) if role[-1:].isdigit())
