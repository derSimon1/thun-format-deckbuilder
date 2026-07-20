from __future__ import annotations

import re

from thun_deckbuilder.card_analyzer import CardAnalysis


def detect_roles(analysis: CardAnalysis) -> frozenset[str]:
    """Assign broad functional roles from Oracle text and card type.

    The detector intentionally uses conservative patterns. False positives are
    more damaging to composition than missing an unusual wording, so new
    patterns should be backed by tests.
    """

    text = analysis.oracle_text.lower()
    roles: set[str] = set()

    if "draw" in analysis.features or "exile the top card" in text:
        roles.add("card_draw")

    if "mana" in analysis.features or "search your library for a basic land" in text:
        roles.add("ramp")

    if "token" in analysis.features:
        roles.add("token_maker")

    if "destroy" in analysis.features or "exile" in analysis.features:
        roles.add("removal")
    if re.search(r"deals? \d+ damage to target creature", text):
        roles.add("removal")

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
        roles.add("burn")

    anthem_patterns = (
        "creatures you control get +",
        "other creatures you control get +",
        "tokens you control get +",
        "creature tokens you control get +",
        "put a +1/+1 counter on each",
    )
    if any(pattern in text for pattern in anthem_patterns):
        roles.add("anthem")
        roles.add("token_payoff")

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
        roles.add("token_payoff")

    if any(
        phrase in text
        for phrase in (
            "creatures you control gain indestructible",
            "permanents you control gain hexproof",
            "target creature gains indestructible",
            "phase out",
        )
    ):
        roles.add("protection")

    if "sacrifice" in text:
        roles.add("sacrifice")

    if analysis.is_creature and analysis.mana_value <= 2:
        roles.add("aggro_creature")

    if analysis.is_creature and analysis.mana_value >= 5:
        roles.add("finisher")

    if any(
        phrase in text
        for phrase in (
            "destroy all creatures",
            "exile all creatures",
            "deals 3 damage to each creature",
            "deals 4 damage to each creature",
        )
    ):
        roles.add("board_wipe")

    return frozenset(roles)
