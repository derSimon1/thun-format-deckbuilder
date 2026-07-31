from thun_deckbuilder.card_contribution import CardContribution
from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.deck_quality import DeckQualityAnalyzer
from thun_deckbuilder.deck_state import DeckState
from thun_deckbuilder.synergy_tag import SynergyTag


def contribution(name: str, tag: SynergyTag) -> CardContribution:
    return CardContribution(name, (), frozenset({tag}), 2)


def test_quality_report_exposes_active_token_synergy() -> None:
    state = DeckState().with_card(
        contribution("Maker", SynergyTag.TOKEN_MAKER), 4
    ).with_card(
        contribution("Payoff", SynergyTag.TOKEN_PAYOFF), 2
    )

    report = DeckQualityAnalyzer().analyze(state, DeckProfile(name="Tokens", lands=0, role_targets=()))

    token_quality = next(item for item in report.synergy_quality if item.label == "Tokens")
    assert token_quality.active
    assert token_quality.score > 50
    assert report.synergy_score == token_quality.score
