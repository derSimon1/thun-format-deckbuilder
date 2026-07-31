from __future__ import annotations

import random
from dataclasses import dataclass, replace

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck
from thun_deckbuilder.matchup_simulator import MatchupReport, MatchupSimulator


@dataclass(frozen=True)
class SideboardPlan:
    opponent_archetype: str
    cards_in: tuple[tuple[str, int], ...]
    cards_out: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class BestOfThreeReport:
    archetype_a: str
    archetype_b: str
    samples: int
    match_wins_a_pct: int
    match_wins_b_pct: int
    game_one: MatchupReport
    postboard: MatchupReport
    plan_a: SideboardPlan
    plan_b: SideboardPlan


def _entry_text(entry: DeckEntry) -> str:
    return " ".join((entry.name, entry.type_line, *entry.roles, *entry.reasons)).lower()


def _sideboard_value(entry: DeckEntry, opponent: str) -> float:
    text = _entry_text(entry)
    score = entry.score
    if opponent in {"burn", "tokens"}:
        if any(key in text for key in ("removal", "destroy", "exile", "lifegain", "life gain", "boardwipe", "each creature")):
            score += 8
    elif opponent == "mill":
        if any(key in text for key in ("graveyard", "shuffle", "counter", "hexproof", "draw")):
            score += 8
    elif opponent == "artifacts":
        if any(key in text for key in ("artifact", "destroy", "exile", "counter")):
            score += 8
    elif opponent == "shrines":
        if any(key in text for key in ("enchantment", "destroy", "exile", "counter")):
            score += 8
    return score


def _expand(entries: tuple[DeckEntry, ...]) -> list[DeckEntry]:
    expanded: list[DeckEntry] = []
    for entry in entries:
        expanded.extend([replace(entry, quantity=1)] * entry.quantity)
    return expanded


def _compress(entries: list[DeckEntry]) -> tuple[DeckEntry, ...]:
    grouped: dict[tuple, tuple[DeckEntry, int]] = {}
    for entry in entries:
        key = (entry.name, entry.mana_cost, entry.mana_value, entry.type_line, entry.score, entry.reasons, entry.roles)
        original, quantity = grouped.get(key, (entry, 0))
        grouped[key] = (original, quantity + 1)
    return tuple(
        replace(entry, quantity=quantity)
        for entry, quantity in sorted(grouped.values(), key=lambda item: (-item[0].score, item[0].name))
    )


def board_for_matchup(
    deck: GeneratedDeck,
    *,
    opponent_archetype: str,
    max_swaps: int = 6,
) -> tuple[GeneratedDeck, SideboardPlan]:
    """Apply a small deterministic sideboard plan for one opposing archetype."""
    if max_swaps < 0:
        raise ValueError("max_swaps cannot be negative")
    main = _expand(deck.mainboard)
    side = sorted(
        _expand(deck.sideboard),
        key=lambda entry: (-_sideboard_value(entry, opponent_archetype), entry.name),
    )
    relevant = [entry for entry in side if _sideboard_value(entry, opponent_archetype) >= entry.score + 5]
    incoming = relevant[: min(max_swaps, len(relevant), len(main))]
    outgoing = sorted(main, key=lambda entry: (entry.score, -entry.mana_value, entry.name))[: len(incoming)]
    for entry in outgoing:
        main.remove(entry)
    main.extend(incoming)
    plan = SideboardPlan(
        opponent_archetype=opponent_archetype,
        cards_in=tuple(sorted(((entry.name, incoming.count(entry)) for entry in set(incoming)))),
        cards_out=tuple(sorted(((entry.name, outgoing.count(entry)) for entry in set(outgoing)))),
    )
    return replace(deck, mainboard=_compress(main)), plan


class BestOfThreeSimulator:
    """Simulate one preboard game followed by up to two postboard games."""

    def simulate(
        self,
        deck_a: GeneratedDeck,
        deck_b: GeneratedDeck,
        *,
        archetype_a: str,
        archetype_b: str,
        samples: int = 2000,
        seed: int = 53,
    ) -> BestOfThreeReport:
        if samples <= 0:
            raise ValueError("samples must be positive")
        simulator = MatchupSimulator()
        game_one = simulator.simulate(
            deck_a, deck_b, archetype_a=archetype_a, archetype_b=archetype_b, samples=samples, seed=seed
        )
        boarded_a, plan_a = board_for_matchup(deck_a, opponent_archetype=archetype_b)
        boarded_b, plan_b = board_for_matchup(deck_b, opponent_archetype=archetype_a)
        postboard = simulator.simulate(
            boarded_a,
            boarded_b,
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=samples,
            seed=seed + 1,
        )

        rng = random.Random(seed + 2)
        wins_a = wins_b = 0
        p1 = game_one.wins_a_pct / max(1, game_one.wins_a_pct + game_one.wins_b_pct)
        pp = postboard.wins_a_pct / max(1, postboard.wins_a_pct + postboard.wins_b_pct)
        for _ in range(samples):
            score_a = score_b = 0
            if rng.random() < p1:
                score_a += 1
            else:
                score_b += 1
            while score_a < 2 and score_b < 2:
                if rng.random() < pp:
                    score_a += 1
                else:
                    score_b += 1
            wins_a += int(score_a == 2)
            wins_b += int(score_b == 2)

        return BestOfThreeReport(
            archetype_a=archetype_a,
            archetype_b=archetype_b,
            samples=samples,
            match_wins_a_pct=round(wins_a * 100 / samples),
            match_wins_b_pct=round(wins_b * 100 / samples),
            game_one=game_one,
            postboard=postboard,
            plan_a=plan_a,
            plan_b=plan_b,
        )


def format_bo3_report(report: BestOfThreeReport) -> str:
    lines = [
        "THUN BEST-OF-THREE MATCHUP",
        "=" * 72,
        f"{report.archetype_a} vs. {report.archetype_b}",
        f"Match wins: {report.archetype_a} {report.match_wins_a_pct}% / {report.archetype_b} {report.match_wins_b_pct}%",
        f"Game 1: {report.game_one.wins_a_pct}% / {report.game_one.wins_b_pct}%",
        f"Postboard games: {report.postboard.wins_a_pct}% / {report.postboard.wins_b_pct}%",
        "",
        f"{report.archetype_a} cards in: " + (", ".join(f"{qty} {name}" for name, qty in report.plan_a.cards_in) or "none"),
        f"{report.archetype_a} cards out: " + (", ".join(f"{qty} {name}" for name, qty in report.plan_a.cards_out) or "none"),
        f"{report.archetype_b} cards in: " + (", ".join(f"{qty} {name}" for name, qty in report.plan_b.cards_in) or "none"),
        f"{report.archetype_b} cards out: " + (", ".join(f"{qty} {name}" for name, qty in report.plan_b.cards_out) or "none"),
    ]
    return "\n".join(lines)
