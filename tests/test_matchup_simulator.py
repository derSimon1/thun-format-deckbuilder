from dataclasses import replace

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishReport
from thun_deckbuilder.matchup_simulator import MatchupSimulator


def entry(name, quantity, mv, type_line, *, roles=(), reasons=()):
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("{1}", 1, ""),
        mana_value=mv,
        type_line=type_line,
        score=1.0,
        roles=tuple(roles),
        reasons=tuple(reasons),
    )


def report(archetype, *, damage=0.0, milled=0.0, artifacts=0.0, shrines=0.0):
    return GoldfishReport(
        archetype=archetype,
        samples=2000,
        turns=5,
        mulligan_rate_pct=20,
        average_unused_mana=1.0,
        average_spells_cast=6.0,
        average_damage=damage,
        average_cards_milled=milled,
        average_artifacts_in_play=artifacts,
        average_shrines_in_play=shrines,
    )


def deck(entries, goldfish):
    return GeneratedDeck(
        mainboard=tuple(entries),
        lands=24,
        goldfish_report=goldfish,
    )


def test_matchup_simulation_is_deterministic():
    burn = deck(
        (entry("Bolt", 3, 1, "Instant", roles=("burn",)),),
        report("burn", damage=16.0),
    )
    mill = deck(
        (entry("Mill", 3, 2, "Sorcery", roles=("mill",)),),
        report("mill", milled=30.0),
    )
    simulator = MatchupSimulator()
    first = simulator.simulate(burn, mill, archetype_a="burn", archetype_b="mill")
    second = simulator.simulate(burn, mill, archetype_a="burn", archetype_b="mill")
    assert first == second
    assert first.wins_a_pct + first.wins_b_pct + first.draws_pct in {99, 100, 101}


def test_interaction_improves_matchup_against_same_speed_deck():
    aggressive = deck(
        (entry("Fast Threat", 12, 1, "Creature"),),
        report("burn", damage=14.0),
    )
    interactive = deck(
        (
            entry("Fast Threat", 6, 1, "Creature"),
            entry("Removal", 6, 2, "Instant", roles=("removal",), reasons=("destroy target creature",)),
        ),
        report("burn", damage=14.0),
    )
    target = deck(
        (entry("Target Threat", 12, 1, "Creature"),),
        report("burn", damage=14.0),
    )
    simulator = MatchupSimulator()
    plain = simulator.simulate(aggressive, target, archetype_a="burn", archetype_b="burn")
    with_interaction = simulator.simulate(interactive, target, archetype_a="burn", archetype_b="burn")
    assert with_interaction.wins_a_pct > plain.wins_a_pct


def test_faster_goldfish_plan_is_favored_when_interaction_is_equal():
    fast = deck((entry("Bolt", 12, 1, "Instant", roles=("burn",)),), report("burn", damage=18.0))
    slow = deck((entry("Bolt", 12, 1, "Instant", roles=("burn",)),), report("burn", damage=11.0))
    result = MatchupSimulator().simulate(fast, slow, archetype_a="burn", archetype_b="burn")
    assert result.wins_a_pct > result.wins_b_pct
