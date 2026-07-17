from __future__ import annotations

from thun_deckbuilder.card_analyzer import CardAnalysis


def detect_roles(analysis: CardAnalysis) -> frozenset[str]:
    roles: set[str] = set()

    if "draw" in analysis.features:
        roles.add("card_draw")

    if "mana" in analysis.features:
        roles.add("ramp")

    if "token" in analysis.features:
        roles.add("token_maker")

    if "destroy" in analysis.features:
        roles.add("removal")

    if "exile" in analysis.features:
        roles.add("removal")

    if "damage" in analysis.features:
        roles.add("burn")

    return frozenset(roles)