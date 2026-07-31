from __future__ import annotations

import re

from thun_deckbuilder.card_analyzer import CardAnalysis
from thun_deckbuilder.synergy_tag import SynergyTag


_TOKEN_PAYOFF_PATTERNS = (
    "creature tokens you control",
    "tokens you control get",
    "whenever one or more tokens",
    "for each token you control",
)
_SPELL_PAYOFF_PATTERNS = (
    "whenever you cast an instant or sorcery",
    "whenever you cast a noncreature spell",
    "magecraft",
    "prowess",
)
_ARTIFACT_PAYOFF_PATTERNS = (
    "artifacts you control",
    "artifact you control",
    "for each artifact",
    "whenever an artifact",
    "affinity for artifacts",
    "metalcraft",
)
_DEATH_TRIGGER_PATTERNS = (
    "whenever another creature dies",
    "whenever a creature you control dies",
    "when this creature dies",
    "when another creature dies",
)


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def detect_synergies(analysis: CardAnalysis) -> frozenset[SynergyTag]:
    """Detect broad and actionable synergy tags from Oracle text and types.

    The broad legacy tags remain available, while the granular tags are used by
    the dynamic synergy scorer.
    """

    synergies: set[SynergyTag] = set()
    text = analysis.oracle_text.lower()
    type_line = analysis.type_line.lower()

    if analysis.is_instant or analysis.is_sorcery:
        synergies.add(SynergyTag.SPELL)

    if "damage" in analysis.features and analysis.is_instant:
        synergies.add(SynergyTag.SPELLSLINGER)

    if "token" in analysis.features:
        synergies.update(
            {SynergyTag.TOKENS, SynergyTag.TOKEN_MAKER, SynergyTag.SACRIFICE_FODDER}
        )

    if _contains_any(text, _TOKEN_PAYOFF_PATTERNS):
        synergies.update({SynergyTag.TOKENS, SynergyTag.TOKEN_PAYOFF})

    if _contains_any(text, _SPELL_PAYOFF_PATTERNS):
        synergies.update({SynergyTag.SPELLSLINGER, SynergyTag.SPELL_PAYOFF})

    if analysis.is_artifact:
        synergies.add(SynergyTag.ARTIFACT)

    if _contains_any(text, _ARTIFACT_PAYOFF_PATTERNS):
        synergies.add(SynergyTag.ARTIFACT_PAYOFF)

    if "shrine" in type_line:
        synergies.update({SynergyTag.SHRINE, SynergyTag.SHRINES})

    if "elf" in type_line:
        synergies.add(SynergyTag.ELVES)

    if "sacrifice" in text:
        synergies.add(SynergyTag.ARISTOCRATS)
        if re.search(r"sacrifice (?:a|another) (?:creature|artifact|permanent)", text):
            synergies.add(SynergyTag.SACRIFICE_OUTLET)

    if _contains_any(text, _DEATH_TRIGGER_PATTERNS):
        synergies.update({SynergyTag.ARISTOCRATS, SynergyTag.DEATH_TRIGGER})

    if "landfall" in text:
        synergies.add(SynergyTag.LANDFALL)

    return frozenset(synergies)
