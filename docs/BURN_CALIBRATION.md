# Mono-Red Burn Calibration

This update calibrates the existing Mono-Red Burn strategy without changing the
composition architecture or public CLI.

## Selection changes

The Burn-specific score now distinguishes between:

- reliable damage that can reduce the opponent's life total;
- creature-only removal and flexible `any target` interaction;
- damage per mana instead of raw damage alone;
- repeatable and scalable damage sources;
- efficient early attackers and slow low-pressure creatures;
- unconditional reach and situational damage effects;
- useful card flow, anti-lifegain text and risky symmetrical damage.

The eligibility filter now keeps the proactive main deck focused. A card must
provide opponent-facing reach, a credible early attacker, or card flow. Pure
creature removal remains available to the sideboard builder but no longer fills
main-deck Burn slots merely because it has the broad `burn` role.

## Purpose

The previous scorer rewarded mana value, the word `damage`, and broad target
phrases independently. That could make inefficient removal or conditional cards
look comparable to reliable face damage. The calibrated scorer evaluates rate,
reach and reliability together, and regression tests preserve those concrete
preferences.
