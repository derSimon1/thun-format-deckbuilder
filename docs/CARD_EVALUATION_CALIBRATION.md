# Card Evaluation Calibration

The intrinsic evaluator now distinguishes the main forms of card quality instead
of treating every Oracle-text match equally.

## Calibrated areas

- **Card flow:** cantrips replace themselves, looting/scry provide selection,
  while drawing two or more cards creates card advantage.
- **Interaction:** exile, destroy, counters, bounce and damage receive different
  values. Speed, mana value and conditional wording affect the result.
- **Creatures:** rate, useful keywords, ETB effects, repeatable value and obvious
  drawbacks are evaluated separately.
- **Situational cards:** one-shot combat tricks and narrow effects receive a
  conservative penalty.
- **Expensive cards:** high mana value is acceptable only when the card has
  meaningful immediate or repeatable impact.

All components remain visible through the existing explain output under
`intrinsic_quality`; no architecture or public CLI behaviour changed.
