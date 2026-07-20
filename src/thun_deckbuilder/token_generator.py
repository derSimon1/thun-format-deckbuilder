from __future__ import annotations

from thun_deckbuilder.token_scoring import score_token_card
from thun_deckbuilder.deck_generator import GeneratedDeck
from thun_deckbuilder.deck_profile import DeckProfile, TOKENS_PROFILE
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase


def _is_mono_white(knowledge: CardKnowledge) -> bool:
    return set(knowledge.analysis.color_identity).issubset({"W"})


def _is_reasonable_token_card(knowledge: CardKnowledge) -> bool:
    analysis = knowledge.analysis
    if analysis.is_land or not _is_mono_white(knowledge) or analysis.mana_value > 6:
        return False
    if not knowledge.roles.intersection(
        {"token_maker", "token_payoff", "removal", "card_draw", "protection"}
    ):
        return False
    text = analysis.oracle_text.lower()
    excluded_phrases = (
        "token that's a copy of target opponent's",
        "token that's a copy of target creature you don't control",
        "create a token that's a copy of target artifact you don't control",
    )
    return not any(phrase in text for phrase in excluded_phrases)


def _score_for_composition(knowledge: CardKnowledge) -> tuple[float, tuple[str, ...]]:
    scored = score_token_card(knowledge.analysis)
    score = scored.score
    reasons = list(scored.reasons)
    role_bonuses = {
        "token_maker": (2.0, "Token-Erzeuger"),
        "token_payoff": (3.0, "Token-Payoff"),
        "removal": (2.0, "Interaktion"),
        "card_draw": (1.5, "Kartennachschub"),
        "protection": (1.5, "Schutz"),
    }
    for role, (bonus, reason) in role_bonuses.items():
        if role in knowledge.roles:
            score += bonus
            if reason not in reasons:
                reasons.append(reason)
    return score, tuple(reasons or ["Passt zum Token-Profil"])


def generate_token_deck(
    knowledge_base: KnowledgeBase,
    deck_size: int = 60,
    lands: int = 24,
    max_copies: int = 3,
) -> GeneratedDeck:
    from thun_deckbuilder.composition_engine import build_composition

    profile = TOKENS_PROFILE
    if lands != TOKENS_PROFILE.lands:
        profile = DeckProfile(
            name=TOKENS_PROFILE.name,
            lands=lands,
            role_targets=TOKENS_PROFILE.role_targets,
            curve_targets=TOKENS_PROFILE.curve_targets,
        )
    result = build_composition(
        knowledge_base.cards,
        profile=profile,
        deck_size=deck_size,
        max_copies=max_copies,
        eligible=_is_reasonable_token_card,
        score_card=_score_for_composition,
    )
    return GeneratedDeck(
        mainboard=result.entries,
        lands=profile.lands,
        profile_name=profile.name,
        requested_roles=result.requested_roles,
        fulfilled_roles=result.fulfilled_roles,
        warnings=result.warnings,
    )
