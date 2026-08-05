from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any, Iterable

from scripts.ci_global_validation import DATABASE_FILE, _prepare_database
from thun_deckbuilder.benchmark import BenchmarkAnalyzer
from thun_deckbuilder.card_analyzer import analyze_card, simulation_metadata_roles
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, parse_mana_cost
from thun_deckbuilder.deck_profile import BURN_PROFILE
from thun_deckbuilder.deck_validation import validate_deck
from thun_deckbuilder.goldfish_simulator import GoldfishSimulator
from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
from thun_deckbuilder.mana_distribution import LandAllocation, ManaDistribution
from thun_deckbuilder.mana_quality import analyze_mana_quality
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = (
    PROJECT_ROOT
    / "research"
    / "decks"
    / "pioneer_rdw_thun_challenger_2026-08-05.json"
)
BASIC_LANDS = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}


def _jsonable(value: object) -> object:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _canonical_section(items: Iterable[dict[str, Any]]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted((str(item["name"]), int(item["quantity"])) for item in items))


def _deck_hash(deck: dict[str, Any]) -> str:
    canonical = {
        "mainboard": _canonical_section(deck["mainboard"]),
        "lands": _canonical_section(deck["lands"]),
        "sideboard": _canonical_section(deck["sideboard"]),
    }
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _generated_snapshot(deck: GeneratedDeck) -> dict[str, Any]:
    lands: list[dict[str, Any]] = []
    if deck.mana_base is not None and deck.mana_base.lands:
        lands = [
            {
                "quantity": int(item.quantity),
                "name": str(item.land_name),
                "color": str(item.color),
            }
            for item in deck.mana_base.lands
        ]
    else:
        lands = [{"quantity": int(deck.lands), "name": "Mountain", "color": "R"}]
    return {
        "mainboard": [
            {"quantity": int(entry.quantity), "name": str(entry.name)}
            for entry in deck.mainboard
        ],
        "lands": lands,
        "sideboard": [
            {"quantity": int(entry.quantity), "name": str(entry.name)}
            for entry in deck.sideboard
        ],
    }


def _entry(card: dict[str, Any], quantity: int) -> DeckEntry:
    analysis = analyze_card(card)
    roles = tuple(
        sorted(
            {
                *(str(role) for role in detect_roles(analysis)),
                *simulation_metadata_roles(analysis),
            }
        )
    )
    return DeckEntry(
        name=analysis.name,
        quantity=quantity,
        mana_cost=parse_mana_cost(str(card.get("mana_cost", ""))),
        mana_value=analysis.mana_value,
        type_line=analysis.type_line,
        score=0.0,
        reasons=("Fixed evidence-backed composition audit",),
        roles=roles,
    )


def _lookup_legal(
    legal_cards: dict[str, dict[str, Any]],
    name: str,
) -> dict[str, Any]:
    card = legal_cards.get(name.casefold())
    if card is None:
        raise ValueError(f"Card is not legal in the current Thun pool: {name}")
    return card


def _build_fixed_deck(
    specification: dict[str, Any],
    legal_cards: dict[str, dict[str, Any]],
) -> GeneratedDeck:
    mainboard = tuple(
        _entry(
            _lookup_legal(legal_cards, str(item["name"])),
            int(item["quantity"]),
        )
        for item in specification["mainboard"]
    )
    sideboard = tuple(
        _entry(
            _lookup_legal(legal_cards, str(item["name"])),
            int(item["quantity"]),
        )
        for item in specification["sideboard"]
    )

    land_allocations: list[LandAllocation] = []
    for item in specification["lands"]:
        name = str(item["name"])
        if name not in BASIC_LANDS:
            _lookup_legal(legal_cards, name)
        land_allocations.append(
            LandAllocation(
                color=str(item.get("color", "R")).upper(),
                land_name=name,
                quantity=int(item["quantity"]),
            )
        )
    land_count = sum(item.quantity for item in land_allocations)

    mana = ManaBaseBuilder().build(
        mainboard,
        total_lands=land_count,
        deck_size=60,
    )
    distribution = ManaDistribution(
        lands=tuple(land_allocations),
        total_lands=land_count,
        required_sources=mana.distribution.required_sources,
    )
    mana_quality = analyze_mana_quality(
        mana.requirement,
        distribution,
        recommended_lands=mana.quality.recommended_lands,
    )
    return GeneratedDeck(
        mainboard=mainboard,
        lands=land_count,
        profile_name=str(specification.get("name", "Fixed Burn Challenger")),
        mana_base=distribution,
        mana_quality=mana_quality,
        sideboard=sideboard,
    )


