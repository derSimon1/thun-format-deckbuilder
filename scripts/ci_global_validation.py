from __future__ import annotations

import gzip
import json
import os
import shutil
import sqlite3
from collections import Counter
from collections.abc import Iterator
from contextlib import closing
from dataclasses import asdict, is_dataclass, replace
from itertools import combinations
from pathlib import Path
from typing import Any

import ijson
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from thun_deckbuilder.benchmark import BenchmarkAnalyzer
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator
from thun_deckbuilder.tournament_simulator import BestOfThreeSimulator


REPOSITORY = "https://github.com/derSimon1/thun-format-deckbuilder"
HEADERS = {
    "User-Agent": f"MagicClubThunDeckbuilder/0.1 (+{REPOSITORY})",
    "Accept": "application/json;q=0.9,*/*;q=0.8",
}
DEFAULTS: dict[str, tuple[str, ...]] = {
    "burn": ("R",),
    "tokens": ("W",),
    "artifacts": ("U", "R"),
    "shrines": ("W", "U", "B", "R", "G"),
    "mill": ("U", "B"),
}
BASIC_LANDS = {
    "W": "Plains",
    "U": "Island",
    "B": "Swamp",
    "R": "Mountain",
    "G": "Forest",
}
ARTIFACT_DIR = Path("artifacts/global")
DATABASE_FILE = Path("data/cards.db")
BULK_FILE = Path("data/default_cards.json")
PREVIOUS_REPORT = Path(".ci-baseline/global-report.json")


