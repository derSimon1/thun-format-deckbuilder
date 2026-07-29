from thun_deckbuilder.composition_engine import CompositionEngine, build_composition
from thun_deckbuilder.deck_profile import DeckProfile, RoleTarget


def test_composition_engine_facade_delegates_to_existing_algorithm(monkeypatch) -> None:
    expected = object()
    captured = {}

    def fake_build(cards, **kwargs):
        captured["cards"] = cards
        captured.update(kwargs)
        return expected

    monkeypatch.setattr("thun_deckbuilder.composition_engine.build_composition", fake_build)

    cards = [object()]
    profile = DeckProfile(
        name="Test",
        lands=24,
        role_targets=(RoleTarget("burn", minimum=0, target=0),),
    )
    eligible = lambda card: True
    score_card = lambda card: (0.0, ())

    result = CompositionEngine().build(
        cards,
        profile=profile,
        deck_size=60,
        max_copies=3,
        eligible=eligible,
        score_card=score_card,
    )

    assert result is expected
    assert captured["cards"] is cards
    assert captured["profile"] is profile
    assert captured["deck_size"] == 60
    assert captured["max_copies"] == 3
    assert captured["eligible"] is eligible
    assert captured["score_card"] is score_card
