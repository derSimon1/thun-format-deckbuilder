# Architecture

## Goal

The application must never allow a deck strategy to accidentally select an illegal card. Legality is therefore resolved before cards enter the knowledge layer.

## Data flow

```text
Scryfall bulk data
    -> SQLite cards + prints
    -> CardDatabase
    -> print-aware legality policy
    -> legal card pool
    -> KnowledgeBase
    -> archetype strategy
    -> generated deck
```

## Key decision: explicit legal card pool

Three alternatives were considered:

1. Filter inside each deck strategy.
2. Make the database return only legal cards.
3. Keep raw database access, but add a central legal-card query used by the KnowledgeBase.

Option 3 was chosen. It keeps the database useful for searches and diagnostics over all cards while ensuring deck generation consumes only a legal pool. It also avoids duplicated legality logic in Burn, Tokens, and future strategies.

## Reprint-aware legality

Legality belongs to printings, not merely to the Oracle card. A card is legal when at least one printing simultaneously satisfies all configured conditions:

- allowed rarity
- paper availability
- not disallowed as digital-only
- set code on the authoritative allow-list
- set code not blocked

This means:

- a Mythic-only card such as Ocelot Pride is rejected;
- a card originally printed as Rare can become legal through a later Common or Uncommon printing;
- an Uncommon printing in an unapproved supplemental set does not make the card legal.

## Configuration

`config/thun.toml` is the sole authoritative format configuration. Earlier JSON configuration fragments were removed because they duplicated or contradicted each other.

The allowed set list is deliberately explicit. Automatic inference from release date or Scryfall `set_type` is unsafe because supplemental products and unusual Standard releases cannot always be classified reliably from those fields alone.

## Testing strategy

Normal tests use a temporary SQLite database containing a small controlled card set. This makes tests:

- fast;
- deterministic;
- independent of a 100+ MB local database;
- suitable for GitHub Actions.

Regression coverage includes Ocelot Pride, legal C/U cards, and Rare-to-Uncommon reprints.

## Deferred work

The following are intentionally not part of this refactor:

- advanced card-text parsing;
- exact token quantity parsing;
- sideboard generation;
- multi-color mana-base construction;
- meta weighting;
- combo graph analysis;
- GUI or web application.

These should be added only after the legal card pool and database update workflow remain stable.
