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


def test_burn_additional_sacrifice_cost_requires_and_consumes_a_creature():
    costly = entry(
        "Costly Burn",
        18,
        1,
        roles=("burn", "cast_additional_creature_sacrifice_1"),
    )
    blocked = GeneratedDeck(mainboard=(costly,), lands=42)
    fodder = entry("Fodder", 18, 1, type_line="Creature", roles=("aggro_creature",))
    paid = GeneratedDeck(mainboard=(fodder, costly), lands=24)
    free = GeneratedDeck(
        mainboard=(fodder, entry("Free Burn", 18, 1, roles=("burn",))),
        lands=24,
    )

    simulator = GoldfishSimulator()
    blocked_report = simulator.simulate(blocked, archetype="burn", samples=400)
    paid_report = simulator.simulate(paid, archetype="burn", samples=400)
    free_report = simulator.simulate(free, archetype="burn", samples=400)

    assert blocked_report.average_spells_cast == 0
    assert paid_report.average_damage < free_report.average_damage


def test_exact_life_burn_is_not_cast_outside_its_window():
    deck = GeneratedDeck(
        mainboard=(
            entry(
                "Narrow Finisher",
                36,
                4,
                roles=(
                    "burn",
                    "burn_damage_10",
                    "cast_target_life_exact_10",
                ),
            ),
        ),
        lands=24,
    )

    report = GoldfishSimulator().simulate(deck, archetype="burn", samples=400)

    assert report.average_spells_cast == 0
    assert report.average_damage == 0


def test_mill_report_tracks_cards_milled_instead_of_damage():
    deck = GeneratedDeck(
        mainboard=(entry("Mind Grind", 36, 2, roles=("mill",)),),
        lands=24,
    )
    report = GoldfishSimulator().simulate(deck, archetype="mill", samples=400)
    assert report.average_cards_milled > 0
    assert report.average_damage == 0


def test_repeatable_mill_metadata_recurs_but_one_shot_permanent_does_not():
    one_shot = GeneratedDeck(
        mainboard=(
            entry(
                "One-Shot Wall",
                36,
                1,
                type_line="Creature",
                roles=("mill_source", "mill_immediate_3"),
            ),
        ),
        lands=24,
    )
    engine = GeneratedDeck(
        mainboard=(
            entry(
                "Repeatable Crab",
                36,
                1,
                type_line="Creature",
                roles=("mill_source", "mill_engine", "mill_repeatable_3"),
            ),
        ),
        lands=24,
    )

    simulator = GoldfishSimulator()
    one_shot_report = simulator.simulate(one_shot, archetype="mill", samples=400)
    engine_report = simulator.simulate(engine, archetype="mill", samples=400)

    assert engine_report.average_cards_milled > one_shot_report.average_cards_milled


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


def test_artifact_goldfish_counts_immediate_token_metadata():
    plain = GeneratedDeck(
        mainboard=(entry("Relic", 36, 1, type_line="Artifact"),),
        lands=24,
    )
    investigate = GeneratedDeck(
        mainboard=(
            entry(
                "Investigating Relic",
                36,
                1,
                type_line="Artifact",
                roles=("artifact_immediate_2",),
            ),
        ),
        lands=24,
    )

    simulator = GoldfishSimulator()
    plain_report = simulator.simulate(plain, archetype="artifacts", samples=300)
    investigate_report = simulator.simulate(
        investigate, archetype="artifacts", samples=300
    )

    assert investigate_report.average_artifacts_in_play > (
        plain_report.average_artifacts_in_play
    )


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


def test_temporary_anthem_does_not_stack_across_turns():
    makers = entry(
        "Raise the Team",
        24,
        1,
        roles=("token_maker", "token_production_immediate", "token_output_1"),
    )
    temporary = GeneratedDeck(
        mainboard=(
            makers,
            entry(
                "Charge",
                12,
                1,
                roles=("anthem",),
                reasons=("Temporärer Team-Bonus",),
            ),
        ),
        lands=24,
    )
    persistent = GeneratedDeck(
        mainboard=(
            makers,
            entry(
                "Glorious Anthem",
                12,
                1,
                roles=("anthem",),
                reasons=("Dauerhafter Team-Bonus",),
            ),
        ),
        lands=24,
    )

    simulator = GoldfishSimulator()
    temporary_report = simulator.simulate(
        temporary, archetype="tokens", samples=500
    )
    persistent_report = simulator.simulate(
        persistent, archetype="tokens", samples=500
    )

    assert persistent_report.average_damage > temporary_report.average_damage


