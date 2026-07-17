from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "data" / "cards.db"

THUN_FORMAT_CODE = "thun"
THUN_FORMAT_NAME = "Magic Club Thun Clubformat"


def create_schema(connection: sqlite3.Connection) -> None:
    """Erstellt die Tabellen für Formate und deren Set-Freigaben."""

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS formats (
            format_code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            deck_size INTEGER NOT NULL,
            sideboard_size INTEGER NOT NULL DEFAULT 0,
            max_copies INTEGER NOT NULL,
            singleton INTEGER NOT NULL DEFAULT 0,
            commander_required INTEGER NOT NULL DEFAULT 0,
            allowed_rarities TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS format_sets (
            format_code TEXT NOT NULL,
            set_code TEXT NOT NULL,
            status TEXT NOT NULL
                CHECK (status IN ('allowed', 'blocked', 'pending')),
            reason TEXT,
            reviewed_at TEXT,
            PRIMARY KEY (format_code, set_code),

            FOREIGN KEY (format_code)
                REFERENCES formats(format_code)
                ON DELETE CASCADE,

            FOREIGN KEY (set_code)
                REFERENCES sets(set_code)
                ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_format_sets_format
            ON format_sets(format_code);

        CREATE INDEX IF NOT EXISTS idx_format_sets_status
            ON format_sets(status);

        CREATE INDEX IF NOT EXISTS idx_format_sets_format_status
            ON format_sets(format_code, status);
        """
    )


def seed_thun_format(connection: sqlite3.Connection) -> None:
    """Legt das normale Magic-Club-Thun-Clubformat an."""

    timestamp = datetime.now(timezone.utc).isoformat()

    connection.execute(
        """
        INSERT INTO formats (
            format_code,
            name,
            description,
            deck_size,
            sideboard_size,
            max_copies,
            singleton,
            commander_required,
            allowed_rarities,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(format_code) DO UPDATE SET
            name = excluded.name,
            description = excluded.description,
            deck_size = excluded.deck_size,
            sideboard_size = excluded.sideboard_size,
            max_copies = excluded.max_copies,
            singleton = excluded.singleton,
            commander_required = excluded.commander_required,
            allowed_rarities = excluded.allowed_rarities,
            updated_at = excluded.updated_at
        """,
        (
            THUN_FORMAT_CODE,
            THUN_FORMAT_NAME,
            (
                "60 Karten Main Deck, 15 Karten Sideboard, "
                "maximal 3 Kopien pro Karte, nur Commons und Uncommons."
            ),
            60,
            15,
            3,
            0,
            0,
            "common,uncommon",
            timestamp,
            timestamp,
        ),
    )


def seed_format_sets(connection: sqlite3.Connection) -> None:
    """
    Fügt sämtliche bekannten Sets zunächst als 'pending' ein.

    Bereits manuell gesetzte Statuswerte bleiben erhalten.
    """

    connection.execute(
    """
    INSERT OR IGNORE INTO format_sets (
        format_code,
        set_code,
        status,
        reason,
        reviewed_at
    )
    SELECT
        ?,
        set_code,
        'pending',
        'Noch nicht für das Thunformat geprüft.',
        NULL
    FROM sets
    """,
    (THUN_FORMAT_CODE,),
)


def create_views(connection: sqlite3.Connection) -> None:
    """Erstellt hilfreiche Views für Verwaltung und spätere Legalität."""

    connection.executescript(
        """
        DROP VIEW IF EXISTS v_format_sets;

        CREATE VIEW v_format_sets AS
        SELECT
            fs.format_code,
            f.name AS format_name,
            fs.set_code,
            s.name AS set_name,
            s.set_type,
            s.released_at,
            s.digital,
            s.parent_set_code,
            fs.status,
            fs.reason,
            fs.reviewed_at
        FROM format_sets AS fs
        JOIN formats AS f
            ON f.format_code = fs.format_code
        JOIN sets AS s
            ON s.set_code = fs.set_code;


        DROP VIEW IF EXISTS v_thun_allowed_sets;

        CREATE VIEW v_thun_allowed_sets AS
        SELECT *
        FROM v_format_sets
        WHERE format_code = 'thun'
          AND status = 'allowed'
        ORDER BY released_at, set_code;


        DROP VIEW IF EXISTS v_thun_pending_sets;

        CREATE VIEW v_thun_pending_sets AS
        SELECT *
        FROM v_format_sets
        WHERE format_code = 'thun'
          AND status = 'pending'
        ORDER BY
            CASE
                WHEN released_at IS NULL THEN 1
                ELSE 0
            END,
            released_at DESC,
            set_code;


        DROP VIEW IF EXISTS v_thun_blocked_sets;

        CREATE VIEW v_thun_blocked_sets AS
        SELECT *
        FROM v_format_sets
        WHERE format_code = 'thun'
          AND status = 'blocked'
        ORDER BY released_at, set_code;
        """
    )


def main() -> int:
    if not DATABASE_FILE.exists():
        print(
            f"Datenbank nicht gefunden: {DATABASE_FILE}",
            file=sys.stderr,
        )
        return 1

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        print("Erstelle Format-Schema ...")
        create_schema(connection)

        print("Lege Thunformat an ...")
        seed_thun_format(connection)

        print("Übernehme bekannte Sets ...")
        seed_format_sets(connection)

        print("Erstelle Views ...")
        create_views(connection)

        connection.commit()

        format_count = connection.execute(
            "SELECT COUNT(*) FROM formats"
        ).fetchone()[0]

        format_set_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM format_sets
            WHERE format_code = ?
            """,
            (THUN_FORMAT_CODE,),
        ).fetchone()[0]

        pending_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM format_sets
            WHERE format_code = ?
              AND status = 'pending'
            """,
            (THUN_FORMAT_CODE,),
        ).fetchone()[0]

        print()
        print("Formatverwaltung erfolgreich erstellt.")
        print(f"Formate:             {format_count:,}")
        print(f"Thun-Seteinträge:    {format_set_count:,}")
        print(f"Noch nicht geprüft:  {pending_count:,}")

        return 0

    except sqlite3.Error as exc:
        connection.rollback()
        print(f"SQLite-Fehler: {exc}", file=sys.stderr)
        return 1

    finally:
        connection.close()


if __name__ == "__main__":
    raise SystemExit(main())