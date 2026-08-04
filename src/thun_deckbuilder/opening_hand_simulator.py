from __future__ import annotations

import hashlib
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from enum import StrEnum
from itertools import combinations

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.mana_requirement import (
    can_pay_mana_requirements,
    mana_symbol_requirements,
)
from thun_deckbuilder.token_plan import TokenPlan


CardSample = tuple[str, float, bool]
_COLORS = frozenset("WUBRG")
_REPEATABLE_PHRASES = (
    "engine",
    "repeatable",
    "repeated",
    "wiederhol",
    "at the beginning",
    "whenever",
    "each upkeep",
    "each end step",
    "kartenvorteil",
    "card advantage",
)


@dataclass(frozen=True)
class OpeningHandReport:
    samples: int
    playable_hands_pct: int
    playable_after_mulligan_pct: int
    mulligan_to_six_pct: int
    two_to_four_lands_pct: int
    early_play_pct: int
    core_by_turn_three_pct: int
    mana_screw_pct: int
    mana_flood_pct: int


class HandPlanClassification(StrEnum):
    PLAN_CAPABLE = "planfaehig"
    MARGINAL = "marginal"
    NOT_PLAN_CAPABLE = "nicht_planfaehig"


@dataclass(frozen=True)
class OpeningHandPlanHand:
    hand_number: int
    cards: tuple[str, ...]
    land_sources: tuple[str, ...]
    turn_one_plays: tuple[str, ...]
    turn_two_plays: tuple[str, ...]
    turn_three_plays: tuple[str, ...]
    suggested_sequence: tuple[str, ...]
    keepable: bool
    mana_error: bool
    color_error: bool
    enabler_access: bool
    engine_access: bool
    payoff_access: bool
    finisher_access: bool
    interaction_access: bool
    dead_cards: tuple[str, ...]
    conflicting_cards: tuple[str, ...]
    classification: HandPlanClassification
    reasons: tuple[str, ...]
    failure_reasons: tuple[str, ...]


@dataclass(frozen=True)
class OpeningHandPlanReport:
    archetype: str
    plan: str
    engine_required: bool | None
    samples: int
    seed: int
    deck_hash: str
    keepability_pct: int
    plan_capable_pct: int
    marginal_pct: int
    not_plan_capable_pct: int
    early_play_turn_two_pct: int
    early_play_turn_three_pct: int
    mana_error_pct: int
    color_error_pct: int
    missing_enabler_pct: int
    missing_engine_pct: int
    missing_payoff_pct: int
    missing_finisher_pct: int
    dead_or_conflicting_pct: int
    top_problem_types: tuple[tuple[str, int], ...]
    hands: tuple[OpeningHandPlanHand, ...]


@dataclass(frozen=True)
class _PlanCard:
    name: str
    kind: str
    mana_value: float = 0.0
    color_requirements: tuple[frozenset[str], ...] = ()
    source_color: str = ""
    type_line: str = ""
    roles: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()

    @property
    def text(self) -> str:
        return " ".join(
            (
                self.name,
                self.type_line,
                *self.roles,
                *self.reasons,
            )
        ).lower()


CORE_PHRASES = {
    "artifacts": ("artifact", "affinity", "improvise", "metalcraft"),
    "shrines": ("shrine",),
    "mill": ("mill", "library into"),
}


def _is_core(entry, archetype: str) -> bool:
    name = entry.name.lower()
    reasons = " ".join(entry.reasons).lower()
    if archetype == "artifacts":
        return "artifact" in entry.type_line.lower() or any(
            phrase in reasons for phrase in CORE_PHRASES[archetype]
        )
    return any(
        phrase in name or phrase in reasons
        for phrase in CORE_PHRASES.get(archetype, ())
    )


def _land_count(cards: list[CardSample]) -> int:
    return sum(1 for kind, _, _ in cards if kind == "land")


def _has_early_play(cards: list[CardSample]) -> bool:
    return any(kind == "spell" and mana_value <= 2 for kind, mana_value, _ in cards)


def _is_playable(cards: list[CardSample]) -> bool:
    lands = _land_count(cards)
    return 2 <= lands <= 4 and _has_early_play(cards)


