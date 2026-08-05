# Pioneer Red Deck Wins — Thun Card-Pool Audit

## Status

Date: 2026-08-05  
Branch: `agent/pioneer-rdw-card-pool-audit`  
Evidence type: read-only metagame and live card-pool audit

This document does not define a Challenger, replace a Champion, or authorize a
generator-profile change. Real Arena evidence is still absent.

## Starting point and evidence

The reference sample contains five successful MTGO Pioneer Challenge lists from
11–18 July 2026. The sample includes one tournament win and four additional
Top-8/Top-16 finishes. Across these lists, the stable structure is:

- 23 lands;
- 25–28 creatures;
- twelve one-mana engine slots;
- nine to twelve cheap damage, pump, or removal spells;
- four copies of the principal creature and burn packages in the source format.

The live audit rebuilt `data/cards.db` from the current Scryfall bulk data and
then applied the authoritative `config/thun.toml` legality rules. The evaluated
pool contained 38,542 Oracle cards, of which 8,021 were Thun legal. Of those,
1,868 were mono-red or colorless by color identity and entered the initial
candidate scan.

The large candidate count is not a strength claim. Automated text matching
produces false positives and is used only for discovery. Every conclusion below
is based on a curated semantic review of Oracle text and timing.

## Directly transferable mainboard functions

Seven of fifteen checked Pioneer mainboard core cards have a direct legal Thun
printing:

| Card | Directly preserved function | Important timing or condition |
|---|---|---|
| Monastery Swiftspear | one-mana haste and prowess | immediate |
| Kumano Faces Kakkazan | turn-one damage, counter support, later body | body arrives only after chapters resolve |
| Burst Lightning | face damage, creature removal, mana sink | four damage requires kicker |
| Monstrous Rage | pump, trample, persistent Role bonus | needs a creature target and is vulnerable to removal in response |
| Reckless Rage | efficient creature removal | requires both an opposing and own creature target; no face damage |
| Ramunap Ruins | late land-based reach | costs four mana and sacrifices a Desert |
| Rockface Village | land-based haste support | sorcery speed and only Lizard, Mouse, Otter, or Raccoon targets |

All six checked sideboard cards are directly legal: Flowstone Infusion,
Magebane Lizard, Pyroclasm, Redcap Melee, Scorching Shot, and Weathered
Runestone.

## Functional replacements

### Soul-Scar Mage

No true replacement was found.

- Sawblade Scamp preserves a one-mana spell engine, but converts casts into oil
  counters and must tap to deal damage.
- Dwarven Forge-Chanter and Electrostatic Infantry preserve spell scaling, but
  cost two mana.
- None reproduces the damage-to-minus-counters function.

Classification: **partial replacement**.

### Emberheart Challenger

The pool contains the individual functions but not on one efficient creature:

- Ancestral Anger supplies pump, trample, and a card;
- Reckless Impulse and Wrenn's Resolve supply explicit reload;
- Clockwork Percussionist supplies a one-mana haste body and death-triggered card
  access.

Classification: **split across multiple cards**.

### Screaming Nemesis and Sunspine Lynx

Giant Cindermaw provides persistent anti-lifegain, while Call In a Professional
provides one-turn anti-lifegain plus immediate damage. Neither reproduces the
original combination of pressure, immediate damage, resilience, and lifegain
suppression.

Classification: **partial replacement with major role-compression loss**.

### Bonecrusher Giant // Stomp

Burst Lightning, Lightning Strike, and Abrade provide appropriate interaction,
but a separate threat slot is required. The source deck's two-for-one card and
its sequencing flexibility are lost.

Classification: **split across multiple cards**.

### Rare utility lands

Ramunap Ruins and Rockface Village are useful direct legal cards. Blighted Gorge
and red modal double-faced cards provide slower reach or land/spell flexibility.
The pool does not reproduce Mutavault or Den of the Bugbear as resilient board
pressure that occupies a land slot.

Classification: **partial replacement**.

## Non-reproducible functions

1. The source lists use three four-of one-mana packages. Under the Thun
   three-copy rule, twelve such slots require at least four distinct card names,
   lowering average one-drop quality.
2. No checked common or uncommon reproduces Screaming Nemesis or Sunspine Lynx
   role compression.
3. No checked common or uncommon combines Bonecrusher Giant's interaction and
   threat in one card.
4. No checked card reproduces Mutavault or Den of the Bugbear as creature-land
   resilience.
5. Persistent anti-lifegain exists only on narrower or slower cards and cannot
   be counted as immediate damage.

## Revised transfer assessment

Prior transfer score: **7.2/10**  
Band: **high structural transfer, partial card-level transfer**  
Confidence: **medium-high**

This is lower than the initial archetype-level estimate. The mono-red mana,
burn, pump, low curve, and sideboard interaction are genuinely transferable.
However, the current successful Pioneer build is not. Its rare midgame cards
compress too many functions into single slots.

The correct Thun interpretation is therefore not “copy Pioneer RDW.” It is:

> Test whether a lower and more redundant mono-red Prowess/Burn shell can use
> legal one-drops, explicit reload, and Ramunap Ruins to compensate for the
> missing rare midgame package.

## Concrete hypothesis

A Thun mono-red Prowess/Burn Challenger can preserve the source archetype's early
sequence if it uses at least four distinct turn-one packages, keeps interaction
mostly at one mana, and adds explicit reload rather than attempting weak
card-for-card replacements for Screaming Nemesis, Sunspine Lynx, or Bonecrusher
Giant.

This hypothesis remains untested. A deck should not be generated until the four
open design questions in
`research/meta/pioneer_rdw_thun_review_2026-08-05.json` are resolved by a
composition audit.

## Technical success criteria for the next experiment

- exactly 60 mainboard and 15 sideboard cards;
- at least twelve credible turn-one plays across at least four card names;
- no effect counted before its real attack, death, chapter, delayed, conditional,
  or activated timing;
- sufficient red sources after Ramunap Ruins and other colorless utility lands;
- explicit reload slots and a measurable post-removal recovery plan;
- no generated card outside the current Thun legality configuration;
- direct comparison against the existing Burn Champion before any replacement
  recommendation;
- a predefined Arena BO3 test with mulligan and matchup observations.

## Exactly one next step

Run a constrained composition audit for a 60/15 mono-red Challenger using the
curated candidate core, then compare it technically with the current Burn
Champion without changing Champion status.
