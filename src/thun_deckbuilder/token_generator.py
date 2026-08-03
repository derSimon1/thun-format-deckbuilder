from __future__ import annotations

from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase
from thun_deckbuilder.token_plan import TokenPlan, detect_token_plan
from thun_deckbuilder.token_profiles import token_profile_for_plan
from thun_deckbuilder.token_scoring import score_token_card


def _is_mono_white(knowledge: CardKnowledge) -> bool:
    return set(knowledge.analysis.color_identity).issubset({"W"})


def _is_reasonable_token_card(knowledge: CardKnowledge) -> bool:
    analysis = knowledge.analysis
    if analysis.is_land or not _is_mono_white(knowledge) or analysis.mana_value > 6:
        return False
    if not knowledge.roles.intersection(
        {
            "token_maker",
            "token_payoff",
            "sacrifice",
            "removal",
            "card_draw",
            "protection",
        }
    ):
        return False
    text = analysis.oracle_text.lower()
    excluded_phrases = (
        "token that's a copy of target opponent's",
        "token that's a copy of target creature you don't control",
        "create a token that's a copy of target artifact you don't control",
        "destroy all creatures",
        "exile all creatures",
    )
    if any(phrase in text for phrase in excluded_phrases):
        return False

    # Cards that merely mention or interact with tokens are not automatically
    # suitable. A token card must create material, reward a token board, provide
    # supported utility, or be a real sacrifice piece for an Aristocrats plan.
    creates_tokens = "create" in text and "token" in text
    token_payoff = "token_payoff" in knowledge.roles
    utility = bool(
        knowledge.roles.intersection({"removal", "card_draw", "protection"})
    )
    sacrifice_piece = "sacrifice" in knowledge.roles
    return creates_tokens or token_payoff or utility or sacrifice_piece


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
            "token_maker": (2.0, "Go Wide: Token-Erzeuger"),
            "token_payoff": (3.0, "Go Wide: Board-Payoff"),
            "card_draw": (1.5, "Kartennachschub"),
            "sacrifice": (-1.5, "Go Wide: planfremde Opferrolle"),
        },
        TokenPlan.VALUE: {
            "token_maker": (1.5, "Value Tokens: Material"),
            "token_payoff": (2.5, "Value Tokens: Payoff"),
            "card_draw": (3.0, "Value Tokens: Kartenvorteil"),
            "sacrifice": (-0.5, "Value Tokens: schwache Planbindung"),
        },
        TokenPlan.ARISTOCRATS: {
            "token_maker": (1.5, "Aristocrats: Opfermaterial"),
            "token_payoff": (2.5, "Aristocrats: Death-Payoff"),
            "card_draw": (1.5, "Kartennachschub"),
            "sacrifice": (4.0, "Aristocrats: Opfermöglichkeit"),
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
    return score, tuple(reasons or [f"Passt zum Token-Plan {plan.label}"])


def generate_token_deck(
    knowledge_base: KnowledgeBase,
    deck_size: int = 60,
    lands: int = 24,
    max_copies: int = 3,
) -> GeneratedDeck:
    from thun_deckbuilder.composition_engine import build_composition

    eligible_cards = tuple(
        card
        for card in knowledge_base.cards
        if _is_reasonable_token_card(card)
    )
    plan_report = detect_token_plan(eligible_cards)
    profile = token_profile_for_plan(plan_report.plan, lands=lands)
    result = build_composition(
        knowledge_base.cards,
        profile=profile,
        deck_size=deck_size,
        max_copies=max_copies,
        eligible=_is_reasonable_token_card,
        score_card=lambda card: _score_for_composition(card, plan_report.plan),
    )
    from thun_deckbuilder.mana_base_builder import ManaBaseBuilder
    from thun_deckbuilder.deck_quality import with_mana_quality

    mana = ManaBaseBuilder().build(
        result.entries,
        total_lands=profile.lands,
        deck_size=deck_size,
    )
    return GeneratedDeck(
        mainboard=result.entries,
        lands=profile.lands,
        profile_name=profile.name,
        requested_roles=result.requested_roles,
        fulfilled_roles=result.fulfilled_roles,
        warnings=result.warnings,
        selections=result.selections,
        quality_report=with_mana_quality(result.quality_report, mana.quality),
        mana_base=mana.distribution,
        mana_quality=mana.quality,
    )
