from thun_deckbuilder.mana_requirement import parse_colored_pips


def test_parse_colored_pips_handles_regular_hybrid_and_phyrexian_symbols():
    pips = parse_colored_pips("{1}{W}{W/U}{B/P}")
    assert pips["W"] == 1.5
    assert pips["U"] == 0.5
    assert pips["B"] == 1.0
    assert pips["R"] == 0.0
