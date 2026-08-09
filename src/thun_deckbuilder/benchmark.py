from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from thun_deckbuilder.deck_generator import GeneratedDeck


@dataclass(frozen=True)
class SignatureTarget:
    key: str
    target: int
    type_phrases: tuple[str, ...] = ()
    reason_phrases: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()


@dataclass(frozen=True)
class BenchmarkProfile:
    archetype: str
    display_name: str
    role_targets: tuple[tuple[str, int], ...]
    curve_targets: tuple[tuple[str, int], ...]
    lands: int
    signature_targets: tuple[SignatureTarget, ...] = ()


@dataclass(frozen=True)
class BenchmarkItem:
    key: str
    target: int
    actual: int
    score: int


@dataclass(frozen=True)
class BenchmarkReport:
    name: str
    role_items: tuple[BenchmarkItem, ...]
    curve_items: tuple[BenchmarkItem, ...]
    land_item: BenchmarkItem
    score: int
    signature_items: tuple[BenchmarkItem, ...] = ()


BENCHMARKS: dict[str, BenchmarkProfile] = {
    "burn": BenchmarkProfile(
        archetype="burn",
        display_name="Mono-Red Burn",
        role_targets=(("burn", 24), ("aggro_creature", 9), ("card_draw", 3)),
        curve_targets=(("1", 12), ("2", 16), ("3", 6), ("4+", 2)),
        lands=24,
    ),
    "tokens": BenchmarkProfile(
        archetype="tokens",
        display_name="Mono-White Tokens",
        role_targets=(("token_maker", 18), ("token_payoff", 6), ("removal", 6), ("card_draw", 3)),
        curve_targets=(("1", 8), ("2", 12), ("3", 10), ("4+", 6)),
        lands=24,
    ),
    "artifacts": BenchmarkProfile(
        archetype="artifacts",
        display_name="Artifact Synergy",
        role_targets=(("card_draw", 5), ("removal", 5)),
        curve_targets=(("1", 10), ("2", 14), ("3", 9), ("4+", 5)),
        lands=22,
        signature_targets=(
            SignatureTarget("artifact_cards", 28, roles=("artifact_enabler",)),
            SignatureTarget(
                "artifact_payoffs",
                6,
                roles=("artifact_payoff",),
            ),
        ),
    ),
    "control": BenchmarkProfile(
        archetype="control",
        display_name="Dimir Control",
        role_targets=(("removal", 8), ("card_draw", 7)),
        curve_targets=(("1", 4), ("2", 12), ("3", 10), ("4+", 9)),
        lands=25,
        signature_targets=(
            SignatureTarget(
                "control_answers",
                14,
                reason_phrases=(
                    "Counter target spell",
                    "Control removal",
                    "Sweeper",
                ),
            ),
            SignatureTarget(
                "control_finishers",
                3,
                reason_phrases=("Control-Finisher",),
            ),
        ),
    ),
    "shrines": BenchmarkProfile(
        archetype="shrines",
        display_name="Five-Color Shrines",
        role_targets=(("ramp", 7), ("card_draw", 5), ("removal", 5)),
        curve_targets=(("1", 3), ("2", 8), ("3", 11), ("4+", 14)),
        lands=24,
        signature_targets=(
            SignatureTarget("shrine_cards", 15, type_phrases=("shrine",)),
            SignatureTarget(
                "fixing_sources",
                7,
                reason_phrases=("Fünffarben-Fixing", "Farben-Fixing"),
            ),
        ),
    ),
    "mill": BenchmarkProfile(
        archetype="mill",
        display_name="Dimir Mill",
        role_targets=(("card_draw", 7), ("removal", 8)),
        curve_targets=(("1", 6), ("2", 12), ("3", 10), ("4+", 8)),
        lands=24,
        signature_targets=(
            SignatureTarget("mill_sources", 20, roles=("mill_source",)),
        ),
    ),
}


def _closeness(actual: int, target: int) -> int:
    if target <= 0:
        return 100 if actual == 0 else 0
    difference = abs(actual - target)
    return max(0, round(100 * (1 - difference / target)))


def _minimum_score(actual: int, target: int) -> int:
    """Score a minimum requirement without penalizing useful excess."""
    if target <= 0:
        return 100
    return min(100, round(100 * actual / target))


def _curve_band(mana_value: float) -> str:
    if mana_value <= 1:
        return "1"
    if mana_value <= 2:
        return "2"
    if mana_value <= 3:
        return "3"
    return "4+"


def _matches_signature(entry, target: SignatureTarget) -> bool:
    type_line = entry.type_line.lower()
    reasons = tuple(reason.lower() for reason in entry.reasons)
    roles = {str(role) for role in entry.roles}
    return (
        any(phrase.lower() in type_line for phrase in target.type_phrases)
        or any(
            phrase.lower() in reason
            for phrase in target.reason_phrases
            for reason in reasons
        )
        or bool(roles.intersection(target.roles))
    )


class BenchmarkAnalyzer:
    def analyze(self, deck: GeneratedDeck, archetype: str) -> BenchmarkReport:
        profile = BENCHMARKS.get(archetype)
        if profile is None:
            raise ValueError(f"No benchmark is defined for archetype '{archetype}'.")

        role_counts: Counter[str] = Counter()
        curve_counts: Counter[str] = Counter()
        for entry in deck.mainboard:
            for role in entry.roles:
                role_counts[str(role)] += entry.quantity
            curve_counts[_curve_band(entry.mana_value)] += entry.quantity

        role_items = tuple(
            BenchmarkItem(role, target, role_counts[role], _minimum_score(role_counts[role], target))
            for role, target in profile.role_targets
        )
        curve_items = tuple(
            BenchmarkItem(band, target, curve_counts[band], _closeness(curve_counts[band], target))
            for band, target in profile.curve_targets
        )
        signature_items = tuple(
            BenchmarkItem(
                target.key,
                target.target,
                sum(
                    entry.quantity
                    for entry in deck.mainboard
                    if _matches_signature(entry, target)
                ),
                0,
            )
            for target in profile.signature_targets
        )
        signature_items = tuple(
            BenchmarkItem(
                item.key,
                item.target,
                item.actual,
                _minimum_score(item.actual, item.target),
            )
            for item in signature_items
        )
        land_item = BenchmarkItem(
            "lands",
            profile.lands,
            deck.lands,
            _closeness(deck.lands, profile.lands),
        )
        all_scores = [
            item.score
            for item in role_items + curve_items + signature_items
        ] + [land_item.score]
        score = round(sum(all_scores) / len(all_scores)) if all_scores else 0
        return BenchmarkReport(
            profile.display_name,
            role_items,
            curve_items,
            land_item,
            score,
            signature_items,
        )