def _bottom_choice(opening: list[CardSample]) -> int:
    """Choose the London-mulligan bottom card using a deterministic hand heuristic."""

    def score(bottom_index: int) -> tuple[int, int, int, int, float]:
        kept = opening[:bottom_index] + opening[bottom_index + 1 :]
        lands = _land_count(kept)
        early = _has_early_play(kept)
        core = any(kind == "spell" and is_core for kind, _, is_core in kept)
        expensive = sum(
            1 for kind, mana_value, _ in kept if kind == "spell" and mana_value >= 4
        )
        return (
            int(_is_playable(kept)),
            int(2 <= lands <= 4),
            int(early),
            int(core),
            -abs(lands - 3) - expensive * 0.25,
        )

    return max(range(len(opening)), key=score)


def _mana_symbols(raw: str, colored: str) -> tuple[frozenset[str], ...]:
    return mana_symbol_requirements(raw, colored)


def _spell_color_weights(deck: GeneratedDeck) -> dict[str, int]:
    weights: Counter[str] = Counter()
    for entry in deck.mainboard:
        for options in _mana_symbols(entry.mana_cost.raw, entry.mana_cost.colored):
            for color in options:
                if color in _COLORS:
                    weights[color] += entry.quantity
    return dict(weights)


def _allocate_inferred_lands(deck: GeneratedDeck) -> list[_PlanCard]:
    weights = _spell_color_weights(deck)
    if not weights:
        return [_PlanCard("Basic Land", "land", source_color="*")] * deck.lands
    total_weight = sum(weights.values())
    raw = {color: deck.lands * weight / total_weight for color, weight in weights.items()}
    quantities = {color: int(value) for color, value in raw.items()}
    remaining = deck.lands - sum(quantities.values())
    order = sorted(
        weights,
        key=lambda color: (raw[color] - quantities[color], weights[color], color),
        reverse=True,
    )
    for color in order[:remaining]:
        quantities[color] += 1
    lands: list[_PlanCard] = []
    for color in "WUBRG":
        lands.extend(
            [_PlanCard(f"Basic {color}", "land", source_color=color)]
            * quantities.get(color, 0)
        )
    return lands


def _plan_library(deck: GeneratedDeck) -> list[_PlanCard]:
    lands: list[_PlanCard] = []
    if deck.mana_base is not None and deck.mana_base.lands:
        for allocation in deck.mana_base.lands:
            lands.extend(
                [
                    _PlanCard(
                        allocation.land_name,
                        "land",
                        source_color=str(allocation.color).upper(),
                    )
                ]
                * allocation.quantity
            )
    else:
        lands = _allocate_inferred_lands(deck)
    if len(lands) < deck.lands:
        lands.extend(
            [_PlanCard("Basic Land", "land", source_color="*")]
            * (deck.lands - len(lands))
        )
    elif len(lands) > deck.lands:
        lands = lands[: deck.lands]

    library = list(lands)
    for entry in deck.mainboard:
        card = _PlanCard(
            name=entry.name,
            kind="spell",
            mana_value=entry.mana_value,
            color_requirements=_mana_symbols(
                entry.mana_cost.raw,
                entry.mana_cost.colored,
            ),
            type_line=entry.type_line,
            roles=tuple(str(role) for role in entry.roles),
            reasons=entry.reasons,
        )
        library.extend([card] * entry.quantity)
    if len(library) < 7:
        raise ValueError("deck must contain at least seven cards")
    return library


def _match_color_requirements(
    requirements: tuple[frozenset[str], ...],
    sources: tuple[str, ...],
) -> bool:
    return can_pay_mana_requirements(requirements, sources)


def _can_cast_with_sources(card: _PlanCard, sources: tuple[str, ...], turn: int) -> bool:
    if card.kind != "spell":
        return False
    mana_needed = max(len(card.color_requirements), int(math.ceil(card.mana_value)))
    if mana_needed > turn or len(sources) < mana_needed:
        return False
    return _match_color_requirements(card.color_requirements, sources)


def _can_cast_by_turn(card: _PlanCard, land_sources: tuple[str, ...], turn: int) -> bool:
    lands_in_play = min(turn, len(land_sources))
    if lands_in_play <= 0:
        return card.mana_value <= 0 and not card.color_requirements
    return any(
        _can_cast_with_sources(card, tuple(source_set), turn)
        for source_set in combinations(land_sources, lands_in_play)
    )


