from thun_deckbuilder.mana_requirement import (
    can_pay_mana_requirements,
    mana_symbol_requirements,
    parse_colored_pips,
)


def test_parse_colored_pips_handles_regular_hybrid_and_phyrexian_symbols():
    pips = parse_colored_pips("{1}{W}{W/U}{B/P}")
    assert pips["W"] == 1.5
    assert pips["U"] == 0.5
    assert pips["B"] == 1.0
    assert pips["R"] == 0.0


def test_true_colorless_is_a_distinct_payment_requirement() -> None:
    requirements = mana_symbol_requirements("{1}{W}{C}")

    assert requirements == (frozenset({"W"}), frozenset({"C"}))
    assert can_pay_mana_requirements(requirements, ("W", "C"))
    assert not can_pay_mana_requirements(requirements, ("W", "W"))
    assert not can_pay_mana_requirements(requirements, ("W", "*"))


def test_wildcard_source_keeps_paying_non_colorless_requirements() -> None:
    requirements = mana_symbol_requirements("{W}{U}")

    assert can_pay_mana_requirements(requirements, ("*", "*"))
    assert can_pay_mana_requirements(
        mana_symbol_requirements("{W/C}"),
        ("*",),
    )
