from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck, ManaCost
from thun_deckbuilder.token_packages import (
    analyze_token_package,
    build_token_package_diagnostics,
)


def raw_card(
    name: str,
    text: str,
    *,
    type_line: str = "Artifact",
    mana_value: int = 2,
):
    return {
        "name": name,
        "mana_value": mana_value,
        "mana_cost": "{1}{W}",
        "colors": ["W"],
        "color_identity": ["W"],
        "type_line": type_line,
        "oracle_text": text,
    }


def analysis(text: str, *, type_line: str = "Artifact"):
    return analyze_card(raw_card("Fixture", text, type_line=type_line))


def entry(name: str, quantity: int, roles: tuple[str, ...]) -> DeckEntry:
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost("{1}{W}", 1, "W"),
        mana_value=2,
        type_line="Artifact",
        roles=roles,
    )


def test_food_is_not_creature_material():
    signals = analyze_token_package(analysis("Create a Food token."))
    assert signals.creates_any_token
    assert signals.creates_noncreature_tokens
    assert not signals.creates_creature_tokens


def test_creature_tokens_are_material_and_multiple_output_is_detected():
    signals = analyze_token_package(
        analysis(
            "Create two 1/1 white Soldier creature tokens.",
            type_line="Sorcery",
        )
    )
    assert signals.creates_creature_tokens
    assert signals.creates_multiple_creature_tokens
    assert not signals.creates_noncreature_tokens


def test_activated_creature_sacrifice_is_an_outlet_even_if_it_makes_food():
    signals = analyze_token_package(
        analysis("{T}, Sacrifice a creature: Create a Food token.")
    )
    assert signals.sacrifice_outlet
    assert signals.creates_noncreature_tokens
    assert not signals.creates_creature_tokens


def test_additional_cost_is_not_a_repeatable_outlet():
    signals = analyze_token_package(
        analysis(
            "As an additional cost to cast this spell, sacrifice a creature. "
            "Draw two cards.",
            type_line="Sorcery",
        )
    )
    assert signals.one_shot_sacrifice
    assert not signals.sacrifice_outlet


def test_self_death_value_is_not_an_aristocrats_death_payoff():
    signals = analyze_token_package(
        analysis(
            "When this creature dies, create a Food token.",
            type_line="Creature — Ox",
        )
    )
    assert signals.self_death_value
    assert not signals.death_payoff
    assert not signals.drain_payoff


def test_other_creature_drain_is_a_death_and_drain_payoff():
    signals = analyze_token_package(
        analysis(
            "Whenever another creature dies, each opponent loses 1 life "
            "and you gain 1 life.",
            type_line="Creature — Cleric",
        )
    )
    assert signals.death_payoff
    assert signals.drain_payoff
    assert not signals.sacrifice_outlet


def test_diagnostics_expose_broad_role_false_positives():
    legal = {
        "food maker": raw_card("Food Maker", "Create a Food token."),
        "soldier maker": raw_card(
            "Soldier Maker",
            "Create two 1/1 white Soldier creature tokens.",
            type_line="Sorcery",
        ),
        "outlet": raw_card(
            "Outlet",
            "{T}, Sacrifice a creature: Scry 1.",
            type_line="Creature — Cleric",
        ),
        "drain": raw_card(
            "Drain",
            "Whenever another creature dies, each opponent loses 1 life.",
            type_line="Creature — Cleric",
        ),
    }
    deck = GeneratedDeck(
        mainboard=(
            entry("Food Maker", 3, ("token_maker",)),
            entry("Soldier Maker", 3, ("token_maker",)),
            entry("Outlet", 3, ("sacrifice",)),
            entry("Drain", 3, ("token_payoff",)),
        ),
        lands=24,
        profile_name="Mono-White Tokens — Aristocrats",
    )

    report = build_token_package_diagnostics(deck, legal)

    assert report["aristocrats"]["material_copies"] == 3
    assert report["aristocrats"]["outlet_copies"] == 3
    assert report["aristocrats"]["death_payoff_copies"] == 3
    assert report["aristocrats"]["component_presence"] is True
    assert report["broad_role_false_positive_copies"] == {
        "token_maker_without_creature_material": 3
    }
