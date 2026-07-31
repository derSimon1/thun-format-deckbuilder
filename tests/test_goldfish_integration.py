from thun_deckbuilder import deck_builder
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishReport
from thun_deckbuilder.prototype import format_deck


def entry(name="Cheap Burn", quantity=36, mana_value=1):
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("{R}", 0, "R"),
        mana_value=mana_value,
        type_line="Instant",
        reasons=("Burn",),
        roles=("burn",),
    )


class FakeKnowledgeBase:
    def __init__(self, database):
        self.database = database

    def load(self):
        pass


class FakeStrategy:
    def generate(self, *, knowledge_base, request):
        return GeneratedDeck(mainboard=(entry(),), lands=24, profile_name="Test Burn")


def test_generate_deck_attaches_goldfish_report(monkeypatch):
    monkeypatch.setattr(deck_builder, "KnowledgeBase", FakeKnowledgeBase)
    monkeypatch.setitem(deck_builder.STRATEGIES, "test-burn", FakeStrategy())

    deck = deck_builder.generate_deck(
        database=object(),
        archetype="test-burn",
        colors=("R",),
    )

    assert deck.goldfish_report is not None
    assert deck.goldfish_report.archetype == "test-burn"
    assert deck.goldfish_report.samples == 2000


def test_format_deck_shows_archetype_goldfish_metrics():
    report = GoldfishReport(
        archetype="mill",
        samples=2000,
        turns=5,
        mulligan_rate_pct=21,
        average_unused_mana=1.2,
        average_spells_cast=6.4,
        average_cards_milled=31.5,
        mill_out_by_final_turn_pct=8,
    )
    deck = GeneratedDeck(
        mainboard=(entry(name="Mill Spell", quantity=36),),
        lands=24,
        goldfish_report=report,
    )

    output = format_deck(deck, archetype="mill", colors=("U", "B"))

    assert "GOLDFISH SIMULATION" in output
    assert "Average cards milled: 31.5" in output
    assert "Mill-out by turn 5: 8%" in output
