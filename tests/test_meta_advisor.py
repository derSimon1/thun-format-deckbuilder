from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishReport
from thun_deckbuilder.meta_advisor import BestOfThreeMetaAnalyzer, format_meta_advice


def entry(name, quantity, *, roles=(), type_line="Instant"):
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("{1}", 1, ""),
        mana_value=1,
        type_line=type_line,
        score=2.0,
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
        mainboard=(entry(f"{archetype} card", 36, type_line="Creature"),),
        sideboard=(),
        lands=24,
        goldfish_report=report,
    )


def test_meta_advisor_covers_every_pair_and_sorts_standings():
    decks = {
        "burn": deck("burn", 18),
        "mill": deck("mill", 30),
        "artifacts": deck("artifacts", 3),
    }
    report = BestOfThreeMetaAnalyzer().analyze(decks, samples_per_matchup=300)
    assert len(report.matchups) == 3
    assert len(report.standings) == 3
    win_rates = [item.estimated_match_win_pct for item in report.standings]
    assert win_rates == sorted(win_rates, reverse=True)


def test_meta_advisor_emits_actionable_recommendation_for_bad_matchup():
    decks = {
        "shrines": deck("shrines", 0.5),
        "burn": deck("burn", 19),
    }
    report = BestOfThreeMetaAnalyzer().analyze(decks, samples_per_matchup=300)
    shrine = next(item for item in report.standings if item.archetype == "shrines")
    assert shrine.worst_matchup == "burn"
    assert any("Removal" in text or "Stabilisierung" in text for text in shrine.recommendations)
    formatted = format_meta_advice(report)
    assert "THUN BEST-OF-THREE META ADVISOR" in formatted
    assert "Worst Matchup" in formatted
