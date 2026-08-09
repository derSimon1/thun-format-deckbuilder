from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping


DIMENSION_WEIGHTS: Mapping[str, float] = {
    "function_coverage": 0.25,
    "redundancy_3copy": 0.20,
    "mana_base": 0.15,
    "role_compression": 0.15,
    "sequence_preservation": 0.15,
    "recovery_resilience": 0.10,
}


class TransferBand(StrEnum):
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


@dataclass(frozen=True)
class ArchetypeTransferRecord:
    archetype_id: str
    name: str
    format: str
    ranked_decks: int
    fingerprint_decks: int
    dimensions: Mapping[str, float]
    fingerprint: tuple[str, ...]
    direct_functions: tuple[str, ...]
    functional_replacements: tuple[str, ...]
    non_reproducible_functions: tuple[str, ...]
    critical_dependency_missing: bool = False
    confidence: str = "medium"

    @property
    def score(self) -> float:
        """Return the transparent 0-10 Thun transfer score."""
        missing = set(DIMENSION_WEIGHTS) - set(self.dimensions)
        extra = set(self.dimensions) - set(DIMENSION_WEIGHTS)
        if missing or extra:
            raise ValueError(
                f"Invalid dimensions for {self.archetype_id}: "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
            )

        weighted = 0.0
        for dimension, weight in DIMENSION_WEIGHTS.items():
            value = self.dimensions[dimension]
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Dimension {dimension!r} for {self.archetype_id} "
                    f"must be between 0 and 1, got {value}."
                )
            weighted += value * weight

        score = weighted * 10.0
        if self.critical_dependency_missing:
            score = min(score, 4.9)
        return round(score, 2)

    @property
    def band(self) -> TransferBand:
        if self.score >= 8.0:
            return TransferBand.VERY_HIGH
        if self.score >= 7.0:
            return TransferBand.HIGH
        if self.score >= 5.0:
            return TransferBand.MEDIUM
        if self.score >= 3.0:
            return TransferBand.LOW
        return TransferBand.VERY_LOW


@dataclass(frozen=True)
class MetaTransferSnapshot:
    snapshot_id: str
    as_of: str
    minimum_ranked_decks: int
    methodology: str
    sources: tuple[Mapping[str, Any], ...]
    principles: tuple[str, ...]
    archetypes: tuple[ArchetypeTransferRecord, ...]

    def validate(self, minimum_archetypes: int = 10) -> None:
        if len(self.archetypes) < minimum_archetypes:
            raise ValueError(
                f"Snapshot requires at least {minimum_archetypes} archetypes; "
                f"found {len(self.archetypes)}."
            )

        ids = [record.archetype_id for record in self.archetypes]
        if len(ids) != len(set(ids)):
            raise ValueError("Archetype IDs must be unique.")

        for record in self.archetypes:
            for sample_name, sample_size in (
                ("ranked decks", record.ranked_decks),
                ("fingerprint decks", record.fingerprint_decks),
            ):
                if sample_size < self.minimum_ranked_decks:
                    raise ValueError(
                        f"{record.archetype_id} has only {sample_size} {sample_name}; "
                        f"minimum is {self.minimum_ranked_decks}."
                    )
            _ = record.score

    def ranked(self) -> tuple[ArchetypeTransferRecord, ...]:
        return tuple(
            sorted(
                self.archetypes,
                key=lambda record: (-record.score, record.format, record.name),
            )
        )


def _record_from_dict(data: Mapping[str, Any]) -> ArchetypeTransferRecord:
    return ArchetypeTransferRecord(
        archetype_id=str(data["id"]),
        name=str(data["name"]),
        format=str(data["format"]),
        ranked_decks=int(data["ranked_decks"]),
        fingerprint_decks=int(data["fingerprint_decks"]),
        dimensions={key: float(value) for key, value in data["dimensions"].items()},
        fingerprint=tuple(str(item) for item in data["fingerprint"]),
        direct_functions=tuple(str(item) for item in data["direct_functions"]),
        functional_replacements=tuple(
            str(item) for item in data["functional_replacements"]
        ),
        non_reproducible_functions=tuple(
            str(item) for item in data["non_reproducible_functions"]
        ),
        critical_dependency_missing=bool(
            data.get("critical_dependency_missing", False)
        ),
        confidence=str(data.get("confidence", "medium")),
    )


def load_snapshot(path: str | Path) -> MetaTransferSnapshot:
    source = Path(path)
    with source.open(encoding="utf-8") as handle:
        data = json.load(handle)

    snapshot = MetaTransferSnapshot(
        snapshot_id=str(data["snapshot_id"]),
        as_of=str(data["as_of"]),
        minimum_ranked_decks=int(data["minimum_ranked_decks"]),
        methodology=str(data["methodology"]),
        sources=tuple(data["sources"]),
        principles=tuple(str(item) for item in data["principles"]),
        archetypes=tuple(_record_from_dict(item) for item in data["archetypes"]),
    )
    snapshot.validate()
    return snapshot
