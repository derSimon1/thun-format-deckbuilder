from __future__ import annotations

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
