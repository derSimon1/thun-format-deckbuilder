from __future__ import annotations

import random
from itertools import combinations as all_combinations

import ci_global_validation as validation

from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.tournament_simulator import (
    BestOfThreeReport,
    BestOfThreeSimulator,
    board_for_matchup,
)


FAST_MATCHUP_SAMPLES = 120
FAST_BO3_SAMPLES = 40
FAST_SIDEBOARD_SWAPS = 3
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
    """Use deterministic sideboarding instead of exhaustive optimization."""

    def simulate(
        self,
        deck_a,
        deck_b,
        *,
        archetype_a: str,
        archetype_b: str,
        samples: int = 2000,
        seed: int = 53,
    ) -> BestOfThreeReport:
        capped_samples = min(samples, FAST_BO3_SAMPLES)
        if capped_samples <= 0:
            raise ValueError("samples must be positive")

        simulator = FastMatchupSimulator()
        game_one = simulator.simulate(
            deck_a,
            deck_b,
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=capped_samples,
            seed=seed,
        )
        tuned_a, plan_a = board_for_matchup(
            deck_a,
            opponent_archetype=archetype_b,
            max_swaps=FAST_SIDEBOARD_SWAPS,
        )
        tuned_b, plan_b = board_for_matchup(
            deck_b,
            opponent_archetype=archetype_a,
            max_swaps=FAST_SIDEBOARD_SWAPS,
        )
        postboard = simulator.simulate(
            tuned_a,
            tuned_b,
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=capped_samples,
            seed=seed + 1,
        )

        rng = random.Random(seed + 2)
        wins_a = wins_b = 0
        game_one_total = max(1, game_one.wins_a_pct + game_one.wins_b_pct)
        postboard_total = max(1, postboard.wins_a_pct + postboard.wins_b_pct)
        game_one_win_a = game_one.wins_a_pct / game_one_total
        postboard_win_a = postboard.wins_a_pct / postboard_total

        for _ in range(capped_samples):
            score_a = int(rng.random() < game_one_win_a)
            score_b = 1 - score_a
            while score_a < 2 and score_b < 2:
                if rng.random() < postboard_win_a:
                    score_a += 1
                else:
                    score_b += 1
            wins_a += int(score_a == 2)
            wins_b += int(score_b == 2)

        return BestOfThreeReport(
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=capped_samples,
            match_wins_a_pct=round(wins_a * 100 / capped_samples),
            match_wins_b_pct=round(wins_b * 100 / capped_samples),
            game_one=game_one,
            postboard=postboard,
            plan_a=plan_a,
            plan_b=plan_b,
            impacts_a=(),
            impacts_b=(),
        )


def main() -> None:
    validation.combinations = fast_combinations
    validation.MatchupSimulator = FastMatchupSimulator
    validation.BestOfThreeSimulator = FastBestOfThreeSimulator
    validation.main()


if __name__ == "__main__":
    main()
