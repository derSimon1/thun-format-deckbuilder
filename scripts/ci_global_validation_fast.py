from __future__ import annotations

from itertools import combinations as all_combinations

import ci_global_validation as validation

from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.tournament_simulator import BestOfThreeSimulator


FAST_MATCHUP_SAMPLES = 120
FAST_BO3_SAMPLES = 40
FAST_MATCHUP_PAIRS = (
    ("tokens", "burn"),
    ("tokens", "artifacts"),
    ("tokens", "mill"),
)


def fast_combinations(archetypes, size: int):
    """Use three Token-focused pairs in cyclic CI, preserving full mode."""

    values = tuple(archetypes)
    if size != 2:
        return all_combinations(values, size)
    available = set(values)
    return (
        pair
        for pair in FAST_MATCHUP_PAIRS
        if pair[0] in available and pair[1] in available
    )


class FastMatchupSimulator(MatchupSimulator):
    """Cap deterministic matchup samples for frequent CI feedback."""

    def simulate(self, *args, samples: int = 2000, **kwargs):
        return super().simulate(
            *args,
            samples=min(samples, FAST_MATCHUP_SAMPLES),
            **kwargs,
        )


class FastBestOfThreeSimulator(BestOfThreeSimulator):
    """Cap expensive sideboard-optimization samples in cyclic CI."""

    def simulate(self, *args, samples: int = 2000, **kwargs):
        return super().simulate(
            *args,
            samples=min(samples, FAST_BO3_SAMPLES),
            **kwargs,
        )


def main() -> None:
    validation.combinations = fast_combinations
    validation.MatchupSimulator = FastMatchupSimulator
    validation.BestOfThreeSimulator = FastBestOfThreeSimulator
    validation.main()


if __name__ == "__main__":
    main()
