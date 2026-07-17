from __future__ import annotations

from thun_deckbuilder.card_analyzer import CardAnalysis


def detect_synergies(analysis: CardAnalysis) -> frozenset[str]:
    synergies: set[str] = set()

    text = analysis.oracle_text.lower()
    type_line = analysis.type_line.lower()

    if "damage" in analysis.features and analysis.is_instant:
        synergies.add("spellslinger")

    if "token" in analysis.features:
        synergies.add("tokens")

    if "shrine" in type_line:
        synergies.add("shrines")

    if "elf" in type_line:
        synergies.add("elves")

    if "sacrifice" in text:
        synergies.add("aristocrats")

    if "landfall" in text:
        synergies.add("landfall")

    return frozenset(synergies)