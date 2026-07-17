from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "data" / "cards.db"

SCRYFALL_SETS_URL = "https://api.scryfall.com/sets"

USER_AGENT = "ThunFormatDeckbuilder/0.1"
TIMEOUT_SECONDS = 60


class SetUpdateError(RuntimeError):
    """Fehler beim Laden oder Speichern der Scryfall-Sets."""


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
    )
    return session


def download_sets(
    session: requests.Session,
) -> list[dict[str, Any]]:
    """Lädt sämtliche Set-Objekte aus der Scryfall-API."""

    response = session.get(
        SCRYFALL_SETS_URL,
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    payload = response.json()

    sets = payload.get("data")

    if not isinstance(sets, list):
        raise SetUpdateError(
            "Die Scryfall-Antwort enthält keine Set-Liste."
        )

    if not sets:
        raise SetUpdateError(
            "Scryfall hat eine leere Set-Liste geliefert."
        )

    return sets


def create_sets_table(
    connection: sqlite3.Connection,
) -> None:
    """Erstellt die Set-Tabelle und benötigte Indizes."""

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS sets (
            set_id TEXT PRIMARY KEY,
            set_code TEXT NOT NULL UNIQUE,
            mtgo_code TEXT,
            arena_code TEXT,
            tcgplayer_id INTEGER,
            name TEXT NOT NULL,
            set_type TEXT NOT NULL,
            released_at TEXT,
            block_code TEXT,
            block_name TEXT,
            parent_set_code TEXT,
            card_count INTEGER NOT NULL DEFAULT 0,
            printed_size INTEGER,
            digital INTEGER NOT NULL DEFAULT 0,
            foil_only INTEGER NOT NULL DEFAULT 0,
            nonfoil_only INTEGER NOT NULL DEFAULT 0,
            icon_svg_uri TEXT,
            search_uri TEXT,
            scryfall_uri TEXT,
            uri TEXT,
            updated_at TEXT NOT NULL,

            thun_allowed INTEGER NOT NULL DEFAULT 0,
            thun_reviewed INTEGER NOT NULL DEFAULT 0,
            thun_note TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_sets_code
            ON sets(set_code);

        CREATE INDEX IF NOT EXISTS idx_sets_type
            ON sets(set_type);

        CREATE INDEX IF NOT EXISTS idx_sets_release
            ON sets(released_at);

        CREATE INDEX IF NOT EXISTS idx_sets_thun_allowed
            ON sets(thun_allowed);

        CREATE INDEX IF NOT EXISTS idx_sets_thun_reviewed
            ON sets(thun_reviewed);
        """
    )


def upsert_set(
    connection: sqlite3.Connection,
    set_data: dict[str, Any],
    updated_at: str,
) -> None:
    """
    Fügt ein Set ein oder aktualisiert dessen Scryfall-Daten.

    Die manuell gepflegten Felder thun_allowed, thun_reviewed und
    thun_note bleiben bei Updates erhalten.
    """

    set_id = set_data.get("id")
    set_code = set_data.get("code")
    name = set_data.get("name")
    set_type = set_data.get("set_type")

    if not set_id or not set_code or not name or not set_type:
        raise SetUpdateError(
            f"Unvollständiges Set-Objekt: {set_data}"
        )

    connection.execute(
        """
        INSERT INTO sets (
            set_id,
            set_code,
            mtgo_code,
            arena_code,
            tcgplayer_id,
            name,
            set_type,
            released_at,
            block_code,
            block_name,
            parent_set_code,
            card_count,
            printed_size,
            digital,
            foil_only,
            nonfoil_only,
            icon_svg_uri,
            search_uri,
            scryfall_uri,
            uri,
            updated_at
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        ON CONFLICT(set_code) DO UPDATE SET
            set_id = excluded.set_id,
            mtgo_code = excluded.mtgo_code,
            arena_code = excluded.arena_code,
            tcgplayer_id = excluded.tcgplayer_id,
            name = excluded.name,
            set_type = excluded.set_type,
            released_at = excluded.released_at,
            block_code = excluded.block_code,
            block_name = excluded.block_name,
            parent_set_code = excluded.parent_set_code,
            card_count = excluded.card_count,
            printed_size = excluded.printed_size,
            digital = excluded.digital,
            foil_only = excluded.foil_only,
            nonfoil_only = excluded.nonfoil_only,
            icon_svg_uri = excluded.icon_svg_uri,
            search_uri = excluded.search_uri,
            scryfall_uri = excluded.scryfall_uri,
            uri = excluded.uri,
            updated_at = excluded.updated_at
        """,
        (
            set_id,
            str(set_code).lower(),
            set_data.get("mtgo_code"),
            set_data.get("arena_code"),
            set_data.get("tcgplayer_id"),
            name,
            set_type,
            set_data.get("released_at"),
            set_data.get("block_code"),
            set_data.get("block"),
            set_data.get("parent_set_code"),
            int(set_data.get("card_count", 0) or 0),
            set_data.get("printed_size"),
            int(bool(set_data.get("digital", False))),
            int(bool(set_data.get("foil_only", False))),
            int(bool(set_data.get("nonfoil_only", False))),
            set_data.get("icon_svg_uri"),
            set_data.get("search_uri"),
            set_data.get("scryfall_uri"),
            set_data.get("uri"),
            updated_at,
        ),
    )


def create_views(
    connection: sqlite3.Connection,
) -> None:
    """Erstellt hilfreiche Ansichten für Set-Prüfung und Freigabe."""

    connection.executescript(
        """
        DROP VIEW IF EXISTS v_sets_pending_review;

        CREATE VIEW v_sets_pending_review AS
        SELECT
            set_code,
            name,
            set_type,
            released_at,
            digital,
            parent_set_code,
            card_count
        FROM sets
        WHERE thun_reviewed = 0
        ORDER BY
            CASE
                WHEN released_at IS NULL THEN 1
                ELSE 0
            END,
            released_at DESC,
            set_code;


        DROP VIEW IF EXISTS v_thun_allowed_sets;

        CREATE VIEW v_thun_allowed_sets AS
        SELECT
            set_code,
            name,
            set_type,
            released_at,
            digital,
            parent_set_code,
            card_count,
            thun_note
        FROM sets
        WHERE thun_allowed = 1
        ORDER BY released_at, set_code;


        DROP VIEW IF EXISTS v_recent_sets;

        CREATE VIEW v_recent_sets AS
        SELECT
            set_code,
            name,
            set_type,
            released_at,
            digital,
            parent_set_code,
            card_count,
            thun_allowed,
            thun_reviewed
        FROM sets
        WHERE released_at IS NOT NULL
        ORDER BY released_at DESC, set_code;
        """
    )


def update_sets() -> tuple[int, int, int]:
    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            f"Datenbank nicht gefunden: {DATABASE_FILE}\n"
            "Führe zuerst aus: python scripts/build_index.py"
        )

    session = create_session()

    try:
        print("Lade Set-Liste von Scryfall ...")
        sets = download_sets(session)

    finally:
        session.close()

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        create_sets_table(connection)

        updated_at = datetime.now(timezone.utc).isoformat()

        for set_data in sets:
            upsert_set(
                connection=connection,
                set_data=set_data,
                updated_at=updated_at,
            )

        create_views(connection)
        connection.commit()

        total_sets = connection.execute(
            "SELECT COUNT(*) FROM sets"
        ).fetchone()[0]

        pending_sets = connection.execute(
            """
            SELECT COUNT(*)
            FROM sets
            WHERE thun_reviewed = 0
            """
        ).fetchone()[0]

        allowed_sets = connection.execute(
            """
            SELECT COUNT(*)
            FROM sets
            WHERE thun_allowed = 1
            """
        ).fetchone()[0]

        return total_sets, pending_sets, allowed_sets

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def main() -> int:
    try:
        total_sets, pending_sets, allowed_sets = update_sets()

        print()
        print("Set-Datenbank erfolgreich aktualisiert.")
        print(f"Sets insgesamt:       {total_sets:,}")
        print(f"Noch nicht geprüft:   {pending_sets:,}")
        print(f"Für Thun freigegeben: {allowed_sets:,}")

        return 0

    except requests.RequestException as exc:
        print(f"Netzwerkfehler: {exc}", file=sys.stderr)
        return 1

    except (
        FileNotFoundError,
        OSError,
        sqlite3.Error,
        SetUpdateError,
    ) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())