def test_additional_sacrifice_cost_requires_and_consumes_a_body():
    costly_anthem = entry(
        "Costly Anthem",
        18,
        1,
        roles=("anthem", "cast_additional_creature_sacrifice_1"),
        reasons=("Dauerhafter Team-Bonus",),
    )
    no_bodies = GeneratedDeck(mainboard=(costly_anthem,), lands=42)
    makers = entry(
        "Maker",
        18,
        1,
        roles=("token_maker", "token_production_immediate", "token_output_1"),
    )
    costly = GeneratedDeck(mainboard=(makers, costly_anthem), lands=24)
    free = GeneratedDeck(
        mainboard=(
            makers,
            entry(
                "Free Anthem",
                18,
                1,
                roles=("anthem",),
                reasons=("Dauerhafter Team-Bonus",),
            ),
        ),
        lands=24,
    )

    simulator = GoldfishSimulator()
    blocked = simulator.simulate(no_bodies, archetype="tokens", samples=400)
    costly_report = simulator.simulate(costly, archetype="tokens", samples=400)
    free_report = simulator.simulate(free, archetype="tokens", samples=400)

    assert blocked.average_spells_cast == 0
    assert costly_report.average_token_board_size < free_report.average_token_board_size


def precise_roles(output: int, mode: str, *extra: str) -> tuple[str, ...]:
    return (
        "token_maker",
        "token_creature_maker",
        f"token_output_{output}",
        f"token_production_{mode}",
        *extra,
    )


def test_two_token_spell_outperforms_one_token_spell():
    one = GeneratedDeck(
        mainboard=(
            entry("One", 40, 1, roles=precise_roles(1, "immediate")),
        ),
        lands=20,
    )
    two = GeneratedDeck(
        mainboard=(
            entry("Two", 40, 1, roles=precise_roles(2, "immediate")),
        ),
        lands=20,
    )
    simulator = GoldfishSimulator()
    one_report = simulator.simulate(one, archetype="tokens", samples=400)
    two_report = simulator.simulate(two, archetype="tokens", samples=400)
    assert two_report.average_damage > one_report.average_damage
    assert two_report.average_token_board_size > one_report.average_token_board_size


def test_death_trigger_does_not_create_free_tokens_in_solitaire():
    deck = GeneratedDeck(
        mainboard=(
            entry("Death Spell", 40, 1, roles=precise_roles(1, "death")),
        ),
        lands=20,
    )
    report = GoldfishSimulator().simulate(deck, archetype="tokens", samples=300)
    assert report.average_damage == 0
    assert report.average_token_board_size == 0


def test_repeatable_engine_is_tracked_and_scales_over_a_longer_game():
    repeatable = GeneratedDeck(
        mainboard=(
            entry("Engine", 36, 2, roles=precise_roles(1, "repeatable")),
        ),
        lands=24,
    )
    simulator = GoldfishSimulator()
    turn_five = simulator.simulate(
        repeatable,
        archetype="tokens",
        samples=500,
        turns=5,
    )
    turn_eight = simulator.simulate(
        repeatable,
        archetype="tokens",
        samples=500,
        turns=8,
    )
    assert turn_five.average_token_engines_in_play > 0
    assert turn_eight.average_damage > turn_five.average_damage
    assert turn_eight.average_token_board_size > turn_five.average_token_board_size


def test_token_maker_creature_contributes_its_own_body():
    spell = GeneratedDeck(
        mainboard=(
            entry("Spell", 36, 2, roles=precise_roles(1, "immediate")),
        ),
        lands=24,
    )
    creature = GeneratedDeck(
        mainboard=(
            entry(
                "Creature Maker",
                36,
                2,
                type_line="Creature — Cleric",
                roles=precise_roles(1, "immediate"),
            ),
        ),
        lands=24,
    )
    simulator = GoldfishSimulator()
    spell_report = simulator.simulate(spell, archetype="tokens", samples=400)
    creature_report = simulator.simulate(creature, archetype="tokens", samples=400)
    assert creature_report.average_damage > spell_report.average_damage
    assert creature_report.average_token_board_size > spell_report.average_token_board_size


def test_conditional_output_is_not_assumed_in_clean_goldfish():
    deck = GeneratedDeck(
        mainboard=(
            entry("Conditional", 40, 1, roles=precise_roles(2, "conditional")),
        ),
        lands=20,
    )
    report = GoldfishSimulator().simulate(deck, archetype="tokens", samples=300)
    assert report.average_damage == 0


def test_invalid_simulation_arguments_are_rejected():
    deck = GeneratedDeck(mainboard=(entry("Bolt", 36, 1),), lands=24)
    try:
        GoldfishSimulator().simulate(deck, archetype="burn", samples=0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
