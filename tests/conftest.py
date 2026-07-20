from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def test_database_path(tmp_path_factory: pytest.TempPathFactory, monkeypatch_session):
    path = tmp_path_factory.mktemp("cards") / "cards.db"
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE cards (
            oracle_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mana_cost TEXT,
            mana_value REAL NOT NULL,
            colors TEXT,
            color_identity TEXT,
            type_line TEXT NOT NULL,
            oracle_text TEXT NOT NULL,
            keywords TEXT
        );
        CREATE TABLE prints (
            scryfall_id TEXT PRIMARY KEY,
            oracle_id TEXT NOT NULL,
            name TEXT NOT NULL,
            set_code TEXT NOT NULL,
            set_name TEXT,
            set_type TEXT,
            rarity TEXT NOT NULL,
            collector_number TEXT,
            released_at TEXT,
            digital INTEGER NOT NULL DEFAULT 0,
            promo INTEGER NOT NULL DEFAULT 0,
            reprint INTEGER NOT NULL DEFAULT 0,
            booster INTEGER NOT NULL DEFAULT 1,
            games TEXT NOT NULL,
            finishes TEXT,
            frame_effects TEXT,
            security_stamp TEXT,
            border_color TEXT,
            layout TEXT,
            lang TEXT,
            arena_id INTEGER,
            image_uri TEXT
        );
        """
    )

    cards: list[tuple[str, str, str, float, list[str], str, str]] = []
    for mv, count in ((1, 4), (2, 4), (3, 3), (4, 2)):
        for index in range(count):
            name = f"Test Burn {mv}-{index + 1}"
            cards.append((f"burn-{mv}-{index}", name, f"{{{mv}}}{{R}}", float(mv), ["R"], "Instant", f"{name} deals 3 damage to any target."))
    for index in range(12):
        mv = 1 + (index % 4)
        name = f"Test Token {index + 1}"
        cards.append((f"token-{index}", name, f"{{{mv}}}{{W}}", float(mv), ["W"], "Creature — Human", "When this enters, create a 1/1 white Soldier creature token."))

    cards.extend([
        ("lightning-strike", "Lightning Strike", "{1}{R}", 2.0, ["R"], "Instant", "Lightning Strike deals 3 damage to any target."),
        ("ocelot-pride", "Ocelot Pride", "{W}", 1.0, ["W"], "Creature — Cat", "At the beginning of your end step, create a 1/1 white Cat creature token."),
        ("rare-reprinted", "Rare Then Uncommon", "{1}{W}", 2.0, ["W"], "Creature — Human", "When this enters, create a 1/1 white Soldier creature token."),
    ])

    for oracle_id, name, mana_cost, mana_value, colors, type_line, oracle_text in cards:
        connection.execute(
            "INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (oracle_id, name, mana_cost, mana_value, json.dumps(colors), json.dumps(colors), type_line, oracle_text, "[]"),
        )
        rarity = "mythic" if name == "Ocelot Pride" else "uncommon"
        set_code = "mh3" if name == "Ocelot Pride" else "dmu"
        connection.execute(
            "INSERT INTO prints (scryfall_id, oracle_id, name, set_code, rarity, digital, games) VALUES (?, ?, ?, ?, ?, 0, 'paper')",
            (f"print-{oracle_id}", oracle_id, name, set_code, rarity),
        )

    connection.execute(
        "INSERT INTO prints (scryfall_id, oracle_id, name, set_code, rarity, digital, games) VALUES (?, ?, ?, ?, ?, 0, 'paper')",
        ("print-rare-original", "rare-reprinted", "Rare Then Uncommon", "mh3", "rare"),
    )
    connection.commit()
    connection.close()

    monkeypatch_session.setenv("THUN_DATABASE_FILE", str(path))
    return path


@pytest.fixture(scope="session")
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch
    patch = MonkeyPatch()
    yield patch
    patch.undo()
