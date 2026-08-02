from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from thun_deckbuilder.calibrated_strategies import ProwessStrategy
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase
from thun_deckbuilder.land_count_optimizer import choose_land_count, consistency_score


DATABASE_FILE = Path("data/cards.db")
JSON_OUTPUT = Path("izzet-prowess-v2-land-diagnostics.json")
TEXT_OUTPUT = Path("izzet-prowess-v2-land-diagnostics.txt")


def main() -> None:
    with CardDatabase(DATABASE_FILE) as database:
        knowledge_base = KnowledgeBase(database)
        knowledge_base.load()

        strategy = ProwessStrategy()
        request = DeckRequest(
            archetype="prowess",
            colors=("U", "R"),
            deck_size=60,
            max_copies=3,
        )
        candidates = tuple(
            strategy._build_candidate(knowledge_base, request, lands)
            for lands in range(18, 23)
        )
        chosen = choose_land_count(
            candidates,
            preferred_lands=strategy.profile.lands,
        )

    rows: list[dict[str, object]] = []
    for candidate in candidates:
        _, _, entries = candidate.payload
        report = candidate.report
        rows.append(
            {
                "lands": candidate.lands,
                "spells": sum(entry.quantity for entry in entries),
                "threats": sum(
                    entry.quantity
                    for entry in entries
                    if "Creature" in entry.type_line
                ),
                "burn_reach": sum(
                    entry.quantity
                    for entry in entries
                    if "burn" in entry.roles
                ),
                "card_flow": sum(
                    entry.quantity
                    for entry in entries
                    if "card_draw" in entry.roles
                ),
                "consistency_score": round(consistency_score(report), 2),
                **asdict(report),
            }
        )

    payload = {
        "chosen_lands": chosen.lands,
        "preferred_lands": strategy.profile.lands,
        "candidates": rows,
    }
    JSON_OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    headings = (
        "lands",
        "score",
        "playable7",
        "playable6",
        "mulligan",
        "lands2to4",
        "early",
        "coreT3",
        "screw",
        "flood",
        "threats",
        "burn",
        "draw",
    )
    lines = [
        f"Prowess land diagnostics: chosen={chosen.lands}, "
        f"preferred={strategy.profile.lands}",
        " | ".join(headings),
    ]
    for row in rows:
        lines.append(
            " | ".join(
                str(value)
                for value in (
                    row["lands"],
                    row["consistency_score"],
                    row["playable_hands_pct"],
                    row["playable_after_mulligan_pct"],
                    row["mulligan_to_six_pct"],
                    row["two_to_four_lands_pct"],
                    row["early_play_pct"],
                    row["core_by_turn_three_pct"],
                    row["mana_screw_pct"],
                    row["mana_flood_pct"],
                    row["threats"],
                    row["burn_reach"],
                    row["card_flow"],
                )
            )
        )
    text = "\n".join(lines) + "\n"
    TEXT_OUTPUT.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
