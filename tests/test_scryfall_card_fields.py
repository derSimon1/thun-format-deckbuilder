import json
import sqlite3

from scripts.build_index import (
    apply_oracle_tags,
    create_database,
    get_card_characteristic,
    insert_card,
)


def test_power_and_toughness_are_stored_as_text():
    connection = sqlite3.connect(":memory:")
    create_database(connection)

    card = {
        "oracle_id": "oracle-1",
        "id": "print-1",
        "name": "Variable Beast",
        "cmc": 3,
        "colors": ["G"],
        "color_identity": ["G"],
        "type_line": "Creature — Beast",
        "oracle_text": "",
        "keywords": [],
        "power": "*",
        "toughness": "1+*",
        "set": "tst",
    }

    assert insert_card(connection, card)

    row = connection.execute(
        """
        SELECT power, toughness
        FROM cards
        WHERE oracle_id = ?
        """,
        ("oracle-1",),
    ).fetchone()

    assert row == ("*", "1+*")


def test_multiface_power_and_toughness_are_preserved():
    card = {
        "card_faces": [
            {"power": "2", "toughness": "2"},
            {"power": "4", "toughness": "4"},
        ]
    }

    assert get_card_characteristic(card, "power") == "2 // 4"
    assert get_card_characteristic(card, "toughness") == "2 // 4"


def test_oracle_tags_are_joined_by_oracle_id_and_sorted(tmp_path):
    connection = sqlite3.connect(":memory:")
    create_database(connection)

    for oracle_id, scryfall_id, name in (
        ("oracle-1", "print-1", "Tagged Creature"),
        ("oracle-2", "print-2", "Untagged Creature"),
    ):
        insert_card(
            connection,
            {
                "oracle_id": oracle_id,
                "id": scryfall_id,
                "name": name,
                "cmc": 2,
                "colors": ["W"],
                "color_identity": ["W"],
                "type_line": "Creature — Test",
                "oracle_text": "",
                "keywords": [],
                "power": "2",
                "toughness": "2",
                "set": "tst",
            },
        )

    oracle_tags = [
        {
            "label": "tokens",
            "taggings": [{"oracle_id": "oracle-1", "weight": 1.0}],
        },
        {
            "label": "anthem",
            "taggings": [{"oracle_id": "oracle-1", "weight": 0.8}],
        },
        {
            "label": "irrelevant",
            "taggings": [{"oracle_id": "missing-oracle-id", "weight": 1.0}],
        },
    ]

    path = tmp_path / "oracle_tags.json"
    path.write_text(json.dumps(oracle_tags), encoding="utf-8")

    taggings_count, tagged_cards = apply_oracle_tags(connection, path)

    assert taggings_count == 3
    assert tagged_cards == 1

    rows = dict(
        connection.execute(
            "SELECT oracle_id, oracle_tags FROM cards ORDER BY oracle_id"
        ).fetchall()
    )
    assert rows["oracle-1"] == "anthem,tokens"
    assert rows["oracle-2"] == ""
