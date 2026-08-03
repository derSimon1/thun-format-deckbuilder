from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.opening_hand_simulator import OpeningHandSimulator
from thun_deckbuilder.token_packages import build_token_package_diagnostics
from thun_deckbuilder.token_production import (
    analyze_token_production,
    build_token_production_capacity,
)


OUTPUT = Path("artifacts/global/tokens/token-packages.json")
ARENA_OUTPUT = Path("artifacts/global/tokens/arena-import.txt")
OPENING_HAND_OUTPUT = Path("artifacts/global/tokens/opening-hands-100.json")
OPENING_HAND_SEED = 1701
OPENING_HAND_SAMPLES = 100


def _production_diagnostics(deck, legal_by_name) -> dict[str, object]:
    cards: list[dict[str, object]] = []
    mode_copies: Counter[str] = Counter()
    immediate_output = repeatable_output = 0
    for entry in deck.mainboard:
        raw = legal_by_name.get(entry.name.casefold())
        if raw is None:
            continue
        profile = analyze_token_production(analyze_card(dict(raw)))
        if not profile.creates_creature_tokens:
            continue
        mode_copies[profile.mode] += entry.quantity
        if profile.mode == "immediate":
            immediate_output += entry.quantity * profile.minimum_output
        elif profile.mode == "repeatable":
            repeatable_output += entry.quantity * profile.minimum_output
        cards.append(
            {
                "name": entry.name,
                "quantity": entry.quantity,
                "profile": asdict(profile),
                "mode": profile.mode,
                "role_markers": sorted(
                    role
                    for role in entry.roles
                    if role.startswith("token_output_")
                    or role.startswith("token_production_")
                ),
            }
        )
    cards.sort(key=lambda item: (str(item["mode"]), str(item["name"])))
    return {
        "mode_copies": dict(sorted(mode_copies.items())),
        "guaranteed_immediate_output_per_all_copies": immediate_output,
        "repeatable_output_per_trigger_per_all_copies": repeatable_output,
        "cards": cards,
    }


def _arena_import(deck) -> str:
    mainboard_lines = [
        f"{entry.quantity} {entry.name}" for entry in deck.mainboard
    ]
    if deck.mana_base is not None:
        mainboard_lines.extend(
            f"{allocation.quantity} {allocation.land_name}"
            for allocation in deck.mana_base.allocations
            if allocation.quantity
        )
    elif deck.lands:
        mainboard_lines.append(f"{deck.lands} Plains")

    sideboard_lines = [
        f"{entry.quantity} {entry.name}" for entry in deck.sideboard
    ]
    mainboard_total = sum(entry.quantity for entry in deck.mainboard) + deck.lands
    sideboard_total = sum(entry.quantity for entry in deck.sideboard)
    if mainboard_total != 60:
        raise ValueError(f"Arena mainboard must contain 60 cards, got {mainboard_total}")
    if sideboard_total != 15:
        raise ValueError(f"Arena sideboard must contain 15 cards, got {sideboard_total}")
    return "\n".join(("Deck", *mainboard_lines, "", "Sideboard", *sideboard_lines, ""))


def _opening_hand_diagnostics(deck) -> dict[str, object]:
    report = OpeningHandSimulator().simulate_plan(
        deck,
        archetype="tokens",
        plan="go_wide",
        samples=OPENING_HAND_SAMPLES,
        seed=OPENING_HAND_SEED,
    )
    if report.samples != OPENING_HAND_SAMPLES or len(report.hands) != OPENING_HAND_SAMPLES:
        raise ValueError(
            "Opening-hand validation must store exactly "
            f"{OPENING_HAND_SAMPLES} hands"
        )
    return asdict(report)


def main() -> None:
    with CardDatabase() as database:
        legal = database.get_all_legal_cards()
        legal_by_name = {
            str(card.get("name", "")).casefold(): card
            for card in legal
            if card.get("name")
        }
        deck = generate_deck(
            database=database,
            archetype="tokens",
            colors=("W",),
        )

    payload = build_token_package_diagnostics(deck, legal_by_name)
    payload["production"] = _production_diagnostics(deck, legal_by_name)
    payload["production"]["pool_capacity"] = build_token_production_capacity(legal)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    ARENA_OUTPUT.write_text(_arena_import(deck), encoding="utf-8")
    opening_hands = _opening_hand_diagnostics(deck)
    OPENING_HAND_OUTPUT.write_text(
        json.dumps(opening_hands, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    aristocrats = payload["aristocrats"]
    false_positives = payload["broad_role_false_positive_copies"]
    production = payload["production"]
    capacity = production["pool_capacity"]
    print(
        "Token package diagnostics: "
        f"material={aristocrats['material_copies']} "
        f"outlets={aristocrats['outlet_copies']} "
        f"death_payoffs={aristocrats['death_payoff_copies']} "
        f"drain_payoffs={aristocrats['drain_payoff_copies']} "
        f"false_positive_copies={sum(false_positives.values())} "
        f"production_modes={production['mode_copies']} "
        f"pool_modes={capacity['distinct_by_mode']} "
        f"opening_hands={opening_hands['samples']} "
        f"opening_seed={opening_hands['seed']} "
        f"plan_capable={opening_hands['plan_capable_pct']}% "
        f"deck_hash={opening_hands['deck_hash']}"
    )


if __name__ == "__main__":
    main()
