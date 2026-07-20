# Deck Engine v0.2

This development package implements three connected steps.

## 1. Strategic card roles

`card_roles.py` now recognizes broader deckbuilding functions, including:

- aggro creature
- anthem and token payoff
- card draw
- removal and board wipe
- protection
- sacrifice
- finisher

The patterns are deliberately conservative and covered by regression tests.

## 2. Profile-driven composition

`deck_profile.py` defines explicit composition goals for Burn and Tokens.
`composition_engine.py` selects cards in two passes:

1. satisfy strategic role targets in priority order;
2. fill remaining slots by quality while preferring under-filled mana bands.

Mandatory minimums fail loudly. Optional missing roles produce warnings instead
of breaking generation. The existing strategy and generator entry points remain
compatible.

## 3. Validation and deck report

`deck_validation.py` checks:

- total deck size
- land count
- copy limit
- duplicate entries
- mandatory role minimums
- role distribution
- mana curve distribution

The normal formatted CLI output now includes a `DECK CHECK` section.

## Verification

Run:

```bash
./scripts/setup_dev.sh
./scripts/run_tests.sh
```

Expected result for this package: `56 passed`.
