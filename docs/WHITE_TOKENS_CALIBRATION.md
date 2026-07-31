# White Tokens Calibration

This update calibrates the existing Mono-White Tokens strategy without changing
its architecture.

## Selection changes

The token-specific score now distinguishes between:

- reliable multi-token spells and single-token effects;
- efficient token output per mana and expensive low-output cards;
- repeatable token engines and one-shot effects;
- persistent anthems and temporary combat pumps;
- direct token payoffs and generic cards that merely mention tokens;
- go-wide support cards and board wipes that undermine the deck's own plan.

The eligibility filter also rejects global creature sweepers and token copy
cards that depend on an opponent's permanent.

## Purpose

These rules address the first observed calibration problem: cards were sometimes
classified correctly at a broad role level but interpreted incorrectly for an
actual go-wide token deck. The new regression tests preserve these concrete
selection preferences.
