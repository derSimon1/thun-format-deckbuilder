from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_scoring import ScoreBreakdown
from thun_deckbuilder.deck_generator import DeckEntry, ManaCost
from thun_deckbuilder.deck_optimizer import optimize_entries
from thun_deckbuilder.knowledge_base import CardKnowledge


def knowledge(name, mv, type_line, text):
    card = {
        "name": name,
        "mana_value": mv,
        "mana_cost": "{1}",
        "colors": ["U"],
        "color_identity": ["U"],
        "type_line": type_line,
        "oracle_text": text,
    }
    return CardKnowledge(card, analyze_card(card), frozenset(), frozenset())


def entry(name, mv, type_line, score=1.0):
    return DeckEntry(name, 3, ManaCost("{1}", 1, ""), mv, type_line, score=score)


def scorer(analysis):
    text = analysis.oracle_text.lower()
    score = 5.0 if "target opponent mills" in text else 1.0
    return ScoreBreakdown(score, ("test",))


def eligible(card, colors):
    return True


def test_mill_optimizer_replaces_generic_filler_with_core_mill():
    filler = knowledge("Slow Filler", 5, "Sorcery", "Draw two cards.")
    mill = knowledge("Mind Burst", 2, "Sorcery", "Target opponent mills 8 cards.")
    entries = (entry("Slow Filler", 5, "Sorcery"),)

    optimized = optimize_entries(
        entries,
        (filler, mill),
        archetype="mill",
        colors=("U", "B"),
        scorer=scorer,
        eligible=eligible,
        max_copies=3,
    )

    counts = {card.name: card.quantity for card in optimized}
    assert counts.get("Mind Burst", 0) > 0
    assert counts.get("Slow Filler", 0) < 3


def test_optimizer_preserves_total_spell_count_and_copy_limit():
    filler = knowledge("Filler", 3, "Sorcery", "Draw a card.")
    engine = knowledge(
        "Mill Engine", 2, "Enchantment",
        "Whenever you draw a card, target opponent mills 2 cards.",
    )
    entries = (entry("Filler", 3, "Sorcery"),)

    optimized = optimize_entries(
        entries,
        (filler, engine),
        archetype="mill",
        colors=("U", "B"),
        scorer=scorer,
        eligible=eligible,
        max_copies=3,
    )

    assert sum(card.quantity for card in optimized) == 3
    assert all(card.quantity <= 3 for card in optimized)


def test_artifact_payoff_receives_pairwise_density_bonus():
    filler = knowledge("Generic Spell", 2, "Sorcery", "Draw a card.")
    artifact = knowledge("Cheap Relic", 1, "Artifact", "{T}: Add {U}.")
    payoff = knowledge(
        "Artifact Payoff", 2, "Creature",
        "Whenever an artifact enters, put a +1/+1 counter on this creature.",
    )
    entries = (entry("Generic Spell", 2, "Sorcery"),)

    optimized = optimize_entries(
        entries,
        (filler, artifact, payoff),
        archetype="artifacts",
        colors=("U",),
        scorer=lambda analysis: ScoreBreakdown(2.0, ("test",)),
        eligible=eligible,
        max_copies=3,
    )

    names = {card.name for card in optimized}
    assert names.intersection({"Cheap Relic", "Artifact Payoff"})
