from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from thun_deckbuilder.config import AppConfig, load_config
from thun_deckbuilder.legality import is_card_legal
from thun_deckbuilder.paths import DATABASE_FILE


def _decode_json_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        try:
            decoded = json.loads(stripped)
            if isinstance(decoded, list):
                return [str(item) for item in decoded]
        except json.JSONDecodeError:
            pass
        return [item.strip() for item in stripped.split(",") if item.strip()]
    return []


def _row_to_card(row: sqlite3.Row) -> dict[str, Any]:
    card = dict(row)
    card["colors"] = _decode_json_list(card.get("colors"))
    card["color_identity"] = _decode_json_list(card.get("color_identity"))
    card.setdefault("mana_cost", "")
    card.setdefault("power", None)
    card.setdefault("toughness", None)
    return card


class CardDatabase:
    """Read-only access to Oracle cards and their printings."""

    def __init__(self, database_path: str | Path | None = None) -> None:
        selected_path = database_path or os.environ.get("THUN_DATABASE_FILE") or DATABASE_FILE
        self.database_path = Path(selected_path).resolve()
        if not self.database_path.is_file():
            raise FileNotFoundError(f"Kartendatenbank nicht gefunden: {self.database_path}")

        self.connection = sqlite3.connect(
            f"file:{self.database_path.as_posix()}?mode=ro",
            uri=True,
        )
        self.connection.row_factory = sqlite3.Row
        self._validate_schema()
        self.card_columns = self._columns("cards")
        self.print_columns = self._columns("prints")

    def _validate_schema(self) -> None:
        tables = {
            str(row[0])
            for row in self.connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        missing = {"cards", "prints"} - tables
        if missing:
            self.connection.close()
            raise ValueError(
                "Ungültige Kartendatenbank. Fehlende Tabellen: "
                + ", ".join(sorted(missing))
            )

    def _columns(self, table: str) -> set[str]:
        return {
            str(row[1])
            for row in self.connection.execute(f"PRAGMA table_info({table})")
        }

    def _card_select_columns(self) -> str:
        desired = [
            "oracle_id", "name", "mana_cost", "mana_value", "colors",
            "color_identity", "type_line", "oracle_text", "keywords",
            "power", "toughness",
        ]
        return ", ".join(column for column in desired if column in self.card_columns)

    def close(self) -> None:
        self.connection.close()

    def get_card_by_name(self, name: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            f"SELECT {self._card_select_columns()} FROM cards "
            "WHERE name = ? COLLATE NOCASE LIMIT 1",
            (name,),
        ).fetchone()
        return _row_to_card(row) if row is not None else None

    def get_all_cards(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            f"SELECT {self._card_select_columns()} FROM cards ORDER BY name"
        ).fetchall()
        return [_row_to_card(row) for row in rows]

    def get_prints(self, oracle_id: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM prints WHERE oracle_id = ? ORDER BY released_at, set_code",
            (oracle_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def get_all_legal_cards(
        self,
        config: AppConfig | None = None,
    ) -> list[dict[str, Any]]:
        active_config = config or load_config()
        cards = self.get_all_cards()
        legal_cards: list[dict[str, Any]] = []
        for card in cards:
            oracle_id = str(card.get("oracle_id", ""))
            if not oracle_id:
                continue
            result = is_card_legal(self.get_prints(oracle_id), active_config)
            if result.legal:
                enriched = dict(card)
                enriched["legal_prints"] = list(result.legal_prints)
                legal_cards.append(enriched)
        return legal_cards

    def is_card_legal_by_name(
        self,
        name: str,
        config: AppConfig | None = None,
    ) -> bool:
        card = self.get_card_by_name(name)
        if card is None:
            return False
        return is_card_legal(
            self.get_prints(str(card["oracle_id"])),
            config or load_config(),
        ).legal

    def __enter__(self) -> "CardDatabase":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.close()
