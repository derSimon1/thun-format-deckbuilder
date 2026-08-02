from thun_deckbuilder.sideboard_builder import RULES


def test_prowess_has_complete_sideboard_plan():
    rules = RULES["prowess"]
    labels = {rule.label for rule in rules}

    assert "countermagic" in labels
    assert "protect threats" in labels
    assert "anti-lifegain" in labels
    assert "cheap creature interaction" in labels
    assert "artifact/enchantment answer" in labels
    assert "graveyard hate" in labels


def test_prowess_sideboard_prioritizes_plan_protection_and_lifegain_hate():
    priorities = {rule.label: rule.priority for rule in RULES["prowess"]}

    assert priorities["protect threats"] >= 5
    assert priorities["anti-lifegain"] >= 5
