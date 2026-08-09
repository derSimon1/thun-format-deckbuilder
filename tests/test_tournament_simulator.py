from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishReport
from thun_deckbuilder.tournament_simulator import BestOfThreeSimulator, board_for_matchup


def entry(name, quantity, *, score=1.0, roles=(), reasons=(), type_line="Instant"):
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("{1}", 1, ""),
        mana_value=1,
        type_line=type_line,
        score=score,
        roles=tuple(roles),
        reasons=tuple(reasons),
    )


def goldfish(archetype, damage=0.0, milled=0.0):
    return GoldfishReport(
        archetype=archetype,
        samples=2000,
        turns=5,
        mulligan_rate_pct=20,
        average_unused_mana=1.0,
        average_spells_cast=6.0,
        average_damage=damage,
        average_cards_milled=milled,
    )


def deck(main, side, report):
    return GeneratedDeck(mainboard=tuple(main), sideboard=tuple(side), lands=24, goldfish_report=report)


def test_board_for_matchup_adds_relevant_cards_and_preserves_size():
    original = deck(
        (entry("Slow Filler", 6, score=0.1), entry("Threat", 30, score=3, type_line="Creature")),
        (entry("Cheap Removal", 3, score=1, roles=("removal",), reasons=("destroy target creature",)),),
        goldfish("burn", damage=14),
    )
    boarded, plan = board_for_matchup(original, opponent_archetype="tokens")
    assert sum(item.quantity for item in boarded.mainboard) == 36
    assert plan.cards_in == (("Cheap Removal", 3),)
    assert any(name == "Slow Filler" for name, _ in plan.cards_out)


def test_bo3_simulation_is_deterministic_and_reports_plans():
    burn = deck(
        (entry("Bolt", 36, score=3, roles=("burn",)),),
        (entry("Sweeper", 3, roles=("removal",), reasons=("damage to each creature",)),),
        goldfish("burn", damage=16),
    )
    tokens = deck(
        (entry("Token Maker", 36, score=3, type_line="Creature"),),
        (entry("Lifegain", 3, reasons=("life gain",)),),
        goldfish("tokens", damage=14),
    )
    simulator = BestOfThreeSimulator()
    first = simulator.simulate(burn, tokens, archetype_a="burn", archetype_b="tokens", samples=500)
    second = simulator.simulate(burn, tokens, archetype_a="burn", archetype_b="tokens", samples=500)
    assert first == second
    assert first.match_wins_a_pct + first.match_wins_b_pct == 100
    assert first.plan_a.cards_in
