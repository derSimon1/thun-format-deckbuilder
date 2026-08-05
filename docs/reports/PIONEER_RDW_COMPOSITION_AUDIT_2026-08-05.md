# Pioneer Red Deck Wins — Thun Composition Audit

## Status

Date: 2026-08-05  
Branch: `agent/pioneer-rdw-composition-audit`  
Calibration base: PR #14 head `2d879e969351fe8c3b266948a9888e02b829f403`  
Card-pool research source: PR #16 head `3908136ae939d4af138025c30b539f949991dd05`

Final result: **technical pass; Arena test authorized; Champion replacement not authorized**.

This experiment used both permitted deck-changing cycles. No further decklist
change is allowed before real Arena evidence.

## Starting point and evidence

The current generated Burn Champion was captured live from the PR #14 code and
the current verified Scryfall database. A stale-snapshot guard first rejected the
older Run-79 list and recorded the actual current Champion before any comparison
was allowed.

The Pioneer transfer audit in PR #16 established a 7.2/10 prior: the low-curve
mono-red structure transfers well, but the rare Pioneer role-compression package
does not. The composition experiment therefore tested functional redundancy
rather than weak card-for-card substitutions.

The technical evidence consists of:

- current Thun legality from the rebuilt card database;
- exact 60/15 and three-copy validation;
- 100 opening hands at seed `1701` for both decks;
- 2,000 five-turn Goldfish samples at seed `31` for both decks;
- the same Burn benchmark and mana-quality implementation for both decks;
- full repository test suite: 403 passing tests.

These are proxies. No Arena game is attached to either deck hash.

## Concrete hypothesis

### Cycle 1

A 20-land Prowess/Burn shell with fifteen turn-one packages, six repeatable
spell-damage creatures, pump, burn, and explicit reload would preserve the
Pioneer opening pattern.

Result: **rejected**.

The list produced more Goldfish damage than the Champion, but failed the
predeclared benchmark and plan-capable gates. It had 27 one-mana spells, 32%
mana-error hands, and only 67% plan-capable hands.

### Cycle 2

The cycle-1 failure was caused by the combined 20-land and 27-one-mana
distribution. Raising the deck to 22 lands, reducing it to twelve turn-one
threat copies plus three one-mana burn spells, preserving six repeatable
spell-damage creatures, and moving the remaining slots into explicit reload and
two- or three-mana burn would restore the benchmark and plan-capable gates.

Result: **technically confirmed**.

## Champion

Name: **Current PR #14 Generated Burn Champion**  
Hash: `0f0a282f0e15ce6f15fae47349f9d7af803d142e76d2a4c25e436edfa9af65d5`

### Champion mainboard — 60

```text
Deck
3 Burst Lightning
3 Sawblade Scamp
3 Shock
3 Voldaren Epicure
3 Coruscation Mage
3 Lightning Strike
2 Reality Hemorrhage
3 Roil Eruption
2 Thermo-Alchemist
3 Thunderdrum Soloist
3 Call In a Professional
2 Fateful End
3 Flick a Coin
24 Mountain
```

### Champion sideboard — 15

```text
Sideboard
3 Smash to Dust
3 Deface
3 Dreadmaw's Ire
3 Explosive Derailment
3 Gleeful Demolition
```

Champion status remains unchanged.

## Challenger

Name: **Thun Mono-Red Redundancy v2**  
Hash: `9dfa387052563548704115599f20ed0b61d5cf41053b422b85ec78f5917888da`  
Status: **untested Challenger; Arena test authorized**

### Challenger mainboard — 60

```text
Deck
3 Monastery Swiftspear
3 Sawblade Scamp
3 Clockwork Percussionist
3 Kumano Faces Kakkazan // Etching of Kumano
3 Burst Lightning
3 Firebrand Archer
3 Kessig Flamebreather
3 Lightning Strike
3 Reckless Impulse
2 Abrade
2 Wrenn's Resolve
3 Call In a Professional
2 Fateful End
2 Flick a Coin
20 Mountain
2 Ramunap Ruins
```

### Challenger sideboard — 15

```text
Sideboard
3 Smash to Dust
3 Pyroclasm
3 Weathered Runestone
3 Magebane Lizard
3 Giant Cindermaw
```

## Structural fingerprint

- 22 lands and 22 red sources;
- twelve turn-one threats across four card names;
- six repeatable spell-damage creatures;
- eleven cards classified as direct face burn;
- seven explicit reload cards;
- three death-triggered conditional reload cards;
- two mainboard artifact-interaction cards;
- two Ramunap Ruins as late activated reach.

Rockface Village remains excluded because no mainboard creature is a Lizard,
Mouse, Otter, or Raccoon. Its haste ability would therefore be unavailable.

## Technical comparison

| Metric | Champion | Challenger | Delta |
|---|---:|---:|---:|
| Benchmark | 83 | 81 | -2 |
| Keepability | 78% | 76% | -2 pp |
| Plan capable | 78% | 75% | -3 pp |
| Early play by turn two | 98% | 97% | -1 pp |
| Early play by turn three | 98% | 97% | -1 pp |
| Mana-error hands | 22% | 24% | +2 pp |
| Average Goldfish damage | 41.61 | 43.69 | +2.08 |
| Kill by turn five | 96% | 96% | 0 pp |
| Average spells cast | 5.94 | 6.33 | +0.39 |
| Average unused mana | 3.84 | 3.14 | -0.70 |
| Mana-quality score | 94 | 100 | +6 |

