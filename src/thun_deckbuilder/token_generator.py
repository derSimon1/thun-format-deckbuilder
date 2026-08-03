from __future__ import annotations

from dataclasses import replace

from thun_deckbuilder.card_role import CardRole
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.engine_density import evaluate_token_engine_density
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.strategy_commitment import evaluate_token_commitment
from thun_deckbuilder.token_packages import analyze_token_package
from thun_deckbuilder.token_plan import TokenPlan, detect_token_plan
from thun_deckbuilder.token_production import (
    analyze_token_production,
    token_production_roles,
)
from thun_deckbuilder.token_profiles import (
    capacity_checked_token_profile,
    token_profile_for_plan,
)
from thun_deckbuilder.token_scoring import score_token_card


def _is_mono_white(knowledge: CardKnowledge) -> bool:
    return set(knowledge.analysis.color_identity).issubset({"W"})


def _with_precise_token_roles(knowledge: CardKnowledge) -> CardKnowledge:
    """Return a Token-specific view with precise package and production roles."""

    signals = analyze_token_package(knowledge.analysis)
    production = analyze_token_production(knowledge.analysis)
    roles = {str(role) for role in knowledge.roles}

    if not signals.creates_creature_tokens:
        roles.discard(CardRole.TOKEN_MAKER.value)
    if not signals.sacrifice_outlet:
        roles.discard(CardRole.SACRIFICE.value)
    if not any(
        (
            signals.anthem,
            signals.evasion_payoff,
            signals.token_value_payoff,
            signals.death_payoff,
            signals.drain_payoff,
        )
    ):
        roles.discard(CardRole.TOKEN_PAYOFF.value)

    roles.discard(CardRole.TOKEN_IMMEDIATE_MAKER.value)
    roles.discard(CardRole.TOKEN_MULTI_MAKER.value)
    roles.discard(CardRole.TOKEN_REPEATABLE_MAKER.value)

    if signals.creates_creature_tokens:
        roles.update(
            {
                CardRole.TOKEN_MAKER.value,
                CardRole.TOKEN_CREATURE_MAKER.value,
                *token_production_roles(knowledge.analysis),
            }
        )
    if production.mode == "immediate":
        roles.add(CardRole.TOKEN_IMMEDIATE_MAKER.value)
        if production.minimum_output >= 2:
            roles.add(CardRole.TOKEN_MULTI_MAKER.value)
    if production.mode == "repeatable":
        roles.add(CardRole.TOKEN_REPEATABLE_MAKER.value)
    if signals.sacrifice_outlet:
        roles.update(
            {
                CardRole.SACRIFICE.value,
                CardRole.SACRIFICE_OUTLET.value,
            }
        )
    if signals.death_payoff:
        roles.update(
            {
                CardRole.DEATH_PAYOFF.value,
                CardRole.TOKEN_PAYOFF.value,
            }
        )
    if signals.drain_payoff:
        roles.update(
            {
                CardRole.DRAIN_PAYOFF.value,
                CardRole.TOKEN_PAYOFF.value,
            }
        )
    if signals.token_value_payoff:
        roles.update(
            {
                CardRole.TOKEN_VALUE_PAYOFF.value,
                CardRole.TOKEN_PAYOFF.value,
            }
        )
    if signals.anthem or signals.evasion_payoff:
        roles.add(CardRole.TOKEN_PAYOFF.value)

    return replace(knowledge, roles=frozenset(roles))


def _base_token_candidate(knowledge: CardKnowledge) -> bool:
    analysis = knowledge.analysis
    if analysis.is_land or not _is_mono_white(knowledge) or analysis.mana_value > 6:
        return False
    text = analysis.oracle_text.lower()
    excluded_phrases = (
        "token that's a copy of target opponent's",
        "token that's a copy of target creature you don't control",
        "create a token that's a copy of target artifact you don't control",
        "destroy all creatures",
        "exile all creatures",
    )
    return not any(phrase in text for phrase in excluded_phrases)


def _is_token_plan_card(knowledge: CardKnowledge) -> bool:
    if not _base_token_candidate(knowledge):
        return False
    signals = analyze_token_package(knowledge.analysis)
    plan_piece = any(
        (
            signals.creates_creature_tokens,
            signals.anthem,
            signals.evasion_payoff,
            signals.token_value_payoff,
            signals.sacrifice_outlet,
            signals.death_payoff,
            signals.drain_payoff,
        )
    )
    utility = bool(
        knowledge.roles.intersection({"removal", "card_draw", "protection"})
    ) and not signals.creates_noncreature_tokens
    return plan_piece or utility


def _is_sparse_pool_filler(knowledge: CardKnowledge) -> bool:
    analysis = knowledge.analysis
    return (
        _base_token_candidate(knowledge)
        and analysis.is_creature
        and analysis.mana_value <= 3
    )


def _is_reasonable_token_card(knowledge: CardKnowledge) -> bool:
    return _is_token_plan_card(knowledge) or _is_sparse_pool_filler(knowledge)


def _copy_capacity(cards: tuple[CardKnowledge, ...], max_copies: int) -> int:
    return len({card.analysis.name.casefold() for card in cards}) * max_copies


def _composition_candidates(
    token_cards: tuple[CardKnowledge, ...],
    plan_cards: tuple[CardKnowledge, ...],
    *,
    spell_slots: int,
    max_copies: int,
) -> tuple[CardKnowledge, ...]:
    if _copy_capacity(plan_cards, max_copies) >= spell_slots:
        return plan_cards
    fillers = tuple(
        card
        for card in token_cards
        if card not in plan_cards and _is_sparse_pool_filler(card)
    )
    return (*plan_cards, *fillers)


