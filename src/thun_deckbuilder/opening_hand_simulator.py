from __future__ import annotations

import random
from dataclasses import dataclass

from thun_deckbuilder.deck_generator import GeneratedDeck


@dataclass(frozen=True)
class OpeningHandReport:
    samples: int
    playable_hands_pct: int
    two_to_four_lands_pct: int
    early_play_pct: int
    core_by_turn_three_pct: int
    mana_screw_pct: int
    mana_flood_pct: int


CORE_PHRASES = {
    "artifacts": ("artifact", "affinity", "improvise", "metalcraft"),
    "shrines": ("shrine",),
    "mill": ("mill", "library into"),
}


def _is_core(entry, archetype: str) -> bool:
    name = entry.name.lower()
    reasons = " ".join(entry.reasons).lower()
    if archetype == "artifacts":
        return "artifact" in entry.type_line.lower() or any(p in reasons for p in CORE_PHRASES[archetype])
    return any(p in name or p in reasons for p in CORE_PHRASES.get(archetype, ()))


class OpeningHandSimulator:
    """Estimate early consistency with deterministic Monte Carlo samples."""

    def simulate(
        self,
        deck: GeneratedDeck,
        *,
        archetype: str,
        samples: int = 2000,
        seed: int = 17,
    ) -> OpeningHandReport:
        library: list[tuple[str, float, bool]] = [("land", 0, False)] * deck.lands
        for entry in deck.mainboard:
            library.extend(
                [("spell", entry.mana_value, _is_core(entry, archetype))] * entry.quantity
            )

        rng = random.Random(seed)
        playable = lands_ok = early = core = screw = flood = 0
        for _ in range(samples):
            shuffled = library[:]
            rng.shuffle(shuffled)
            opening = shuffled[:7]
            turn_three = shuffled[:10]
            land_count = sum(1 for kind, _, _ in opening if kind == "land")
            has_early = any(kind == "spell" and mv <= 2 for kind, mv, _ in opening)
            has_core = any(kind == "spell" and is_core for kind, _, is_core in turn_three)
            is_playable = 2 <= land_count <= 4 and has_early

            playable += int(is_playable)
            lands_ok += int(2 <= land_count <= 4)
            early += int(has_early)
            core += int(has_core)
            screw += int(land_count <= 1)
            flood += int(land_count >= 5)

        pct = lambda value: round(value * 100 / samples)
        return OpeningHandReport(
            samples=samples,
            playable_hands_pct=pct(playable),
            two_to_four_lands_pct=pct(lands_ok),
            early_play_pct=pct(early),
            core_by_turn_three_pct=pct(core),
            mana_screw_pct=pct(screw),
            mana_flood_pct=pct(flood),
        )
