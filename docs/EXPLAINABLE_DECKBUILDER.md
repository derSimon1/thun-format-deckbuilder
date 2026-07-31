# Explainable Deck Builder

This package adds a measurable quality report and a human-readable trace for the iterative composition engine.

## Deck quality

`DeckQualityAnalyzer` evaluates the completed spell section against the active `DeckProfile`.

- Role target fulfilment contributes 70%.
- Mana-curve target fulfilment contributes 30%.
- Every component is capped at 100% so overfilling one target cannot hide another weakness.
- Mandatory role minimums remain enforced by the composition engine.

The report contains per-role and per-curve results as well as role, curve, and overall scores.

## Explanations

The generated deck now carries every `SelectionTrace`. The CLI can display the complete iterative decision history:

```bash
thun-deckbuilder build tokens --colors W --explain
```

Without `--explain`, normal deck generation remains unchanged except that the compact quality report is shown.

## Regression baseline

This package raises the test suite from 76 to 81 tests. Future packages can assert quality scores to detect changes that technically pass but produce worse decks.
