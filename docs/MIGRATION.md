# Migration from the previous project state

## Main changes

- Central legality is now used by the deckbuilding flow.
- `KnowledgeBase.load()` loads only legal cards.
- `CardDatabase` now exposes `get_prints()`, `get_all_legal_cards()`, and `is_card_legal_by_name()`.
- `config/thun.toml` replaces the conflicting JSON rule files.
- Tests create their own temporary database.
- Generated data files and accidental empty files were removed.
- A command-line entry point was added.

## Files intentionally removed

- `config/archetypes.json` — malformed and not used by the current strategy system
- `config/thun_rules.json` — placeholder values and duplicate rules
- `config/allowed_sets.json` — merged into `thun.toml`
- `config/card_tags.json` — unused placeholder
- accidental root files named `from`, `import`, `analyze_card`, `6`, and `thun_deckbuilder.card_analyzer`
- generated or empty data files

## Local database

Your existing `data/cards.db` can still be used. Keep it outside Git and copy it into the new project under `data/cards.db`, or rebuild it with the scripts.

## Verification

```bash
python -m pip install -e ".[dev]"
pytest
thun-deckbuilder legal "Ocelot Pride"
thun-deckbuilder legal "Lightning Strike"
```

Expected legality results:

- Ocelot Pride: not legal
- Lightning Strike: legal, provided the database includes its allowed C/U printing
