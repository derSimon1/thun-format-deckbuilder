# Thun Format Deckbuilder

Deckbuilding and legality engine for the Magic Club Thun format.

## Current scope

- SQLite card database built from Scryfall bulk data
- Central legality check across all printings of an Oracle card
- Common/uncommon paper prints from explicitly allowed sets
- Reprint-aware legality
- Mono-red Burn prototype
- Mono-white Tokens prototype
- Reproducible tests using a small temporary SQLite database

## Installation

```bash
python -m pip install -e ".[dev]"
```

## Build the local card database

The generated files are intentionally not stored in Git.

```bash
python scripts/download_scryfall.py
python scripts/build_index.py
```

This creates `data/default_cards.json` and `data/cards.db`.

## Run tests

```bash
pytest
```

The tests do not require the full Scryfall database.

## Check legality

```bash
thun-deckbuilder legal "Ocelot Pride"
thun-deckbuilder legal "Lightning Strike"
```

## Generate decks

```bash
thun-deckbuilder build burn --colors R
thun-deckbuilder build tokens --colors W
```

## Important configuration

`config/thun.toml` is the single authoritative format configuration. The `allowed_sets` list must be reviewed whenever new Standard sets are added.

See `docs/ARCHITECTURE.md` and `docs/MIGRATION.md` for design decisions and upgrade notes.
