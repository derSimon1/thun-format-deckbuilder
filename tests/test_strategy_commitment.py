from thun_deckbuilder.deck_generator import DeckEntry, ManaCost
from thun_deckbuilder.strategy_commitment import evaluate_token_commitment
from thun_deckbuilder.token_plan import TokenPlan


def entry(name: str, quantity: int, roles: tuple[str, ...]) -> DeckEntry:
    return DeckEntry(
        name=name,
        quantity=quantity,
        mana_cost=ManaCost(raw="{1}{W}", generic=1, colored="W"),
        mana_value=2,
        type_line="Creature",
        roles=roles,
    )


def test_go_wide_commitment_counts_defining_roles_and_neutral_utility():
    report = evaluate_token_commitment(
        (
            entry("Maker", 12, ("token_maker",)),
            entry("Anthem", 6, ("token_payoff", "anthem")),
            entry("Removal", 4, ("removal",)),
        ),
        TokenPlan.GO_WIDE,
    )

    assert report.commitment_score == 1.0
    assert report.committed_cards == 18
    assert report.neutral_cards == 4
    assert report.conflicting_cards == 0


def test_plan_foreign_role_creates_mismatch_warning():
    report = evaluate_token_commitment(
        (
            entry("Maker", 6, ("token_maker",)),
            entry("Outlet", 6, ("sacrifice",)),
        ),
        TokenPlan.GO_WIDE,
    )

    assert report.commitment_score == 0.5
    assert report.conflicting_cards == 6
    assert any("planfremde Rollen" in warning for warning in report.warnings)
    assert any("zu niedrig" in warning for warning in report.warnings)


def test_aristocrats_treats_sacrifice_as_committed_and_anthem_as_conflict():
    report = evaluate_token_commitment(
        (
            entry("Fodder", 9, ("token_maker",)),
            entry("Outlet", 3, ("sacrifice",)),
            entry("Drain", 3, ("token_payoff",)),
            entry("Anthem", 3, ("anthem",)),
        ),
        TokenPlan.ARISTOCRATS,
    )

    assert report.committed_cards == 15
    assert report.conflicting_cards == 3
    assert report.commitment_score == 15 / 18
    assert dict(report.role_densities)["sacrifice"] == 3
