import pytest

from thun_deckbuilder.calibrated_strategies import (
    ArtifactStrategy,
    MillStrategy,
    ShrineStrategy,
)
from thun_deckbuilder.control_strategy import ControlStrategy
from thun_deckbuilder.deck_request import DeckRequest


def _request(archetype: str, colors: tuple[str, ...]) -> DeckRequest:
    return DeckRequest(
        archetype=archetype,
        colors=colors,
        deck_size=60,
        max_copies=3,
    )


def test_artifact_strategy_accepts_configurable_colors():
    strategy = ArtifactStrategy()
    strategy._validate_request(_request("artifacts", ("U", "R")))


def test_shrine_strategy_requires_all_five_colors():
    strategy = ShrineStrategy()
    with pytest.raises(ValueError):
        strategy._validate_request(_request("shrines", ("W", "U", "B", "R")))

    strategy._validate_request(_request("shrines", ("W", "U", "B", "R", "G")))


def test_mill_strategy_requires_dimir():
    strategy = MillStrategy()
    with pytest.raises(ValueError):
        strategy._validate_request(_request("mill", ("U",)))

    strategy._validate_request(_request("mill", ("U", "B")))


def test_control_strategy_requires_dimir():
    strategy = ControlStrategy()
    with pytest.raises(ValueError):
        strategy._validate_request(_request("control", ("U",)))

    strategy._validate_request(_request("control", ("U", "B")))


def test_calibrated_strategies_reject_non_sixty_card_decks():
    request = DeckRequest(
        archetype="mill",
        colors=("U", "B"),
        deck_size=80,
        max_copies=3,
    )
    with pytest.raises(ValueError):
        MillStrategy()._validate_request(request)
