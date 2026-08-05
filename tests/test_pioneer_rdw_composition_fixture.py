import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (
    ROOT
    / "research"
    / "decks"
    / "pioneer_rdw_thun_challenger_v2_2026-08-05.json"
)
V1_RESULT = (
    ROOT
    / "research"
    / "decks"
    / "pioneer_rdw_thun_challenger_v1_result_2026-08-05.json"
)
BASICS = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def load_v1_result():
    return json.loads(V1_RESULT.read_text(encoding="utf-8"))


def total(items):
    return sum(int(item["quantity"]) for item in items)


def test_v1_negative_result_is_preserved():
    result = load_v1_result()
    assert result["status"] == "rejected_technical"
    assert result["failed_gates"] == ["benchmark_delta", "plan_capable_delta"]
    assert result["arena_test_authorized"] is False
    assert result["champion_replacement_authorized"] is False


def test_challenger_is_exactly_60_15():
    challenger = load_fixture()["challenger"]
    assert total(challenger["mainboard"]) + total(challenger["lands"]) == 60
    assert total(challenger["sideboard"]) == 15


def test_challenger_respects_three_copy_rule_across_all_sections():
    challenger = load_fixture()["challenger"]
    copies = Counter()
    for section in ("mainboard", "lands", "sideboard"):
        for item in challenger[section]:
            if item["name"] not in BASICS:
                copies[item["name"]] += int(item["quantity"])
    assert copies
    assert max(copies.values()) <= 3


def test_turn_one_plan_has_exact_final_redundancy():
    challenger = load_fixture()["challenger"]
    quantities = {
        item["name"]: int(item["quantity"])
        for item in challenger["mainboard"]
    }
    names = challenger["functional_groups"]["turn_one_packages"]
    assert len(set(names)) == 4
    assert sum(quantities[name] for name in names) == 12


def test_challenger_has_six_repeatable_spell_damage_creatures():
    challenger = load_fixture()["challenger"]
    quantities = {
        item["name"]: int(item["quantity"])
        for item in challenger["mainboard"]
    }
    names = challenger["functional_groups"]["repeatable_spell_damage"]
    assert sum(quantities[name] for name in names) == 6


def test_final_cycle_uses_22_lands_and_no_pump_package():
    challenger = load_fixture()["challenger"]
    assert total(challenger["lands"]) == 22
    assert challenger["functional_groups"]["pump_or_trample"] == []
    assert total(challenger["mainboard"]) == 38


def test_rockface_village_is_explicitly_rejected():
    rejected = {
        item["name"]: item["reason"]
        for item in load_fixture()["challenger"]["rejected_cards"]
    }
    assert "Rockface Village" in rejected
    assert "Lizard, Mouse, Otter, or Raccoon" in rejected["Rockface Village"]


def test_champion_replacement_requires_arena_comparison():
    fixture = load_fixture()
    assert fixture["arena_success_criteria"][
        "champion_replacement_requires_direct_arena_comparison"
    ] is True
    assert fixture["challenger"]["status"] == "untested"
    assert fixture["cycle"] == 2


def test_exactly_one_next_step_is_recorded():
    fixture = load_fixture()
    assert isinstance(fixture["next_step"], str)
    assert fixture["next_step"].strip()