def _analyze_deck(deck: GeneratedDeck) -> tuple[GeneratedDeck, dict[str, Any]]:
    opening = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="burn",
        samples=100,
        seed=1701,
    )
    goldfish = GoldfishSimulator().simulate(
        deck,
        archetype="burn",
        samples=2000,
        turns=5,
        seed=31,
    )
    benchmark = BenchmarkAnalyzer().analyze(deck, "burn")
    enriched = replace(
        deck,
        opening_hand_report=opening,
        goldfish_report=goldfish,
        benchmark_report=benchmark,
    )
    validation = validate_deck(enriched, profile=BURN_PROFILE)

    curve = {"0-1": 0, "2": 0, "3": 0, "4+": 0}
    roles: Counter[str] = Counter()
    creatures = 0
    for entry in enriched.mainboard:
        key = (
            "0-1"
            if entry.mana_value <= 1
            else "2"
            if entry.mana_value <= 2
            else "3"
            if entry.mana_value <= 3
            else "4+"
        )
        curve[key] += entry.quantity
        creatures += entry.quantity if "creature" in entry.type_line.lower() else 0
        for role in entry.roles:
            roles[str(role)] += entry.quantity

    return enriched, {
        "benchmark": _jsonable(benchmark),
        "opening_hand": _jsonable(opening),
        "goldfish": _jsonable(goldfish),
        "mana_quality": _jsonable(enriched.mana_quality),
        "profile_validation": _jsonable(validation),
        "curve": curve,
        "creatures": creatures,
        "role_counts": dict(sorted(roles.items())),
    }


def _copy_limit_errors(specification: dict[str, Any]) -> list[str]:
    copies: Counter[str] = Counter()
    for section in ("mainboard", "lands", "sideboard"):
        for item in specification[section]:
            name = str(item["name"])
            if name in BASIC_LANDS:
                continue
            copies[name] += int(item["quantity"])
    return [
        f"{quantity} copies of {name} across mainboard and sideboard"
        for name, quantity in sorted(copies.items())
        if quantity > 3
    ]


def _quantity_for_names(
    specification: dict[str, Any],
    names: Iterable[str],
    *,
    include_lands: bool = False,
) -> int:
    wanted = {str(name) for name in names}
    sections = [specification["mainboard"]]
    if include_lands:
        sections.append(specification["lands"])
    return sum(
        int(item["quantity"])
        for section in sections
        for item in section
        if str(item["name"]) in wanted
    )


def _structural_metrics(specification: dict[str, Any]) -> dict[str, Any]:
    groups = specification["functional_groups"]
    turn_one_names = tuple(groups["turn_one_packages"])
    return {
        "mainboard_total": sum(int(item["quantity"]) for item in specification["mainboard"])
        + sum(int(item["quantity"]) for item in specification["lands"]),
        "sideboard_total": sum(int(item["quantity"]) for item in specification["sideboard"]),
        "spell_count": sum(int(item["quantity"]) for item in specification["mainboard"]),
        "land_count": sum(int(item["quantity"]) for item in specification["lands"]),
        "red_sources": sum(
            int(item["quantity"])
            for item in specification["lands"]
            if str(item.get("color", "")).upper() == "R"
        ),
        "turn_one_copies": _quantity_for_names(specification, turn_one_names),
        "distinct_turn_one_names": len(set(turn_one_names)),
        "repeatable_spell_damage_copies": _quantity_for_names(
            specification,
            groups["repeatable_spell_damage"],
        ),
        "direct_face_burn_copies": _quantity_for_names(
            specification,
            groups["direct_face_burn"],
        ),
        "pump_or_trample_copies": _quantity_for_names(
            specification,
            groups["pump_or_trample"],
        ),
        "explicit_reload_copies": _quantity_for_names(
            specification,
            groups["explicit_reload"],
        ),
        "conditional_reload_copies": _quantity_for_names(
            specification,
            groups["conditional_reload"],
        ),
        "copy_limit_errors": _copy_limit_errors(specification),
    }