The Challenger passed every predeclared hard gate. It did **not** demonstrate
technical superiority: it remains slightly worse in keepability, plan
capability, and mana errors. The higher Goldfish damage is encouraging but is
not enough to replace the Champion.

## Technical gate results

- PASS — exactly 60 mainboard cards;
- PASS — exactly 15 sideboard cards;
- PASS — maximum three copies across mainboard and sideboard;
- PASS — at least twelve turn-one threat copies;
- PASS — at least four distinct turn-one threat names;
- PASS — at least eighteen red sources;
- PASS — at least two explicit reload copies;
- PASS — benchmark no more than five points below the Champion;
- PASS — plan-capable rate no more than five points below the Champion;
- PASS — early play by turn two at least 95%;
- PASS — early play by turn three at least 95%;
- PASS — mana-quality report sufficient.

The existing `BURN_PROFILE` requires exactly 24 lands. The Challenger is a
predeclared 22-land subprofile, so that profile mismatch is retained as a
diagnostic warning rather than introduced after the fact as an additional hard
gate.

## Mulligan guide

### Keep

- Two or three lands, one of the twelve turn-one threats, and either a
  repeatable spell-damage creature or direct burn.
- One land only with at least two castable one-mana cards and no hand that
  depends on resolving a three-mana spell.
- Four lands only with a turn-one threat and explicit reload.

### Mulligan

- Zero lands or five or more lands.
- No turn-one threat, no direct burn, and no credible turn-two engine.
- A one-land hand containing Call In a Professional, Fateful End, or Flick a
  Coin without sufficient early action.
- Ramunap Ruins as the only land when repeated red activation would require
  avoidable life loss.

## Sideboard plans

### White Tokens or go-wide

In: 3 Pyroclasm, 3 Smash to Dust  
Out: 3 Clockwork Percussionist, 2 Wrenn's Resolve, 1 Fateful End

Pyroclasm is symmetrical and should normally be cast before rebuilding. Smash
to Dust is strongest against artifact tokens or one-toughness boards and is not
a universal sweeper.

### Artifacts

In: 3 Smash to Dust  
Out: 2 Wrenn's Resolve, 1 Fateful End

Retain Abrade. Select the relevant Smash to Dust mode; do not count all modes as
simultaneously available.

### Spell-heavy tempo or prowess

In: 3 Magebane Lizard  
Out: 2 Abrade, 1 Fateful End

Magebane Lizard triggers for both players. Its damage is conditional on the
relevant noncreature spells actually being cast.

### Lifegain or midrange

In: 3 Giant Cindermaw  
Out: 2 Abrade, 1 Flick a Coin

Giant Cindermaw prevents opponents from gaining life only while it remains on
the battlefield. It does not provide immediate entry damage.

### Graveyard or library cheat

In: 3 Weathered Runestone  
Out: 2 Abrade, 1 Fateful End

Weathered Runestone does not stop cards entering from hand or exile and adds no
direct pressure.

## Technical test plan

The reproducible workflow must continue to:

1. rebuild the current verified card database;
2. stop if the generated Champion no longer matches its snapshot;
3. run the complete repository test suite;
4. validate legality, exact counts, and three-copy limits;
5. run both decks with the same opening-hand and Goldfish seeds;
6. emit JSON, Markdown, and Arena-import artifacts;
7. preserve failed experiments and their hashes.

## Arena test plan

Format: Best of Three  
Minimum sample: **12 matches and at least 24 games**

The sample must include, where Arena pairings permit:

- white tokens or another go-wide deck;
- an artifact deck;
- spell-heavy tempo or prowess;
- lifegain or midrange;
- control or removal-heavy decks.

For every game record:

- play or draw;
- opening seven and mulligan decision;
- turn-one and turn-two sequence;
- stranded three-mana cards;
- red-source or Ramunap Ruins life-cost problems;
- reload spells cast and cards actually converted into useful spells;
- sideboard cards drawn and their real impact;
- model prediction versus real outcome.

## Arena success criteria

- match win rate at least 50%;
- nonfunctional opening rate no more than 20%;
- games with stranded three-mana cards no more than 15%;
- no repeated red-source failure;
- direct Arena comparison with the current Burn Champion before any Champion
  replacement decision.

Passing these criteria would still not automatically replace the Champion. The
matchups, sequencing, sideboard contribution, and failure modes must be reviewed
semantically.

## Model limitations

- The Goldfish model is a deterministic technical proxy, not a win-rate model.
- It compresses card text into broad roles and does not fully model prowess,
  attack triggers, Saga chapter timing, death-triggered reload, real combat, or
  opposing interaction.
- Ramunap Ruins is counted as a red source, but colored activation costs life;
  its damage ability requires four mana and sacrificing a Desert.
- The higher Goldfish damage may be overvalued if the real metagame removes the
  repeatable spell-damage creatures efficiently.
- No real Arena evidence exists for the Challenger hash.

## Decision

- Cycle 1: technically rejected and archived.
- Cycle 2: all technical gates passed.
- Arena test: authorized.
- Champion replacement: not authorized.
- Generator change: not authorized.
- KGB: **no new KGB**.

## Exactly one next step

Import Challenger hash
`9dfa387052563548704115599f20ed0b61d5cf41053b422b85ec78f5917888da`
into Arena and execute the predefined twelve-match Best-of-Three test while
preserving the current Burn Champion.
