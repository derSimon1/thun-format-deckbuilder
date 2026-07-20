from __future__ import annotations

import argparse

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.prototype import format_deck


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Magic Club Thun deckbuilder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    deck = subparsers.add_parser("build", help="Generate a prototype deck")
    deck.add_argument("archetype", choices=("burn", "tokens"))
    deck.add_argument("--colors", nargs="+", required=True)

    legality = subparsers.add_parser("legal", help="Check one card")
    legality.add_argument("card_name")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    with CardDatabase() as database:
        if args.command == "legal":
            card = database.get_card_by_name(args.card_name)
            if card is None:
                print(f"Karte nicht gefunden: {args.card_name}")
                return 2
            legal = database.is_card_legal_by_name(args.card_name)
            print(f"{card['name']}: {'LEGAL' if legal else 'NICHT LEGAL'}")
            return 0 if legal else 1

        deck = generate_deck(
            database=database,
            archetype=args.archetype,
            colors=args.colors,
        )
        print(format_deck(deck, archetype=args.archetype, colors=tuple(args.colors)))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
