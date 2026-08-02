from __future__ import annotations

import json
import os
import sqlite3
from collections import Counter
from pathlib import Path

import ijson
import requests

from thun_deckbuilder.arena_export import format_arena_export
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck

HEADERS = {
    "User-Agent": "MagicClubThunDeckbuilder/0.1 (GitHub Actions)",
    "Accept": "application/json",
}
ALLOWED_COLORS = {"U", "R"}


def _download_default_cards(target: Path) -> None:
    response = requests.get(
        "https://api.scryfall.com/bulk-data",
        headers=HEADERS,
        timeout=60,
    )
    response.raise_for_status()
    entries = response.json().get("data", [])
    default_cards = next(
        (entry for entry in entries if entry.get("type") == "default_cards"),
        None,
    )
    if default_cards is None or not default_cards.get("download_uri"):
        raise RuntimeError("Scryfall bulk index does not contain default_cards.")

    with requests.get(
        default_cards["download_uri"],
        headers=HEADERS,
        stream=True,
        timeout=180,
    ) as download:
        download.raise_for_status()
        with target.open("wb") as output:
            for chunk in download.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)


def _build_database(bulk_file: Path, database_file: Path) -> None:
    database_file.unlink(missing_ok=True)
    connection = sqlite3.connect(database_file)
    connection.executescript(
        """
        CREATE TABLE cards (
            oracle_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mana_cost TEXT NOT NULL DEFAULT '',
            mana_value REAL NOT NULL DEFAULT 0,
            colors TEXT NOT NULL DEFAULT '[]',
            color_identity TEXT NOT NULL DEFAULT '[]',
            type_line TEXT NOT NULL DEFAULT '',
            oracle_text TEXT NOT NULL DEFAULT '',
            keywords TEXT NOT NULL DEFAULT '[]',
            power TEXT,
            toughness TEXT
        );
        CREATE TABLE prints (
            oracle_id TEXT NOT NULL,
            set_code TEXT NOT NULL,
            rarity TEXT NOT NULL,
            digital INTEGER NOT NULL DEFAULT 0,
            games TEXT NOT NULL DEFAULT '[]',
            released_at TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (oracle_id) REFERENCES cards (oracle_id)
        );
        CREATE INDEX prints_oracle_id ON prints (oracle_id);
        CREATE INDEX prints_set_code ON prints (set_code);
        """
    )

    card_rows: dict[str, tuple[object, ...]] = {}
    print_rows: list[tuple[object, ...]] = []
    with bulk_file.open("rb") as source:
        for item in ijson.items(source, "item"):
            oracle_id = item.get("oracle_id")
            if not oracle_id:
                continue
            faces = item.get("card_faces") or []
            mana_cost = item.get("mana_cost") or " // ".join(
                str(face.get("mana_cost", "")) for face in faces
            )
            oracle_text = item.get("oracle_text") or " // ".join(
                str(face.get("oracle_text", "")) for face in faces
            )
            power = item.get("power")
            toughness = item.get("toughness")
            if faces and power is None:
                power = faces[0].get("power")
            if faces and toughness is None:
                toughness = faces[0].get("toughness")

            card_rows[str(oracle_id)] = (
                str(oracle_id),
                item.get("name", ""),
                mana_cost,
                float(item.get("cmc", 0) or 0),
                json.dumps(item.get("colors", [])),
                json.dumps(item.get("color_identity", [])),
                item.get("type_line", ""),
                oracle_text,
                json.dumps(item.get("keywords", [])),
                power,
                toughness,
            )
            print_rows.append(
                (
                    str(oracle_id),
                    str(item.get("set", "")).lower(),
                    str(item.get("rarity", "")).lower(),
                    int(bool(item.get("digital", False))),
                    json.dumps(item.get("games", [])),
                    item.get("released_at", ""),
                )
            )

    connection.executemany(
        "INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        card_rows.values(),
    )
    connection.executemany(
        "INSERT INTO prints VALUES (?, ?, ?, ?, ?, ?)",
        print_rows,
    )
    connection.commit()
    connection.close()
    print(f"Built {database_file} with {len(card_rows)} cards and {len(print_rows)} prints.")


def _validate_card(database: CardDatabase, name: str, *, kind: str) -> dict[str, object]:
    card = database.get_card_by_name(name)
    assert card is not None, f"Unknown {kind}: {name}."
    assert database.is_card_legal_by_name(name), f"Illegal {kind}: {name}."
    identity = set(card.get("color_identity", ()))
    assert identity.issubset(ALLOWED_COLORS), (
        f"Off-color {kind} {name}: {sorted(identity)}."
    )
    return card


