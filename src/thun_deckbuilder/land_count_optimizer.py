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
    """Score practical early-game consistency without double-counting metrics.

    ``mulligan_to_six_pct`` is the inverse of raw seven-card playability, while
    ``two_to_four_lands_pct`` and ``early_play_pct`` are components of the
    post-mulligan playability test. The score therefore uses the combined
    post-mulligan result, gives natural seven-card playability a smaller bonus,
    and independently balances access to the early/core plan against screw and
    flood through turn three.
    """
    return (
        report.playable_after_mulligan_pct * 2.25
        + report.playable_hands_pct * 0.35
        + report.early_play_pct * 0.75
        + report.core_by_turn_three_pct * 0.75
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
