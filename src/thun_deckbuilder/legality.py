from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from thun_deckbuilder.config import AppConfig


@dataclass(frozen=True)
class PrintLegalityResult:
    legal: bool
    reason: str


@dataclass(frozen=True)
class CardLegalityResult:
    legal: bool
    reason: str
    legal_prints: tuple[dict[str, Any], ...]


def _contains_paper(games: object) -> bool:
    if isinstance(games, (list, tuple, set)):
        return "paper" in {str(game).lower() for game in games}
    return "paper" in str(games).lower()


def is_print_legal(
    card_print: dict[str, Any],
    config: AppConfig,
) -> PrintLegalityResult:
    rarity = str(card_print.get("rarity", "")).lower()
    set_code = str(card_print.get("set_code", card_print.get("set", ""))).lower()
    digital = bool(card_print.get("digital", False))
    games = card_print.get("games", "")

    if rarity not in config.legality.allowed_rarities:
        return PrintLegalityResult(False, "Rarity is not allowed.")
    if digital and not config.legality.allow_digital:
        return PrintLegalityResult(False, "Digital print.")
    if config.legality.paper_only and not _contains_paper(games):
        return PrintLegalityResult(False, "Not available in paper.")
    if set_code in config.sets.blocked_sets:
        return PrintLegalityResult(False, "Set is blocked.")
    if set_code not in config.sets.allowed_sets:
        return PrintLegalityResult(False, "Set is not allowed.")
    return PrintLegalityResult(True, "Legal.")


def is_card_legal(
    prints: Iterable[dict[str, Any]],
    config: AppConfig,
) -> CardLegalityResult:
    print_list = list(prints)
    if not print_list:
        return CardLegalityResult(False, "No prints found.", ())

    legal_prints = tuple(
        card_print
        for card_print in print_list
        if is_print_legal(card_print, config).legal
    )
    if legal_prints:
        return CardLegalityResult(
            True,
            "At least one legal print exists.",
            legal_prints,
        )
    return CardLegalityResult(False, "No legal print exists.", ())
