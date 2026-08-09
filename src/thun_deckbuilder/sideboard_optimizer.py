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


_LABEL_MATCHUPS: dict[str, frozenset[str]] = {
    "graveyard hate": frozenset({"mill"}),
    "creature sweeper": frozenset({"burn", "tokens"}),
    "countermagic": frozenset({"burn", "artifacts", "control", "mill", "shrines"}),
    "anti-aggro removal": frozenset({"burn", "tokens"}),
    "hand disruption": frozenset({"artifacts", "control", "mill", "shrines"}),
    "artifact/enchantment answer": frozenset({"artifacts", "shrines"}),
    "answer opposing artifacts": frozenset({"artifacts"}),
    "protect artifacts": frozenset({"control", "mill", "shrines"}),
    "protection": frozenset({"burn", "control", "tokens"}),
    "anti-lifegain": frozenset({"control", "tokens"}),
    "protect enchantments": frozenset({"control", "mill"}),
    "enchantment recursion": frozenset({"control", "mill"}),
    "protect mill plan": frozenset({"control", "mill"}),
}

_MARKER_MATCHUPS: dict[str, frozenset[str]] = {
    "sideboard_graveyard_hate": frozenset({"mill"}),
    "sideboard_creature_sweeper": frozenset({"burn", "tokens"}),
    "sideboard_countermagic": frozenset({"burn", "artifacts", "control", "mill", "shrines"}),
    "sideboard_anti_aggro_removal": frozenset({"burn", "tokens"}),
    "sideboard_hand_disruption": frozenset({"artifacts", "control", "mill", "shrines"}),
    "sideboard_artifact_enchantment_answer": frozenset({"artifacts", "shrines"}),
    "sideboard_answer_opposing_artifacts": frozenset({"artifacts"}),
    "sideboard_protect_artifacts": frozenset({"control", "mill", "shrines"}),
    "sideboard_protection": frozenset({"burn", "control", "tokens"}),
    "sideboard_anti_lifegain": frozenset({"control", "tokens"}),
    "sideboard_protect_enchantments": frozenset({"control", "mill"}),
    "sideboard_enchantment_recursion": frozenset({"control", "mill"}),
    "sideboard_protect_mill_plan": frozenset({"control", "mill"}),
}

_FALLBACK_SIGNALS: dict[str, tuple[str, ...]] = {
    "burn": (
        "destroy target creature",
        "exile target creature",
        "target creature gets -",
        "damage to each creature",
        "life gain",
        "lifegain",
        "counter target spell",
    ),
    "tokens": (
        "destroy all creatures",
        "exile all creatures",
        "damage to each creature",
        "target creature gets -",
        "destroy target creature",
        "exile target creature",
    ),
    "artifacts": (
        "destroy target artifact",
        "exile target artifact",
        "gain control of target artifact",
        "counter target spell",
        "target opponent discards",
    ),
    "control": (
        "counter target spell",
        "target opponent discards",
        "can't be countered",
    ),
    "mill": (
        "graveyard",
        "shuffle",
        "counter target spell",
        "hexproof",
        "target opponent discards",
    ),
    "shrines": (
        "destroy target enchantment",
        "exile target enchantment",
        "counter target spell",
        "target opponent discards",
    ),
}


def _text(entry: DeckEntry) -> str:
    return " ".join((entry.name, entry.type_line, *entry.roles, *entry.reasons)).lower()


def _sideboard_labels(entry: DeckEntry) -> tuple[str, ...]:
    prefix = "sideboard: "
    return tuple(
        reason.lower()[len(prefix) :].strip()
        for reason in entry.reasons
        if reason.lower().startswith(prefix)
    )


def _sideboard_markers(entry: DeckEntry) -> tuple[str, ...]:
    return tuple(role for role in entry.roles if role.startswith("sideboard_"))


def _sideboard_relevant(entry: DeckEntry, opponent: str) -> bool:
    """Return whether a sideboard card addresses the declared opponent plan."""

    markers = _sideboard_markers(entry)
    if markers:
        return any(opponent in _MARKER_MATCHUPS.get(marker, frozenset()) for marker in markers)
    labels = _sideboard_labels(entry)
    if labels:
        return any(opponent in _LABEL_MATCHUPS.get(label, frozenset()) for label in labels)
    text = _text(entry)
    return any(phrase in text for phrase in _FALLBACK_SIGNALS.get(opponent, ()))


