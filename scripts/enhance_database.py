from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "data" / "cards.db"


def supports_fts5(connection: sqlite3.Connection) -> bool:
    """Prüft, ob die verwendete SQLite-Version FTS5 unterstützt."""

    try:
        connection.execute(
            "CREATE VIRTUAL TABLE temp.fts5_test USING fts5(content)"
        )
        connection.execute("DROP TABLE temp.fts5_test")
        return True
    except sqlite3.OperationalError:
        return False


def create_indexes(connection: sqlite3.Connection) -> None:
    """Erstellt Indizes für häufige Filter- und Join-Abfragen."""

    connection.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_cards_name_nocase
            ON cards(name COLLATE NOCASE);

        CREATE INDEX IF NOT EXISTS idx_cards_mana_value
            ON cards(mana_value);

        CREATE INDEX IF NOT EXISTS idx_cards_type_line
            ON cards(type_line);

        CREATE INDEX IF NOT EXISTS idx_cards_colors
            ON cards(colors);

        CREATE INDEX IF NOT EXISTS idx_cards_color_identity
            ON cards(color_identity);

        CREATE INDEX IF NOT EXISTS idx_prints_oracle_id
            ON prints(oracle_id);

        CREATE INDEX IF NOT EXISTS idx_prints_set_code
            ON prints(set_code);

        CREATE INDEX IF NOT EXISTS idx_prints_set_type
            ON prints(set_type);

        CREATE INDEX IF NOT EXISTS idx_prints_rarity
            ON prints(rarity);

        CREATE INDEX IF NOT EXISTS idx_prints_released_at
            ON prints(released_at);

        CREATE INDEX IF NOT EXISTS idx_prints_digital
            ON prints(digital);

        CREATE INDEX IF NOT EXISTS idx_prints_promo
            ON prints(promo);

        CREATE INDEX IF NOT EXISTS idx_prints_set_rarity
            ON prints(set_code, rarity);

        CREATE INDEX IF NOT EXISTS idx_prints_oracle_set
            ON prints(oracle_id, set_code);
        """
    )


def create_views(connection: sqlite3.Connection) -> None:
    """Erstellt wiederverwendbare Ansichten für spätere Module."""

    connection.executescript(
        """
        DROP VIEW IF EXISTS v_card_prints;

        CREATE VIEW v_card_prints AS
        SELECT
            c.oracle_id,
            c.name,
            c.mana_cost,
            c.mana_value,
            c.colors,
            c.color_identity,
            c.type_line,
            c.oracle_text,
            c.keywords,
            p.scryfall_id,
            p.set_code,
            p.set_name,
            p.set_type,
            p.rarity,
            p.collector_number,
            p.released_at,
            p.digital,
            p.promo,
            p.reprint,
            p.booster,
            p.games,
            p.lang,
            p.arena_id,
            p.image_uri
        FROM cards AS c
        JOIN prints AS p
            ON p.oracle_id = c.oracle_id;


        DROP VIEW IF EXISTS v_common_uncommon_prints;

        CREATE VIEW v_common_uncommon_prints AS
        SELECT *
        FROM v_card_prints
        WHERE rarity IN ('common', 'uncommon');


        DROP VIEW IF EXISTS v_paper_common_uncommon_prints;

        CREATE VIEW v_paper_common_uncommon_prints AS
        SELECT *
        FROM v_common_uncommon_prints
        WHERE digital = 0
          AND games LIKE '%paper%';


        DROP VIEW IF EXISTS v_card_summary;

        CREATE VIEW v_card_summary AS
        SELECT
            c.oracle_id,
            c.name,
            c.mana_cost,
            c.mana_value,
            c.colors,
            c.color_identity,
            c.type_line,
            c.oracle_text,
            c.keywords,
            COUNT(p.scryfall_id) AS print_count,
            MIN(p.released_at) AS first_release,
            MAX(p.released_at) AS latest_release,
            GROUP_CONCAT(DISTINCT p.set_code) AS set_codes,
            GROUP_CONCAT(DISTINCT p.rarity) AS rarities
        FROM cards AS c
        LEFT JOIN prints AS p
            ON p.oracle_id = c.oracle_id
        GROUP BY c.oracle_id;
        """
    )


def create_fts_index(connection: sqlite3.Connection) -> bool:
    """
    Erstellt eine eigenständige FTS5-Tabelle.

    Die Tabelle wird bei jedem Lauf neu aus der cards-Tabelle aufgebaut.
    """

    if not supports_fts5(connection):
        return False

    connection.executescript(
        """
        DROP TABLE IF EXISTS cards_fts;

        CREATE VIRTUAL TABLE cards_fts USING fts5(
            oracle_id UNINDEXED,
            name,
            type_line,
            oracle_text,
            keywords,
            tokenize = 'unicode61 remove_diacritics 2',
            prefix = '2 3 4'
        );

        INSERT INTO cards_fts (
            oracle_id,
            name,
            type_line,
            oracle_text,
            keywords
        )
        SELECT
            oracle_id,
            name,
            COALESCE(type_line, ''),
            COALESCE(oracle_text, ''),
            COALESCE(keywords, '')
        FROM cards;
        """
    )

    return True


def run_integrity_checks(connection: sqlite3.Connection) -> None:
    """Bricht ab, wenn die Datenbank offensichtlich beschädigt ist."""

    result = connection.execute("PRAGMA integrity_check").fetchone()

    if not result or result[0] != "ok":
        raise RuntimeError(
            f"SQLite-Integritätsprüfung fehlgeschlagen: {result}"
        )

    card_count = connection.execute(
        "SELECT COUNT(*) FROM cards"
    ).fetchone()[0]

    print_count = connection.execute(
        "SELECT COUNT(*) FROM prints"
    ).fetchone()[0]

    if card_count == 0:
        raise RuntimeError("Die Tabelle 'cards' ist leer.")

    if print_count == 0:
        raise RuntimeError("Die Tabelle 'prints' ist leer.")


def main() -> int:
    if not DATABASE_FILE.exists():
        print(
            f"Datenbank nicht gefunden: {DATABASE_FILE}",
            file=sys.stderr,
        )
        print(
            "Führe zuerst aus: python scripts/build_index.py",
            file=sys.stderr,
        )
        return 1

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        print("Prüfe Datenbank ...")
        run_integrity_checks(connection)

        print("Erstelle Indizes ...")
        create_indexes(connection)

        print("Erstelle Views ...")
        create_views(connection)

        print("Erstelle Volltextindex ...")
        fts_created = create_fts_index(connection)

        connection.commit()

        card_count = connection.execute(
            "SELECT COUNT(*) FROM cards"
        ).fetchone()[0]

        print_count = connection.execute(
            "SELECT COUNT(*) FROM prints"
        ).fetchone()[0]

        print()
        print("Datenbank erfolgreich erweitert.")
        print(f"Oracle-Karten: {card_count:,}")
        print(f"Druckversionen: {print_count:,}")
        print(
            "FTS5-Suche: "
            + ("aktiv" if fts_created else "nicht verfügbar")
        )

        return 0

    except (sqlite3.Error, RuntimeError) as exc:
        connection.rollback()
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    finally:
        connection.close()


if __name__ == "__main__":
    raise SystemExit(main())