def _castable_cards(
    cards: tuple[_PlanCard, ...],
    land_sources: tuple[str, ...],
    turn: int,
) -> tuple[_PlanCard, ...]:
    return tuple(
        card
        for card in cards
        if card.kind == "spell" and _can_cast_by_turn(card, land_sources, turn)
    )


def _normalized_plan(deck: GeneratedDeck, archetype: str, plan: str | None) -> str:
    if plan:
        return plan.strip().lower().replace(" ", "_")
    if archetype != "tokens":
        return archetype
    profile = deck.profile_name.lower()
    if "aristocrat" in profile:
        return "aristocrats"
    if "value" in profile:
        return "value_tokens"
    return "go_wide"


def _signals(card: _PlanCard, archetype: str, plan: str) -> dict[str, bool]:
    roles = set(card.roles)
    text = card.text
    repeatable = any(phrase in text for phrase in _REPEATABLE_PHRASES)
    is_creature = "creature" in card.type_line.lower()
    interaction = bool(
        roles.intersection({"removal", "protection", "board_wipe"})
    ) or any(
        phrase in text
        for phrase in ("counter target", "destroy target", "exile target", "return target")
    )
    finisher = "finisher" in roles or (is_creature and card.mana_value >= 5) or any(
        phrase in text for phrase in ("finisher", "win condition", "wincondition", "lethal")
    )
    engine = "card_draw" in roles or repeatable
    enabler = payoff = False

    if archetype == "burn":
        pressure = bool(roles.intersection({"burn", "aggro_creature"})) or any(
            phrase in text for phrase in ("damage", "haste", "face-burn")
        )
        enabler = pressure
        payoff = pressure
        finisher = finisher or pressure
        interaction = interaction or "burn" in roles
    elif archetype == "tokens":
        maker = "token_maker" in roles or any(
            phrase in text
            for phrase in ("token-erzeuger", "token maker", "opfermaterial", "material")
        )
        outlet = "sacrifice" in roles or any(
            phrase in text for phrase in ("opfermöglichkeit", "sacrifice outlet", "outlet")
        )
        token_payoff = bool(roles.intersection({"token_payoff", "anthem"})) or any(
            phrase in text for phrase in ("board-payoff", "death-payoff", "drain", "anthem", "payoff")
        )
        enabler = maker
        if plan == "value_tokens":
            engine = engine or (maker and repeatable)
            payoff = token_payoff or engine
        elif plan == "aristocrats":
            engine = outlet
            payoff = token_payoff and any(
                phrase in text
                for phrase in ("death", "drain", "dies", "opponent loses", "payoff")
            )
        else:
            payoff = token_payoff
        finisher = finisher or (payoff and card.mana_value >= 3)
    elif archetype == "artifacts":
        artifact = (
            "artifact" in card.type_line.lower()
            or "artifact" in text
            or "artefakt" in text
        )
        enabler = artifact and card.mana_value <= 2
        payoff = any(
            phrase in text
            for phrase in (
                "affinity",
                "improvise",
                "metalcraft",
                "artifactfall",
                "artefakt-synergie",
                "payoff",
            )
        ) or "finisher" in roles
        engine = engine or (artifact and repeatable)
        finisher = finisher or payoff
    elif archetype == "mill":
        mill = "mill_source" in roles
        enabler = mill
        engine = engine or "mill_engine" in roles
        payoff = mill
        finisher = finisher or mill
    elif archetype == "control":
        enabler = interaction
        payoff = "board_wipe" in roles or engine
    else:
        core = any(
            phrase in text for phrase in CORE_PHRASES.get(archetype, ())
        )
        enabler = core
        payoff = core
        finisher = finisher or core

    return {
        "enabler": enabler,
        "engine": engine,
        "payoff": payoff,
        "finisher": finisher,
        "interaction": interaction,
        "maker": archetype == "tokens"
        and ("token_maker" in roles or "material" in text),
        "outlet": archetype == "tokens"
        and (
            "sacrifice" in roles
            or "outlet" in text
            or "opfermöglichkeit" in text
        ),
        "death_payoff": archetype == "tokens"
        and (
            "death-payoff" in text
            or "drain" in text
            or "dies" in text
        ),
    }


