from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_profile import DeckProfile


@dataclass(frozen=True)
class DeckStateEntry:
    card_name: str
    quantity: int
    contribution: CardContribution

    def __post_init__(self) -> None:
        if not self.card_name:
            raise ValueError("Card name cannot be empty.")
        if self.quantity <= 0:
            raise ValueError("Deck entry quantity must be positive.")


@dataclass(frozen=True)
class DeckState:
    """Immutable snapshot of a deck while it is being constructed."""

    entries: tuple[DeckStateEntry, ...] = ()

    @property
    def total_cards(self) -> int:
        return sum(entry.quantity for entry in self.entries)

    @property
    def land_count(self) -> int:
        return sum(entry.quantity for entry in self.entries if entry.contribution.is_land)

    @property
    def spell_count(self) -> int:
        return self.total_cards - self.land_count

    def quantity_of(self, card_name: str) -> int:
        return sum(entry.quantity for entry in self.entries if entry.card_name == card_name)

    def role_count(self, role: str) -> float:
        return sum(
            entry.quantity * entry.contribution.strength_for(role)
            for entry in self.entries
        )

    def tag_count(self, tag: str) -> int:
        return sum(
            entry.quantity
            for entry in self.entries
            if tag in entry.contribution.tags
        )

    def curve_count(self, maximum_mana_value: float, previous_maximum: float = -1) -> int:
        return sum(
            entry.quantity
            for entry in self.entries
            if not entry.contribution.is_land
            and previous_maximum < entry.contribution.mana_value <= maximum_mana_value
        )

    def color_pip_count(self, color: str) -> int:
        return sum(
            entry.quantity * entry.contribution.pip_count(color)
            for entry in self.entries
        )

    def remaining_slots(self, deck_size: int) -> int:
        return max(0, deck_size - self.total_cards)

    def remaining_spell_slots(self, profile: DeckProfile, deck_size: int) -> int:
        return max(0, profile.spell_slots(deck_size) - self.spell_count)

    def can_add(
        self,
        contribution: CardContribution,
        quantity: int,
        *,
        deck_size: int,
        max_copies: int,
    ) -> bool:
        if quantity <= 0:
            return False
        if self.total_cards + quantity > deck_size:
            return False
        if self.quantity_of(contribution.card_name) + quantity > max_copies:
            return False
        return True

    def with_card(
        self,
        contribution: CardContribution,
        quantity: int,
        *,
        deck_size: int | None = None,
        max_copies: int | None = None,
    ) -> "DeckState":
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if deck_size is not None and max_copies is not None and not self.can_add(
            contribution,
            quantity,
            deck_size=deck_size,
            max_copies=max_copies,
        ):
            raise ValueError(f"Cannot add {quantity} copies of '{contribution.card_name}'.")

        updated: list[DeckStateEntry] = []
        found = False
        for entry in self.entries:
            if entry.card_name == contribution.card_name:
                updated.append(
                    DeckStateEntry(
                        card_name=entry.card_name,
                        quantity=entry.quantity + quantity,
                        contribution=contribution,
                    )
                )
                found = True
            else:
                updated.append(entry)
        if not found:
            updated.append(
                DeckStateEntry(
                    card_name=contribution.card_name,
                    quantity=quantity,
                    contribution=contribution,
                )
            )
        updated.sort(key=lambda item: (item.contribution.mana_value, item.card_name))
        return DeckState(entries=tuple(updated))
