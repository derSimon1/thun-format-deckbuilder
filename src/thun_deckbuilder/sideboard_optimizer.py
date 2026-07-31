from __future__ import annotations

from dataclasses import dataclass, replace

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck
from thun_deckbuilder.matchup_simulator import MatchupSimulator


@dataclass(frozen=True)
class SideboardPlan:
    opponent_archetype: str
    cards_in: tuple[tuple[str, int], ...]
    cards_out: tuple[tuple[str, int], ...]


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


def _text(entry: DeckEntry) -> str:
    return " ".join((entry.name, entry.type_line, *entry.roles, *entry.reasons)).lower()


def _sideboard_value(entry: DeckEntry, opponent: str) -> float:
    text = _text(entry)
    score = entry.score
    signals = {
        "burn": ("removal", "destroy", "exile", "lifegain", "life gain", "each creature"),
        "tokens": ("removal", "destroy", "exile", "lifegain", "each creature"),
        "mill": ("graveyard", "shuffle", "counter", "hexproof", "draw"),
        "artifacts": ("artifact", "destroy", "exile", "counter"),
        "shrines": ("enchantment", "destroy", "exile", "counter"),
    }
    if any(key in text for key in signals.get(opponent, ())):
        score += 8
    return score


def _expand(entries: tuple[DeckEntry, ...]) -> list[DeckEntry]:
    return [replace(entry, quantity=1) for entry in entries for _ in range(entry.quantity)]


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
    current_win = baseline
    impacts: list[SideboardCardImpact] = []
    used_names: set[str] = set()
    used_in: list[DeckEntry] = []
    used_out: list[DeckEntry] = []
    available = sorted(_expand(deck.sideboard), key=lambda entry: (-_sideboard_value(entry, opponent_archetype), entry.name))

    for step in range(max_swaps):
        best = None
        main = _expand(current.mainboard)
        for incoming in available:
            if incoming.name in used_names:
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
        if best is None or best[0] <= current_win:
            break
        win_pct, _, _, incoming, outgoing, trial = best
        impacts.append(SideboardCardImpact(incoming.name, outgoing.name, win_pct - current_win))
        current_win = win_pct
        current = trial
        used_names.add(incoming.name)
        used_in.append(incoming)
        used_out.append(outgoing)

    plan = SideboardPlan(
        opponent_archetype=opponent_archetype,
        cards_in=tuple(sorted((name, sum(1 for item in used_in if item.name == name)) for name in {item.name for item in used_in})),
        cards_out=tuple(sorted((name, sum(1 for item in used_out if item.name == name)) for name in {item.name for item in used_out})),
    )
    return OptimizedSideboardPlan(current, plan, baseline, current_win, tuple(impacts))