def _dead_and_conflicting(
    cards: tuple[_PlanCard, ...], archetype: str, plan: str
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    dead: list[str] = []
    conflicting: list[str] = []
    for card in cards:
        if card.kind != "spell":
            continue
        signals = _signals(card, archetype, plan)
        roles = set(card.roles)
        if archetype == "burn":
            if (
                not any(signals[key] for key in ("enabler", "engine", "interaction"))
                and card.mana_value >= 3
            ):
                dead.append(card.name)
        elif archetype == "tokens":
            if plan == "go_wide" and "sacrifice" in roles and not signals["maker"]:
                conflicting.append(card.name)
            elif plan == "value_tokens" and "sacrifice" in roles and not signals["engine"]:
                conflicting.append(card.name)
            elif plan == "aristocrats" and "anthem" in roles and not any(
                (signals["maker"], signals["outlet"], signals["death_payoff"])
            ):
                conflicting.append(card.name)
        elif archetype == "artifacts":
            if "artifact" not in card.type_line.lower() and not any(
                signals[key] for key in ("engine", "payoff", "interaction")
            ):
                dead.append(card.name)
        elif archetype == "mill":
            if not any(signals[key] for key in ("enabler", "engine", "interaction")):
                dead.append(card.name)
        elif archetype == "control":
            if "aggro_creature" in roles and not signals["interaction"]:
                conflicting.append(card.name)
            elif (
                not any(signals[key] for key in ("interaction", "engine", "finisher"))
                and card.mana_value >= 3
            ):
                dead.append(card.name)
    return tuple(sorted(dead)), tuple(sorted(conflicting))


def _sequence_priority(card: _PlanCard, archetype: str, plan: str) -> tuple[int, float, str]:
    signals = _signals(card, archetype, plan)
    priority = (
        8 * int(signals["enabler"])
        + 6 * int(signals["interaction"])
        + 4 * int(signals["engine"])
        + 3 * int(signals["payoff"])
        + int(signals["finisher"])
    )
    return (-priority, card.mana_value, card.name)


def _suggested_sequence(
    spells: tuple[_PlanCard, ...],
    land_sources: tuple[str, ...],
    archetype: str,
    plan: str,
) -> tuple[str, ...]:
    remaining = list(spells)
    result: list[str] = []
    for turn in (1, 2, 3):
        castable = [
            card for card in remaining if _can_cast_by_turn(card, land_sources, turn)
        ]
        if not castable:
            result.append(f"T{turn}: -")
            continue
        chosen = min(
            castable,
            key=lambda card: _sequence_priority(card, archetype, plan),
        )
        result.append(f"T{turn}: {chosen.name}")
        remaining.remove(chosen)
    return tuple(result)


def _deck_hash(deck: GeneratedDeck) -> str:
    mana_base = []
    if deck.mana_base is not None:
        mana_base = [
            (str(item.color), item.land_name, item.quantity)
            for item in deck.mana_base.lands
        ]
    payload = {
        "lands": deck.lands,
        "mana_base": sorted(mana_base),
        "mainboard": sorted(
            (
                entry.name,
                entry.quantity,
                entry.mana_cost.raw,
                entry.mana_value,
                tuple(entry.roles),
            )
            for entry in deck.mainboard
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _classify_plan(
    *,
    archetype: str,
    plan: str,
    hand: tuple[_PlanCard, ...],
    castable_turn_two: tuple[_PlanCard, ...],
    castable_turn_three: tuple[_PlanCard, ...],
    land_count: int,
    color_error: bool,
) -> tuple[HandPlanClassification, tuple[str, ...], tuple[str, ...]]:
    spells = tuple(card for card in hand if card.kind == "spell")
    signals = {id(card): _signals(card, archetype, plan) for card in spells}
    castable_t2_ids = {id(card) for card in castable_turn_two}
    castable_t3_ids = {id(card) for card in castable_turn_three}

    def count(key: str, *, castable_by: int | None = None) -> int:
        allowed = None
        if castable_by == 2:
            allowed = castable_t2_ids
        elif castable_by == 3:
            allowed = castable_t3_ids
        return sum(
            1
            for card in spells
            if signals[id(card)][key] and (allowed is None or id(card) in allowed)
        )

    reasons: list[str] = []
    failures: list[str] = []
    if land_count <= 1:
        failures.append("mana_screw")
    elif land_count >= 5:
        failures.append("mana_flood")
    if color_error:
        failures.append("color_mismatch")

    classification = HandPlanClassification.NOT_PLAN_CAPABLE
    if archetype == "burn":
        pressure = count("enabler", castable_by=3)
        if count("enabler", castable_by=2) and pressure >= 2 and not color_error:
            classification = HandPlanClassification.PLAN_CAPABLE
            reasons.append("early_pressure_and_burn_density")
        elif pressure >= 1 and not color_error:
            classification = HandPlanClassification.MARGINAL
            reasons.append("single_early_pressure_source")
        else:
            failures.append("missing_early_pressure")
        if pressure < 2:
            failures.append("insufficient_burn_density")
    elif archetype == "tokens":
        makers = count("maker", castable_by=3)
        if plan == "aristocrats":
            core = (
                count("maker") > 0,
                count("outlet") > 0,
                count("death_payoff") > 0,
            )
            pieces = sum(core)
            if pieces == 3 and makers > 0 and not color_error:
                classification = HandPlanClassification.PLAN_CAPABLE
                reasons.append("complete_aristocrats_core")
            elif pieces >= 2 and not color_error:
                classification = HandPlanClassification.MARGINAL
                reasons.append("partial_aristocrats_core")
            else:
                failures.append("incomplete_aristocrats_core")
        elif plan == "value_tokens":
            engines = count("engine")
            if makers > 0 and engines > 0 and not color_error:
                classification = HandPlanClassification.PLAN_CAPABLE
                reasons.append("maker_plus_value_engine")
            elif makers > 0 or engines > 0:
                classification = HandPlanClassification.MARGINAL
                reasons.append("maker_or_engine_only")
            else:
                failures.append("missing_token_maker")
                failures.append("missing_value_engine")
        else:
            early_makers = count("maker", castable_by=2)
            payoffs = count("payoff")
            if (
                early_makers > 0
                and (makers >= 2 or payoffs > 0)
                and not color_error
            ):
                classification = HandPlanClassification.PLAN_CAPABLE
                reasons.append("maker_plus_go_wide_scaling")
            elif makers > 0 or payoffs > 0:
                classification = HandPlanClassification.MARGINAL
                reasons.append("maker_or_payoff_only")
            else:
                failures.append("missing_token_maker")
                failures.append("missing_go_wide_payoff")
            if early_makers == 0:
                failures.append("missing_early_token_maker")
    elif archetype == "artifacts":
        enablers = count("enabler", castable_by=3)
        support = count("engine") + count("payoff")
        if enablers > 0 and support > 0 and not color_error:
            classification = HandPlanClassification.PLAN_CAPABLE
            reasons.append("artifact_enabler_plus_synergy")
        elif enablers > 0 or support > 0:
            classification = HandPlanClassification.MARGINAL
            reasons.append("artifact_half_package")
        else:
            failures.append("missing_artifact_enabler")
            failures.append("missing_artifact_payoff")
    elif archetype == "mill":
        mill_sources = count("enabler", castable_by=3)
        support = count("interaction", castable_by=2) + count("engine")
        if mill_sources > 0 and support > 0 and not color_error:
            classification = HandPlanClassification.PLAN_CAPABLE
            reasons.append("mill_engine_plus_protection")
        elif mill_sources > 0 or support > 0:
            classification = HandPlanClassification.MARGINAL
            reasons.append("mill_or_protection_only")
        else:
            failures.append("missing_mill_engine")
            failures.append("missing_interaction")
    elif archetype == "control":
        early_interaction = count("interaction", castable_by=2)
        resources = count("engine")
        total_interaction = count("interaction")
        if (
            early_interaction > 0
            and (resources > 0 or total_interaction >= 2)
            and not color_error
        ):
            classification = HandPlanClassification.PLAN_CAPABLE
            reasons.append("early_answer_plus_resource_plan")
        elif early_interaction > 0 or resources > 0:
            classification = HandPlanClassification.MARGINAL
            reasons.append("answer_or_resource_only")
        else:
            failures.append("missing_relevant_interaction")
            failures.append("missing_card_advantage")
    else:
        core = count("enabler", castable_by=3)
        if core > 0 and not color_error:
            classification = HandPlanClassification.PLAN_CAPABLE
            reasons.append("early_core_access")
        elif count("enabler") > 0:
            classification = HandPlanClassification.MARGINAL
            reasons.append("core_access_not_yet_castable")
        else:
            failures.append("missing_core_piece")

    if (
        classification == HandPlanClassification.PLAN_CAPABLE
        and (land_count <= 1 or land_count >= 5)
    ):
        classification = HandPlanClassification.MARGINAL
        reasons.append("plan_pieces_with_unstable_mana")

    if not castable_turn_two:
        failures.append("no_turn_two_play")
    if not castable_turn_three:
        failures.append("no_turn_three_play")
    return classification, tuple(reasons), tuple(dict.fromkeys(failures))


class OpeningHandSimulator:
    """Estimate early consistency with deterministic Monte Carlo samples.

    ``simulate`` preserves the historical aggregate London-mulligan model.
    ``simulate_plan`` stores reproducible raw seven-card hands and evaluates
    whether the declared archetype plan can realistically start.
    """

    def simulate(
        self,
        deck: GeneratedDeck,
        *,
        archetype: str,
        samples: int = 2000,
        seed: int = 17,
    ) -> OpeningHandReport:
        library: list[CardSample] = [("land", 0, False)] * deck.lands
        for entry in deck.mainboard:
            library.extend(
                [("spell", entry.mana_value, _is_core(entry, archetype))]
                * entry.quantity
            )

        rng = random.Random(seed)
        raw_playable = post_mulligan_playable = mulligans = 0
        lands_ok = early = core = screw = flood = 0

        for _ in range(samples):
            shuffled = library[:]
            rng.shuffle(shuffled)
            opening = shuffled[:7]
            raw_is_playable = _is_playable(opening)
            raw_playable += int(raw_is_playable)

            if raw_is_playable:
                kept = opening
                draw_sequence = shuffled
            else:
                mulligans += 1
                reshuffled = library[:]
                rng.shuffle(reshuffled)
                seven = reshuffled[:7]
                bottom_index = _bottom_choice(seven)
                bottomed = seven[bottom_index]
                kept = seven[:bottom_index] + seven[bottom_index + 1 :]
                draw_sequence = kept + reshuffled[7:] + [bottomed]

            land_count = _land_count(kept)
            has_early = _has_early_play(kept)
            cards_seen_by_turn_three = draw_sequence[: len(kept) + 3]
            has_core = any(
                kind == "spell" and is_core
                for kind, _, is_core in cards_seen_by_turn_three
            )

            post_mulligan_playable += int(_is_playable(kept))
            lands_ok += int(2 <= land_count <= 4)
            early += int(has_early)
            core += int(has_core)
            screw += int(land_count <= 1)
            flood += int(land_count >= 5)

        pct = lambda value: round(value * 100 / samples)
        return OpeningHandReport(
            samples=samples,
            playable_hands_pct=pct(raw_playable),
            playable_after_mulligan_pct=pct(post_mulligan_playable),
            mulligan_to_six_pct=pct(mulligans),
            two_to_four_lands_pct=pct(lands_ok),
            early_play_pct=pct(early),
            core_by_turn_three_pct=pct(core),
            mana_screw_pct=pct(screw),
            mana_flood_pct=pct(flood),
        )

    def simulate_plan(
        self,
        deck: GeneratedDeck,
        *,
        archetype: str,
        plan: str | None = None,
        samples: int = 100,
        seed: int = 1701,
    ) -> OpeningHandPlanReport:
        if samples <= 0:
            raise ValueError("samples must be positive")
        normalized_archetype = archetype.strip().lower()
        normalized_plan = _normalized_plan(deck, normalized_archetype, plan)
        library = _plan_library(deck)
        rng = random.Random(seed)
        hands: list[OpeningHandPlanHand] = []
        problems: Counter[str] = Counter()

        for hand_number in range(1, samples + 1):
            shuffled = library[:]
            rng.shuffle(shuffled)
            hand = tuple(shuffled[:7])
            spells = tuple(card for card in hand if card.kind == "spell")
            land_sources = tuple(
                card.source_color for card in hand if card.kind == "land"
            )
            castable_one = _castable_cards(spells, land_sources, 1)
            castable_two = _castable_cards(spells, land_sources, 2)
            castable_three = _castable_cards(spells, land_sources, 3)
            colored_spells = tuple(
                card
                for card in spells
                if card.color_requirements and card.mana_value <= 3
            )
            enough_mana_for_early = len(land_sources) >= min(
                3,
                max(
                    (math.ceil(card.mana_value) for card in colored_spells),
                    default=0,
                ),
            )
            color_error = bool(
                colored_spells
                and enough_mana_for_early
                and not any(card in castable_three for card in colored_spells)
            )
            mana_error = len(land_sources) <= 1 or len(land_sources) >= 5
            dead_cards, conflicting_cards = _dead_and_conflicting(
                spells, normalized_archetype, normalized_plan
            )
            classification, reasons, failure_reasons = _classify_plan(
                archetype=normalized_archetype,
                plan=normalized_plan,
                hand=hand,
                castable_turn_two=castable_two,
                castable_turn_three=castable_three,
                land_count=len(land_sources),
                color_error=color_error,
            )
            all_signals = [
                _signals(card, normalized_archetype, normalized_plan)
                for card in spells
            ]
            keepable = (
                2 <= len(land_sources) <= 4
                and bool(castable_three)
                and not color_error
                and len(dead_cards) + len(conflicting_cards) <= 2
            )
            problems.update(failure_reasons)
            if dead_cards or conflicting_cards:
                problems["dead_or_conflicting_cards"] += 1
            hands.append(
                OpeningHandPlanHand(
                    hand_number=hand_number,
                    cards=tuple(card.name for card in hand),
                    land_sources=land_sources,
                    turn_one_plays=tuple(
                        sorted({card.name for card in castable_one})
                    ),
                    turn_two_plays=tuple(
                        sorted({card.name for card in castable_two})
                    ),
                    turn_three_plays=tuple(
                        sorted({card.name for card in castable_three})
                    ),
                    suggested_sequence=_suggested_sequence(
                        spells,
                        land_sources,
                        normalized_archetype,
                        normalized_plan,
                    ),
                    keepable=keepable,
                    mana_error=mana_error,
                    color_error=color_error,
                    enabler_access=any(signal["enabler"] for signal in all_signals),
                    engine_access=any(signal["engine"] for signal in all_signals),
                    payoff_access=any(signal["payoff"] for signal in all_signals),
                    finisher_access=any(signal["finisher"] for signal in all_signals),
                    interaction_access=any(
                        signal["interaction"] for signal in all_signals
                    ),
                    dead_cards=dead_cards,
                    conflicting_cards=conflicting_cards,
                    classification=classification,
                    reasons=reasons,
                    failure_reasons=failure_reasons,
                )
            )

        def pct(predicate) -> int:
            return round(
                sum(1 for hand in hands if predicate(hand)) * 100 / samples
            )

        return OpeningHandPlanReport(
            archetype=normalized_archetype,
            plan=normalized_plan,
            engine_required=(
                TokenPlan(normalized_plan).requires_engine
                if normalized_archetype == "tokens"
                else None
            ),
            samples=samples,
            seed=seed,
            deck_hash=_deck_hash(deck),
            keepability_pct=pct(lambda hand: hand.keepable),
            plan_capable_pct=pct(
                lambda hand: hand.classification
                == HandPlanClassification.PLAN_CAPABLE
            ),
            marginal_pct=pct(
                lambda hand: hand.classification == HandPlanClassification.MARGINAL
            ),
            not_plan_capable_pct=pct(
                lambda hand: hand.classification
                == HandPlanClassification.NOT_PLAN_CAPABLE
            ),
            early_play_turn_two_pct=pct(lambda hand: bool(hand.turn_two_plays)),
            early_play_turn_three_pct=pct(lambda hand: bool(hand.turn_three_plays)),
            mana_error_pct=pct(lambda hand: hand.mana_error),
            color_error_pct=pct(lambda hand: hand.color_error),
            missing_enabler_pct=pct(lambda hand: not hand.enabler_access),
            missing_engine_pct=pct(lambda hand: not hand.engine_access),
            missing_payoff_pct=pct(lambda hand: not hand.payoff_access),
            missing_finisher_pct=pct(lambda hand: not hand.finisher_access),
            dead_or_conflicting_pct=pct(
                lambda hand: bool(hand.dead_cards or hand.conflicting_cards)
            ),
            top_problem_types=tuple(problems.most_common(3)),
            hands=tuple(hands),
        )
