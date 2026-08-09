from thun_deckbuilder.deck_generator import DeckEntry, ManaCost
from thun_deckbuilder.mana_base_builder import ManaBaseBuilder


def entry(name: str, quantity: int, mana_cost: str, mana_value: float) -> DeckEntry:
    return DeckEntry(name, quantity, ManaCost(mana_cost, 0, ""), mana_value, "Instant")


def test_builder_recommends_fewer_lands_for_low_curve_deck():
    entries = (entry("Cheap", 36, "{R}", 1.0),)
    result = ManaBaseBuilder().build(entries, deck_size=60)
    assert result.distribution.total_lands == 22
    assert result.distribution.sources_for("R") == 22
    assert result.quality.score == 100


def test_builder_respects_explicit_land_count():
    entries = (entry("White", 20, "{W}", 2.0), entry("Blue", 16, "{2}{U}", 3.0))
    result = ManaBaseBuilder().build(entries, total_lands=24, deck_size=60)
    assert result.distribution.total_lands == 24
    assert sum(land.quantity for land in result.distribution.lands) == 24
    assert result.distribution.sources_for("W") > result.distribution.sources_for("U")


def test_builder_guarantees_real_colorless_sources_for_colorless_costs():
    entries = (
        entry("White", 30, "{W}", 1.0),
        entry("True Colorless", 1, "{2}{C}{C}", 4.0),
    )

    result = ManaBaseBuilder().build(entries, total_lands=24, deck_size=60)

    assert result.distribution.sources_for("C") >= 2
    assert result.quality.sufficient
