from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path
from typing import Any

import ijson
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


def _download_uri(payload: dict[str, Any]) -> str | None:
    for key in ("download_uri", "jsonl_download_uri"):
        value = payload.get(key)
        if value:
            return str(value)
    return None


def get_bulk_download_url(session: requests.Session) -> str:
    """Liest den Scryfall-Bulk-Index und liefert die Download-URL.

    Scryfall historically supplied ``download_uri`` with a JSON array and now
    supplies ``jsonl_download_uri`` with gzip-compressed JSON Lines. Both forms
    are accepted. If the list object contains only a detail URI, that object is
    resolved once before failing.
    """

    response = session.get(BULK_INDEX_URL, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    payload: dict[str, Any] = response.json()

    for item in payload.get("data", []):
        if item.get("type") != BULK_TYPE:
            continue

        download_uri = _download_uri(item)
        if download_uri:
            return download_uri

        detail_uri = item.get("uri")
        if detail_uri:
            detail_response = session.get(str(detail_uri), timeout=TIMEOUT_SECONDS)
            detail_response.raise_for_status()
            detail_payload: dict[str, Any] = detail_response.json()
            detail_download_uri = _download_uri(detail_payload)
            if detail_download_uri:
                return detail_download_uri

        raise ScryfallDownloadError(
            f"Bulk-Datensatz '{BULK_TYPE}' hat keine Download-URL."
        )

    raise ScryfallDownloadError(
        f"Bulk-Datensatz '{BULK_TYPE}' wurde nicht gefunden."
    )


def _jsonl_to_json_array(
    source: Path,
    destination: Path,
    *,
    compressed: bool,
) -> int:
    """Konvertiert JSON Lines streamend in das bestehende JSON-Array-Format."""

    input_context = (
        gzip.open(source, "rt", encoding="utf-8")
        if compressed
        else source.open("r", encoding="utf-8")
    )
    count = 0
    with input_context as input_handle:
        with destination.open("w", encoding="utf-8") as output_handle:
            output_handle.write("[\n")
            first = True
            for line_number, line in enumerate(input_handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    card = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ScryfallDownloadError(
                        f"Ungültige JSONL-Zeile {line_number}: {exc}"
                    ) from exc
                if not first:
                    output_handle.write(",\n")
                json.dump(card, output_handle, ensure_ascii=False, separators=(",", ":"))
                first = False
                count += 1
            output_handle.write("\n]\n")
    if count == 0:
        raise ScryfallDownloadError("Die Scryfall-JSONL-Datei ist leer.")
    return count


def download_file(
    session: requests.Session,
    url: str,
    destination: Path,
) -> None:
    """Lädt und normalisiert den Bulk-Datensatz atomar."""

    downloaded_file = destination.with_suffix(destination.suffix + ".download.tmp")
    converted_file = destination.with_suffix(destination.suffix + ".tmp")

    try:
        with session.get(
            url,
            stream=True,
            timeout=TIMEOUT_SECONDS,
        ) as response:
            response.raise_for_status()

            total_bytes = 0
            with downloaded_file.open("wb") as file_handle:
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

        if "jsonl" in url.lower():
            with downloaded_file.open("rb") as file_handle:
                compressed = file_handle.read(2) == b"\x1f\x8b"
            _jsonl_to_json_array(
                downloaded_file,
                converted_file,
                compressed=compressed,
            )
            converted_file.replace(destination)
            downloaded_file.unlink(missing_ok=True)
        else:
            downloaded_file.replace(destination)

    except Exception:
        downloaded_file.unlink(missing_ok=True)
        converted_file.unlink(missing_ok=True)
        raise


def validate_download(path: Path) -> int:
    """Prüft das große JSON-Array streamend, ohne es komplett zu laden."""

    count = 0
    sample_card: dict[str, Any] | None = None
    try:
        with path.open("rb") as file_handle:
            for card in ijson.items(file_handle, "item"):
                if sample_card is None:
                    sample_card = card
                count += 1
    except (ijson.JSONError, OSError) as exc:
        raise ScryfallDownloadError(
            f"Die heruntergeladene Datei ist kein gültiges JSON-Array: {exc}"
        ) from exc

    if sample_card is None or count == 0:
        raise ScryfallDownloadError("Die Scryfall-Kartenliste ist leer.")

    required_fields = {
        "id",
        "name",
        "set",
        "rarity",
        "type_line",
    }
    missing_fields = required_fields - sample_card.keys()
    if missing_fields:
        raise ScryfallDownloadError(
            "Die Datei sieht nicht wie Scryfall-Kartendaten aus. "
            f"Fehlende Felder: {sorted(missing_fields)}"
        )
    return count


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