def _gate_results(
    fixture: dict[str, Any],
    champion_metrics: dict[str, Any],
    challenger_metrics: dict[str, Any],
    structural: dict[str, Any],
) -> dict[str, bool]:
    criteria = fixture["technical_success_criteria"]
    champion_benchmark = int(champion_metrics["benchmark"]["score"])
    challenger_benchmark = int(challenger_metrics["benchmark"]["score"])
    champion_plan = int(champion_metrics["opening_hand"]["plan_capable_pct"])
    challenger_plan = int(challenger_metrics["opening_hand"]["plan_capable_pct"])
    return {
        "exact_mainboard": structural["mainboard_total"] == int(criteria["exact_mainboard"]),
        "exact_sideboard": structural["sideboard_total"] == int(criteria["exact_sideboard"]),
        "copy_limit": not structural["copy_limit_errors"],
        "turn_one_density": structural["turn_one_copies"] >= int(criteria["minimum_turn_one_copies"]),
        "turn_one_redundancy": structural["distinct_turn_one_names"]
        >= int(criteria["minimum_distinct_turn_one_names"]),
        "red_sources": structural["red_sources"] >= int(criteria["minimum_red_sources"]),
        "explicit_reload": structural["explicit_reload_copies"]
        >= int(criteria["minimum_explicit_reload_copies"]),
        "benchmark_delta": challenger_benchmark
        >= champion_benchmark - int(criteria["maximum_benchmark_drop_vs_champion"]),
        "plan_capable_delta": challenger_plan
        >= champion_plan - int(criteria["maximum_plan_capable_drop_vs_champion"]),
        "turn_two_play": int(challenger_metrics["opening_hand"]["early_play_turn_two_pct"])
        >= int(criteria["minimum_turn_two_play_pct"]),
        "turn_three_play": int(challenger_metrics["opening_hand"]["early_play_turn_three_pct"])
        >= int(criteria["minimum_turn_three_play_pct"]),
        "profile_validation": bool(challenger_metrics["profile_validation"]["valid"]),
        "mana_quality": bool(challenger_metrics["mana_quality"]["sufficient"]),
    }


def _arena_text(specification: dict[str, Any]) -> str:
    lines = ["Deck"]
    lines.extend(
        f"{int(item['quantity'])} {item['name']}"
        for item in specification["mainboard"]
    )
    lines.extend(
        f"{int(item['quantity'])} {item['name']}"
        for item in specification["lands"]
    )
    lines.extend(["", "Sideboard"])
    lines.extend(
        f"{int(item['quantity'])} {item['name']}"
        for item in specification["sideboard"]
    )
    return "\n".join(lines) + "\n"


def _delta(after: Any, before: Any) -> Any:
    if isinstance(after, (int, float)) and isinstance(before, (int, float)):
        return round(after - before, 2)
    return None


