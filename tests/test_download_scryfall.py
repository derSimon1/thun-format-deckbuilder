import gzip
import json

from scripts.download_scryfall import (
    BULK_INDEX_URL,
    _jsonl_to_json_array,
    get_bulk_download_url,
    validate_download,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []

    def get(self, url, **kwargs):
        self.urls.append(url)
        return FakeResponse(self.responses.pop(0))


def test_bulk_download_url_accepts_legacy_json_uri():
    session = FakeSession([
        {"data": [{"type": "default_cards", "download_uri": "https://data.example/cards.json"}]}
    ])
    assert get_bulk_download_url(session) == "https://data.example/cards.json"
    assert session.urls == [BULK_INDEX_URL]


def test_bulk_download_url_accepts_current_jsonl_uri():
    session = FakeSession([
        {"data": [{"type": "default_cards", "jsonl_download_uri": "https://data.example/cards.jsonl.gz"}]}
    ])
    assert get_bulk_download_url(session) == "https://data.example/cards.jsonl.gz"


def test_bulk_download_url_follows_detail_uri():
    detail_uri = "https://api.scryfall.com/bulk-data/example"
    session = FakeSession([
        {"data": [{"type": "default_cards", "uri": detail_uri}]},
        {"type": "default_cards", "jsonl_download_uri": "https://data.example/cards.jsonl.gz"},
    ])
    assert get_bulk_download_url(session) == "https://data.example/cards.jsonl.gz"
    assert session.urls == [BULK_INDEX_URL, detail_uri]


def test_compressed_jsonl_is_normalized_to_valid_array(tmp_path):
    cards = [
        {"id": "1", "name": "A", "set": "tst", "rarity": "common", "type_line": "Creature"},
        {"id": "2", "name": "B", "set": "tst", "rarity": "uncommon", "type_line": "Instant"},
    ]
    source = tmp_path / "cards.jsonl.gz"
    destination = tmp_path / "cards.json"
    with gzip.open(source, "wt", encoding="utf-8") as handle:
        for card in cards:
            handle.write(json.dumps(card) + "\n")

    assert _jsonl_to_json_array(source, destination, compressed=True) == 2
    assert json.loads(destination.read_text(encoding="utf-8")) == cards
    assert validate_download(destination) == 2
