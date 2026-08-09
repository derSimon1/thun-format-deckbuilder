from __future__ import annotations

import ci_global_validation as validation


V2_DEFAULTS: dict[str, tuple[str, ...]] = {
    "burn": ("R",),
    "tokens": ("W",),
    "artifacts": ("U", "R"),
    "control": ("U", "B"),
    "mill": ("U", "B"),
}
_BASE_CORE_COUNT = validation._core_count


def _core_count(archetype, deck, legal_cards):
    if archetype != "control":
        return _BASE_CORE_COUNT(archetype, deck, legal_cards)
    count = 0
    for entry in deck.mainboard:
        card = legal_cards.get(entry.name.casefold(), {})
        text = str(card.get("oracle_text", "")).lower()
        reasons = " ".join(entry.reasons).lower()
        roles = set(entry.roles)
        if roles.intersection({"removal", "card_draw", "board_wipe", "finisher"}) or any(
            phrase in text or phrase in reasons
            for phrase in (
                "counter target",
                "control removal",
                "sweeper",
                "card advantage",
                "control-finisher",
            )
        ):
            count += entry.quantity
    return count


def configure() -> None:
    validation.DEFAULTS = dict(V2_DEFAULTS)
    validation._core_count = _core_count


def main() -> None:
    configure()
    validation.main()


if __name__ == "__main__":
    main()
