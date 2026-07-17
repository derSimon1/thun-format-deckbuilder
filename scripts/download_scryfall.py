from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

BULK_INDEX_URL = "https://api.scryfall.com/bulk-data"
BULK_TYPE = "default_cards"

OUTPUT_FILE = DATA_DIR / "default_cards.json"

USER_AGENT = "ThunFormatDeckbuilder/0.1"
TIMEOUT_SECONDS = 120
CHUNK_SIZE = 1024 * 1024


class ScryfallDownloadError(RuntimeError):
    """Fehler beim Herunterladen oder Prüfen der Scryfall-Daten."""


def get_bulk_download_url(session: requests.Session) -> str:
    """Liest den Scryfall-Bulk-Index und liefert die Download-URL."""

    response = session.get(BULK_INDEX_URL, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    payload: dict[str, Any] = response.json()

    for item in payload.get("data", []):
        if item.get("type") == BULK_TYPE:
            download_uri = item.get("download_uri")

            if not download_uri:
                raise ScryfallDownloadError(
                    f"Bulk-Datensatz '{BULK_TYPE}' hat keine Download-URL."
                )

            return download_uri

    raise ScryfallDownloadError(
        f"Bulk-Datensatz '{BULK_TYPE}' wurde nicht gefunden."
    )


def download_file(
    session: requests.Session,
    url: str,
    destination: Path,
) -> None:
    """Lädt die Datei zunächst temporär und ersetzt sie danach atomar."""

    temporary_file = destination.with_suffix(destination.suffix + ".tmp")

    try:
        with session.get(
            url,
            stream=True,
            timeout=TIMEOUT_SECONDS,
        ) as response:
            response.raise_for_status()

            total_bytes = 0

            with temporary_file.open("wb") as file_handle:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if not chunk:
                        continue

                    file_handle.write(chunk)
                    total_bytes += len(chunk)

                    downloaded_mb = total_bytes / 1024 / 1024
                    print(
                        f"\rHeruntergeladen: {downloaded_mb:.1f} MB",
                        end="",
                        flush=True,
                    )

        print()
        temporary_file.replace(destination)

    except Exception:
        temporary_file.unlink(missing_ok=True)
        raise


def validate_download(path: Path) -> int:
    """Prüft, ob eine nichtleere Scryfall-Kartenliste vorliegt."""

    try:
        with path.open("r", encoding="utf-8") as file_handle:
            cards = json.load(file_handle)
    except json.JSONDecodeError as exc:
        raise ScryfallDownloadError(
            f"Die heruntergeladene Datei ist kein gültiges JSON: {exc}"
        ) from exc

    if not isinstance(cards, list):
        raise ScryfallDownloadError(
            "Die Scryfall-Datei enthält keine JSON-Liste."
        )

    if not cards:
        raise ScryfallDownloadError(
            "Die Scryfall-Kartenliste ist leer."
        )

    required_fields = {
        "id",
        "name",
        "set",
        "rarity",
        "type_line",
    }

    sample_card = cards[0]
    missing_fields = required_fields - sample_card.keys()

    if missing_fields:
        raise ScryfallDownloadError(
            "Die Datei sieht nicht wie Scryfall-Kartendaten aus. "
            f"Fehlende Felder: {sorted(missing_fields)}"
        )

    return len(cards)


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
    )

    try:
        print("Lese Scryfall-Bulk-Index ...")
        download_url = get_bulk_download_url(session)

        print(f"Lade '{BULK_TYPE}' herunter ...")
        download_file(
            session=session,
            url=download_url,
            destination=OUTPUT_FILE,
        )

        print("Prüfe heruntergeladene Datei ...")
        card_count = validate_download(OUTPUT_FILE)

        file_size_mb = OUTPUT_FILE.stat().st_size / 1024 / 1024

        print("Download erfolgreich.")
        print(f"Kartendrucke: {card_count:,}")
        print(f"Dateigröße:   {file_size_mb:.1f} MB")
        print(f"Gespeichert:  {OUTPUT_FILE}")

        return 0

    except requests.RequestException as exc:
        print(f"Netzwerkfehler: {exc}", file=sys.stderr)
        return 1

    except (OSError, ScryfallDownloadError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())