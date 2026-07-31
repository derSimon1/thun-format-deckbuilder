from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.synergy_engine import SynergyEngine
from thun_deckbuilder.synergy_tag import SynergyTag


def contribution(name: str, *tags: SynergyTag | str) -> CardContribution:
    return CardContribution(
        card_name=name,
        roles=(),
        tags=frozenset(tags),
        mana_value=2,
    )


def total_bonus(candidate: CardContribution, state: DeckState) -> float:
    return sum(component.value for component in SynergyEngine().score(candidate, state))


def test_token_payoff_gets_bonus_from_existing_token_makers() -> None:
    state = DeckState().with_card(
        contribution("Token Spell", SynergyTag.TOKEN_MAKER),
        3,
    )

    bonus = total_bonus(
        contribution("Anthem", SynergyTag.TOKEN_PAYOFF),
        state,
    )

    assert bonus == 3.0


def test_token_payoff_has_no_bonus_in_empty_deck() -> None:
    bonus = total_bonus(
        contribution("Anthem", SynergyTag.TOKEN_PAYOFF),
        DeckState(),
    )

    assert bonus == 0


def test_shrine_bonus_grows_with_existing_shrines_and_is_capped() -> None:
    shrine = contribution("Shrine", SynergyTag.SHRINE)
    small_state = DeckState().with_card(shrine, 2)
    large_state = DeckState().with_card(shrine, 9)

    assert total_bonus(contribution("New Shrine", SynergyTag.SHRINE), small_state) == 4
    assert total_bonus(contribution("New Shrine", SynergyTag.SHRINE), large_state) == 12


def test_artifact_payoff_is_enabled_by_artifact_density() -> None:
    state = DeckState().with_card(
        contribution("Cheap Artifact", SynergyTag.ARTIFACT),
        6,
    )

    bonus = total_bonus(
        contribution("Artifact Payoff", SynergyTag.ARTIFACT_PAYOFF),
        state,
    )

    assert bonus == 3.0