def _comparison(champion: dict[str, Any], challenger: dict[str, Any]) -> dict[str, Any]:
    fields = {
        "benchmark": (champion["benchmark"]["score"], challenger["benchmark"]["score"]),
        "keepability_pct": (
            champion["opening_hand"]["keepability_pct"],
            challenger["opening_hand"]["keepability_pct"],
        ),
        "plan_capable_pct": (
            champion["opening_hand"]["plan_capable_pct"],
            challenger["opening_hand"]["plan_capable_pct"],
        ),
        "turn_two_play_pct": (
            champion["opening_hand"]["early_play_turn_two_pct"],
            challenger["opening_hand"]["early_play_turn_two_pct"],
        ),
        "turn_three_play_pct": (
            champion["opening_hand"]["early_play_turn_three_pct"],
            challenger["opening_hand"]["early_play_turn_three_pct"],
        ),
        "mana_error_pct": (
            champion["opening_hand"]["mana_error_pct"],
            challenger["opening_hand"]["mana_error_pct"],
        ),
        "average_damage": (
            champion["goldfish"]["average_damage"],
            challenger["goldfish"]["average_damage"],
        ),
        "kill_by_turn_five_pct": (
            champion["goldfish"]["kill_by_final_turn_pct"],
            challenger["goldfish"]["kill_by_final_turn_pct"],
        ),
        "average_spells_cast": (
            champion["goldfish"]["average_spells_cast"],
            challenger["goldfish"]["average_spells_cast"],
        ),
        "average_unused_mana": (
            champion["goldfish"]["average_unused_mana"],
            challenger["goldfish"]["average_unused_mana"],
        ),
        "mana_quality": (
            champion["mana_quality"]["score"],
            challenger["mana_quality"]["score"],
        ),
    }
    return {
        name: {"champion": before, "challenger": after, "delta": _delta(after, before)}
        for name, (before, after) in fields.items()
    }


def build_audit(fixture_path: Path) -> dict[str, Any]:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    _prepare_database()

    with CardDatabase(DATABASE_FILE) as database:
        legal_cards = {
            str(card.get("name", "")).casefold(): card
            for card in database.get_all_legal_cards()
        }
        current_champion = generate_deck(
            database=database,
            archetype="burn",
            colors=("R",),
        )
        current_snapshot = _generated_snapshot(current_champion)
        expected_snapshot = {
            key: fixture["champion"][key]
            for key in ("mainboard", "lands", "sideboard")
        }
        champion_matches = all(
            _canonical_section(current_snapshot[section])
            == _canonical_section(expected_snapshot[section])
            for section in ("mainboard", "lands", "sideboard")
        )
        if not champion_matches:
            return {
                "status": "STOP_STALE_CHAMPION",
                "experiment_id": fixture["experiment_id"],
                "expected_champion": expected_snapshot,
                "current_generated_champion": current_snapshot,
                "reason": "The current generated Burn Champion no longer matches the Run 79 snapshot; a fair comparison requires a refreshed champion fixture.",
            }

        challenger = _build_fixed_deck(fixture["challenger"], legal_cards)

    champion_enriched, champion_metrics = _analyze_deck(current_champion)
    challenger_enriched, challenger_metrics = _analyze_deck(challenger)
    structural = _structural_metrics(fixture["challenger"])
    gates = _gate_results(
        fixture,
        champion_metrics,
        challenger_metrics,
        structural,
    )
    technical_pass = all(gates.values())

    return {
        "status": "PASS" if technical_pass else "FAIL_TECHNICAL_GATE",
        "experiment_id": fixture["experiment_id"],
        "date": fixture["date"],
        "hypothesis": fixture["hypothesis"],
        "source": fixture["source"],
        "champion": {
            "name": fixture["champion"]["name"],
            "hash": _deck_hash(expected_snapshot),
            "recorded_hash": fixture["champion"]["recorded_hash"],
            "metrics": champion_metrics,
            "recorded_metrics": fixture["champion"]["recorded_metrics"],
            "current_snapshot_matches_fixture": champion_matches,
            "arena": _arena_text(expected_snapshot),
        },
        "challenger": {
            "name": fixture["challenger"]["name"],
            "hash": _deck_hash(fixture["challenger"]),
            "metrics": challenger_metrics,
            "structural_metrics": structural,
            "arena": _arena_text(fixture["challenger"]),
            "mulligan_guide": fixture["challenger"]["mulligan_guide"],
            "sideboard_plans": fixture["challenger"]["sideboard_plans"],
            "rejected_cards": fixture["challenger"]["rejected_cards"],
        },
        "comparison": _comparison(champion_metrics, challenger_metrics),
        "technical_gates": gates,
        "technical_gate_passed": technical_pass,
        "arena_test_authorized": technical_pass,
        "champion_replacement_authorized": False,
        "kgb_decision": "no new KGB",
        "limitations": [
            "The repository Goldfish model is a deterministic technical proxy, not an Arena win-rate estimate.",
            "The Burn Goldfish model compresses card text into broad roles and does not fully represent prowess, attack triggers, Saga chapter timing, combat tricks, death-triggered reload, or opponent interaction.",
            "Ramunap Ruins is counted as a red source, but its colored activation costs life and its damage ability requires four mana plus sacrificing a Desert.",
            "No real Arena games are attached to either hash in this experiment.",
        ],
        "arena_test_plan": fixture["arena_test_plan"],
        "arena_success_criteria": fixture["arena_success_criteria"],
        "next_step": (
            "Import the Challenger into Arena and execute the predefined 12-match BO3 test while preserving the Burn Champion."
            if technical_pass
            else "Do not run Arena yet; inspect the failed technical gates and revise at most one composition hypothesis."
        ),
    }


