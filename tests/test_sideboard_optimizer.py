from thun_deckbuilder.calibration_advisor import recommend_calibrations
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishReport
from thun_deckbuilder.sideboard_optimizer import optimize_sideboard_plan
from thun_deckbuilder.tournament_simulator import BestOfThreeSimulator


def entry(name, quantity, *, score=1.0, roles=(), reasons=(), type_line="Instant"):
    return DeckEntry(name, quantity, ManaCost("{1}", 1, ""), 1, type_line, score, tuple(reasons), tuple(roles))


def report(archetype, damage):
    return GoldfishReport(archetype, 2000, 5, 20, 1.0, 6.0, average_damage=damage)


def deck(main, side, archetype, damage):
    return GeneratedDeck(mainboard=tuple(main), sideboard=tuple(side), lands=24, goldfish_report=report(archetype, damage))


def test_optimizer_preserves_size_and_only_accepts_positive_swaps():
    player = deck(
        (entry("Weak", 6, score=0.1), entry("Threat", 30, score=3, type_line="Creature")),
        (entry("Removal", 3, score=2, roles=("removal",), reasons=("destroy target creature",)),),
        "burn", 14,
    )
    opponent = deck((entry("Creature", 36, score=3, type_line="Creature"),), (), "tokens", 14)
    result = optimize_sideboard_plan(player, opponent, archetype="burn", opponent_archetype="tokens", samples=200)
    assert sum(item.quantity for item in result.deck.mainboard) == 36
    assert all(item.win_rate_delta > 0 for item in result.impacts)
    assert result.postboard_win_pct >= result.baseline_win_pct


def test_bo3_reports_impacts_and_advisor_uses_them():
    burn = deck(
        (entry("Weak", 6, score=0.1), entry("Bolt", 30, score=3, roles=("burn",))),
        (entry("Sweeper", 3, score=2, roles=("removal",), reasons=("damage to each creature",)),),
        "burn", 15,
    )
    tokens = deck((entry("Token", 36, score=3, type_line="Creature"),), (), "tokens", 13)
    report_ = BestOfThreeSimulator().simulate(burn, tokens, archetype_a="burn", archetype_b="tokens", samples=200)
    assert report_.match_wins_a_pct + report_.match_wins_b_pct == 100
    advice = recommend_calibrations(report_)
    assert advice
    assert any(item.archetype == "burn" for item in advice)
