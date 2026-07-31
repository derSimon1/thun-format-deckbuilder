# Version 2.0 – Archetype, Calibration and Sideboard

This release combines three previously planned development packages without changing the existing deck-construction architecture.

## Archetype Intelligence

The candidate evaluator now adds explicit archetype-fit and archetype-curve components. Burn rewards cheap burn, aggressive creatures and draw; Tokens rewards token makers, payoffs, removal and protection. Expensive cards receive a small archetype-specific penalty.

## Real Deck Calibration

`BenchmarkAnalyzer` compares generated decks with stable role, curve and land targets for Mono-Red Burn and Mono-White Tokens. The report is available through:

```bash
thun-deckbuilder build burn --colors R --benchmark
thun-deckbuilder build tokens --colors W --benchmark
```

The benchmark is intentionally diagnostic: it does not force exact card names and therefore exposes interpretation and composition problems instead of hiding them.

## Sideboard Builder

Generated decks now include a conservative sideboard assembled from legal, on-colour cards. It prioritizes common answers such as artifact/enchantment interaction, graveyard hate, anti-lifegain, protection and sweepers. The three-copy limit is respected across mainboard and sideboard.

Sideboards may contain fewer than 15 cards when the legal pool has too few suitable, detected answers. This is surfaced in the printed output rather than filled with unrelated cards.
