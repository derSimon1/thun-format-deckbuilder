# Synergy Engine – Version 1.1

The deckbuilder now scores cards against the current `DeckState`, not only by
static card quality, role demand, and mana curve.

## Supported interactions

- Token makers and token payoffs
- Instants/sorceries and spell payoffs
- Artifacts and artifact payoffs
- Sacrifice fodder, sacrifice outlets, and death triggers
- Shrines scaling with other Shrines

`SynergyTag` provides a normalized vocabulary. Existing legacy tags remain
compatible. `SynergyEngine` returns regular `ScoreComponent` objects with the
category `synergy`, so `--explain` shows each bonus and its enabling card count.

## Quality report

The deck quality report now includes detected synergy packages and a separate
synergy score. The established overall score remains unchanged in this step so
existing quality benchmarks stay comparable.

## Scope

This package deliberately does not change the mana base, sideboard, legality,
or command structure. It is the first package focused directly on improving
card combinations during iterative selection.
