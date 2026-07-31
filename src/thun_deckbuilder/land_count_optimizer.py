from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar

from thun_deckbuilder.opening_hand_simulator import OpeningHandReport


T = TypeVar("T")


@dataclass(frozen=True)
class LandCountCandidate(Generic[T]):
    lands: int
    payload: T
    report: OpeningHandReport


def consistency_score(report: OpeningHandReport) -> float:
    """Score an opening-hand report for practical early-game consistency."""
    return (
        report.playable_after_mulligan_pct * 2.25
        + report.playable_hands_pct * 0.75
        + report.two_to_four_lands_pct
        + report.early_play_pct * 0.75
        + report.core_by_turn_three_pct * 0.75
        - report.mulligan_to_six_pct * 0.35
        - report.mana_screw_pct * 1.5
        - report.mana_flood_pct * 1.25
    )


def choose_land_count(
    candidates: Iterable[LandCountCandidate[T]],
    *,
    preferred_lands: int,
) -> LandCountCandidate[T]:
    """Choose the most consistent candidate with stable deterministic ties."""
    options = tuple(candidates)
    if not options:
        raise ValueError("At least one land-count candidate is required.")
    return max(
        options,
        key=lambda candidate: (
            consistency_score(candidate.report),
            -abs(candidate.lands - preferred_lands),
            -candidate.lands,
        ),
    )