def _http_session() -> requests.Session:
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def _bulk_uri(record: dict[str, object]) -> str | None:
    for key in ("jsonl_download_uri", "download_uri"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _find_bulk_record(payload: object) -> dict[str, object] | None:
    stack = [payload]
    while stack:
        current = stack.pop()
        if isinstance(current, list):
            stack.extend(current)
        elif isinstance(current, dict):
            bulk_type = str(current.get("type", "")).lower()
            bulk_name = str(current.get("name", "")).lower()
            if (
                bulk_type == "default_cards" or bulk_name == "default cards"
            ) and _bulk_uri(current):
                return current
            stack.extend(current.values())
    return None


def _first_byte(path: Path) -> bytes:
    with path.open("rb") as source:
        while True:
            value = source.read(1)
            if not value or not value.isspace():
                return value


def _download_bulk(target: Path) -> None:
    raw = target.with_suffix(".raw")
    normalized = target.with_suffix(".download")
    raw.unlink(missing_ok=True)
    normalized.unlink(missing_ok=True)
    with _http_session() as session:
        diagnostics: list[str] = []
        record = None
        for endpoint in (
            "https://api.scryfall.com/bulk-data/default_cards",
            "https://api.scryfall.com/bulk-data",
        ):
            try:
                response = session.get(endpoint, timeout=(15, 60))
                response.raise_for_status()
                record = _find_bulk_record(response.json())
            except (requests.RequestException, ValueError) as error:
                diagnostics.append(f"{endpoint}: {type(error).__name__}: {error}")
                continue
            if record is not None:
                break
            diagnostics.append(f"{endpoint}: no default_cards record")
        if record is None:
            raise RuntimeError("Unable to resolve Scryfall bulk data: " + " | ".join(diagnostics))
        uri = _bulk_uri(record)
        if uri is None:
            raise RuntimeError("Scryfall default_cards record has no supported URI")
        with session.get(uri, stream=True, timeout=(15, 300)) as download:
            download.raise_for_status()
            download.raw.decode_content = False
            with raw.open("wb") as output:
                shutil.copyfileobj(download.raw, output, length=1024 * 1024)
    if raw.stat().st_size < 1_000_000:
        raise RuntimeError("Downloaded Scryfall bulk file is unexpectedly small")
    with raw.open("rb") as source:
        magic = source.read(2)
    if magic == b"\x1f\x8b":
        with gzip.open(raw, "rb") as source, normalized.open("wb") as output:
            shutil.copyfileobj(source, output, length=1024 * 1024)
        raw.unlink(missing_ok=True)
    else:
        raw.replace(normalized)
    if _first_byte(normalized) not in {b"[", b"{"}:
        raise RuntimeError("Scryfall bulk file is neither JSON array nor JSON Lines")
    normalized.replace(target)


def _bulk_items(path: Path) -> Iterator[dict[str, Any]]:
    if _first_byte(path) == b"[":
        with path.open("rb") as source:
            for item in ijson.items(source, "item"):
                if isinstance(item, dict):
                    yield item
        return
    with path.open("r", encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                item = json.loads(stripped)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"Invalid JSON Lines record at line {line_number}") from error
            if isinstance(item, dict):
                yield item


def _database_usable(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        with closing(sqlite3.connect(path)) as connection:
            tables = {
                str(row[0])
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            integrity = str(connection.execute("PRAGMA quick_check").fetchone()[0]).lower()
            cards = int(connection.execute("SELECT COUNT(*) FROM cards").fetchone()[0])
            prints = int(connection.execute("SELECT COUNT(*) FROM prints").fetchone()[0])
        return {"cards", "prints"}.issubset(tables) and integrity == "ok" and cards > 1000 and prints > 1000
    except (OSError, sqlite3.DatabaseError, TypeError, ValueError):
        return False


def _build_database(bulk: Path, database: Path) -> None:
    temporary = database.with_suffix(".tmp")
    temporary.unlink(missing_ok=True)
    connection = sqlite3.connect(temporary)
    try:
        connection.executescript(
            """
            PRAGMA journal_mode=OFF;
            PRAGMA synchronous=OFF;
            PRAGMA temp_store=MEMORY;
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
                released_at TEXT NOT NULL DEFAULT ''
            );
            """
        )
        card_rows: dict[str, tuple[object, ...]] = {}
        print_rows: list[tuple[object, ...]] = []
        for item in _bulk_items(bulk):
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
            key = str(oracle_id)
            card_rows[key] = (
                key,
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
                    key,
                    str(item.get("set", "")).lower(),
                    str(item.get("rarity", "")).lower(),
                    int(bool(item.get("digital", False))),
                    json.dumps(item.get("games", [])),
                    item.get("released_at", ""),
                )
            )
        if not card_rows or not print_rows:
            raise RuntimeError("Scryfall bulk data contained no usable cards")
        connection.executemany("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", card_rows.values())
        connection.executemany("INSERT INTO prints VALUES (?, ?, ?, ?, ?, ?)", print_rows)
        connection.executescript(
            "CREATE INDEX prints_oracle_id ON prints (oracle_id);"
            "CREATE INDEX prints_set_code ON prints (set_code);"
        )
        connection.commit()
    except Exception:
        connection.close()
        temporary.unlink(missing_ok=True)
        raise
    else:
        connection.close()
    if not _database_usable(temporary):
        temporary.unlink(missing_ok=True)
        raise RuntimeError("Built card database failed integrity checks")
    temporary.replace(database)
    print(f"Built {database} with {len(card_rows)} cards and {len(print_rows)} prints")


def _prepare_database() -> None:
    DATABASE_FILE.parent.mkdir(exist_ok=True)
    reuse = os.environ.get("THUN_REUSE_CARD_DATABASE") == "1"
    if reuse and _database_usable(DATABASE_FILE):
        print(f"Reusing verified database {DATABASE_FILE}")
        return
    DATABASE_FILE.unlink(missing_ok=True)
    _download_bulk(BULK_FILE)
    try:
        _build_database(BULK_FILE, DATABASE_FILE)
    finally:
        BULK_FILE.unlink(missing_ok=True)


def _jsonable(value: object) -> object:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _arena_text(deck, colors: tuple[str, ...]) -> str:
    lines = ["Deck"]
    lines.extend(f"{entry.quantity} {entry.name}" for entry in deck.mainboard)
    if deck.mana_base is not None and deck.mana_base.lands:
        lines.extend(f"{land.quantity} {land.land_name}" for land in deck.mana_base.lands)
    else:
        land_name = BASIC_LANDS.get(colors[0], "Basic Land") if len(colors) == 1 else "Basic Land"
        lines.append(f"{deck.lands} {land_name}")
    lines.extend(["", "Sideboard"])
    lines.extend(f"{entry.quantity} {entry.name}" for entry in deck.sideboard)
    return "\n".join(lines) + "\n"


def _curve(deck) -> dict[str, int]:
    result = {"0-1": 0, "2": 0, "3": 0, "4+": 0}
    for entry in deck.mainboard:
        key = "0-1" if entry.mana_value <= 1 else "2" if entry.mana_value <= 2 else "3" if entry.mana_value <= 3 else "4+"
        result[key] += entry.quantity
    return result


def _role_counts(deck) -> Counter[str]:
    counts: Counter[str] = Counter()
    for entry in deck.mainboard:
        for role in entry.roles:
            counts[str(role)] += entry.quantity
    return counts


def _core_count(archetype: str, deck, legal_cards: dict[str, dict[str, Any]]) -> int:
    count = 0
    for entry in deck.mainboard:
        card = legal_cards.get(entry.name.casefold(), {})
        text = str(card.get("oracle_text", "")).lower()
        type_line = entry.type_line.lower()
        reasons = " ".join(entry.reasons).lower()
        if archetype == "burn" and "burn" in entry.roles:
            count += entry.quantity
        elif archetype == "tokens" and ({"token_maker", "token_payoff"} & set(entry.roles)):
            count += entry.quantity
        elif archetype == "artifacts" and ("artifact" in type_line or "artifact" in text):
            count += entry.quantity
        elif archetype == "shrines" and ("shrine" in type_line or "shrine" in text or "schrein" in reasons):
            count += entry.quantity
        elif archetype == "mill" and ("mill" in text or "library into" in text or "mill" in reasons):
            count += entry.quantity
    return count


def _validate_archetype(database: CardDatabase, archetype: str, colors: tuple[str, ...], legal_cards: dict[str, dict[str, Any]]) -> tuple[object, dict[str, object]]:
    deck = generate_deck(database=database, archetype=archetype, colors=colors)
    opening = deck.opening_hand_report or OpeningHandSimulator().simulate(deck, archetype=archetype)
    benchmark = BenchmarkAnalyzer().analyze(deck, archetype)
    deck = replace(deck, opening_hand_report=opening, benchmark_report=benchmark)

    errors: list[str] = []
    warnings = list(deck.warnings)
    lands = sum(land.quantity for land in deck.mana_base.lands) if deck.mana_base is not None else deck.lands
    spells = sum(entry.quantity for entry in deck.mainboard)
    sideboard = sum(entry.quantity for entry in deck.sideboard)
    if spells + lands != 60:
        errors.append(f"mainboard size is {spells + lands}, expected 60")
    if sideboard != 15:
        errors.append(f"sideboard size is {sideboard}, expected 15")
    if not 18 <= lands <= 27:
        errors.append(f"land count {lands} is outside supported range 18-27")

    combined: Counter[str] = Counter()
    allowed_colors = set(colors)
    for entry in (*deck.mainboard, *deck.sideboard):
        combined[entry.name] += entry.quantity
        card = legal_cards.get(entry.name.casefold())
        if card is None:
            errors.append(f"illegal or unknown card: {entry.name}")
            continue
        identity = set(card.get("color_identity", ()))
        if not identity.issubset(allowed_colors):
            errors.append(f"off-color card {entry.name}: {sorted(identity)} not in {sorted(allowed_colors)}")
    for name, quantity in combined.items():
        if quantity > 3:
            errors.append(f"copy limit exceeded: {quantity} {name} across mainboard and sideboard")

    if deck.mana_base is not None and deck.mana_base.total_lands != lands:
        errors.append("mana-base total does not match deck land count")
    if deck.mana_quality is not None and not deck.mana_quality.sufficient:
        errors.append("mana quality reports insufficient colored sources")
    if deck.quality_report is not None and not deck.quality_report.minimums_met:
        errors.append("deck profile minimum role requirements are not met")

    roles = _role_counts(deck)
    curve = _curve(deck)
    creatures = sum(entry.quantity for entry in deck.mainboard if "creature" in entry.type_line.lower())
    early_plays = sum(entry.quantity for entry in deck.mainboard if entry.mana_value <= 2)
    metrics = {
        "status": "PASS" if not errors else "FAIL",
        "colors": list(colors),
        "mainboard": spells + lands,
        "sideboard": sideboard,
        "lands": lands,
        "spells": spells,
        "curve": curve,
        "early_plays": early_plays,
        "creatures": creatures,
        "interaction": roles.get("removal", 0),
        "card_flow": roles.get("card_draw", 0),
        "burn_reach": roles.get("burn", 0),
        "core_cards": _core_count(archetype, deck, legal_cards),
        "role_counts": dict(sorted(roles.items())),
        "quality": _jsonable(deck.quality_report),
        "mana_quality": _jsonable(deck.mana_quality),
        "opening_hand": _jsonable(opening),
        "goldfish": _jsonable(deck.goldfish_report),
        "benchmark": _jsonable(benchmark),
        "errors": errors,
        "warnings": warnings,
    }

    prefix = ARTIFACT_DIR / archetype
    prefix.mkdir(parents=True, exist_ok=True)
    (prefix / f"{archetype}-arena.txt").write_text(_arena_text(deck, colors), encoding="utf-8")
    (prefix / f"{archetype}-validation.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (prefix / f"{archetype}-benchmark.json").write_text(json.dumps(_jsonable(benchmark), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (prefix / f"{archetype}-warnings.txt").write_text("\n".join(warnings or ["none"]) + "\n", encoding="utf-8")
    text = [
        f"{archetype}: {metrics['status']}",
        f"mainboard={metrics['mainboard']} sideboard={sideboard} lands={lands}",
        f"early_plays={early_plays} creatures={creatures} interaction={metrics['interaction']} card_flow={metrics['card_flow']} burn_reach={metrics['burn_reach']} core={metrics['core_cards']}",
        f"benchmark={benchmark.score}/100",
    ]
    text.extend(f"ERROR: {item}" for item in errors)
    text.extend(f"WARNING: {item}" for item in warnings)
    (prefix / f"{archetype}-validation.txt").write_text("\n".join(text) + "\n", encoding="utf-8")
    return deck, metrics


def _comparison(current: dict[str, object], previous: dict[str, object] | None) -> dict[str, object]:
    if not previous:
        return {"baseline": "none", "regressions": [], "changes": []}
    regressions: list[dict[str, object]] = []
    changes: list[dict[str, object]] = []
    previous_archetypes = previous.get("archetypes", {}) if isinstance(previous, dict) else {}
    current_archetypes = current.get("archetypes", {})
    for archetype, payload in current_archetypes.items():
        before = previous_archetypes.get(archetype, {}) if isinstance(previous_archetypes, dict) else {}
        for path in (
            ("benchmark", "score"),
            ("opening_hand", "playable_after_mulligan_pct"),
            ("mana_quality", "score"),
        ):
            old = before
            new = payload
            for key in path:
                old = old.get(key) if isinstance(old, dict) else None
                new = new.get(key) if isinstance(new, dict) else None
            if isinstance(old, (int, float)) and isinstance(new, (int, float)) and old != new:
                item = {"archetype": archetype, "metric": ".".join(path), "before": old, "after": new, "delta": new - old}
                changes.append(item)
                if new < old:
                    regressions.append(item)
    return {"baseline": "restored", "regressions": regressions, "changes": changes}


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    _prepare_database()
    previous = None
    if PREVIOUS_REPORT.is_file():
        try:
            previous = json.loads(PREVIOUS_REPORT.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            previous = None

    aggregate: dict[str, object] = {
        "status": "PASS",
        "archetypes": {},
        "matchups": [],
        "best_of_three": [],
    }
    failed = False
    with CardDatabase(DATABASE_FILE) as database:
        legal_cards = {
            str(card.get("name", "")).casefold(): card
            for card in database.get_all_legal_cards()
        }
        decks: dict[str, object] = {}
        for archetype, colors in DEFAULTS.items():
            try:
                deck, metrics = _validate_archetype(database, archetype, colors, legal_cards)
            except Exception as error:
                failed = True
                aggregate["archetypes"][archetype] = {
                    "status": "ERROR",
                    "errors": [f"{type(error).__name__}: {error}"],
                }
                print(f"{archetype}: ERROR: {type(error).__name__}: {error}")
                continue
            decks[archetype] = deck
            aggregate["archetypes"][archetype] = metrics
            failed = failed or metrics["status"] != "PASS"
            print(f"{archetype}: {metrics['status']} benchmark={metrics['benchmark']['score']}/100")

        for archetype_a, archetype_b in combinations(sorted(decks), 2):
            deck_a = decks[archetype_a]
            deck_b = decks[archetype_b]
            matchup = MatchupSimulator().simulate(
                deck_a,
                deck_b,
                archetype_a=archetype_a,
                archetype_b=archetype_b,
                samples=500,
            )
            bo3 = BestOfThreeSimulator().simulate(
                deck_a,
                deck_b,
                archetype_a=archetype_a,
                archetype_b=archetype_b,
                samples=300,
            )
            aggregate["matchups"].append(_jsonable(matchup))
            aggregate["best_of_three"].append(_jsonable(bo3))

    aggregate["status"] = "FAIL" if failed else "PASS"
    comparison = _comparison(aggregate, previous)
    aggregate["comparison"] = comparison
    (ARTIFACT_DIR / "global-report.json").write_text(json.dumps(aggregate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ARTIFACT_DIR / "regressions.json").write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ARTIFACT_DIR / "matchups.json").write_text(json.dumps(aggregate["matchups"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ARTIFACT_DIR / "best-of-three.json").write_text(json.dumps(aggregate["best_of_three"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = [
        f"Global deckbuilder validation: {aggregate['status']}",
        f"Archetypes checked: {len(aggregate['archetypes'])}",
        f"Matchups checked: {len(aggregate['matchups'])}",
        f"Regressions versus previous run: {len(comparison['regressions'])}",
    ]
    for archetype, metrics in aggregate["archetypes"].items():
        summary.append(f"{archetype}: {metrics.get('status')} benchmark={metrics.get('benchmark', {}).get('score', 'n/a')}")
    (ARTIFACT_DIR / "global-summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
