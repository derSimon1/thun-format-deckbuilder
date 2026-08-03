import pytest

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase
from thun_deckbuilder.token_strategy import TokenStrategy


def build_knowledge_base(
    database: CardDatabase,
) -> KnowledgeBase:
    knowledge_base = KnowledgeBase(database)
    knowledge_base.load()
    return knowledge_base


def test_token_strategy_generates_60_card_deck():
    request = DeckRequest(
        archetype="tokens",
        colors=("W",),
    )

    with CardDatabase() as database:
        knowledge_base = build_knowledge_base(database)
        deck = TokenStrategy().generate(
            knowledge_base=knowledge_base,
            request=request,
        )

    spell_count = sum(entry.quantity for entry in deck.mainboard)
    assert spell_count == 36
    assert deck.lands == 24
    assert spell_count + deck.lands == 60


def test_full_pool_selects_and_fulfils_reliable_go_wide_package():
    with CardDatabase() as database:
        deck = generate_deck(
            database=database,
            archetype="tokens",
            colors=["W"],
        )

    role_counts: dict[str, int] = {}
    for entry in deck.mainboard:
        for role in set(entry.roles):
            normalized_role = getattr(role, "value", str(role))
            role_counts[normalized_role] = (
                role_counts.get(normalized_role, 0) + entry.quantity
            )

    assert "Go Wide" in deck.profile_name
    assert role_counts["token_creature_maker"] >= 15
    assert role_counts["token_immediate_maker"] >= 9
    assert role_counts["token_multi_maker"] >= 6
    assert role_counts["anthem"] >= 3


def test_generic_builder_generates_token_deck():
    with CardDatabase() as database:
        deck = generate_deck(
            database=database,
            archetype="tokens",
            colors=["W"],
        )

    assert sum(entry.quantity for entry in deck.mainboard) == 36


def test_token_strategy_respects_copy_limit():
    with CardDatabase() as database:
        deck = generate_deck(
            database=database,
            archetype="tokens",
            colors=["W"],
            max_copies=3,
        )

    assert all(entry.quantity <= 3 for entry in deck.mainboard)


def test_token_strategy_rejects_wrong_color():
    request = DeckRequest(
        archetype="tokens",
        colors=("R",),
    )

    with CardDatabase() as database:
        knowledge_base = build_knowledge_base(database)

        with pytest.raises(
            ValueError,
            match="nur Mono-Weiss",
        ):
            TokenStrategy().generate(
                knowledge_base=knowledge_base,
                request=request,
            )
