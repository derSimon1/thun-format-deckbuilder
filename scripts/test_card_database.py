from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SOURCE_DIR))

from thun_deckbuilder.card_database import CardDatabase


DATABASE_FILE = PROJECT_ROOT / "data" / "cards.db"


def main() -> None:
    with CardDatabase(DATABASE_FILE) as database:
        print(f"Karten: {database.count_cards():,}")
        print(f"Prints: {database.count_prints():,}")
        print(f"FTS aktiv: {database.fts_available}")
        print()

        card = database.get_card_by_name("Lightning Strike")

        if card:
            print("Gefundene Karte:")
            print(card["name"])
            print(card["mana_cost"])
            print(card["type_line"])
            print(card["oracle_text"])
            print(f"Sets: {card['set_codes']}")
            print()

        print("Suche nach 'create token':")

        results = database.search_text(
            '"create" "token"',
            limit=10,
        )

        for result in results:
            print(
                f"- {result['name']} "
                f"({result['mana_value']} Mana)"
            )

        print()
        print("Rote Instants bis Mana Value 2:")

        results = database.find_cards(
            color_identity="R",
            type_contains="Instant",
            mana_value_max=2,
            limit=20,
        )

        for result in results:
            print(
                f"- {result['name']}: "
                f"{result['mana_cost']}"
            )


if __name__ == "__main__":
    main()