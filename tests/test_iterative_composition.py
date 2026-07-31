from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.composition_engine import build_composition
from thun_deckbuilder.deck_profile import CurveTarget, DeckProfile, RoleTarget
from thun_deckbuilder.knowledge_base import CardKnowledge


def make_card(name: str, roles: set[str], mana_value: int = 2) -> CardKnowledge:
    card = {
        "name": name,
        "mana_cost": "{1}{W}",
        "mana_value": mana_value,
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": "Instant",
        "oracle_text": "Test text.",
    }
    return CardKnowledge(card, analyze_card(card), frozenset(roles), frozenset())


def test_iterative_selection_changes_score_as_need_is_filled() -> None:
    profile = DeckProfile(
        name="Small Tokens",
        lands=0,
        role_targets=(RoleTarget("token_maker", minimum=1, target=1),),
        curve_targets=(CurveTarget(2, 2),),
    )
    cards = (
        make_card("Token Spell", {"token_maker"}),
        make_card("Quality Spell", {"protection"}),
    )

    result = build_composition(
        cards,
        profile=profile,
        deck_size=2,
        max_copies=1,
        eligible=lambda card: True,
        score_card=lambda card: (20.0 if card.analysis.name == "Quality Spell" else 10.0, ("base",)),
    )

    assert result.selections[0].card_name == "Token Spell"
    assert result.selections[1].card_name == "Quality Spell"
    assert result.selections[0].primary_need == "token_maker"
    assert dict(result.fulfilled_roles)["token_maker"] == 1


def test_selection_trace_records_every_copy() -> None:
    profile = DeckProfile(
        name="Tiny",
        lands=0,
        role_targets=(RoleTarget("burn", minimum=0, target=0),),
    )
    card = make_card("Burn", {"burn"}, mana_value=1)
    result = build_composition(
        (card,),
        profile=profile,
        deck_size=3,
        max_copies=3,
        eligible=lambda item: True,
        score_card=lambda item: (5.0, ("base",)),
    )

    assert len(result.selections) == 3
    assert [trace.quantity_after_selection for trace in result.selections] == [1, 2, 3]
