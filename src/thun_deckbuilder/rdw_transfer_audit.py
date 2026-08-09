from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


FUNCTION_ORDER = (
    "one_mana_threat",
    "spell_matter_threat",
    "face_burn",
    "combat_trick",
    "repeatable_reach",
    "reload",
    "anti_lifegain",
    "resilient_threat",
    "utility_land",
    "creature_removal",
    "artifact_hate",
    "graveyard_hate",
    "go_wide_hate",
)


@dataclass(frozen=True)
class CandidateAssessment:
    name: str
    mana_value: float
    type_line: str
    oracle_text: str
    functions: tuple[str, ...]
    score: float
    reasons: tuple[str, ...]
    timing_caveats: tuple[str, ...]

    @property
    def immediate(self) -> bool:
        return not self.timing_caveats


def _text(card: Mapping[str, Any]) -> str:
    return str(card.get("oracle_text", "")).strip()


def _lower(card: Mapping[str, Any]) -> str:
    return _text(card).lower()


def _type_line(card: Mapping[str, Any]) -> str:
    return str(card.get("type_line", ""))


def _mana_value(card: Mapping[str, Any]) -> float:
    return float(card.get("mana_value", card.get("cmc", 0)) or 0)


def _numeric_power(card: Mapping[str, Any]) -> float | None:
    try:
        return float(card.get("power"))
    except (TypeError, ValueError):
        return None


def _red_identity(card: Mapping[str, Any]) -> bool:
    identity = {str(value).upper() for value in card.get("color_identity", [])}
    return identity.issubset({"R"})


def _deals_face_damage(text: str) -> bool:
    targets = (
        "any target",
        "target player",
        "target opponent",
        "each opponent",
        "that player",
        "its controller",
    )
    return "damage" in text and any(target in text for target in targets)


def _deals_creature_damage(text: str) -> bool:
    return "damage" in text and any(
        phrase in text
        for phrase in (
            "target creature",
            "each creature",
            "creature you don't control",
        )
    )


def timing_caveats(card: Mapping[str, Any]) -> tuple[str, ...]:
    text = _lower(card)
    caveats: list[str] = []
    if re.search(r"whenever .* attacks|when .* attacks|whenever you attack", text):
        caveats.append("attack_trigger")
    if re.search(r"when .* dies|whenever .* dies", text):
        caveats.append("death_trigger")
    if any(
        phrase in text
        for phrase in (
            "at the beginning of your next",
            "at the beginning of the next",
            "at the beginning of your end step",
            "at the beginning of each end step",
        )
    ):
        caveats.append("delayed_trigger")
    if any(
        phrase in text
        for phrase in (
            " if ",
            "unless",
            "as long as",
            "only if",
            "for each",
            "provided that",
        )
    ):
        caveats.append("conditional")
    if ":" in text:
        caveats.append("activated")
    return tuple(dict.fromkeys(caveats))


