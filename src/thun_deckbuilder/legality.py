from dataclasses import dataclass


@dataclass
class PrintLegalityResult:
    legal: bool
    reason: str


def is_print_legal(
    *,
    rarity: str,
    digital: bool,
    games: str,
    set_allowed: bool,
) -> PrintLegalityResult:
    """
    Prüft einen einzelnen Druck auf Thun-Legalität.
    """

    rarity = rarity.lower()

    if rarity not in ("common", "uncommon"):
        return PrintLegalityResult(
            False,
            "Rarity is not common or uncommon."
        )

    if digital:
        return PrintLegalityResult(
            False,
            "Digital print."
        )

    if "paper" not in games.lower():
        return PrintLegalityResult(
            False,
            "Not available in paper."
        )

    if not set_allowed:
        return PrintLegalityResult(
            False,
            "Set not allowed."
        )

    return PrintLegalityResult(
        True,
        "Legal."
    )
from collections.abc import Iterable
from typing import Any


@dataclass
class CardLegalityResult:
    legal: bool
    reason: str
    legal_prints: list[dict[str, Any]]


def is_card_legal(
    prints: Iterable[dict[str, Any]],
) -> CardLegalityResult:
    """
    Prüft alle Druckversionen einer Karte.

    Eine Karte ist legal, wenn mindestens ein Print legal ist.
    """

    print_list = list(prints)

    if not print_list:
        return CardLegalityResult(
            legal=False,
            reason="No prints found.",
            legal_prints=[],
        )

    legal_prints: list[dict[str, Any]] = []

    for card_print in print_list:
        result = is_print_legal(
            rarity=str(card_print.get("rarity", "")),
            digital=bool(card_print.get("digital", False)),
            games=str(card_print.get("games", "")),
            set_allowed=bool(card_print.get("set_allowed", False)),
        )

        if result.legal:
            legal_prints.append(card_print)

    if legal_prints:
        return CardLegalityResult(
            legal=True,
            reason="At least one legal print exists.",
            legal_prints=legal_prints,
        )

    return CardLegalityResult(
        legal=False,
        reason="No legal print exists.",
        legal_prints=[],
    )