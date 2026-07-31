from __future__ import annotations

import argparse

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.prototype import format_deck


ARCHETYPES = ("burn", "tokens", "artifacts", "shrines", "mill")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Magic Club Thun deckbuilder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    deck = subparsers.add_parser("build", help="Generate a prototype deck")
    deck.add_argument("archetype", choices=ARCHETYPES)
    deck.add_argument("--colors", nargs="+", required=True)
    deck.add_argument("--explain", action="store_true", help="Show every iterative selection decision")
    deck.add_argument("--benchmark", action="store_true", help="Show calibration benchmark report")

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
        if args.benchmark:
            from dataclasses import replace
            from thun_deckbuilder.benchmark import BenchmarkAnalyzer
            deck = replace(deck, benchmark_report=BenchmarkAnalyzer().analyze(deck, args.archetype))
        print(format_deck(
            deck,
            archetype=args.archetype,
            colors=tuple(args.colors),
            explain=args.explain,
        ))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
