from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files


@dataclass(frozen=True)
class BenchmarkRoleTarget:
    role: str
    target: float
    minimum: float = 0.0


@dataclass(frozen=True)
class BenchmarkCurveTarget:
    maximum_mana_value: float
    target: int


@dataclass(frozen=True)
class BenchmarkDefinition:
    key: str
    name: str
    archetype: str
    colors: tuple[str, ...]
    lands: int
    role_targets: tuple[BenchmarkRoleTarget, ...]
    curve_targets: tuple[BenchmarkCurveTarget, ...]


class BenchmarkLoader:
    def load(self, key: str) -> BenchmarkDefinition:
        normalized = key.strip().lower().replace("-", "_")
        resource = files("thun_deckbuilder.benchmarks").joinpath(f"{normalized}.json")
        if not resource.is_file():
            raise KeyError(f"Unknown benchmark: {key}")
        data = json.loads(resource.read_text(encoding="utf-8"))
        return BenchmarkDefinition(
            key=normalized,
            name=str(data["name"]),
            archetype=str(data["archetype"]),
            colors=tuple(str(color).upper() for color in data["colors"]),
            lands=int(data["lands"]),
            role_targets=tuple(
                BenchmarkRoleTarget(
                    role=str(item["role"]),
                    target=float(item["target"]),
                    minimum=float(item.get("minimum", 0)),
                )
                for item in data.get("roles", ())
            ),
            curve_targets=tuple(
                BenchmarkCurveTarget(
                    maximum_mana_value=float(item["maximum_mana_value"]),
                    target=int(item["target"]),
                )
                for item in data.get("curve", ())
            ),
        )

    def available(self) -> tuple[str, ...]:
        root = files("thun_deckbuilder.benchmarks")
        return tuple(sorted(item.name[:-5] for item in root.iterdir() if item.name.endswith(".json")))
