from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CardAnalysis:
    name: str
    mana_value: float
    colors: tuple[str, ...]
    color_identity: tuple[str, ...]
    type_line: str
    oracle_text: str

    is_land: bool
    is_creature: bool
    is_artifact: bool
    is_enchantment: bool
    is_instant: bool
    is_sorcery: bool
    is_planeswalker: bool
    is_legendary: bool

    power: float | None
    toughness: float | None

    features: frozenset[str]


_TRANSFORM_GATES = (
    "cast it transformed",
    "craft with",
    "daybound",
    "return this card transformed",
    "transform this",
)

_NUMBER_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
}


def cast_accessible_oracle_text(analysis: CardAnalysis) -> str:
    """Return rules text available without first transforming the front face.

    The card database preserves multi-face boundaries with `` // ``. Modal
    faces such as Adventures and Rooms remain available because either half can
    be cast. A back face gated by transform, craft, daybound, or a defeated
    battle is not active when the front face is cast and must not be treated as
    an immediate effect.
    """

    faces = analysis.oracle_text.split(" // ")
    if len(faces) < 2:
        return analysis.oracle_text
    front = faces[0]
    if any(marker in front.lower() for marker in _TRANSFORM_GATES):
        return front
    return analysis.oracle_text


def cast_accessible_effect_segments(analysis: CardAnalysis) -> tuple[str, ...]:
    """Return cast-accessible Oracle abilities without losing sentence context.

    Oracle newlines and modal-face separators delimit abilities. Full stops do
    not: reminder text and follow-up sentences often carry the condition or
    target that governs a later ``create`` or team-buff phrase.
    """

    raw_segments = tuple(
        segment.strip().lower()
        for segment in re.split(
            r"\n| // ", cast_accessible_oracle_text(analysis)
        )
        if segment.strip()
    )
    segments: list[str] = []
    choice_context = ""
    for segment in raw_segments:
        if "choose one" in segment:
            choice_context = segment
            segments.append(segment)
            continue
        if choice_context and (
            segment.startswith("•") or re.match(r"^\+\s*\{", segment)
        ):
            segments.append(f"{choice_context} {segment}")
            continue
        choice_context = ""
        segments.append(segment)
    return tuple(segments)


def additional_creature_sacrifice_cost(analysis: CardAnalysis) -> int:
    """Return the minimum creature count required as an additional cast cost."""

    for segment in cast_accessible_effect_segments(analysis):
        match = re.search(
            r"as an additional cost[^.\n]*?sacrifice "
            r"(a|an|one|two|three|four|\d+)(?: or more)? creatures?",
            segment,
        )
        if match is None:
            continue
        raw = match.group(1)
        return _NUMBER_WORDS.get(raw, int(raw) if raw.isdigit() else 1)
    return 0


def has_activated_sacrifice_outlet(
    analysis: CardAnalysis,
    *,
    permanent_type: str | None = None,
) -> bool:
    """Return whether a cast-accessible activated cost sacrifices material."""

    required_type = permanent_type.lower() if permanent_type else None
    for segment in cast_accessible_effect_segments(analysis):
        for match in re.finditer(r"([^.\n:]{0,180}):", segment):
            cost = match.group(1).lower()
            sacrificed = re.search(
                r"sacrifice (?:a|an|another|one|two|three|four|\d+) "
                r"(creatures?|artifacts?|permanents?)",
                cost,
            )
            if sacrificed is None or "as an additional cost" in cost:
                continue
            kind = sacrificed.group(1).removesuffix("s")
            if required_type is None or kind == required_type:
                return True
    return False


def exact_target_life_gate(analysis: CardAnalysis) -> int | None:
    """Return an exact target-life cast gate when Oracle text specifies one."""

    match = re.search(
        r"if target (?:player|opponent) has exactly (\d+) life",
        cast_accessible_oracle_text(analysis).lower(),
    )
    return int(match.group(1)) if match else None


def simulation_metadata_roles(analysis: CardAnalysis) -> tuple[str, ...]:
    """Return machine-readable cast and effect metadata for deck entries."""

    roles: list[str] = []
    sacrifice_cost = additional_creature_sacrifice_cost(analysis)
    if sacrifice_cost:
        roles.append(f"cast_additional_creature_sacrifice_{sacrifice_cost}")
    life_gate = exact_target_life_gate(analysis)
    if life_gate is not None:
        roles.append(f"cast_target_life_exact_{life_gate}")
        damage = max(
            (
                int(value)
                for value in re.findall(
                    r"(?:deals?|deal) (\d+) damage",
                    cast_accessible_oracle_text(analysis).lower(),
                )
            ),
            default=0,
        )
        if damage:
            roles.append(f"burn_damage_{damage}")
    return tuple(roles)


