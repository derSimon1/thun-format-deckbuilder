import pytest

from thun_deckbuilder.card_analyzer import analyze_card, simulation_metadata_roles
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.deck_builder import generate_deck
from thun_deckbuilder.deck_request import DeckRequest
from thun_deckbuilder.knowledge_base import KnowledgeBase
from thun_deckbuilder.paths import DATABASE_FILE
from thun_deckbuilder.token_strategy import TokenStrategy


def build_knowledge_base(
    database: CardDatabase,
) -> KnowledgeBase:
    knowledge_base = KnowledgeBase(database)
    knowledge_base.load()
    return knowledge_base


def _has_role(entry, expected: str) -> bool:
    for role in entry.roles:
        if role == expected or getattr(role, "value", None) == expected:
            return True
        if str(role).removeprefix("CardRole.").lower() == expected:
            return True
    return False


def _role_copies(deck, role: str) -> int:
    return sum(
        entry.quantity
        for entry in deck.mainboard
        if _has_role(entry, role)
    )


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
    with CardDatabase(DATABASE_FILE) as database:
        assert database.database_path == DATABASE_FILE.resolve()
        deck = generate_deck(
            database=database,
            archetype="tokens",
            colors=["W"],
        )

    assert "Go Wide" in deck.profile_name
    assert _role_copies(deck, "token_creature_maker") >= 15
    assert _role_copies(deck, "token_immediate_maker") >= 9
    assert _role_copies(deck, "token_multi_maker") >= 6
    assert _role_copies(deck, "anthem") >= 3


def test_full_pool_preserves_additional_sacrifice_cost_metadata():
    """Metadata detection must not depend on forcing one card into the deck.

    The live card pool can legitimately change which legal token cards are selected.
    This regression protects the semantic fact we care about: Duty Beyond Death has
    an additional creature-sacrifice cast cost and must never be classified as a
    free sacrifice outlet merely because it contains the word "sacrifice".
    """

    with CardDatabase(DATABASE_FILE) as database:
        duty = database.get_card_by_name("Duty Beyond Death")

    assert duty is not None
    analysis = analyze_card(duty)
    assert "cast_additional_creature_sacrifice_1" in simulation_metadata_roles(analysis)


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
