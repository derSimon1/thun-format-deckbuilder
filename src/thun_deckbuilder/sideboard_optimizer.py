from __future__ import annotations

from dataclasses import dataclass, replace

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck
from thun_deckbuilder.matchup_simulator import MatchupSimulator
from thun_deckbuilder.tournament_simulator import SideboardPlan, _compress, _expand, _sideboard_value


@dataclass(frozen=True)
class SideboardCardImpact:
    card_in: str
    card_out: str
    win_rate_delta: int


@dataclass(frozen=True)
class OptimizedSideboardPlan:
    deck: GeneratedDeck
    plan: SideboardPlan
    baseline_win_pct: int
    postboard_win_pct: int
    impacts: tuple[SideboardCardImpact, ...]


def optimize_sideboard_plan(
    deck: GeneratedDeck,
    opponent: GeneratedDeck,
    *,
    archetype: str,
    opponent_archetype: str,
    max_swaps: int = 6,
    samples: int = 600,
    seed: int = 71,
) -> OptimizedSideboardPlan:
    simulator = MatchupSimulator()
    baseline = simulator.simulate(
        deck, opponent,
        archetype_a=archetype,
        archetype_b=opponent_archetype,
        samples=samples,
        seed=seed,
    ).wins_a_pct
    current = deck
    impacts: list[SideboardCardImpact] = []
    used_in: list[DeckEntry] = []
    used_out: list[DeckEntry] = []

    available = sorted(
        _expand(deck.sideboard),
        key=lambda entry: (-_sideboard_value(entry, opponent_archetype), entry.name),
    )
    for step in range(max_swaps):
        best = None
        main = _expand(current.mainboard)
        for incoming in available:
            if incoming in used_in:
                continue
            for outgoing in sorted(main, key=lambda entry: (entry.score, -entry.mana_value, entry.name))[:8]:
                trial_main = list(main)
                trial_main.remove(outgoing)
                trial_main.append(incoming)
                trial = replace(current, mainboard=_compress(trial_main), goldfish_report=None)
                win_pct = simulator.simulate(
                    trial, opponent,
                    archetype_a=archetype,
                    archetype_b=opponent_archetype,
                    samples=samples,
                    seed=seed + step + 1,
                ).wins_a_pct
                candidate = (win_pct, incoming.name, outgoing.name, incoming, outgoing, trial)
                if best is None or candidate[:3] > best[:3]:
                    best = candidate
        if best is None:
            break
        win_pct, _, _, incoming, outgoing, trial = best
        previous = baseline if not impacts else baseline + sum(item.win_rate_delta for item in impacts)
        delta = win_pct - previous
        if delta <= 0:
            break
        current = trial
        used_in.append(incoming)
        used_out.append(outgoing)
        impacts.append(SideboardCardImpact(incoming.name, outgoing.name, delta))

    postboard = baseline + sum(item.win_rate_delta for item in impacts)
    plan = SideboardPlan(
        opponent_archetype=opponent_archetype,
        cards_in=tuple(sorted((name, sum(1 for item in used_in if item.name == name)) for name in {item.name for item in used_in})),
        cards_out=tuple(sorted((name, sum(1 for item in used_out if item.name == name)) for name in {item.name for item in used_out})),
    )
    return OptimizedSideboardPlan(current, plan, baseline, postboard, tuple(impacts))
