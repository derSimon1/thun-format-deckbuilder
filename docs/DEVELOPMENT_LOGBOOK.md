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

### Lethal-Race-Hartkappung – Run 75

- Commit `c197679978ae117ddc93846a895f0773f3634df0`.
- Workflow `Token Go Wide – Lethal Race Calibration`, ID `30832425136`, fehlgeschlagen; Artefakt `8863583892`.
- Fast-Validierung und Token-Diagnose grün; 307 Tests bestanden, 1 Test scheiterte an einer Monte-Carlo-Rundungsdifferenz von 0,001.
- Die wichtigere fachliche Auswertung widerlegte die harte Kappung: Tokens–Artifacts fiel 76→0 %, Control–Burn sprang 0→100 %.
- Ursache: Eine vollständige Deckelung bei 20 zerstört die zwischen den Archetypen kalibrierte Fortschrittsskala.
- Entscheidung: harte Kappung verwerfen und zuerst korrigieren; kein weiterer Optimierungszyklus vor grünem Gate.
- KGB: keine neue KGB.

## Aktueller Zyklus – Lethal Race Diminishing Returns

- **Ursache:** Lineare Überkill-Wertung ist zu dominant, harte Kappung ist jedoch zu aggressiv und verzerrt archetypenübergreifende Vergleiche.
- **Hypothese:** Schaden bis 20 bleibt linear; darüber erhält zusätzlicher Schaden nur logarithmischen Nutzen. Die Killrate liefert einen kleinen Konsistenzbonus. Dadurch bleibt Tokens gegen Artifacts vergleichbar, während Burns Überkill nicht mehr doppelt zählt.
- **Änderungen:** logarithmisch abnehmender Überkill-Nutzen; robuster Unit-Test direkt auf der Fortschrittsfunktion; Workflow-Run-Name `Token Go Wide – Lethal Race Diminishing Returns`.
- **Erfolg:** vollständige Testsuite, Fast und Diagnose grün; Deck-Hash und Benchmarks unverändert; Tokens–Artifacts bleibt konkurrenzfähig; Control–Burn und Tokens–Burn zeigen plausible Richtung ohne harte 0/100-Artefakte allein durch Skalierung.
- **Rollback:** wenn die archetypenübergreifenden Matchups erneut kippen oder der Burn-Überkill weiterhin praktisch linear wirkt.
- **KGB-Entscheidung vor Push:** keine neue KGB; Diagnosekalibrierung bei fortbestehendem `baseline: none`.

## Nächster ausführbarer Schritt

Den Diminishing-Returns-Fix veröffentlichen und Workflow, Tests, Deck-Hash, Matchups sowie Artefakte vollständig auswerten. Erst danach weiter optimieren.
