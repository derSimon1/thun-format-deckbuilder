# Standard and Pioneer Archetype Transfer Audit — 2026-08-05

## Status

This document records a **read-only research snapshot**. It does not alter deck
selection, candidate scoring, Champion status, or Arena recommendations.
Technical transfer scores are priors for further research. They are not win-rate
predictions and cannot replace Arena evidence.

## Research question

Which successful current Standard and Pioneer structures are most likely to
survive the Thun-format constraints?

The relevant constraints are defined by `config/thun.toml`, especially:

- common and uncommon cards only;
- legal paper printings from the configured set allow-list;
- 60-card mainboard and 15-card sideboard;
- at most three copies of a nonbasic card.

## Evidence scope

The snapshot contains twelve archetypes, six from Standard and six from Pioneer.
Every archetype exceeds both thresholds:

1. at least 100 source-reported decklists in the two-month metagame selection;
2. at least 100 ranked decks in the source card-presence fingerprint.

The source deck counts are not vendored raw decklists. They are the public
aggregator's reported sample sizes. The audit therefore stores provenance,
methodology and explicit limitations rather than pretending to contain 5,377
individually verified lists.

The primary evidence comes from MTGDecks metagame and card-presence pages. The
Wizards June 29, 2026 announcement provides official Standard context: Izzet
variants and Badgermole-Cub strategies remained the two main format pressures,
while Four-Color Control and other challengers established meaningful shares.

## Transfer dimensions

Each archetype receives a 0–1 value for six explicit dimensions:

| Dimension | Weight | Meaning |
|---|---:|---|
| Function coverage | 25% | Availability of the archetype's required effects at common/uncommon |
| Three-copy redundancy | 20% | Ability to reproduce core functions across multiple card names |
| Mana-base feasibility | 15% | Ability to cast the deck on time under Thun land constraints |
| Role-compression replacement | 15% | Ability to replace rare cards that perform multiple jobs |
| Sequence preservation | 15% | Ability to preserve the original early and midgame play pattern |
| Recovery and resilience | 10% | Ability to reload or continue after the first exchange |

A missing critical dependency caps a score at 4.9. This prevents excellent
support functions from disguising a non-transferable named combo or mana system.

## Current ranking

The executable ranking is generated from
`research/meta/archetype_transfer_snapshot_2026-08-05.json`.

Expected order:

1. Pioneer Red Deck Wins
2. Mono-Green Landfall
3. Pioneer Izzet Prowess
4. Standard Izzet Spellementals
5. Standard Izzet Prowess
6. Pioneer Dimir Ninjas
7. Pioneer Golgari Midrange
8. Selesnya Gearhulk
9. Pioneer Azorius Control
10. Jeskai Lessons
11. Four-Color Control
12. Abzan Greasefang

Small score changes may reorder adjacent archetypes. The important conclusion is
more stable than the exact ordering:

- low-curve mono-color or two-color shells with redundant commons/uncommons
  transfer best;
- rare-heavy role-compression strategies transfer only partially;
- four-color mana and named rare combos are structural blockers.

## Cross-archetype findings

1. A relevant play by turn two is a recurring success condition.
2. Role compression matters more than raw card count.
3. Enablers should remain useful without their ideal payoff.
4. Functional redundancy is mandatory under the three-copy rule.
5. Lands must be evaluated as strategic resources, not only colored sources.
6. Reload and resilience are separate from opening-hand quality.
7. Interaction must be available at the required turn and speed.
8. Payoffs must convert setup into damage, cards, mana, board control, or inevitability.
9. Mana sinks and selection reduce late-game dead draws.
10. The least replaceable core function sets the transfer ceiling.

## Generator implications

Do not add twelve new deck profiles yet. The immediate implementation target is a
read-only audit layer that:

- stores the original archetype fingerprint;
- distinguishes direct functions, functional replacements and non-reproducible
  functions;
- validates sample-size and scoring provenance;
- ranks candidate archetypes for later card-pool audits;
- refuses to classify a named combo as transferred when its defining function is
  absent.

Only after a card-level Thun-pool audit should an archetype receive a generator
profile. No current Champion should be replaced on this evidence alone.

## Programmatic use

`load_snapshot(...)` provides the validated read-only API for the stored JSON
snapshot. Loading the snapshot performs no network requests and does not modify
repository data.

## Success criteria for the next experiment

A follow-up card-pool audit should be accepted only if it:

- resolves every required function against current Oracle text;
- distinguishes immediate effects from attack, death, chapter, delayed and
  conditional effects;
- reports castability and three-copy redundancy;
- marks missing critical functions explicitly;
- produces a reproducible Challenger hypothesis without changing a Champion;
- defines an Arena test before any claim of real deck strength.
