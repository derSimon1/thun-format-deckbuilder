from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.token_packages import build_token_package_diagnostics
from thun_deckbuilder.token_production import analyze_token_production


OUTPUT = Path("artifacts/global/tokens/token-packages.json")


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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    aristocrats = payload["aristocrats"]
    false_positives = payload["broad_role_false_positive_copies"]
    production = payload["production"]
    print(
        "Token package diagnostics: "
        f"material={aristocrats['material_copies']} "
        f"outlets={aristocrats['outlet_copies']} "
        f"death_payoffs={aristocrats['death_payoff_copies']} "
        f"drain_payoffs={aristocrats['drain_payoff_copies']} "
        f"false_positive_copies={sum(false_positives.values())} "
        f"production_modes={production['mode_copies']}"
    )


if __name__ == "__main__":
    main()
