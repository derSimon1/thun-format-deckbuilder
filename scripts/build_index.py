from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Any

import ijson


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "default_cards.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "cards.db"

BATCH_SIZE = 2_000


def create_database(connection: sqlite3.Connection) -> None:
    """Erstellt die Tabellen für Oracle-Karten und einzelne Druckversionen."""

    connection.executescript(
        """
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA temp_store = MEMORY;

        CREATE TABLE IF NOT EXISTS cards (
            oracle_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mana_cost TEXT,
            mana_value REAL NOT NULL DEFAULT 0,
            colors TEXT NOT NULL DEFAULT '',
            color_identity TEXT NOT NULL DEFAULT '',
            type_line TEXT,
            oracle_text TEXT,
            keywords TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS prints (
            scryfall_id TEXT PRIMARY KEY,
            oracle_id TEXT NOT NULL,
            name TEXT NOT NULL,
            set_code TEXT NOT NULL,
            set_name TEXT,
            set_type TEXT,
            rarity TEXT,
            collector_number TEXT,
            released_at TEXT,
            digital INTEGER NOT NULL DEFAULT 0,
            promo INTEGER NOT NULL DEFAULT 0,
            reprint INTEGER NOT NULL DEFAULT 0,
            booster INTEGER NOT NULL DEFAULT 0,
            games TEXT NOT NULL DEFAULT '',
            finishes TEXT NOT NULL DEFAULT '',
            frame_effects TEXT NOT NULL DEFAULT '',
            security_stamp TEXT,
            border_color TEXT,
            layout TEXT,
            lang TEXT,
            arena_id INTEGER,
            image_uri TEXT,
            FOREIGN KEY (oracle_id) REFERENCES cards (oracle_id)
        );

        CREATE INDEX IF NOT EXISTS idx_prints_oracle_id
            ON prints (oracle_id);

        CREATE INDEX IF NOT EXISTS idx_prints_set_code
            ON prints (set_code);

        CREATE INDEX IF NOT EXISTS idx_prints_rarity
            ON prints (rarity);

        CREATE INDEX IF NOT EXISTS idx_cards_name
            ON cards (name);

        CREATE INDEX IF NOT EXISTS idx_cards_color_identity
            ON cards (color_identity);
        """
    )


def join_values(value: Any) -> str:
    """Speichert Listen kompakt als kommaseparierten Text."""

    if not isinstance(value, list):
        return ""

    return ",".join(str(item) for item in value)


def get_image_uri(card: dict[str, Any]) -> str | None:
    """Liest ein geeignetes Kartenbild, auch bei doppelseitigen Karten."""

    image_uris = card.get("image_uris")

    if isinstance(image_uris, dict):
        return image_uris.get("normal") or image_uris.get("large")

    card_faces = card.get("card_faces")

    if isinstance(card_faces, list):
        for face in card_faces:
            face_images = face.get("image_uris", {})
            if isinstance(face_images, dict):
                image_uri = face_images.get("normal") or face_images.get("large")
                if image_uri:
                    return image_uri

    return None


def get_oracle_text(card: dict[str, Any]) -> str:
    """Verbindet bei mehrseitigen Karten die Oracle-Texte aller Seiten."""

    oracle_text = card.get("oracle_text")

    if isinstance(oracle_text, str):
        return oracle_text

    card_faces = card.get("card_faces")

    if not isinstance(card_faces, list):
        return ""

    face_texts = [
        face.get("oracle_text", "")
        for face in card_faces
        if face.get("oracle_text")
    ]

    return "\n//\n".join(face_texts)


def get_mana_cost(card: dict[str, Any]) -> str:
    mana_cost = card.get("mana_cost")

    if isinstance(mana_cost, str):
        return mana_cost

    card_faces = card.get("card_faces")

    if not isinstance(card_faces, list):
        return ""

    costs = [
        face.get("mana_cost", "")
        for face in card_faces
        if face.get("mana_cost")
    ]

    return " // ".join(costs)