def saga_chapter_is_delayed(segment: str, full_text: str) -> bool:
    match = re.match(r"^(i|ii|iii|iv|v|vi)\s*[—-]", segment)
    if match is None or "read ahead" in full_text:
        return False
    return match.group(1) != "i"


def cast_immediate_team_buff_segments(
    analysis: CardAnalysis,
) -> tuple[str, ...]:
    """Return global team buffs available from the normal cast.

    Target-limited, name-limited, delayed-trigger and extra Spree-mode effects
    are not global Go-Wide anthems. Self-enter triggers and read-ahead Saga
    chapters remain cast-accessible.
    """

    text = cast_accessible_oracle_text(analysis).lower()
    power_patterns = (
        "other creatures you control get +",
        "creature tokens you control get +",
        "creatures you control get +",
        "tokens you control get +",
    )
    counter_pattern = "put a +1/+1 counter on each creature you control"
    accepted: list[str] = []
    front_name = analysis.name.split(" // ", 1)[0].lower()
    enter_markers = (
        "when this creature enters",
        "when this permanent enters",
        "when this enchantment enters",
        "when this artifact enters",
        f"when {front_name} enters",
    )
    for segment in cast_accessible_effect_segments(analysis):
        power_pattern = next(
            (pattern for pattern in power_patterns if pattern in segment),
            None,
        )
        counter_buff = counter_pattern in segment
        if power_pattern is None and not counter_buff:
            continue
        effect_index = (
            segment.index(power_pattern)
            if power_pattern is not None
            else segment.index(counter_pattern)
        )
        if ":" in segment[:effect_index] or "solved —" in segment[:effect_index]:
            continue
        if power_pattern is not None:
            prefix = segment[:effect_index].rstrip()
            allowed_prefix = not prefix or any(
                marker in prefix for marker in enter_markers
            )
            if not allowed_prefix:
                continue
        if " get +" in segment and re.search(r"get \+0/", segment):
            continue
        if any(
            limit in segment
            for limit in (
                "target creature",
                "target player controls",
                "each of up to",
                "you control named",
            )
        ):
            continue
        if "+ {" in segment or saga_chapter_is_delayed(segment, text):
            continue
        triggered = any(
            marker in segment
            for marker in ("whenever", "at the beginning", "if ", "when ")
        )
        if triggered and not any(marker in segment for marker in enter_markers):
            continue
        accepted.append(segment)
    return tuple(accepted)


def _parse_number(value: Any) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_values(value: Any) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(
            sorted(str(item).upper() for item in value)
        )

    if isinstance(value, str):
        if not value:
            return ()

        return tuple(
            sorted(
                item.strip().upper()
                for item in value.split(",")
                if item.strip()
            )
        )

    return ()


def analyze_card(card: dict[str, Any]) -> CardAnalysis:
    type_line = str(card.get("type_line", ""))
    oracle_text = str(card.get("oracle_text", ""))
    type_line_lower = type_line.lower()

    return CardAnalysis(
        name=str(card.get("name", "")),
        mana_value=float(
            card.get("mana_value", card.get("cmc", 0)) or 0
        ),
        colors=_normalize_values(card.get("colors", [])),
        color_identity=_normalize_values(
            card.get("color_identity", [])
        ),
        type_line=type_line,
        oracle_text=str(card.get("oracle_text", "")),
        is_land="land" in type_line_lower,
        is_creature="creature" in type_line_lower,
        is_artifact="artifact" in type_line_lower,
        is_enchantment="enchantment" in type_line_lower,
        is_instant="instant" in type_line_lower,
        is_sorcery="sorcery" in type_line_lower,
        is_planeswalker="planeswalker" in type_line_lower,
        is_legendary="legendary" in type_line_lower,
        power=_parse_number(card.get("power")),
        toughness=_parse_number(card.get("toughness")),
        features=frozenset(detect_features(oracle_text)),
    )
def detect_features(oracle_text: str) -> set[str]:

    text = oracle_text.lower()

    features = set()

    if "draw" in text:
        features.add("draw")

    if "damage" in text:
        features.add("damage")

    if "create" in text and "token" in text:
        features.add("token")

    if "search your library" in text:
        features.add("search_library")

    if "add {" in text:
        features.add("mana")

    if "destroy target" in text:
        features.add("destroy")

    if "exile target" in text:
        features.add("exile")

    if "mill" in text:
        features.add("mill")

    if "gain life" in text:
        features.add("lifegain")

    return features
