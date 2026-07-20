from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from thun_deckbuilder.paths import THUN_CONFIG_FILE


@dataclass(frozen=True)
class FormatConfig:
    code: str
    name: str
    deck_size: int
    sideboard_size: int
    max_copies: int
    singleton: bool
    commander_required: bool


@dataclass(frozen=True)
class LegalityConfig:
    allowed_rarities: tuple[str, ...]
    paper_only: bool
    allow_digital: bool
    allow_acorn: bool
    allow_bonus_sheets: bool
    allow_special_guests: bool


@dataclass(frozen=True)
class SetConfig:
    starting_set: str
    blocked_sets: tuple[str, ...]
    allowed_sets: tuple[str, ...]


@dataclass(frozen=True)
class AppConfig:
    format: FormatConfig
    legality: LegalityConfig
    sets: SetConfig


def _lower_tuple(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        raise ValueError("Konfigurationswert muss eine Liste sein.")
    return tuple(str(value).strip().lower() for value in values)


def load_config(path: str | Path = THUN_CONFIG_FILE) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Konfigurationsdatei nicht gefunden: {config_path}"
        )

    with config_path.open("rb") as file_handle:
        raw = tomllib.load(file_handle)

    format_data = raw["format"]
    legality_data = raw["legality"]
    set_data = raw["sets"]

    config = AppConfig(
        format=FormatConfig(
            code=str(format_data["code"]),
            name=str(format_data["name"]),
            deck_size=int(format_data["deck_size"]),
            sideboard_size=int(format_data["sideboard_size"]),
            max_copies=int(format_data["max_copies"]),
            singleton=bool(format_data["singleton"]),
            commander_required=bool(format_data["commander_required"]),
        ),
        legality=LegalityConfig(
            allowed_rarities=_lower_tuple(legality_data["allowed_rarities"]),
            paper_only=bool(legality_data["paper_only"]),
            allow_digital=bool(legality_data["allow_digital"]),
            allow_acorn=bool(legality_data["allow_acorn"]),
            allow_bonus_sheets=bool(legality_data["allow_bonus_sheets"]),
            allow_special_guests=bool(legality_data["allow_special_guests"]),
        ),
        sets=SetConfig(
            starting_set=str(set_data["starting_set"]).lower(),
            blocked_sets=_lower_tuple(set_data["blocked_sets"]),
            allowed_sets=_lower_tuple(set_data["allowed_sets"]),
        ),
    )

    overlap = set(config.sets.allowed_sets) & set(config.sets.blocked_sets)
    if overlap:
        raise ValueError(
            "Sets dürfen nicht gleichzeitig erlaubt und gesperrt sein: "
            + ", ".join(sorted(overlap))
        )
    return config
