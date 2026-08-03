from __future__ import annotations

import json
import random
from itertools import combinations as all_combinations

import ci_global_validation_v2 as v2

from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator
from thun_deckbuilder.tournament_simulator import (
    BestOfThreeReport,
    BestOfThreeSimulator,
    board_for_matchup,
)


validation = v2.validation
FAST_MATCHUP_SAMPLES = 120
FAST_BO3_SAMPLES = 40
FAST_SIDEBOARD_SWAPS = 3
OPENING_HAND_PLAN_SAMPLES = 100
OPENING_HAND_PLAN_SEED = 1701
FAST_MATCHUP_PAIRS = (
    ("tokens", "burn"),
    ("tokens", "artifacts"),
    ("tokens", "mill"),
    ("control", "burn"),
    ("control", "tokens"),
    ("control", "artifacts"),
)
_BASE_VALIDATE_ARCHETYPE = validation._validate_archetype


def fast_combinations(archetypes, size: int):
    """Use Token- and Control-focused pairs in cyclic CI, preserving full mode."""

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


def validate_archetype_with_plan_hands(
    database,
    archetype,
    colors,
    legal_cards,
):
    """Add exactly 100 reproducible plan-aware raw hands to fast artifacts."""

    deck, metrics = _BASE_VALIDATE_ARCHETYPE(
        database,
        archetype,
        colors,
        legal_cards,
    )
    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype=archetype,
        samples=OPENING_HAND_PLAN_SAMPLES,
        seed=OPENING_HAND_PLAN_SEED,
    )
    payload = validation._jsonable(report)
    summary = dict(payload)
    summary.pop("hands", None)
    metrics["opening_hand_plan"] = summary

    prefix = validation.ARTIFACT_DIR / archetype
    raw_path = prefix / f"{archetype}-opening-hands.json"
    raw_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (prefix / f"{archetype}-validation.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with (prefix / f"{archetype}-validation.txt").open(
        "a",
        encoding="utf-8",
    ) as output:
        output.write(
            "opening_hand_plan="
            f"seed:{report.seed} samples:{report.samples} "
            f"keepability:{report.keepability_pct} "
            f"plan_capable:{report.plan_capable_pct} "
            f"early_t2:{report.early_play_turn_two_pct} "
            f"early_t3:{report.early_play_turn_three_pct}\n"
        )
    return deck, metrics


def main() -> None:
    v2.configure()
    validation.combinations = fast_combinations
    validation.MatchupSimulator = FastMatchupSimulator
    validation.BestOfThreeSimulator = FastBestOfThreeSimulator
    validation._validate_archetype = validate_archetype_with_plan_hands
    validation.main()


if __name__ == "__main__":
    main()
