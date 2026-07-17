from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _database_has_cards_table(database_path: Path) -> bool:
    if not database_path.is_file():
        return False

    try:
        connection = sqlite3.connect(
            f"file:{database_path}?mode=ro",
            uri=True,
        )

        row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'cards'
            """
        ).fetchone()

        connection.close()
        return row is not None

    except sqlite3.Error:
        return False


def _find_default_database() -> Path:
    candidates = [
        PROJECT_ROOT / "data" / "cards.db",
        PROJECT_ROOT / "cards.db",
        PROJECT_ROOT / "database" / "cards.db",
    ]

    for candidate in candidates:
        if _database_has_cards_table(candidate):
            return candidate

    for candidate in PROJECT_ROOT.rglob("cards.db"):
        if _database_has_cards_table(candidate):
            return candidate

    raise FileNotFoundError(
        "Keine gültige cards.db mit einer Tabelle 'cards' gefunden."
    )


def _decode_json_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):
        stripped_value = value.strip()

        if not stripped_value:
            return []

        try:
            decoded = json.loads(stripped_value)

            if isinstance(decoded, list):
                return [str(item) for item in decoded]

        except json.JSONDecodeError:
            pass

        return [
            item.strip()
            for item in stripped_value.split(",")
            if item.strip()
        ]

    return []


def _row_to_card(row: sqlite3.Row) -> dict[str, Any]:
    card = dict(row)

    card["colors"] = _decode_json_list(card.get("colors"))
    card["color_identity"] = _decode_json_list(
        card.get("color_identity")
    )

    card.setdefault("mana_cost", "")
    card.setdefault("power", None)
    card.setdefault("toughness", None)

    return card


class CardDatabase:
    def __init__(
        self,
        database_path: str | Path | None = None,
    ) -> None:
        if database_path is None:
            self.database_path = _find_default_database()
        else:
            self.database_path = Path(database_path).resolve()

            if not _database_has_cards_table(self.database_path):
                raise FileNotFoundError(
                    "Die angegebene Datenbank existiert nicht oder "
                    "enthält keine Tabelle 'cards': "
                    f"{self.database_path}"
                )

        self.connection = sqlite3.connect(
            f"file:{self.database_path}?mode=ro",
            uri=True,
        )
        self.connection.row_factory = sqlite3.Row

        self.card_columns = self._get_card_columns()

    def _get_card_columns(self) -> set[str]:
        rows = self.connection.execute(
            "PRAGMA table_info(cards)"
        ).fetchall()

        return {
            str(row["name"])
            for row in rows
        }

    def _select_columns(self) -> str:
        required_columns = [
            "name",
            "mana_value",
            "colors",
            "color_identity",
            "type_line",
            "oracle_text",
        ]

        optional_columns = [
            "mana_cost",
        ]

        columns = [
            column
            for column in required_columns + optional_columns
            if column in self.card_columns
        ]

        return ", ".join(columns)

    def close(self) -> None:
        self.connection.close()

    def get_card_by_name(
        self,
        name: str,
    ) -> dict[str, Any] | None:
        columns = self._select_columns()

        query = f"""
        SELECT {columns}
        FROM cards
        WHERE name = ?
        LIMIT 1
        """

        row = self.connection.execute(
            query,
            (name,),
        ).fetchone()

        if row is None:
            return None

        return _row_to_card(row)

    def get_all_cards(self) -> list[dict[str, Any]]:
        columns = self._select_columns()

        query = f"""
        SELECT {columns}
        FROM cards
        """

        rows = self.connection.execute(query).fetchall()

        return [
            _row_to_card(row)
            for row in rows
        ]

    def __enter__(self) -> "CardDatabase":
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()