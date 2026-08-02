from __future__ import annotations

import ci_global_validation as validation

from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.tournament_simulator import BestOfThreeSimulator


FAST_MATCHUP_SAMPLES = 120
FAST_BO3_SAMPLES = 40


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
    validation.MatchupSimulator = FastMatchupSimulator
    validation.BestOfThreeSimulator = FastBestOfThreeSimulator
    validation.main()


if __name__ == "__main__":
    main()
