# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

### Stabiler Bestätigungsstand

- Commit `2bd921c1688c72d4b5949bd0f93cb65a9d1d206c` beseitigte den Full-Pool-Test-Leak.
- Workflow `30824779542`, Run 69, wurde dreimal vollständig auf demselben Head ausgeführt.
- alle drei Durchgänge grün; jeweils 301 Tests, Fast-Validierung und Token-Diagnose erfolgreich.

### Castability-Zyklus – Run 70

- Commit `94c8430835222b63b40a8b8465ef35df17787526`.
- Workflow `30827014882`, erfolgreich; Artefakt `8861386466`.
- 302 Tests, Fast und Diagnose grün.
- `Warping Wail` wurde wegen nicht unterstützter `{C}`-Kosten ausgeschlossen und durch `Parting Gust` ersetzt.
- Benchmarks 83/96/90/85/80 für Burn/Tokens/Artifacts/Control/Mill.
- Token: 23,58 Schaden, 62 % Killrate, Board 9,20, Keepability/Planfähigkeit 77/77 %.
- KGB: keine neue KGB.

### 23-Land-Experiment – Run 71

- Commit `d50680c828067f9ada586c8bd0564f3b6abcd5d2`.
- Workflow `30827655973`, technisch rot wegen eines noch auf 24 Länder gebundenen Strukturtests; Fast und Diagnose liefen erfolgreich.
- Artefakt `global-calibration-pr-71`, ID `8861699274`.
- fachliches Delta gegen Run 70: Benchmark 96→94; Mana-Screw-Hände 13→16; Early Play T2/T3 94/96→92/94 %; Schaden 23,58→23,66; Killrate 62→63 %; ungenutztes Mana 3,33→3,14.
- Interpretation: minimale Goldfish-Verbesserung bei klar schlechterer Starthand- und Kurvenstabilität. Hypothese widerlegt.
- Entscheidung: 23 Länder werden verworfen; Rückkehr zu 24 Plains und 36 Spells.
- KGB: keine neue KGB.

### Rollback-Bestätigung – Run 72

- Commit `b5e1b0bd1def26a9ce62b24fe0a5ffe12a765e1b`.
- Workflow `30828260897`, erfolgreich; Artefakt `8861942756`.
- 302 Tests, Fast und Diagnose grün.
- Benchmarks wieder 83/96/90/85/80; Token-Paket 36 Maker mit 24 sofortigen, 6 Death-, 3 bedingten und 3 aktivierten Kopien.
- KGB: keine neue KGB.

## Aktueller Zyklus – Immediate Maker Scoring

- **Ursache:** Neun von 36 Maker-Kopien produzieren nicht sofort; Death-, bedingte und aktivierte Maker werden im Go-Wide-Scoring trotz geringerer Zuverlässigkeit noch zu ähnlich zu sofortigen Makern bewertet.
- **Hypothese:** Modusspezifische Abwertungen für Death-, bedingte und aktivierte Produktion erhöhen den Anteil sofortiger Produktion oder verbessern die konkrete Kartenauswahl, ohne Pflichtdichten und andere Archetypen zu regressieren.
- **Änderungen:** direkte Go-Wide-Produktionsanpassung im Kompositionsscore; Regressionstests für alle drei Modi; sprechender Workflow-Run-Name `Token Go Wide – Immediate Maker Scoring`.
- **Erfolg:** vollständige Testsuite, Fast-Validierung und Token-Diagnose grün; sofortige Maker nicht niedriger als 24; Benchmark und Starthandstabilität mindestens auf Run-72-Niveau oder ein klar begründetes positives Deckdelta.
- **Rollback:** bei sinkender Pflichtrollendichte, Benchmark-Regressionssignal oder schlechterer Starthand-/Goldfish-Gesamtwirkung.
- **KGB-Entscheidung vor Push:** keine neue KGB; erst nach Artefaktauswertung.

## Nächster ausführbarer Schritt

Den Immediate-Maker-Scoring-Zyklus veröffentlichen, den sprechend benannten Workflow vollständig auswerten und anhand von Deckliste, Produktionsmodi, Opening Hands, Goldfish und Matchups über Behalten oder Rollback entscheiden.
