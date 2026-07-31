from __future__ import annotations

from enum import StrEnum


class SynergyTag(StrEnum):
    """Normalized vocabulary for card-to-deck interactions."""

    TOKEN_MAKER = "token_maker"
    TOKEN_PAYOFF = "token_payoff"
    SPELL = "spell"
    SPELL_PAYOFF = "spell_payoff"
    ARTIFACT = "artifact"
    ARTIFACT_PAYOFF = "artifact_payoff"
    SACRIFICE_FODDER = "sacrifice_fodder"
    SACRIFICE_OUTLET = "sacrifice_outlet"
    DEATH_TRIGGER = "death_trigger"
    SHRINE = "shrine"

    # Compatibility tags retained from the original analyser.
    TOKENS = "tokens"
    SPELLSLINGER = "spellslinger"
    SHRINES = "shrines"
    ARISTOCRATS = "aristocrats"
    LANDFALL = "landfall"
    ELVES = "elves"


def normalize_synergy_tag(tag: SynergyTag | str) -> SynergyTag | str:
    if isinstance(tag, SynergyTag):
        return tag
    try:
        return SynergyTag(str(tag).strip().lower())
    except ValueError:
        return str(tag).strip().lower()
