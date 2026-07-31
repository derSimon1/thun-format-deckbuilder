from __future__ import annotations

import random
from dataclasses import dataclass

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.matchup_simulator import MatchupReport, MatchupSimulator
from thun_deckbuilder.sideboard_optimizer import (
    SideboardCardImpact,
    SideboardPlan,
    optimize_sideboard_plan,
)


@dataclass(frozen=True)
class BestOfThreeReport:
    archetype_a: str
    archetype_b: str
    samples: int
    match_wins_a_pct: int
    match_wins_b_pct: int
    game_one: MatchupReport
    postboard: MatchupReport
    plan_a: SideboardPlan
    plan_b: SideboardPlan
    impacts_a: tuple[SideboardCardImpact, ...] = ()
    impacts_b: tuple[SideboardCardImpact, ...] = ()


class BestOfThreeSimulator:
    def simulate(
        self,
        deck_a: GeneratedDeck,
        deck_b: GeneratedDeck,
        *,
        archetype_a: str,
        archetype_b: str,
        samples: int = 2000,
        seed: int = 53,
    ) -> BestOfThreeReport:
        if samples <= 0:
            raise ValueError("samples must be positive")
        simulator = MatchupSimulator()
        game_one = simulator.simulate(
            deck_a, deck_b,
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=samples,
            seed=seed,
        )
        tuned_a = optimize_sideboard_plan(
            deck_a, deck_b,
            archetype=archetype_a,
            opponent_archetype=archetype_b,
            samples=min(samples, 600),
            seed=seed + 10,
        )
        tuned_b = optimize_sideboard_plan(
            deck_b, deck_a,
            archetype=archetype_b,
            opponent_archetype=archetype_a,
            samples=min(samples, 600),
            seed=seed + 20,
        )
        postboard = simulator.simulate(
            tuned_a.deck, tuned_b.deck,
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=samples,
            seed=seed + 1,
        )
        rng = random.Random(seed + 2)
        wins_a = wins_b = 0
        p1 = game_one.wins_a_pct / max(1, game_one.wins_a_pct + game_one.wins_b_pct)
        pp = postboard.wins_a_pct / max(1, postboard.wins_a_pct + postboard.wins_b_pct)
        for _ in range(samples):
            score_a = score_b = 0
            score_a += int(rng.random() < p1)
            score_b = 1 - score_a
            while score_a < 2 and score_b < 2:
                if rng.random() < pp:
                    score_a += 1
                else:
                    score_b += 1
            wins_a += int(score_a == 2)
            wins_b += int(score_b == 2)
        return BestOfThreeReport(
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=samples,
            match_wins_a_pct=round(wins_a * 100 / samples),
            match_wins_b_pct=round(wins_b * 100 / samples),
            game_one=game_one,
            postboard=postboard,
            plan_a=tuned_a.plan,
            plan_b=tuned_b.plan,
            impacts_a=tuned_a.impacts,
            impacts_b=tuned_b.impacts,
        )


def format_bo3_report(report: BestOfThreeReport) -> str:
    lines = [
        "THUN BEST-OF-THREE MATCHUP", "=" * 72,
        f"{report.archetype_a} vs. {report.archetype_b}",
        f"Match wins: {report.archetype_a} {report.match_wins_a_pct}% / {report.archetype_b} {report.match_wins_b_pct}%",
        f"Game 1: {report.game_one.wins_a_pct}% / {report.game_one.wins_b_pct}%",
        f"Postboard games: {report.postboard.wins_a_pct}% / {report.postboard.wins_b_pct}%", "",
    ]
    for archetype, plan, impacts in (
        (report.archetype_a, report.plan_a, report.impacts_a),
        (report.archetype_b, report.plan_b, report.impacts_b),
    ):
        lines.append(f"{archetype} cards in: " + (", ".join(f"{qty} {name}" for name, qty in plan.cards_in) or "none"))
        lines.append(f"{archetype} cards out: " + (", ".join(f"{qty} {name}" for name, qty in plan.cards_out) or "none"))
        for impact in impacts:
            lines.append(f"  +{impact.win_rate_delta} pp: {impact.card_in} for {impact.card_out}")
    return "\n".join(lines)
