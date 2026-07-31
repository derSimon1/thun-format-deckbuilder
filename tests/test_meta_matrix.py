from thun_deckbuilder.cli import ARCHETYPES, build_parser
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishReport
from thun_deckbuilder.meta_matrix import MetaMatrixAnalyzer, format_meta_matrix


def entry(name, quantity, *, roles=()):
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("{1}", 1, ""),
        mana_value=1,
        type_line="Creature",
        score=1.0,
        roles=tuple(roles),
    )


def deck(archetype, progress):
    report = GoldfishReport(
        archetype=archetype,
        samples=2000,
        turns=5,
        mulligan_rate_pct=20,
        average_unused_mana=1.0,
        average_spells_cast=6.0,
        average_damage=progress if archetype in {"burn", "tokens"} else 0.0,
        average_cards_milled=progress if archetype == "mill" else 0.0,
        average_artifacts_in_play=progress if archetype == "artifacts" else 0.0,
        average_shrines_in_play=progress if archetype == "shrines" else 0.0,
    )
    return GeneratedDeck(
        mainboard=(entry(f"{archetype} threat", 12),),
        lands=24,
        goldfish_report=report,
    )


def test_cli_parses_matchup_and_meta_commands():
    parser = build_parser()
    matchup = parser.parse_args(("matchup", "burn", "mill", "--samples", "500"))
    assert matchup.archetype_a == "burn"
    assert matchup.archetype_b == "mill"
    assert matchup.samples == 500

    meta = parser.parse_args(("meta", "burn", "mill", "artifacts"))
    assert meta.archetypes == ["burn", "mill", "artifacts"]
    assert set(ARCHETYPES).issuperset(meta.archetypes)


def test_meta_matrix_runs_every_pair_and_sorts_standings():
    decks = {
        "burn": deck("burn", 19.0),
        "mill": deck("mill", 25.0),
        "artifacts": deck("artifacts", 2.0),
    }
    report = MetaMatrixAnalyzer().analyze(decks, samples_per_matchup=500)

    assert len(report.matchups) == 3
    assert len(report.standings) == 3
    assert report.standings[0].wins_pct >= report.standings[-1].wins_pct
    assert all(standing.matches == 2 for standing in report.standings)


def test_meta_matrix_marks_clear_outliers_and_formats_warnings():
    decks = {
        "burn": deck("burn", 20.0),
        "mill": deck("mill", 8.0),
        "artifacts": deck("artifacts", 1.0),
    }
    report = MetaMatrixAnalyzer().analyze(decks, samples_per_matchup=1000)
    classifications = {item.archetype: item.classification for item in report.standings}

    assert "OVERPERFORMER" in classifications.values()
    assert "UNDERPERFORMER" in classifications.values()
    rendered = format_meta_matrix(report)
    assert "THUN META MATRIX" in rendered
    assert "META WARNINGS" in rendered