def _score_for_composition(
    knowledge: CardKnowledge,
    plan: TokenPlan = TokenPlan.GO_WIDE,
) -> tuple[float, tuple[str, ...]]:
    scored = score_token_card(knowledge.analysis, plan=plan)
    score = scored.score
    reasons = list(scored.reasons)

    common_bonuses = {
        "removal": (2.0, "Interaktion"),
        "protection": (1.5, "Schutz"),
    }
    plan_bonuses = {
        TokenPlan.GO_WIDE: {
            "token_creature_maker": (1.0, "Go Wide: Kreatur-Token-Erzeuger"),
            "token_immediate_maker": (2.5, "Go Wide: garantierte Sofortproduktion"),
            "token_multi_maker": (3.5, "Go Wide: mehrere garantierte Körper"),
            "anthem": (3.0, "Go Wide: Board-Payoff"),
            "token_repeatable_maker": (0.5, "Go Wide: sekundäre Engine"),
            "card_draw": (0.5, "Kartennachschub"),
            "sacrifice_outlet": (-1.5, "Go Wide: planfremdes Opferpaket"),
        },
        TokenPlan.VALUE: {
            "token_creature_maker": (1.5, "Value Tokens: Kreaturmaterial"),
            "token_repeatable_maker": (3.5, "Value Tokens: automatische Engine"),
            "token_value_payoff": (3.0, "Value Tokens: direkter Payoff"),
            "card_draw": (2.5, "Value Tokens: Kartenvorteil"),
            "sacrifice_outlet": (-1.0, "Value Tokens: planfremdes Opferpaket"),
        },
        TokenPlan.ARISTOCRATS: {
            "token_creature_maker": (1.5, "Aristocrats: Kreatur-Opfermaterial"),
            "sacrifice_outlet": (4.0, "Aristocrats: wiederholbares Outlet"),
            "death_payoff": (4.0, "Aristocrats: Death-Payoff"),
            "drain_payoff": (2.0, "Aristocrats: Drain-Finisher"),
            "card_draw": (1.5, "Kartennachschub"),
            "anthem": (-1.5, "Aristocrats: planfremder Anthem-Payoff"),
        },
    }
    for role, (bonus, reason) in {
        **common_bonuses,
        **plan_bonuses[plan],
    }.items():
        if role in knowledge.roles:
            score += bonus
            if reason not in reasons:
                reasons.append(reason)
    if not reasons and knowledge.analysis.is_creature:
        score -= 2.0
        reasons.append("Neutraler Sparse-Pool-Füller")
    return score, tuple(reasons or [f"Passt zum Token-Plan {plan.label}"])


def generate_token_deck(
    knowledge_base: KnowledgeBase,
    deck_size: int = 60,
    lands: int = 24,
    max_copies: int = 3,
) -> GeneratedDeck:
    from thun_deckbuilder.composition_engine import build_composition

    token_cards = tuple(_with_precise_token_roles(card) for card in knowledge_base.cards)
    plan_cards = tuple(card for card in token_cards if _is_token_plan_card(card))
    plan_report = detect_token_plan(plan_cards, max_copies=max_copies)
    configured_profile = token_profile_for_plan(plan_report.plan, lands=lands)
    composition_cards = _composition_candidates(
        token_cards,
        plan_cards,
        spell_slots=configured_profile.spell_slots(deck_size),
        max_copies=max_copies,
    )
    profile, capacity_warnings = capacity_checked_token_profile(
        configured_profile,
        composition_cards,
        max_copies=max_copies,
        deck_size=deck_size,
    )
    allowed_names = {card.analysis.name for card in composition_cards}
    result = build_composition(
        composition_cards,
        profile=profile,
        deck_size=deck_size,
        max_copies=max_copies,
        eligible=lambda card: card.analysis.name in allowed_names,
        score_card=lambda card: _score_for_composition(card, plan_report.plan),
    )
    commitment = evaluate_token_commitment(result.entries, plan_report.plan)
    engine_density = evaluate_token_engine_density(
        result.entries,
        composition_cards,
        plan_report.plan,
    )

    from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
    from thun_deckbuilder.deck_quality import with_mana_quality

    mana = ManaBaseBuilder().build(
        result.entries,
        total_lands=profile.lands,
        deck_size=deck_size,
    )
    plan_summary = (
        f"Token Plan {plan_report.plan.label}: confidence={plan_report.confidence:.0%}; "
        + ", ".join(
            f"{plan.value}={score:.1f}" for plan, score in plan_report.scores
        )
    )
    commitment_summary = (
        f"Strategy Commitment {plan_report.plan.label}: "
        f"{commitment.commitment_score:.0%}; "
        f"committed={commitment.committed_cards}, "
        f"conflicting={commitment.conflicting_cards}, "
        f"neutral={commitment.neutral_cards}"
    )
    engine_summary = (
        f"Engine Density {plan_report.plan.label}: "
        f"{engine_density.engine_density:.0%}; "
        f"copies={engine_density.engine_copies}/{engine_density.spell_copies}, "
        f"distinct={engine_density.distinct_engines}"
    )
    return GeneratedDeck(
        mainboard=result.entries,
        lands=profile.lands,
        profile_name=profile.name,
        requested_roles=result.requested_roles,
        fulfilled_roles=result.fulfilled_roles,
        warnings=(
            plan_summary,
            commitment_summary,
            engine_summary,
            *capacity_warnings,
            *result.warnings,
            *commitment.warnings,
            *engine_density.warnings,
        ),
        selections=result.selections,
        quality_report=with_mana_quality(result.quality_report, mana.quality),
        mana_base=mana.distribution,
        mana_quality=mana.quality,
    )