def insert_card(
    connection: sqlite3.Connection,
    card: dict[str, Any],
) -> bool:
    """Speichert einen Print und aktualisiert den Oracle-Karteneintrag."""

    oracle_id = card.get("oracle_id")
    scryfall_id = card.get("id")
    name = card.get("name")

    # Tokens und einige Sonderobjekte besitzen keine Oracle-ID.
    if not oracle_id or not scryfall_id or not name:
        return False

    connection.execute(
        """
        INSERT INTO cards (
            oracle_id,
            name,
            mana_cost,
            mana_value,
            colors,
            color_identity,
            type_line,
            oracle_text,
            keywords
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(oracle_id) DO UPDATE SET
            name = excluded.name,
            mana_cost = excluded.mana_cost,
            mana_value = excluded.mana_value,
            colors = excluded.colors,
            color_identity = excluded.color_identity,
            type_line = excluded.type_line,
            oracle_text = excluded.oracle_text,
            keywords = excluded.keywords
        """,
        (
            oracle_id,
            name,
            get_mana_cost(card),
            float(card.get("cmc", 0) or 0),
            join_values(card.get("colors", [])),
            join_values(card.get("color_identity", [])),
            card.get("type_line", ""),
            get_oracle_text(card),
            join_values(card.get("keywords", [])),
        ),
    )

    connection.execute(
        """
        INSERT OR REPLACE INTO prints (
            scryfall_id,
            oracle_id,
            name,
            set_code,
            set_name,
            set_type,
            rarity,
            collector_number,
            released_at,
            digital,
            promo,
            reprint,
            booster,
            games,
            finishes,
            frame_effects,
            security_stamp,
            border_color,
            layout,
            lang,
            arena_id,
            image_uri
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            scryfall_id,
            oracle_id,
            name,
            card.get("set", "").lower(),
            card.get("set_name", ""),
            card.get("set_type", ""),
            card.get("rarity", ""),
            card.get("collector_number", ""),
            card.get("released_at", ""),
            int(bool(card.get("digital", False))),
            int(bool(card.get("promo", False))),
            int(bool(card.get("reprint", False))),
            int(bool(card.get("booster", False))),
            join_values(card.get("games", [])),
            join_values(card.get("finishes", [])),
            join_values(card.get("frame_effects", [])),
            card.get("security_stamp"),
            card.get("border_color", ""),
            card.get("layout", ""),
            card.get("lang", ""),
            card.get("arena_id"),
            get_image_uri(card),
        ),
    )

    return True


def build_index() -> tuple[int, int, int]:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Scryfall-Datei nicht gefunden: {INPUT_FILE}\n"
            "Führe zuerst aus: python scripts/download_scryfall.py"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Eine vorhandene Datenbank wird bewusst neu aufgebaut.
    OUTPUT_FILE.unlink(missing_ok=True)

    connection = sqlite3.connect(OUTPUT_FILE)

    try:
        create_database(connection)

        print(f"Lese Scryfall-Datei streamend: {INPUT_FILE}")
        print("Die Datei wird nicht vollständig in den RAM geladen.")

        processed_prints = 0
        stored_prints = 0
        skipped_prints = 0

        with INPUT_FILE.open("rb") as file_handle:
            for card in ijson.items(file_handle, "item"):
                processed_prints += 1

                if insert_card(connection, card):
                    stored_prints += 1
                else:
                    skipped_prints += 1

                if processed_prints % BATCH_SIZE == 0:
                    connection.commit()
                    print(
                        f"\rVerarbeitet: {processed_prints:,} Drucke",
                        end="",
                        flush=True,
                    )

        connection.commit()
        print()

        unique_cards = connection.execute(
            "SELECT COUNT(*) FROM cards"
        ).fetchone()[0]

        return unique_cards, stored_prints, skipped_prints

    finally:
        connection.close()


def main() -> int:
    try:
        unique_cards, stored_prints, skipped_prints = build_index()

        file_size_mb = OUTPUT_FILE.stat().st_size / 1024 / 1024

        print("Index erfolgreich erstellt.")
        print(f"Eindeutige Karten: {unique_cards:,}")
        print(f"Gespeicherte Prints: {stored_prints:,}")
        print(f"Übersprungene Prints: {skipped_prints:,}")
        print(f"Datenbankgröße: {file_size_mb:.1f} MB")
        print(f"Datei: {OUTPUT_FILE}")

        return 0

    except (OSError, sqlite3.Error) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())