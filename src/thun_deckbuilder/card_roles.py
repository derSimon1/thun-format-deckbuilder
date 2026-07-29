from __future__ import annotations

import re

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.card_role import CardRole


def detect_roles(analysis: CardAnalysis) -> frozenset[CardRole]:
    """Assign broad functional roles from Oracle text and card type.

    The detector intentionally uses conservative patterns. False positives are
    more damaging to composition than missing an unusual wording, so new
    patterns should be backed by tests.
    """

    text = analysis.oracle_text.lower()
    roles: set[CardRole] = set()

    if "draw" in analysis.features or "exile the top card" in text:
        roles.add(CardRole.CARD_DRAW)

    if "mana" in analysis.features or "search your library for a basic land" in text:
        roles.add(CardRole.RAMP)

    if "token" in analysis.features:
        roles.add(CardRole.TOKEN_MAKER)

    if "destroy" in analysis.features or "exile" in analysis.features:
        roles.add(CardRole.REMOVAL)
    if re.search(r"deals? \d+ damage to target creature", text):
        roles.add(CardRole.REMOVAL)

    if "damage" in analysis.features and any(
        phrase in text
        for phrase in (
            "any target",
            "target player",
            "target opponent",
            "each opponent",
            "each player",
        )
    ):
        roles.add(CardRole.BURN)

    anthem_patterns = (
        "creatures you control get +",
        "other creatures you control get +",
        "tokens you control get +",
        "creature tokens you control get +",
        "put a +1/+1 counter on each",
    )
    if any(pattern in text for pattern in anthem_patterns):
        roles.add(CardRole.ANTHEM)
        roles.add(CardRole.TOKEN_PAYOFF)

    if any(
        phrase in text
        for phrase in (
            "whenever a token enters",
            "whenever one or more tokens",
            "for each token you control",
            "for each creature token you control",
            "creature tokens you control have",
        )
    ):
        roles.add(CardRole.TOKEN_PAYOFF)

    if any(
        phrase in text
        for phrase in (
            "creatures you control gain indestructible",
            "permanents you control gain hexproof",
            "target creature gains indestructible",
            "phase out",
        )
    ):
        roles.add(CardRole.PROTECTION)

    if "sacrifice" in text:
        roles.add(CardRole.SACRIFICE)

    if analysis.is_creature and analysis.mana_value <= 2:
        roles.add(CardRole.AGGRO_CREATURE)

    if analysis.is_creature and analysis.mana_value >= 5:
        roles.add(CardRole.FINISHER)

    if any(
        phrase in text
        for phrase in (
            "destroy all creatures",
            "exile all creatures",
            "deals 3 damage to each creature",
            "deals 4 damage to each creature",
        )
    ):
        roles.add(CardRole.BOARD_WIPE)

    return frozenset(roles)
