from dataclasses import dataclass


@dataclass(frozen=True)
class CardRoles:
    removal: bool = False
    burn: bool = False
    draw: bool = False
    ramp: bool = False
    counterspell: bool = False
    token: bool = False


def detect_roles(card: dict) -> CardRoles:

    text = card.get("oracle_text", "").lower()

    type_line = card.get("type_line", "").lower()

    return CardRoles(

        removal=(
            "destroy target" in text
            or
            "exile target" in text
        ),

        burn=(
            "deals" in text
            and
            "damage" in text
        ),

        draw=(
            "draw a card" in text
            or
            "draw two cards" in text
            or
            "draw three cards" in text
        ),

        ramp=(
            "search your library for a basic land" in text
            or
            "add {g}" in text
        ),

        counterspell=(
            "counter target spell" in text
        ),

        token=(
            "create" in text
            and
            "token" in text
        ),
    )