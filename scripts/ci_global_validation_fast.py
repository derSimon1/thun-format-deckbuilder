from __future__ import annotations

import json
import random
import re
from itertools import combinations as all_combinations

import ci_global_validation_v2 as v2

from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.matchup_calibration import (
    build_calibration_report,
    load_observations,
)
from thun_deckbuilder.mill_signals import analyze_mill
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator
from thun_deckbuilder.paths import CONFIG_DIR
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


def _sideboard_diagnostics(deck) -> dict[str, object]:
    cards = [
        {
            "name": entry.name,
            "quantity": entry.quantity,
            "score": entry.score,
            "reasons": list(entry.reasons),
            "roles": list(entry.roles),
        }
        for entry in deck.sideboard
    ]
    return {
        "total_cards": sum(entry.quantity for entry in deck.sideboard),
        "cards": cards,
    }


def _mill_deck_diagnostics(deck) -> dict[str, object]:
    def metadata(entry, prefix: str) -> int:
        for role in entry.roles:
            match = re.fullmatch(rf"{re.escape(prefix)}(\d+)", str(role))
            if match:
                return int(match.group(1))
        return 0

    cards = [
        {
            "name": entry.name,
            "quantity": entry.quantity,
            "mana_value": entry.mana_value,
            "engine": "mill_engine" in entry.roles,
            "immediate_cards": metadata(entry, "mill_immediate_"),
            "repeatable_cards": metadata(entry, "mill_repeatable_"),
            "conditional_cards": metadata(entry, "mill_conditional_"),
            "roles": list(entry.roles),
            "reasons": list(entry.reasons),
        }
        for entry in deck.mainboard
        if "mill_source" in entry.roles
    ]
    return {
        "source_copies": sum(card["quantity"] for card in cards),
        "engine_copies": sum(
            card["quantity"] for card in cards if card["engine"]
        ),
        "distinct_sources": len(cards),
        "immediate_capacity": sum(
            card["quantity"] * card["immediate_cards"] for card in cards
        ),
        "repeatable_capacity": sum(
            card["quantity"] * card["repeatable_cards"] for card in cards
        ),
        "conditional_capacity": sum(
            card["quantity"] * card["conditional_cards"] for card in cards
        ),
        "cards": cards,
    }


def _control_deck_diagnostics(deck) -> dict[str, object]:
    cards = [
        {
            "name": entry.name,
            "quantity": entry.quantity,
            "mana_value": entry.mana_value,
            "answer": "control_answer" in entry.roles,
            "card_advantage": "control_card_advantage" in entry.roles,
            "finisher": "control_finisher" in entry.roles,
            "sweeper": "control_sweeper" in entry.roles,
            "roles": list(entry.roles),
            "reasons": list(entry.reasons),
        }
        for entry in deck.mainboard
    ]
    return {
        "answer_copies": sum(
            card["quantity"] for card in cards if card["answer"]
        ),
        "card_advantage_copies": sum(
            card["quantity"] for card in cards if card["card_advantage"]
        ),
        "finisher_copies": sum(
            card["quantity"] for card in cards if card["finisher"]
        ),
        "sweeper_copies": sum(
            card["quantity"] for card in cards if card["sweeper"]
        ),
        "cards": cards,
    }


def _artifact_deck_diagnostics(deck) -> dict[str, object]:
    def metadata(entry, prefix: str) -> int:
        for role in entry.roles:
            match = re.fullmatch(rf"{re.escape(prefix)}(\d+)", str(role))
            if match:
                return int(match.group(1))
        return 0

    cards = [
        {
            "name": entry.name,
            "quantity": entry.quantity,
            "mana_value": entry.mana_value,
            "enabler": "artifact_enabler" in entry.roles,
            "payoff": "artifact_payoff" in entry.roles,
            "engine": "artifact_engine" in entry.roles,
            "immediate_artifacts": metadata(entry, "artifact_immediate_"),
            "conditional_artifacts": metadata(entry, "artifact_conditional_"),
            "repeatable_artifacts": metadata(entry, "artifact_repeatable_"),
            "roles": list(entry.roles),
            "reasons": list(entry.reasons),
        }
        for entry in deck.mainboard
    ]
    return {
        "enabler_copies": sum(card["quantity"] for card in cards if card["enabler"]),
        "payoff_copies": sum(card["quantity"] for card in cards if card["payoff"]),
        "engine_copies": sum(card["quantity"] for card in cards if card["engine"]),
        "immediate_capacity": sum(
            card["quantity"] * card["immediate_artifacts"] for card in cards
        ),
        "conditional_capacity": sum(
            card["quantity"] * card["conditional_artifacts"] for card in cards
        ),
        "repeatable_capacity": sum(
            card["quantity"] * card["repeatable_artifacts"] for card in cards
        ),
        "cards": cards,
    }