def _validate_and_export(database_file: Path) -> None:
    with CardDatabase(database_file) as database:
        deck = generate_deck(
            database=database,
            archetype="prowess",
            colors=("U", "R"),
        )
        main_spells = sum(entry.quantity for entry in deck.mainboard)
        mana_lands = (
            sum(land.quantity for land in deck.mana_base.lands)
            if deck.mana_base is not None
            else deck.lands
        )
        main_total = main_spells + mana_lands
        sideboard_total = sum(entry.quantity for entry in deck.sideboard)
        assert main_total == 60, f"Expected 60 mainboard cards, got {main_total}."
        assert sideboard_total == 15, f"Expected 15 sideboard cards, got {sideboard_total}."
        assert 18 <= mana_lands <= 22, f"Unexpected Prowess land count: {mana_lands}."

        combined: Counter[str] = Counter()
        for entry in (*deck.mainboard, *deck.sideboard):
            combined[entry.name] += entry.quantity
            _validate_card(database, entry.name, kind="card")
        for name, quantity in combined.items():
            card = database.get_card_by_name(name)
            type_line = str(card.get("type_line", "")) if card else ""
            if "Basic Land" not in type_line:
                assert quantity <= 3, f"Copy limit exceeded: {quantity} {name}."

        if deck.mana_base is not None:
            for land in deck.mana_base.lands:
                _validate_card(database, land.land_name, kind="land")

        threat_count = sum(
            entry.quantity for entry in deck.mainboard if "Creature" in entry.type_line
        )
        burn_count = sum(
            entry.quantity for entry in deck.mainboard if "burn" in entry.roles
        )
        draw_count = sum(
            entry.quantity for entry in deck.mainboard if "card_draw" in entry.roles
        )
        curve_one = sum(
            entry.quantity for entry in deck.mainboard if entry.mana_value <= 1
        )
        curve_two = sum(
            entry.quantity
            for entry in deck.mainboard
            if 1 < entry.mana_value <= 2
        )
        curve_three = sum(
            entry.quantity
            for entry in deck.mainboard
            if 2 < entry.mana_value <= 3
        )
        curve_four_plus = sum(
            entry.quantity for entry in deck.mainboard if entry.mana_value > 3
        )
        cheap_count = curve_one + curve_two

        assert threat_count >= 10, f"Too few threats: {threat_count}."
        assert burn_count >= 8, f"Too little burn/reach: {burn_count}."
        assert draw_count >= 6, f"Too little card flow: {draw_count}."
        assert cheap_count >= 28, f"Curve is too slow: only {cheap_count} cards cost two or less."
        assert curve_four_plus <= 2, (
            f"Curve is too top-heavy: {curve_four_plus} cards cost four or more."
        )

        arena_text = format_arena_export(deck)
        Path("izzet-prowess-v2-arena.txt").write_text(
            arena_text + "\n",
            encoding="utf-8",
        )
        metrics = {
            "status": "PASS",
            "mainboard": main_total,
            "sideboard": sideboard_total,
            "lands": mana_lands,
            "threats": threat_count,
            "burn_reach": burn_count,
            "card_flow": draw_count,
            "curve": {
                "mana_value_0_1": curve_one,
                "mana_value_2": curve_two,
                "mana_value_3": curve_three,
                "mana_value_4_plus": curve_four_plus,
            },
            "legality": "PASS",
            "color_identity": "U/R PASS",
            "copy_limit": "PASS",
        }
        Path("izzet-prowess-v2-validation.json").write_text(
            json.dumps(metrics, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        validation = "\n".join(
            (
                "Izzet Prowess V2 validation: PASS",
                f"Mainboard: {main_total}",
                f"Sideboard: {sideboard_total}",
                f"Lands: {mana_lands}",
                f"Threats: {threat_count}",
                f"Burn/reach cards: {burn_count}",
                f"Card-flow cards: {draw_count}",
                "Mana curve: "
                f"MV0-1={curve_one}, MV2={curve_two}, MV3={curve_three}, "
                f"MV4+={curve_four_plus}",
                "Legality: PASS",
                "Color identity U/R: PASS",
                "Three-copy limit across mainboard and sideboard: PASS",
            )
        )
        Path("izzet-prowess-v2-validation.txt").write_text(
            validation + "\n",
            encoding="utf-8",
        )
        print(validation)
        print("\n--- ARENA DECK LIST ---")
        print(arena_text)


def main() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    bulk_file = data_dir / "default_cards.json"
    database_file = data_dir / "cards.db"

    reuse_database = (
        os.environ.get("THUN_REUSE_CARD_DATABASE") == "1"
        and database_file.is_file()
    )
    if reuse_database:
        print(f"Reusing cached card database: {database_file}")
    else:
        _download_default_cards(bulk_file)
        try:
            _build_database(bulk_file, database_file)
        finally:
            bulk_file.unlink(missing_ok=True)

    _validate_and_export(database_file)


if __name__ == "__main__":
    main()
