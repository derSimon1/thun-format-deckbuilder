from __future__ import annotations

from dataclasses import replace

from thun_deckbuilder.calibrated_strategies import CalibratedStrategy
from thun_deckbuilder.control_scoring import score_control_card
from thun_deckbuilder.control_signals import analyze_control
from thun_deckbuilder.deck_profile import CurveTarget, DeckProfile, RoleTarget
from thun_deckbuilder.knowledge_base import CardKnowledge
from thun_deckbuilder.sideboard_builder import (
    COUNTERSPELL,
    CREATURE_SWEEPER,
    GRAVEYARD_HATE,
    RULES,
    SideboardRule,
)


CONTROL_PROFILE = DeckProfile(
    name="Dimir Control",
    lands=25,
    role_targets=(
        RoleTarget("control_answer", minimum=12, target=14),
        RoleTarget("control_card_advantage", minimum=4, target=6),
        RoleTarget("control_finisher", minimum=3, target=3),
        RoleTarget("removal", minimum=0, target=9),
        RoleTarget("card_draw", minimum=0, target=7),
    ),
    curve_targets=(
        CurveTarget(1, 4),
        CurveTarget(2, 12),
        CurveTarget(3, 10),
        CurveTarget(4, 5),
        CurveTarget(99, 4),
    ),
)

CONTROL_SIDEBOARD_RULES = (
    GRAVEYARD_HATE,
    CREATURE_SWEEPER,
    COUNTERSPELL,
    SideboardRule(
        "anti-aggro removal",
        (
            "destroy target creature",
            "exile target creature",
            "target creature gets -",
            "return target creature",
        ),
        roles=("removal",),
        priority=4.5,
    ),
    SideboardRule(
        "hand disruption",
        (
            "target opponent reveals",
            "that player discards",
            "target opponent discards",
        ),
        priority=4,
    ),
)
RULES["control"] = CONTROL_SIDEBOARD_RULES


def _within_colors(knowledge: CardKnowledge, colors: tuple[str, ...]) -> bool:
    return set(knowledge.analysis.color_identity).issubset(set(colors))


def _control_eligible(knowledge: CardKnowledge, colors: tuple[str, ...]) -> bool:
    analysis = knowledge.analysis
    if analysis.is_land or not _within_colors(knowledge, colors):
        return False
    text = analysis.oracle_text.lower()
    functional = any(
        phrase in text
        for phrase in (
            "counter target",
            "destroy target",
            "exile target",
            "return target creature",
            "target creature gets -",
            "destroy all creatures",
            "exile all creatures",
            "all creatures get -",
            "each creature gets -",
            "return all creatures",
            "draw a card",
            "draw two",
            "draw three",
            "surveil",
            "scry",
            "look at the top",
        )
    )
    control_roles = knowledge.roles.intersection(
        {"control_answer", "control_card_advantage", "control_finisher"}
    )
    return functional or bool(control_roles)


class ControlStrategy(CalibratedStrategy):
    def __init__(self) -> None:
        super().__init__(
            profile=CONTROL_PROFILE,
            scorer=score_control_card,
            eligibility=_control_eligible,
            required_colors=frozenset({"U", "B"}),
        )

    def _knowledge_cards(self, knowledge_base) -> tuple[CardKnowledge, ...]:
        refined: list[CardKnowledge] = []
        for knowledge in knowledge_base.cards:
            signals = analyze_control(knowledge.analysis)
            roles = set(knowledge.roles)
            if signals.reliable_answer:
                roles.add("control_answer")
            if signals.card_advantage:
                roles.add("control_card_advantage")
            if signals.finisher:
                roles.add("control_finisher")
            if signals.sweeper:
                roles.add("control_sweeper")
            refined.append(replace(knowledge, roles=frozenset(roles)))
        return tuple(refined)