def _write_mill_capacity() -> None:
    cards: list[dict[str, object]] = []
    allowed_colors = {"U", "B"}
    with CardDatabase(validation.DATABASE_FILE) as database:
        for card in database.get_all_legal_cards():
            analysis = analyze_card(card)
            if analysis.is_land:
                continue
            if not set(analysis.color_identity).issubset(allowed_colors):
                continue
            signals = analyze_mill(analysis)
            if not signals.source:
                continue
            cards.append(
                {
                    "name": analysis.name,
                    "mana_value": analysis.mana_value,
                    "color_identity": list(analysis.color_identity),
                    "engine": signals.engine,
                    "scalable": signals.scalable,
                    "fixed_cards": signals.fixed_cards,
                    "immediate_cards": signals.immediate_cards,
                    "repeatable_cards": signals.repeatable_cards,
                    "conditional_cards": signals.conditional_cards,
                }
            )
    cards.sort(key=lambda item: (item["mana_value"], item["name"]))
    payload = {
        "distinct_sources": len(cards),
        "maximum_copies_at_three": len(cards) * 3,
        "engine_sources": sum(bool(card["engine"]) for card in cards),
        "scalable_sources": sum(bool(card["scalable"]) for card in cards),
        "cards": cards,
    }
    (validation.ARTIFACT_DIR / "mill-capacity.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_matchup_calibration() -> None:
    report_path = validation.ARTIFACT_DIR / "global-report.json"
    global_report = json.loads(report_path.read_text(encoding="utf-8"))
    observations = load_observations(CONFIG_DIR / "matchup_observations.json")
    calibration = build_calibration_report(global_report, observations)
    (validation.ARTIFACT_DIR / "matchup-calibration.json").write_text(
        json.dumps(calibration, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    global_report["empirical_matchup_calibration"] = calibration
    report_path.write_text(
        json.dumps(global_report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary_path = validation.ARTIFACT_DIR / "global-summary.txt"
    with summary_path.open("a", encoding="utf-8") as summary:
        summary.write(
            "Empirical matchup calibration: "
            f"{calibration['status']} "
            f"matched_games={calibration['matched_games']} "
            f"coverage={calibration['prediction_coverage_pct']}%\n"
        )
    print(
        "Empirical matchup calibration: "
        f"{calibration['status']} "
        f"matched_games={calibration['matched_games']} "
        f"coverage={calibration['prediction_coverage_pct']}%"
    )


def validate_archetype_with_plan_hands(
    database,
    archetype,
    colors,
    legal_cards,
):
    """Add reproducible hand, sideboard and Mill diagnostics."""

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

    sideboard_payload = _sideboard_diagnostics(deck)
    metrics["sideboard_diagnostics"] = sideboard_payload

    prefix = validation.ARTIFACT_DIR / archetype
    raw_path = prefix / f"{archetype}-opening-hands.json"
    raw_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (prefix / f"{archetype}-sideboard.json").write_text(
        json.dumps(sideboard_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if archetype == "mill":
        mill_payload = _mill_deck_diagnostics(deck)
        metrics["mill_diagnostics"] = mill_payload
        (prefix / "mill-sources.json").write_text(
            json.dumps(mill_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if archetype == "control":
        control_payload = _control_deck_diagnostics(deck)
        metrics["control_diagnostics"] = control_payload
        (prefix / "control-sequence.json").write_text(
            json.dumps(control_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if archetype == "artifacts":
        artifact_payload = _artifact_deck_diagnostics(deck)
        metrics["artifact_diagnostics"] = artifact_payload
        (prefix / "artifact-access.json").write_text(
            json.dumps(artifact_payload, indent=2, sort_keys=True) + "\n",
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
        output.write(
            "sideboard_diagnostics="
            f"cards:{sideboard_payload['total_cards']} "
            f"entries:{len(sideboard_payload['cards'])}\n"
        )
        if archetype == "mill":
            output.write(
                "mill_diagnostics="
                f"sources:{metrics['mill_diagnostics']['source_copies']} "
                f"engines:{metrics['mill_diagnostics']['engine_copies']} "
                f"distinct:{metrics['mill_diagnostics']['distinct_sources']}\n"
            )
        if archetype == "control":
            output.write(
                "control_diagnostics="
                f"answers:{metrics['control_diagnostics']['answer_copies']} "
                "card_advantage:"
                f"{metrics['control_diagnostics']['card_advantage_copies']} "
                f"finishers:{metrics['control_diagnostics']['finisher_copies']} "
                f"sweepers:{metrics['control_diagnostics']['sweeper_copies']}\n"
            )
        if archetype == "artifacts":
            output.write(
                "artifact_diagnostics="
                f"enablers:{metrics['artifact_diagnostics']['enabler_copies']} "
                f"payoffs:{metrics['artifact_diagnostics']['payoff_copies']} "
                f"engines:{metrics['artifact_diagnostics']['engine_copies']} "
                f"immediate:{metrics['artifact_diagnostics']['immediate_capacity']} "
                f"conditional:{metrics['artifact_diagnostics']['conditional_capacity']} "
                f"repeatable:{metrics['artifact_diagnostics']['repeatable_capacity']}\n"
            )
    return deck, metrics


def main() -> None:
    v2.configure()
    validation.combinations = fast_combinations
    validation.MatchupSimulator = FastMatchupSimulator
    validation.BestOfThreeSimulator = FastBestOfThreeSimulator
    validation._validate_archetype = validate_archetype_with_plan_hands
    validation.main()
    _write_matchup_calibration()
    _write_mill_capacity()


if __name__ == "__main__":
    main()
