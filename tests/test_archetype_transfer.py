import json
from pathlib import Path

import pytest

from thun_deckbuilder.archetype_transfer import (
    ArchetypeTransferRecord,
    TransferBand,
    load_snapshot,
)


SNAPSHOT = (
    Path(__file__).resolve().parents[1]
    / "research"
    / "meta"
    / "archetype_transfer_snapshot_2026-08-05.json"
)


def test_snapshot_contains_at_least_ten_supported_archetypes():
    snapshot = load_snapshot(SNAPSHOT)
    assert len(snapshot.archetypes) >= 10
    assert all(record.ranked_decks >= 100 for record in snapshot.archetypes)
    assert all(record.fingerprint_decks >= 100 for record in snapshot.archetypes)
    assert {record.format for record in snapshot.archetypes} == {"Pioneer", "Standard"}


def test_ranking_places_redundant_low_rarity_shells_above_named_combo():
    ranked = load_snapshot(SNAPSHOT).ranked()
    names = [record.name for record in ranked]
    assert names.index("Pioneer Red Deck Wins") < names.index("Abzan Greasefang")
    assert names.index("Mono-Green Landfall") < names.index("Four-Color Control")


def test_critical_missing_dependency_caps_score():
    record = ArchetypeTransferRecord(
        archetype_id="critical-combo",
        name="Critical Combo",
        format="Pioneer",
        ranked_decks=100,
        fingerprint_decks=100,
        dimensions={
            "function_coverage": 1,
            "redundancy_3copy": 1,
            "mana_base": 1,
            "role_compression": 1,
            "sequence_preservation": 1,
            "recovery_resilience": 1,
        },
        fingerprint=("A",),
        direct_functions=(),
        functional_replacements=(),
        non_reproducible_functions=("Unique combo",),
        critical_dependency_missing=True,
    )
    assert record.score == 4.9
    assert record.band == TransferBand.LOW


def test_snapshot_rejects_an_archetype_below_minimum(tmp_path):
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    data["archetypes"][0]["ranked_decks"] = 99
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="only 99 ranked decks"):
        load_snapshot(path)


def test_dimension_schema_is_strict():
    record = ArchetypeTransferRecord(
        archetype_id="broken",
        name="Broken",
        format="Standard",
        ranked_decks=100,
        fingerprint_decks=100,
        dimensions={"function_coverage": 0.5},
        fingerprint=(),
        direct_functions=(),
        functional_replacements=(),
        non_reproducible_functions=(),
    )
    with pytest.raises(ValueError, match="Invalid dimensions"):
        _ = record.score
