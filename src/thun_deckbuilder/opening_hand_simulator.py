from __future__ import annotations

import random
from dataclasses import dataclass

from thun_deckbuilder.deck_generator import GeneratedDeck


CardSample = tuple[str, float, bool]


@dataclass(frozen=True)
class OpeningHandReport:
    samples: int
    playable_hands_pct: int
    playable_after_mulligan_pct: int
    mulligan_to_six_pct: int
    two_to_four_lands_pct: int
    early_play_pct: int
    core_by_turn_three_pct: int
    mana_screw_pct: int
    mana_flood_pct: int


CORE_PHRASES = {
    "artifacts": ("artifact", "affinity", "improvise", "metalcraft"),
    "shrines": ("shrine",),
    "mill": ("mill", "library into"),
    "prowess": ("echte prowess-bedrohung", "prowess-bedrohung"),
}


def _is_core(entry, archetype: str) -> bool:
    name = entry.name.lower()
    reasons = " ".join(entry.reasons).lower()
    if archetype == "artifacts":
        return "artifact" in entry.type_line.lower() or any(
            phrase in reasons for phrase in CORE_PHRASES[archetype]
        )
    return any(
        phrase in name or phrase in reasons
        for phrase in CORE_PHRASES.get(archetype, ())
    )


def _land_count(cards: list[CardSample]) -> int:
    return sum(1 for kind, _, _ in cards if kind == "land")


def _has_early_play(cards: list[CardSample]) -> bool:
    return any(kind == "spell" and mana_value <= 2 for kind, mana_value, _ in cards)


def _is_playable(cards: list[CardSample]) -> bool:
    lands = _land_count(cards)
    return 2 <= lands <= 4 and _has_early_play(cards)


def _bottom_choice(opening: list[CardSample]) -> int:
    """Choose the London-mulligan bottom card using a deterministic hand heuristic."""
    def score(bottom_index: int) -> tuple[int, int, int, int, float]:
        kept = opening[:bottom_index] + opening[bottom_index + 1 :]
        lands = _land_count(kept)
        early = _has_early_play(kept)
        core = any(kind == "spell" and is_core for kind, _, is_core in kept)
        expensive = sum(
            1 for kind, mana_value, _ in kept if kind == "spell" and mana_value >= 4
        )
        return (
            int(_is_playable(kept)),
            int(2 <= lands <= 4),
            int(early),
            int(core),
            -abs(lands - 3) - expensive * 0.25,
        )

    return max(range(len(opening)), key=score)


class OpeningHandSimulator:
    """Estimate early consistency with deterministic Monte Carlo samples.

    Unplayable seven-card hands take one London mulligan to six. The simulator
    draws a fresh seven and bottoms the card that produces the strongest six.
    Mana screw and flood are measured after the first three draw steps so the
    land-count optimizer can balance early casting reliability against flooding.
    """

    def simulate(
        self,
        deck: GeneratedDeck,
        *,
        archetype: str,
        samples: int = 2000,
        seed: int = 17,
    ) -> OpeningHandReport:
        library: list[CardSample] = [("land", 0, False)] * deck.lands
        for entry in deck.mainboard:
            library.extend(
                [("spell", entry.mana_value, _is_core(entry, archetype))]
                * entry.quantity
            )

        rng = random.Random(seed)
        raw_playable = post_mulligan_playable = mulligans = 0
        lands_ok = early = core = screw = flood = 0

        for _ in range(samples):
            shuffled = library[:]
            rng.shuffle(shuffled)
            opening = shuffled[:7]
            raw_is_playable = _is_playable(opening)
            raw_playable += int(raw_is_playable)

            if raw_is_playable:
                kept = opening
                draw_sequence = shuffled
            else:
                mulligans += 1
                reshuffled = library[:]
                rng.shuffle(reshuffled)
                seven = reshuffled[:7]
                bottom_index = _bottom_choice(seven)
                bottomed = seven[bottom_index]
                kept = seven[:bottom_index] + seven[bottom_index + 1 :]
                draw_sequence = kept + reshuffled[7:] + [bottomed]

            land_count = _land_count(kept)
            has_early = _has_early_play(kept)
            cards_seen_by_turn_three = draw_sequence[: len(kept) + 3]
            turn_three_land_count = _land_count(cards_seen_by_turn_three)
            has_core = any(
                kind == "spell" and is_core
                for kind, _, is_core in cards_seen_by_turn_three
            )

            post_mulligan_playable += int(_is_playable(kept))
            lands_ok += int(2 <= land_count <= 4)
            early += int(has_early)
            core += int(has_core)
            screw += int(turn_three_land_count <= 1)
            flood += int(turn_three_land_count >= 5)

        pct = lambda value: round(value * 100 / samples)
        return OpeningHandReport(
            samples=samples,
            playable_hands_pct=pct(raw_playable),
            playable_after_mulligan_pct=pct(post_mulligan_playable),
            mulligan_to_six_pct=pct(mulligans),
            two_to_four_lands_pct=pct(lands_ok),
            early_play_pct=pct(early),
            core_by_turn_three_pct=pct(core),
            mana_screw_pct=pct(screw),
            mana_flood_pct=pct(flood),
        )
