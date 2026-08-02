from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.goldfish_simulator import GoldfishSimulator


def entry(name, quantity, mana_value, *, type_line="Instant", roles=(), reasons=()):
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("", 0, ""),
        mana_value=mana_value,
        type_line=type_line,
        roles=roles,
        reasons=reasons,
    )


def test_goldfish_is_deterministic():
    deck = GeneratedDeck(
        mainboard=(entry("Bolt", 36, 1, roles=("burn",)),),
        lands=24,
    )
    simulator = GoldfishSimulator()
    assert simulator.simulate(deck, archetype="burn", samples=300) == simulator.simulate(
        deck, archetype="burn", samples=300
    )


def test_fast_burn_deck_deals_more_damage_than_slow_burn_deck():
    fast = GeneratedDeck(
        mainboard=(entry("Cheap Bolt", 40, 1, roles=("burn",)),),
        lands=20,
    )
    slow = GeneratedDeck(
        mainboard=(entry("Slow Bolt", 36, 4, roles=("burn",)),),
        lands=24,
    )
    simulator = GoldfishSimulator()
    fast_report = simulator.simulate(fast, archetype="burn", samples=500)
    slow_report = simulator.simulate(slow, archetype="burn", samples=500)
    assert fast_report.average_damage > slow_report.average_damage
    assert fast_report.average_spells_cast > slow_report.average_spells_cast


def test_mill_report_tracks_cards_milled_instead_of_damage():
    deck = GeneratedDeck(
        mainboard=(entry("Mind Grind", 36, 2, roles=("mill",)),),
        lands=24,
    )
    report = GoldfishSimulator().simulate(deck, archetype="mill", samples=400)
    assert report.average_cards_milled > 0
    assert report.average_damage == 0


def test_artifact_and_shrine_reports_track_board_progress():
    artifacts = GeneratedDeck(
        mainboard=(entry("Cheap Relic", 36, 1, type_line="Artifact"),),
        lands=24,
    )
    shrines = GeneratedDeck(
        mainboard=(
            entry("Sanctum", 36, 2, type_line="Legendary Enchantment — Shrine"),
        ),
        lands=24,
    )
    simulator = GoldfishSimulator()
    artifact_report = simulator.simulate(artifacts, archetype="artifacts", samples=300)
    shrine_report = simulator.simulate(shrines, archetype="shrines", samples=300)
    assert artifact_report.average_artifacts_in_play > 0
    assert shrine_report.average_shrines_in_play > 0


def test_token_payoffs_without_a_board_do_not_create_damage():
    deck = GeneratedDeck(
        mainboard=(entry("Empty Anthem", 36, 1, roles=("anthem",)),),
        lands=24,
    )
    report = GoldfishSimulator().simulate(deck, archetype="tokens", samples=300)
    assert report.average_damage == 0


def test_token_makers_attack_only_after_summoning_sickness():
    deck = GeneratedDeck(
        mainboard=(entry("Raise the Team", 40, 1, roles=("token_maker",)),),
        lands=20,
    )
    simulator = GoldfishSimulator()
    turn_one = simulator.simulate(deck, archetype="tokens", samples=300, turns=1)
    turn_two = simulator.simulate(deck, archetype="tokens", samples=300, turns=2)
    assert turn_one.average_damage == 0
    assert turn_two.average_damage > 0


def test_token_payoffs_improve_existing_combat_progress():
    plain = GeneratedDeck(
        mainboard=(entry("Raise the Team", 30, 1, roles=("token_maker",)),),
        lands=30,
    )
    supported = GeneratedDeck(
        mainboard=(
            entry("Raise the Team", 24, 1, roles=("token_maker",)),
            entry("Battle Anthem", 6, 2, roles=("anthem", "token_payoff")),
        ),
        lands=30,
    )
    simulator = GoldfishSimulator()
    plain_report = simulator.simulate(plain, archetype="tokens", samples=600)
    supported_report = simulator.simulate(supported, archetype="tokens", samples=600)
    assert supported_report.average_damage > plain_report.average_damage


def test_invalid_simulation_arguments_are_rejected():
    deck = GeneratedDeck(mainboard=(entry("Bolt", 36, 1),), lands=24)
    try:
        GoldfishSimulator().simulate(deck, archetype="burn", samples=0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
