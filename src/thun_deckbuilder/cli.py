from __future__ import annotations

import argparse

from thun_deckbuilder.calibration_advisor import format_calibration_recommendations
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.meta_advisor import BestOfThreeMetaAnalyzer, format_meta_advice
from thun_deckbuilder.meta_matrix import MetaMatrixAnalyzer, format_matchup_report, format_meta_matrix
from thun_deckbuilder.prototype import format_deck
from thun_deckbuilder.tournament_simulator import BestOfThreeSimulator, format_bo3_report


ARCHETYPES = ("burn", "tokens", "artifacts", "shrines", "mill")
DEFAULT_COLORS = {
    "burn": ("R",), "tokens": ("W",), "artifacts": ("U", "R"),
    "shrines": ("W", "U", "B", "R", "G"), "mill": ("U", "B"),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Magic Club Thun deckbuilder")
    subparsers = parser.add_subparsers(dest="command", required=True)
    deck = subparsers.add_parser("build", help="Generate a prototype deck")
    deck.add_argument("archetype", choices=ARCHETYPES)
    deck.add_argument("--colors", nargs="+", required=True)
    deck.add_argument("--explain", action="store_true")
    deck.add_argument("--benchmark", action="store_true")
    matchup = subparsers.add_parser("matchup", help="Compare two generated archetypes")
    matchup.add_argument("archetype_a", choices=ARCHETYPES)
    matchup.add_argument("archetype_b", choices=ARCHETYPES)
    matchup.add_argument("--samples", type=int, default=2000)
    bo3 = subparsers.add_parser("bo3", help="Simulate a sideboard-aware best-of-three matchup")
    bo3.add_argument("archetype_a", choices=ARCHETYPES)
    bo3.add_argument("archetype_b", choices=ARCHETYPES)
    bo3.add_argument("--samples", type=int, default=2000)
    meta = subparsers.add_parser("meta", help="Run a round-robin archetype meta analysis")
    meta.add_argument("archetypes", nargs="*", choices=ARCHETYPES, default=list(ARCHETYPES))
    meta.add_argument("--samples", type=int, default=2000)
    meta_bo3 = subparsers.add_parser("meta-bo3", help="Run sideboard-aware meta analysis and advice")
    meta_bo3.add_argument("archetypes", nargs="*", choices=ARCHETYPES, default=list(ARCHETYPES))
    meta_bo3.add_argument("--samples", type=int, default=2000)
    legality = subparsers.add_parser("legal", help="Check one card")
    legality.add_argument("card_name")
    return parser


def _generate_default(database: CardDatabase, archetype: str):
    return generate_deck(database=database, archetype=archetype, colors=DEFAULT_COLORS[archetype])


def _validate_meta_archetypes(archetypes: tuple[str, ...]) -> None:
    if len(set(archetypes)) < 2:
        build_parser().error("meta analysis requires at least two distinct archetypes")


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
        if args.command in {"matchup", "bo3"}:
            deck_a = _generate_default(database, args.archetype_a)
            deck_b = _generate_default(database, args.archetype_b)
            if args.command == "matchup":
                report = MatchupSimulator().simulate(deck_a, deck_b, archetype_a=args.archetype_a, archetype_b=args.archetype_b, samples=args.samples)
                print(format_matchup_report(report))
            else:
                report = BestOfThreeSimulator().simulate(deck_a, deck_b, archetype_a=args.archetype_a, archetype_b=args.archetype_b, samples=args.samples)
                print(format_bo3_report(report))
                print()
                print(format_calibration_recommendations(report))
            return 0
        if args.command in {"meta", "meta-bo3"}:
            archetypes = tuple(args.archetypes or ARCHETYPES)
            _validate_meta_archetypes(archetypes)
            decks = {archetype: _generate_default(database, archetype) for archetype in archetypes}
            if args.command == "meta":
                print(format_meta_matrix(MetaMatrixAnalyzer().analyze(decks, samples_per_matchup=args.samples)))
            else:
                print(format_meta_advice(BestOfThreeMetaAnalyzer().analyze(decks, samples_per_matchup=args.samples)))
            return 0
        deck = generate_deck(database=database, archetype=args.archetype, colors=args.colors)
        if args.benchmark:
            from dataclasses import replace
            from thun_deckbuilder.benchmark import BenchmarkAnalyzer
            deck = replace(deck, benchmark_report=BenchmarkAnalyzer().analyze(deck, args.archetype))
        print(format_deck(deck, archetype=args.archetype, colors=tuple(args.colors), explain=args.explain))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
