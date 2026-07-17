from __future__ import annotations

from dataclasses import dataclass


SUPPORTED_ARCHETYPES = frozenset(
    {
        "burn",
        "tokens",
    }
)

VALID_COLORS = frozenset(
    {
        "W",
        "U",
        "B",
        "R",
        "G",
    }
)


@dataclass(frozen=True)
class DeckRequest:
    archetype: str
    colors: tuple[str, ...]
    deck_size: int = 60
    max_copies: int = 3

    def __post_init__(self) -> None:
        normalized_archetype = (
            self.archetype
            .strip()
            .lower()
        )

        normalized_colors = tuple(
            color.strip().upper()
            for color in self.colors
        )

        object.__setattr__(
            self,
            "archetype",
            normalized_archetype,
        )

        object.__setattr__(
            self,
            "colors",
            normalized_colors,
        )

        if normalized_archetype not in SUPPORTED_ARCHETYPES:
            supported = ", ".join(
                sorted(SUPPORTED_ARCHETYPES)
            )

            raise ValueError(
                f"Unbekannter Archetyp: {self.archetype}. "
                f"Unterstützt werden aktuell: {supported}."
            )

        invalid_colors = (
            set(normalized_colors)
            - VALID_COLORS
        )

        if invalid_colors:
            invalid = ", ".join(
                sorted(invalid_colors)
            )

            raise ValueError(
                "Ungültige Farbe oder Farbkombination: "
                f"{invalid}."
            )

        if not normalized_colors:
            raise ValueError(
                "Mindestens eine Farbe muss angegeben werden."
            )

        if len(set(normalized_colors)) != len(
            normalized_colors
        ):
            raise ValueError(
                "Eine Farbe darf nicht mehrfach angegeben werden."
            )

        if self.deck_size <= 0:
            raise ValueError(
                "Die Deckgröße muss größer als 0 sein."
            )

        if self.max_copies <= 0:
            raise ValueError(
                "Die maximale Kopienzahl muss größer als 0 sein."
            )