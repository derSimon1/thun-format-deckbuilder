from __future__ import annotations

import json
from pathlib import Path

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.token_packages import build_token_package_diagnostics


OUTPUT = Path("artifacts/global/tokens/token-packages.json")


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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    aristocrats = payload["aristocrats"]
    false_positives = payload["broad_role_false_positive_copies"]
    print(
        "Token package diagnostics: "
        f"material={aristocrats['material_copies']} "
        f"outlets={aristocrats['outlet_copies']} "
        f"death_payoffs={aristocrats['death_payoff_copies']} "
        f"drain_payoffs={aristocrats['drain_payoff_copies']} "
        f"false_positive_copies={sum(false_positives.values())}"
    )


if __name__ == "__main__":
    main()
