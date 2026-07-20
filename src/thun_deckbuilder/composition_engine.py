from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from thun_deckbuilder.deck_generator import DeckEntry, ManaCost, parse_mana_cost
from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.knowledge_base import CardKnowledge


@dataclass(frozen=True)
class CompositionCandidate:
    knowledge: CardKnowledge
    score: float
    reasons: tuple[str, ...]

    @property
    def name(self) -> str:
        return self.knowledge.analysis.name


@dataclass(frozen=True)
class CompositionResult:
    entries: tuple[DeckEntry, ...]
    requested_roles: tuple[tuple[str, int], ...]
    fulfilled_roles: tuple[tuple[str, int], ...]
    warnings: tuple[str, ...]


ScoreFunction = Callable[[CardKnowledge], tuple[float, tuple[str, ...]]]
EligibilityFunction = Callable[[CardKnowledge], bool]


def _curve_band(mana_value: float, profile: DeckProfile) -> int:
    for index, target in enumerate(profile.curve_targets):
        if mana_value <= target.maximum_mana_value:
            return index
    return len(profile.curve_targets)


def _entry(candidate: CompositionCandidate, quantity: int) -> DeckEntry:
    analysis = candidate.knowledge.analysis
    mana_cost = parse_mana_cost(str(candidate.knowledge.card.get("mana_cost", "")))
    return DeckEntry(
        name=analysis.name,
        quantity=quantity,
        mana_cost=mana_cost,
        mana_value=analysis.mana_value,
        type_line=analysis.type_line,
        score=candidate.score,
        reasons=candidate.reasons,
        roles=tuple(sorted(candidate.knowledge.roles)),
    )


def build_composition(
    cards: Iterable[CardKnowledge],
    *,
    profile: DeckProfile,
    deck_size: int,
    max_copies: int,
    eligible: EligibilityFunction,
    score_card: ScoreFunction,
) -> CompositionResult:
    """Select cards by strategic role, then fill remaining slots by quality.

    A card can satisfy more than one role, but its copies are added only once.
    Missing optional roles produce warnings and are filled with the best eligible
    cards. Missing mandatory role minimums fail loudly.
    """

    spell_slots = profile.spell_slots(deck_size)
    candidates: list[CompositionCandidate] = []
    for card in cards:
        if not eligible(card):
            continue
        score, reasons = score_card(card)
        candidates.append(
            CompositionCandidate(
                knowledge=card,
                score=score,
                reasons=reasons,
            )
        )
    candidates.sort(
        key=lambda item: (
            -item.score,
            item.knowledge.analysis.mana_value,
            item.name,
        )
    )

    selected: dict[str, tuple[CompositionCandidate, int]] = {}
    fulfilled: dict[str, int] = {target.role: 0 for target in profile.role_targets}
    warnings: list[str] = []
    band_counts = [0 for _ in profile.curve_targets]

    def remaining_slots() -> int:
        return spell_slots - sum(quantity for _, quantity in selected.values())

    def add(candidate: CompositionCandidate, quantity: int) -> int:
        if quantity <= 0 or remaining_slots() <= 0:
            return 0
        previous = selected.get(candidate.name)
        current_quantity = previous[1] if previous else 0
        available = max_copies - current_quantity
        amount = min(quantity, available, remaining_slots())
        if amount <= 0:
            return 0
        selected[candidate.name] = (candidate, current_quantity + amount)
        if profile.curve_targets:
            band = _curve_band(candidate.knowledge.analysis.mana_value, profile)
            if band < len(band_counts):
                band_counts[band] += amount
        for role in fulfilled:
            if role in candidate.knowledge.roles:
                fulfilled[role] += amount
        return amount

    # First satisfy role targets in profile priority order.
    for role_target in profile.role_targets:
        role_candidates = [item for item in candidates if role_target.role in item.knowledge.roles]
        for candidate in role_candidates:
            needed = role_target.target - fulfilled[role_target.role]
            if needed <= 0 or remaining_slots() <= 0:
                break
            add(candidate, needed)

        achieved = fulfilled[role_target.role]
        if achieved < role_target.minimum:
            raise ValueError(
                f"Not enough cards for mandatory role '{role_target.role}': "
                f"required {role_target.minimum}, found {achieved}."
            )
        if achieved < role_target.target:
            warnings.append(
                f"Role '{role_target.role}' reached {achieved}/{role_target.target}; "
                "remaining slots were filled by overall card quality."
            )

    # Fill remaining slots with quality while preferring under-filled curve bands.
    while remaining_slots() > 0:
        available = [
            item for item in candidates
            if selected.get(item.name, (item, 0))[1] < max_copies
        ]
        if not available:
            raise ValueError(f"Not enough eligible cards; {remaining_slots()} spell slots remain.")

        def fill_priority(item: CompositionCandidate) -> tuple[int, float, float, str]:
            if profile.curve_targets:
                band = _curve_band(item.knowledge.analysis.mana_value, profile)
                under_target = (
                    band < len(profile.curve_targets)
                    and band_counts[band] < profile.curve_targets[band].target
                )
            else:
                under_target = False
            return (0 if under_target else 1, -item.score, item.knowledge.analysis.mana_value, item.name)

        candidate = min(available, key=fill_priority)
        add(candidate, max_copies)

    entries = tuple(
        _entry(candidate, quantity)
        for candidate, quantity in sorted(
            selected.values(),
            key=lambda value: (value[0].knowledge.analysis.mana_value, value[0].name),
        )
    )
    return CompositionResult(
        entries=entries,
        requested_roles=tuple((target.role, target.target) for target in profile.role_targets),
        fulfilled_roles=tuple((role, fulfilled[role]) for role in fulfilled),
        warnings=tuple(warnings),
    )
