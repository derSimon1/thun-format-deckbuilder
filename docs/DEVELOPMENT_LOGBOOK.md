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
- `Warping Wail` wurde wegen nicht unterstützter `{C}`-Kosten ausgeschlossen und durch `Parting Gust` ersetzt.
- Benchmarks 83/96/90/85/80 für Burn/Tokens/Artifacts/Control/Mill.
- KGB: keine neue KGB.

### 23-Land-Experiment und Rollback – Runs 71–72

- 23 Länder verbesserten Schaden und Killrate nur minimal, verschlechterten aber Benchmark, Mana-Screw und Early Play deutlich.
- Commit `b5e1b0bd1def26a9ce62b24fe0a5ffe12a765e1b` stellte 24 Plains wieder her.
- Workflow `30828260897`, Run 72, erfolgreich; Artefakt `8861942756`.
- KGB: keine neue KGB.

### Immediate-Maker-Scoring – Run 73

- Commit `0ad7852eeba872eedf2eb77dc7d69e5e9cd273ee`.
- Workflow `Token Go Wide – Immediate Maker Scoring`, ID `30830854931`, erfolgreich; Artefakt `8862990345`.
- 305 Tests, Fast und Diagnose grün.
- Benchmarks: Burn 83, Tokens 98, Artifacts 90, Control 85, Mill 80; keine Regression.
- Produktionsmodi: sofortige Maker 24→30, bedingte 3→0, aktivierte 3→0, Death 6→3.
- Token-Material 36→33; zwei Kopien `Witch's Oven` wurden als reine Opfer-Outlets gewählt.
- Interpretation: Kernhypothese klar bestätigt, aber ein neuer planfremder Auswahlfehler wurde sichtbar.
- KGB: keine neue KGB, da `baseline: none` fortbesteht und der Outlet-Fehler zuerst korrigiert wird.

## Aktueller Zyklus – Remove Sacrifice Outlets

- **Ursache:** Reine Opfer-Outlets wie `Witch's Oven` erfüllen keinen Go-Wide-Hauptplan und verdrängen Kreatur-Token-Maker.
- **Hypothese:** Planabhängige Kandidatenfilterung entfernt reine Opfer-Outlets aus Go Wide, erhält sie aber für Aristocrats. Dadurch steigt das echte Token-Material ohne Verlust der Run-73-Verbesserungen.
- **Änderungen:** reine Opfer-Outlets nach Planerkennung für Go Wide ausschließen; Regressionstest gegen ein Food-Outlet; Workflow-Run-Name `Token Go Wide – Remove Sacrifice Outlets`.
- **Erfolg:** vollständige Testsuite, Fast und Diagnose grün; Outlet-Kopien 0; Material mindestens 33, sofortige Maker mindestens 30, Token-Benchmark mindestens 98 und andere Benchmarks stabil.
- **Rollback:** bei Benchmark-, Opening-Hand- oder Goldfish-Gesamtregression ohne kompensierenden fachlichen Gewinn.
- **KGB-Entscheidung vor Push:** keine neue KGB; Entscheidung nach Artefaktauswertung.

## Nächster ausführbarer Schritt

Den Outlet-Filter veröffentlichen und anhand des sprechend benannten Workflows, der Deckliste sowie Produktions-, Opening-Hand-, Goldfish- und Matchup-Metriken vollständig bewerten.
