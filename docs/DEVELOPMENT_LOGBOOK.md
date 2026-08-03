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
- KGB: keine neue KGB.

### Remove Sacrifice Outlets – Run 74

- Commit `9b4cdb57e92f3753d434fef8c522ed0885aaacd0`.
- Workflow `Token Go Wide – Remove Sacrifice Outlets`, ID `30831547747`, erfolgreich; Artefakt `8863249096`.
- 306 Tests, Fast und Diagnose grün.
- Benchmarks stabil bei 83/98/90/85/80; reine Opfer-Outlets 2→0.
- echtes Token-Material 33→35, sofortige Maker 30, Multi-Maker 22, Anthems 7.
- Opening Hands 77 % Keepability und Planfähigkeit; Goldfish 24,94 Schaden, 66 % Killrate, Board 9,10.
- Matchups Tokens gegen Burn/Artifacts/Mill: 0/76/100 %.
- KGB: keine neue KGB; `baseline: none` besteht fort.

## Aktueller Zyklus – Lethal Race Calibration

- **Ursache:** Der Matchup-Simulator bewertet durchschnittlichen Schaden linear. Burns 45,99 Schaden entsprechen dadurch 230 % Fortschritt, obwohl 20 Schaden bereits lethal sind. Überkill dominiert das Matchup stärker als Konsistenz und Interaktion.
- **Hypothese:** Kappen des Schadensfortschritts bei 20 und Ergänzen der tatsächlichen Killrate ergibt ein differenzierteres Rennmodell. Das Deck selbst und alle Benchmark-, Opening-Hand- und Goldfish-Metriken müssen unverändert bleiben.
- **Änderungen:** gemeinsame Lethal-Race-Funktion für Burn und Tokens; Regressionstests gegen Überkill-Doppelzählung und für Killraten-Konsistenz; Workflow-Run-Name `Token Go Wide – Lethal Race Calibration`.
- **Erfolg:** vollständige Testsuite, Fast und Diagnose grün; Deck-Hash und Deckmetriken unverändert; Burn-Matchup nicht mehr allein durch irrelevanten Überkill determiniert; andere Matchups plausibel und ohne Regressionssignal.
- **Rollback:** wenn das Modell langsamere Decks trotz klar schlechter Killrate bevorzugt oder Deck-/Benchmarkwerte unerwartet verändert.
- **KGB-Entscheidung vor Push:** keine neue KGB, da nur das Diagnosemodell kalibriert wird und `baseline: none` fortbesteht.

## Nächster ausführbarer Schritt

Die Lethal-Race-Kalibrierung veröffentlichen und Workflow, vollständige Tests, Deck-Hash, Matchups sowie alle Artefakte auswerten. Danach evidenzbasiert behalten oder zurückrollen.
