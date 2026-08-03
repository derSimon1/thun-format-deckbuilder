from thun_deckbuilder.benchmark import BenchmarkAnalyzer
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost


def entry(name, qty, mv, type_line, roles=(), reasons=()):
    return DeckEntry(
        name,
        qty,
        ManaCost("", 0, ""),
        mv,
        type_line,
        reasons=reasons,
        roles=roles,
    )


def test_artifact_benchmark_counts_artifact_density():
    deck = GeneratedDeck(
        mainboard=(
            entry("Cheap Artifact", 24, 1, "Artifact"),
            entry("Draw Engine", 5, 2, "Artifact Creature", ("card_draw",)),
            entry("Removal", 5, 2, "Instant", ("removal",)),
            entry("Payoff", 4, 3, "Creature", reasons=("Affinity-Payoff",)),
        ),
        lands=22,
    )

    report = BenchmarkAnalyzer().analyze(deck, "artifacts")

    assert report.signature_items[0].key == "artifact_cards"
    assert report.signature_items[0].actual == 29
    assert report.land_item.score == 100


def test_control_benchmark_counts_answers_and_finishers():
    deck = GeneratedDeck(
        mainboard=(
            entry("Counter", 9, 2, "Instant", reasons=("Counter target spell",)),
            entry("Removal", 6, 2, "Instant", ("removal",), ("Control removal",)),
            entry("Draw", 7, 3, "Instant", ("card_draw",), ("Card advantage engine",)),
            entry("Finisher", 3, 6, "Creature", ("finisher",), ("Control-Finisher",)),
            entry("Support", 10, 3, "Instant"),
        ),
        lands=25,
    )

    report = BenchmarkAnalyzer().analyze(deck, "control")

    assert report.signature_items[0].key == "control_answers"
    assert report.signature_items[0].actual == 15
    assert report.signature_items[1].actual == 3
    assert report.land_item.score == 100


def test_shrine_benchmark_counts_shrines_and_fixing():
    deck = GeneratedDeck(
        mainboard=(
            entry("Shrine", 18, 3, "Legendary Enchantment — Shrine"),
            entry("Fixing", 7, 2, "Artifact", ("ramp",), ("Fünffarben-Fixing",)),
            entry("Draw", 5, 3, "Enchantment", ("card_draw",)),
            entry("Removal", 6, 2, "Instant", ("removal",)),
        ),
        lands=24,
    )

    report = BenchmarkAnalyzer().analyze(deck, "shrines")

    assert report.signature_items[0].actual == 18
    assert report.signature_items[1].actual == 7


def test_mill_benchmark_counts_real_mill_sources():
    deck = GeneratedDeck(
        mainboard=(
            entry("Mill Spell", 18, 2, "Sorcery", reasons=("Millt 8 Karten",)),
            entry("Mill Engine", 6, 2, "Creature", reasons=("Wiederholbares Mill",)),
            entry("Draw", 6, 2, "Instant", ("card_draw",)),
            entry("Removal", 6, 2, "Instant", ("removal",)),
        ),
        lands=24,
    )

    report = BenchmarkAnalyzer().analyze(deck, "mill")

    signature = report.signature_items[0]
    assert signature.key == "mill_sources"
    assert signature.actual == 24
    assert signature.score == 100
    assert report.land_item.score == 100
