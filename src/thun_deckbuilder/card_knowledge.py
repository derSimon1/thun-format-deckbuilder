from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from thun_deckbuilder.card_analyzer import CardAnalysis, analyze_card
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.card_synergies import detect_synergies


@dataclass(frozen=True)
class CardKnowledge:
    analysis: CardAnalysis
    roles: frozenset[str]
    synergies: frozenset[str]



def build_card_knowledge(card: dict[str, Any]) -> CardKnowledge:
    analysis = analyze_card(card)

    return CardKnowledge(
        analysis=analysis,
        roles=detect_roles(analysis),
        synergies=detect_synergies(analysis),
        
    )