def render_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# Pioneer RDW — Thun Composition Audit",
        "",
        f"Status: **{audit['status']}**",
        "",
    ]
    if audit["status"] == "STOP_STALE_CHAMPION":
        lines.extend([audit["reason"], ""])
        return "\n".join(lines)

    lines.extend(
        [
            "## Hypothesis",
            "",
            audit["hypothesis"],
            "",
            "## Champion versus Challenger",
            "",
            "| Metric | Champion | Challenger | Delta |",
            "|---|---:|---:|---:|",
        ]
    )
    for name, values in audit["comparison"].items():
        lines.append(
            f"| {name} | {values['champion']} | {values['challenger']} | {values['delta']} |"
        )

    lines.extend(["", "## Technical gates", ""])
    for name, passed in audit["technical_gates"].items():
        lines.append(f"- {'PASS' if passed else 'FAIL'} — `{name}`")

    structural = audit["challenger"]["structural_metrics"]
    lines.extend(
        [
            "",
            "## Challenger structure",
            "",
            f"- Mainboard: {structural['mainboard_total']}",
            f"- Sideboard: {structural['sideboard_total']}",
            f"- Lands / red sources: {structural['land_count']} / {structural['red_sources']}",
            f"- Turn-one packages: {structural['turn_one_copies']} copies across {structural['distinct_turn_one_names']} names",
            f"- Repeatable spell-damage creatures: {structural['repeatable_spell_damage_copies']}",
            f"- Direct face burn: {structural['direct_face_burn_copies']}",
            f"- Explicit / conditional reload: {structural['explicit_reload_copies']} / {structural['conditional_reload_copies']}",
            "",
            "## Arena import",
            "",
            "```text",
            audit["challenger"]["arena"].rstrip(),
            "```",
            "",
            "## Decision",
            "",
            f"- Technical gate: {'passed' if audit['technical_gate_passed'] else 'failed'}",
            f"- Arena test authorized: {audit['arena_test_authorized']}",
            "- Champion replacement authorized: false",
            "- KGB: no new KGB",
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in audit["limitations"])
    lines.extend(["", "## Exactly one next step", "", audit["next_step"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--arena-output", type=Path, required=True)
    args = parser.parse_args()

    audit = build_audit(args.fixture)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.arena_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(render_markdown(audit), encoding="utf-8")
    if audit.get("challenger"):
        args.arena_output.write_text(audit["challenger"]["arena"], encoding="utf-8")
    else:
        args.arena_output.write_text("", encoding="utf-8")
    print(f"status={audit['status']}")
    print(f"wrote={args.json_output}")
    print(f"wrote={args.markdown_output}")
    print(f"wrote={args.arena_output}")
    return 0 if audit["status"] in {"PASS", "FAIL_TECHNICAL_GATE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
