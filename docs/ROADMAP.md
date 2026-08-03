# Roadmap

## Development System v2.0

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Shrines bleibt optionaler Regressionstest. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten ausführbaren Schritt.

## Erledigt

- [x] Fast-Validierung, Cache, Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] genau 100 reproduzierbare Starthände je Referenzdeck
- [x] Keepability, Early Play und Planfähigkeit getrennt
- [x] Manafehler dürfen nicht als planfähige Hände gelten
- [x] Token-Planerkennung, Strategy Commitment und Token Engine Density
- [x] Control als fünfter Referenzarchetyp
- [x] Control-Benchmark 85, sechs Finisher und 53 % Finisher-Zugang
- [x] fünf Pflichtarchetypen und sechs priorisierte Fast-Matchups
- [x] maschinenlesbare Sideboard-Marker und Diagnoseartefakte
- [x] Phrase-first-Sideboardklassifikation fachlich durch Run-49-Artefakte bestätigt

## Abschluss Sideboard-Zyklus

- [ ] korrigierten Regressionstest im nächsten Workflow bestätigen
- [ ] vollständige Testsuite und Fast-Validierung grün
- [ ] Sideboard-Diagnoseartefakte bleiben vorhanden
- [ ] kein Graveyard-Hate gegen Burn, Tokens oder Artifacts
- [ ] danach Sideboard-Kalibrierung ohne neue externe Evidenz pausieren

## Primäre nächste Entwicklungsphase – Mill

- [ ] Gegner-Mill-Quellen maschinenlesbar erkennen
- [ ] reale Kartenpoolkapazität dokumentieren
- [ ] kapazitätsgeprüfte Mindestdichte definieren
- [ ] Komposition und Optimierer erhalten die Mindestdichte
- [ ] Benchmark und Opening-Hand-Analyse verwenden dieselbe Mill-Definition
- [ ] finales Deck enthält einen realistisch anlaufenden Millplan
- [ ] Planfähigkeit steigt über 0 %, ohne Keepability oder Mana künstlich zu verschlechtern
- [ ] 100 Rohhände auf Mill-Quelle, Engine, Schutz, Interaktion und tote Karten prüfen
- [ ] Mill gegen Tokens und einen Control-/Engine-Plan validieren

## Danach

1. relevante Control-Antworten aus konkreten Gegnerdecks ableiten
2. Token-Subarchetypen als separate Referenzdecks benchmarken
3. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
4. Finish Density allgemein modellieren
5. belastbare Regression-Baseline statt `baseline: none`
6. erste vollständig qualifizierte v2-KGB
7. Meta- und Club-Benchmark

## Definition of Done für den Test-Hotfix

- alle Tests grün
- Fast-Validierung grün und unter zehn Minuten
- fünf Referenzarchetypen und sechs Matchups
- je Deck exakt 100 Hände mit Seed `1701`
- Sideboard-Diagnoseartefakte vorhanden
- Control boardet Disfigure statt Graveyard-Hate gegen Burn und Tokens
- keine ungeeignete Control-Karte gegen Artifacts
- Logbook setzt Mill als genau einen nächsten Schritt

## Definition of Done für den ersten Mill-Zyklus

- eindeutige Definition einer Gegner-Mill-Quelle
- Kartenpoolkapazität vor Mindestwert dokumentiert
- keine Schwellenwertsenkung nur zum Bestehen
- legales 60/15-Deck mit belegter Mill-Quellendichte
- vollständige Testsuite und Fast-Validierung grün
- genau 100 Mill-Hände mit Seed `1701`
- Vergleich gegen Run 48: Planfähigkeit, Keepability, Early Play, Manafehler, tote Karten und Benchmark
- genau ein weiterer priorisierter Schritt dokumentiert
