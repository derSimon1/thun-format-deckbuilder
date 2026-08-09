# Arena Token Playtest — 2026-08-05/06

## Purpose

Empirical validation of the Mono-White Token calibration from PR #14 and two predefined Challenger variants. These results are Arena evidence, not simulated matchup output.

## Decks

### TOK-A — Builder Baseline

Origin: PR #14 / Run 99 baseline.

Mainboard difference reference: contains 3 `Duty Beyond Death`.

Result: **0-3 BO3 matches / 0-6 games**.

Observed failure modes:
- functional opening hands still failed to produce enough real pressure;
- `Duty Beyond Death` was repeatedly conditional and low-impact;
- the deck could make bodies but struggled to convert them into lethal attacks;
- poor recovery once opposing value engines, larger blockers, flying threats or efficient spell-tempo were established.

Decision: **rejected as an active deck candidate**. This does not by itself invalidate the entire Token generator.

### TOK-B — Immediate Pressure

Change from TOK-A:
-3 `Duty Beyond Death`
+2 `Battle Menu`
+1 `Sworn Companions`

Evidence:
- initial BO3: 0-1 match / 0-2 games, with one game reducing the opponent to 2 life;
- dedicated BO1 screen: **4-2** across six completed games.

Observed strengths:
- cleaner deployment;
- fewer conditional cards;
- better conversion of board width into actual pressure;
- `Charge` functioned as real reach in successful wide-board states.

Observed weaknesses:
- still weak after opponents stabilize with superior permanent engines, flyers or stronger go-wide scaling;
- limited protection, persistent anthem density, evasion and card advantage.

Decision: **provisional Token mainboard leader / Challenger**.

### TOK-C — Repeatable Pressure

Change from TOK-A:
-3 `Duty Beyond Death`
+3 `Cathar's Call`

Dedicated BO1 result: **3-2** across five games. One win was an early opponent concession and has low evidentiary weight.

Observed strengths:
- `Cathar's Call` provides a real repeatable ceiling against slower boards.

Observed weaknesses:
- four-mana setup is slower than TOK-B's unconditional makers;
- requires a surviving creature and a profitable attack;
- does not independently stabilize a losing board.

Decision: **retain as Challenger evidence; TOK-B remains ahead**.

## Model calibration finding

The PR #14 Token benchmark and opening-hand plan metrics materially overstated real competitive strength of TOK-A. The central gap is that successful deployment and token count do not sufficiently measure closing power, resilience, evasion, card quality after stabilization, or interaction with opposing engines.

## Current decision

1. Do not promote the PR #14 Token baseline.
2. Preserve TOK-A as negative empirical evidence.
3. Use TOK-B as the Token mainboard finalist for future focused BO3 validation.
4. Keep TOK-C as a slower-engine Challenger hypothesis.
5. Do not alter generator scoring solely from this small Arena sample; use the evidence to define the next bounded calibration experiment.
