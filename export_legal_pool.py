"""
Export the full Thun-format legal card pool to CSV.

Ausführen aus dem Repo-Root (thun-format-deckbuilder-main/):

    python export_legal_pool.py

Erwartet, dass data/cards.db bereits existiert (wie fuer die CLI/Tests).
Erzeugt: thun_legal_pool.csv
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from thun_deckbuilder.card_database import CardDatabase  # noqa: E402


def main() -> None:
    with CardDatabase() as db:
        cards = db.get_all_legal_cards()

    out_path = Path("thun_legal_pool.csv")
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "name",
                "mana_cost",
                "mana_value",
                "colors",
                "color_identity",
                "type_line",
                "oracle_text",
                "keywords",
                "power",
                "toughness",
                "oracle_tags",
                "legal_prints",
            ]
        )
        for c in cards:
            keywords = c.get("keywords")
            if isinstance(keywords, list):
                keywords = ";".join(keywords)
            oracle_tags = c.get("oracle_tags") or []
            legal_prints = c.get("legal_prints") or []
            writer.writerow(
                [
                    c.get("name"),
                    c.get("mana_cost"),
                    c.get("mana_value"),
                    ";".join(c.get("colors") or []),
                    ";".join(c.get("color_identity") or []),
                    c.get("type_line"),
                    (c.get("oracle_text") or "").replace("\n", " | "),
                    keywords,
                    c.get("power"),
                    c.get("toughness"),
                    ";".join(str(tag) for tag in oracle_tags),
                    ";".join(str(p) for p in legal_prints),
                ]
            )

    print(f"Exportiert: {len(cards)} legale Karten -> {out_path.resolve()}")


if __name__ == "__main__":
    main()
