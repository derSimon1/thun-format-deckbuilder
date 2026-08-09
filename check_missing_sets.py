"""
Prueft, ob in Scryfalls Set-Liste neue, bereits veroeffentlichte Kandidaten
existieren, die in config/thun.toml noch fehlen.

Nutzung (im Projekt-Root ausfuehren, braucht Internet):
    python check_missing_sets.py

Gibt KEINE automatischen Aenderungen - nur einen Bericht, den man selbst
pruefen und in config/thun.toml einpflegen kann.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import requests

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # Fallback fuer aeltere Python-Versionen

CONFIG_PATH = Path(__file__).resolve().parent / "config" / "thun.toml"
SCRYFALL_SETS_URL = "https://api.scryfall.com/sets"
USER_AGENT = "ThunFormatDeckbuilder/0.1 (set-checker)"

# Set-Typen, die als "normale", draftbare Erweiterungen zaehlen.
# 'expansion' deckt auch Standard-legale Universes-Beyond-Tentpole-Sets ab.
# Die Set-API allein beweist aber keine Standard-Legalitaet; Treffer bleiben
# deshalb bewusst nur Kandidaten fuer eine manuelle Pruefung.
RELEVANT_SET_TYPES = {"expansion", "core"}


def load_config_allowed_sets() -> tuple[set[str], str]:
    with CONFIG_PATH.open("rb") as f:
        config = tomllib.load(f)

    allowed = {code.lower() for code in config["sets"]["allowed_sets"]}
    starting_set_code = config["sets"].get("starting_set", "bfz").lower()
    return allowed, starting_set_code


def fetch_scryfall_sets() -> list[dict]:
    response = requests.get(
        SCRYFALL_SETS_URL,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["data"]


def find_starting_set_date(sets: list[dict], starting_set_code: str) -> str:
    for s in sets:
        if s.get("code", "").lower() == starting_set_code:
            return s.get("released_at", "0000-00-00")
    raise RuntimeError(f"Start-Set '{starting_set_code}' nicht bei Scryfall gefunden.")


def main() -> int:
    if not CONFIG_PATH.exists():
        print(f"Fehler: {CONFIG_PATH} nicht gefunden.", file=sys.stderr)
        return 1

    print("Lese config/thun.toml ...")
    allowed_sets, starting_set_code = load_config_allowed_sets()

    print("Lade aktuelle Set-Liste von Scryfall ...")
    all_sets = fetch_scryfall_sets()

    start_date = find_starting_set_date(all_sets, starting_set_code)
    today = date.today().isoformat()
    print(f"Startpunkt des Formats: {starting_set_code} ({start_date})")
    print(f"Pruefdatum: {today}\n")

    candidates = []
    for s in all_sets:
        code = s.get("code", "").lower()
        set_type = s.get("set_type", "")
        released_at = s.get("released_at")
        digital = s.get("digital", False)

        if not released_at or released_at < start_date:
            continue
        if released_at > today:
            continue
        if set_type not in RELEVANT_SET_TYPES:
            continue
        if digital:
            continue
        if code in allowed_sets:
            continue

        candidates.append((released_at, code, s.get("name", "")))

    candidates.sort()

    if not candidates:
        print("Keine fehlenden Set-Kandidaten gefunden - allowed_sets ist aktuell.")
        return 0

    print(f"{'MOEGLICH FEHLEND':<20} | {'Code':<6} | Released   | Name")
    print("-" * 70)
    for released_at, code, name in candidates:
        print(f"{'>>> PRUEFEN <<<':<20} | {code:<6} | {released_at} | {name}")

    print()
    print("Hinweis: Das sind KANDIDATEN, keine automatische Wahrheit. Die")
    print("Scryfall-Set-API kennt den Set-Typ, beweist aber nicht allein die")
    print("Standard-Legalitaet. Bitte jeden Code gegen eine belastbare")
    print("Standard-Quelle pruefen, bevor er in allowed_sets aufgenommen wird.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
