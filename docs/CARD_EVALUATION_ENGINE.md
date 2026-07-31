# Card Evaluation Engine

Package 7 adds a conservative intrinsic card-quality layer. It complements rather than replaces archetype scoring, deck needs, curve scoring and synergy.

The engine currently evaluates:

- mana efficiency
- instant-speed flexibility
- card advantage and selection
- direct interaction
- immediate battlefield impact
- creature rate
- tempo and resilience keywords
- expensive cards without clear immediate impact

Every contribution appears as an `intrinsic_quality` component in the existing explainable score trace. The rules deliberately avoid pretending to fully understand arbitrary Oracle text. Ambiguous card interactions remain a later calibration task supported by benchmark decks.
