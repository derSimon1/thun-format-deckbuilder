import csv

import export_legal_pool


class FakeCardDatabase:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def get_all_legal_cards(self):
        return [
            {
                "name": "Tagged Creature",
                "mana_cost": "{1}{G}",
                "mana_value": 2.0,
                "colors": ["G"],
                "color_identity": ["G"],
                "type_line": "Creature — Beast",
                "oracle_text": "Trample",
                "keywords": ["Trample"],
                "power": "2",
                "toughness": "3",
                "oracle_tags": ["trample-matters", "creature-type-matters"],
                "legal_prints": ["TST #1"],
            }
        ]


def test_export_includes_power_toughness_and_oracle_tags(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(export_legal_pool, "CardDatabase", FakeCardDatabase)

    export_legal_pool.main()

    with (tmp_path / "thun_legal_pool.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    row = rows[0]
    assert row["power"] == "2"
    assert row["toughness"] == "3"
    assert row["oracle_tags"] == "trample-matters;creature-type-matters"
