from __future__ import annotations

import re
from dataclasses import dataclass


_CARD_LINE = re.compile(
    r"^\s*(?P<quantity>\d+)\s+(?P<name>.+?)"
    r"(?:\s+\([A-Za-z0-9]+\)\s+[A-Za-z0-9-]+)?\s*$"
)
_SECTION_NAMES = {
    "mainboard": "mainboard",
    "deck": "mainboard",
    "sideboard": "sideboard",
    "commander": "commander",
    "companions": "companion",
    "companion": "companion",
    "maybeboard": "maybeboard",
    "considering": "maybeboard",
}


@dataclass(frozen=True)
class ImportedCard:
    name: str
    quantity: int
    section: str = "mainboard"


@dataclass(frozen=True)
class ImportedDeck:
    cards: tuple[ImportedCard, ...]
    source: str = "moxfield-export"

    @property
    def mainboard(self) -> tuple[ImportedCard, ...]:
        return tuple(card for card in self.cards if card.section == "mainboard")

    @property
    def sideboard(self) -> tuple[ImportedCard, ...]:
        return tuple(card for card in self.cards if card.section == "sideboard")

    @property
    def mainboard_size(self) -> int:
        return sum(card.quantity for card in self.mainboard)


def parse_moxfield_text(text: str) -> ImportedDeck:
    """Parse Moxfield's plain-text export format.

    Supported card lines include both ``3 Card Name`` and
    ``3 Card Name (SET) 123``. Unknown headings and comments are ignored.
    """
    section = "mainboard"
    cards: list[ImportedCard] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "//")):
            continue

        normalized = line.rstrip(":").strip().lower()
        if normalized in _SECTION_NAMES:
            section = _SECTION_NAMES[normalized]
            continue

        match = _CARD_LINE.match(line)
        if not match:
            continue
        quantity = int(match.group("quantity"))
        name = match.group("name").strip()
        if quantity <= 0 or not name:
            continue
        cards.append(ImportedCard(name=name, quantity=quantity, section=section))

    if not cards:
        raise ValueError("No card lines found in Moxfield export.")
    return ImportedDeck(cards=tuple(cards))
