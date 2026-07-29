# Deck State Engine v1

This package adds the stable state layer required for dynamic deck selection without replacing the current working Burn and Tokens prototype.

## Added components

- `CardContribution`: normalized roles, synergy tags, mana value and color pips.
- `DeckState`: immutable snapshots with role, tag, curve and pip counters.
- `DeckNeedsAnalyzer`: derives current role and curve pressure from an existing `DeckProfile`.
- `CandidateScore`: explainable score components for the next composition step.

## Compatibility guarantee

The existing `composition_engine.py`, Burn generator, Token generator and CLI remain unchanged in this package. The new layer is additive and independently tested. The dynamic composition engine will only replace the old selection path after it can reproduce valid 60-card prototype decks in regression tests.

## Next acceptance gate

Before the current prototype is replaced, the next package must demonstrate:

1. all existing tests remain green;
2. Burn and Tokens still produce 60-card legal decks;
3. mandatory role minima remain satisfied;
4. every selected card has an explainable score;
5. rollback is possible by reverting one feature commit.