def _sideboard_value(entry: DeckEntry, opponent: str) -> float:
    return entry.score + (8 if _sideboard_relevant(entry, opponent) else 0)


def _mainboard_cut_key(entry: DeckEntry, opponent: str) -> tuple:
    """Prefer matchup-appropriate cuts before generic low-score cuts.

    Against Burn, conditional and death-triggered token makers are the slowest
    parts of the Go-Wide plan. Immediate/multi makers, anthems, card draw and
    protection are preserved because they either race or stabilize directly.
    """

    roles = set(entry.roles)
    if opponent == "burn":
        if roles.intersection({"token_production_death", "token_production_conditional"}):
            tempo_tier = 0
        elif roles.intersection({"token_immediate_maker", "token_multi_maker"}):
            tempo_tier = 2
        else:
            tempo_tier = 1
        strategic_tier = int(bool(roles.intersection({"anthem", "card_draw", "protection"})))
        return (tempo_tier, strategic_tier, entry.score, -entry.mana_value, entry.name)
    return (1, 0, entry.score, -entry.mana_value, entry.name)


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


def _group_by_name(entries: list[DeckEntry]) -> tuple[tuple[DeckEntry, ...], ...]:
    """Group expanded entries without losing deterministic search order."""

    names = sorted({entry.name for entry in entries})
    return tuple(
        tuple(entry for entry in entries if entry.name == name)
        for name in names
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
        deck, opponent, archetype_a=archetype, archetype_b=opponent_archetype,
        samples=samples, seed=seed,
    ).wins_a_pct
    current = deck
    current_win = baseline
    impacts: list[SideboardCardImpact] = []
    used_in: list[DeckEntry] = []
    used_out: list[DeckEntry] = []
    available = sorted(
        (entry for entry in _expand(deck.sideboard) if _sideboard_relevant(entry, opponent_archetype)),
        key=lambda entry: (-_sideboard_value(entry, opponent_archetype), entry.name),
    )

    while len(used_in) < max_swaps:
        best = None
        main = _expand(current.mainboard)
        remaining = max_swaps - len(used_in)
        incoming_groups = _group_by_name(available)
        outgoing_groups = sorted(
            _group_by_name(main),
            key=lambda group: _mainboard_cut_key(group[0], opponent_archetype),
        )[:8]
        for incoming_group in incoming_groups:
            for outgoing_group in outgoing_groups:
                max_quantity = min(
                    len(incoming_group), len(outgoing_group), remaining
                )
                for quantity in range(1, max_quantity + 1):
                    incoming = incoming_group[:quantity]
                    outgoing = outgoing_group[:quantity]
                    trial_main = list(main)
                    for entry in outgoing:
                        trial_main.remove(entry)
                    trial_main.extend(incoming)
                    trial = replace(
                        current,
                        mainboard=_compress(trial_main),
                        goldfish_report=None,
                    )
                    win_pct = simulator.simulate(
                        trial, opponent, archetype_a=archetype,
                        archetype_b=opponent_archetype, samples=samples,
                        seed=seed + len(used_in) + 1,
                    ).wins_a_pct
                    candidate = (
                        win_pct,
                        quantity,
                        incoming[0].name,
                        outgoing[0].name,
                        incoming,
                        outgoing,
                        trial,
                    )
                    if best is None or candidate[:4] > best[:4]:
                        best = candidate
        if best is None or best[0] <= current_win:
            break
        win_pct, _, _, _, incoming, outgoing, trial = best
        impacts.append(
            SideboardCardImpact(
                incoming[0].name,
                outgoing[0].name,
                win_pct - current_win,
            )
        )
        current_win = win_pct
        current = trial
        used_in.extend(incoming)
        used_out.extend(outgoing)
        used_names = {entry.name for entry in used_in}
        available = [entry for entry in available if entry.name not in used_names]

    plan = SideboardPlan(
        opponent_archetype=opponent_archetype,
        cards_in=tuple(sorted((name, sum(1 for item in used_in if item.name == name)) for name in {item.name for item in used_in})),
        cards_out=tuple(sorted((name, sum(1 for item in used_out if item.name == name)) for name in {item.name for item in used_out})),
    )
    return OptimizedSideboardPlan(current, plan, baseline, current_win, tuple(impacts))
