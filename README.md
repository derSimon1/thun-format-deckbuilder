# Thun Format Deckbuilder

Ein Deckbuilder und Kalibrierungsprojekt für das Magic Club Thun Clubformat.

## Aktueller Entwicklungsstand

Die aktive Konsolidierung läuft auf `integration/deckbuilder-v3`. Diese Linie verbindet die globale Multi-Archetypen-Kalibrierung aus PR #14 mit dem bereits akzeptierten Meta-Transfer-Audit aus PR #15 und der Pioneer-RDW-Kartenpool-Forschung aus PR #16.

PR #13 (Izzet Prowess) und PR #17 (Pioneer-RDW Challenger) bleiben separate Experimente, bis ihre Arena-Evidenz ausreichend ist. Modellwerte allein ersetzen keine realen Playtests.

## Unterstützte Archetypen

```bash
thun-deckbuilder build burn --colors R
thun-deckbuilder build tokens --colors W
thun-deckbuilder build artifacts --colors U R
thun-deckbuilder build shrines --colors W U B R G
thun-deckbuilder build mill --colors U B
```

Mit `--benchmark` werden archetypische Kernfunktionen, Dichte und weitere Kalibrierungsmetriken geprüft. Opening-Hand-, Goldfish- und Matchup-Simulationen sind Heuristiken und dürfen nicht als reale Winrate interpretiert werden.

## Empirische Evidenz

Arena-Ergebnisse werden getrennt von Modellresultaten dokumentiert. Der aktuelle Mono-White-Token-Test zeigte:

- TOK-A Builder Baseline: 0-3 BO3 / 0-6 Games — als aktiver Deckkandidat verworfen;
- TOK-B Immediate Pressure: 4-2 im dedizierten BO1-Mainboard-Screen — vorläufiger Token-Finalist;
- TOK-C Repeatable Pressure: 3-2 BO1, davon ein Low-Information-Concession-Win — Challenger.

Siehe `docs/reports/ARENA_TOKEN_PLAYTEST_2026-08-06.md` und `research/decks/token_arena_challengers_2026-08-06.json`.

## Repository-Struktur

- `src/thun_deckbuilder/` — Builder, Scoring, Simulation und Audit-Code
- `tests/` — Regressionstests
- `research/` — reproduzierbare Meta- und Challenger-Daten
- `docs/reports/` — aktuelle technische und empirische Auswertungen
- `docs/archive/` — historische Zwischenstände und alte Changelogs
- `config/thun.toml` — verbindliche Formatkonfiguration

## Tests

```bash
python -m pytest
```

## Grundsatz

Champion- oder Generatoränderungen benötigen reproduzierbare technische Evidenz und, wo Deckstärke betroffen ist, reale Arena-Validierung. Ein einzelnes Spiel oder ein hoher Simulationsscore reicht nicht aus.