def assess_rdw_candidate(card: Mapping[str, Any]) -> CandidateAssessment | None:
    if not _red_identity(card):
        return None

    name = str(card.get("name", ""))
    type_line = _type_line(card)
    type_lower = type_line.lower()
    text = _lower(card)
    mv = _mana_value(card)
    power = _numeric_power(card)
    is_land = "land" in type_lower
    is_creature = "creature" in type_lower
    is_instant = "instant" in type_lower
    is_sorcery = "sorcery" in type_lower

    functions: list[str] = []
    reasons: list[str] = []
    score = 0.0

    if is_creature and mv <= 1:
        functions.append("one_mana_threat")
        score += 4.0
        reasons.append("one-mana creature")
        if power is not None:
            score += min(power, 2.0) * 0.5
        if "haste" in text:
            score += 1.5
            reasons.append("haste")
        if "prowess" in text or "whenever you cast a noncreature spell" in text:
            score += 2.0
            reasons.append("spell-matter scaling")
        if "enters" in text and _deals_face_damage(text):
            score += 1.5
            reasons.append("immediate damage on entry")

    spell_matter_phrases = (
        "prowess",
        "whenever you cast a noncreature spell",
        "whenever you cast an instant or sorcery spell",
        "whenever you cast your second spell",
        "whenever you cast a spell during your turn",
    )
    if is_creature and mv <= 3 and any(phrase in text for phrase in spell_matter_phrases):
        functions.append("spell_matter_threat")
        score += max(1.0, 4.0 - mv)
        reasons.append("cheap spell-matter threat")

    if (is_instant or is_sorcery) and mv <= 3 and _deals_face_damage(text):
        functions.append("face_burn")
        score += max(1.0, 5.0 - mv)
        reasons.append("damage can reach the opponent")
        if "any target" in text:
            score += 1.0
            reasons.append("flexible target")
        if mv <= 1:
            score += 1.0
            reasons.append("one-mana interaction")

    pump_pattern = re.search(r"gets? \+[0-9x*]+/\+[0-9x*]+ until end of turn", text)
    if (is_instant or is_sorcery) and mv <= 2 and pump_pattern:
        functions.append("combat_trick")
        score += max(1.0, 4.0 - mv)
        reasons.append("cheap temporary power increase")
        if "trample" in text:
            score += 1.5
            reasons.append("trample converts power into damage")
        if "draw a card" in text or "exile the top card" in text:
            score += 1.0
            reasons.append("replaces or extends itself")

    repeatable_trigger = any(
        phrase in text
        for phrase in (
            "whenever you cast a noncreature spell",
            "whenever you cast an instant or sorcery spell",
            "whenever you cast your second spell",
        )
    )
    if is_creature and repeatable_trigger and _deals_face_damage(text):
        functions.append("repeatable_reach")
        score += max(1.0, 4.0 - mv)
        reasons.append("repeatable spell-triggered damage")

    reload_phrases = (
        "exile the top card of your library. you may play",
        "exile the top two cards of your library",
        "you may play those cards until the end of your next turn",
        "you may play them until the end of your next turn",
        "draw two cards",
    )
    if mv <= 3 and any(phrase in text for phrase in reload_phrases):
        functions.append("reload")
        score += max(1.0, 4.0 - mv)
        reasons.append("low-cost card access")

    if any(
        phrase in text
        for phrase in (
            "players can't gain life",
            "your opponents can't gain life",
            "opponents can't gain life",
        )
    ):
        functions.append("anti_lifegain")
        score += 3.0
        reasons.append("prevents opposing lifegain")

    if is_creature and any(
        phrase in text
        for phrase in (
            "return this card from your graveyard",
            "return it to the battlefield",
            "you may cast this card from your graveyard",
            "unearth",
            "escape—",
            "ward",
            "indestructible",
        )
    ):
        functions.append("resilient_threat")
        score += 2.0
        reasons.append("resilience or graveyard reuse")

    if is_land:
        non_mana_text = re.sub(r"\{t\}: add [^.]+\.?", "", text)
        utility_phrases = (
            "deals 1 damage",
            "deals 2 damage",
            "becomes a",
            "gains haste",
            "create a",
            "sacrifice",
            "discard a card",
        )
        if any(phrase in non_mana_text for phrase in utility_phrases):
            functions.append("utility_land")
            score += 3.0
            reasons.append("land contributes a non-mana function")
            if "enters the battlefield tapped" in text:
                score -= 1.0
                reasons.append("enters tapped")

    if mv <= 3 and _deals_creature_damage(text):
        functions.append("creature_removal")
        score += max(0.5, 3.0 - mv)
        reasons.append("cheap creature interaction")

    if mv <= 3 and any(
        phrase in text
        for phrase in (
            "destroy target artifact",
            "exile target artifact",
            "artifact can't block",
        )
    ):
        functions.append("artifact_hate")
        score += 2.0
        reasons.append("artifact interaction")

    if any(
        phrase in text
        for phrase in (
            "exile all cards from target player's graveyard",
            "cards in graveyards can't",
            "players can't cast spells from graveyards",
            "exile target card from a graveyard",
        )
    ):
        functions.append("graveyard_hate")
        score += 2.0
        reasons.append("graveyard interaction")

    if mv <= 3 and any(
        phrase in text
        for phrase in (
            "damage to each creature",
            "damage to each non-flying creature",
            "damage to each creature without flying",
        )
    ):
        functions.append("go_wide_hate")
        score += 2.0
        reasons.append("small-board sweeper")

    if not functions:
        return None

    caveats = timing_caveats(card)
    penalties = {
        "attack_trigger": 0.75,
        "death_trigger": 1.25,
        "delayed_trigger": 1.0,
        "conditional": 0.5,
        "activated": 0.25,
    }
    for caveat in caveats:
        score -= penalties[caveat]

    return CandidateAssessment(
        name=name,
        mana_value=mv,
        type_line=type_line,
        oracle_text=_text(card),
        functions=tuple(function_name for function_name in FUNCTION_ORDER if function_name in functions),
        score=round(score, 2),
        reasons=tuple(reasons),
        timing_caveats=caveats,
    )


def rank_candidates(
    cards: Iterable[Mapping[str, Any]],
    *,
    limit_per_function: int = 20,
) -> dict[str, list[CandidateAssessment]]:
    buckets: dict[str, list[CandidateAssessment]] = {name: [] for name in FUNCTION_ORDER}
    seen: set[str] = set()
    for card in cards:
        assessment = assess_rdw_candidate(card)
        if assessment is None or assessment.name in seen:
            continue
        seen.add(assessment.name)
        for function_name in assessment.functions:
            buckets[function_name].append(assessment)

    for function_name, candidates in buckets.items():
        candidates.sort(key=lambda item: (-item.score, item.mana_value, item.name))
        buckets[function_name] = candidates[:limit_per_function]
    return buckets
