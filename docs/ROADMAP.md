# Roadmap

## Development System v2.0 / Prompt 2.1

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
- [x] Phrase-first-Sideboardklassifikation durch Run 50 bestätigt
- [x] kein Graveyard-Hate gegen Burn, Tokens oder Artifacts
- [x] Prompt 2.1 mit Artifact-first, Zyklusvertrag und Abschlussreserve vorbereitet

## Nächster Drei-Stunden-Lauf – Primärziel Mill

### Session-Start, maximal 20 Minuten

- [ ] Branch-/PR-Head, Mergeability und aktive CI prüfen
- [ ] Run 50 als technischen Ausgangsstand bestätigen
- [ ] aktuelles Mill-Artefakt und 100 Rohhände auswerten
- [ ] Zyklusvertrag mit Erfolg, Invarianten, Abbruch und Zeitschätzung festhalten

### Mill-Zyklus 1 – Definition und Kapazität

- [ ] zentrale Definition einer Gegner-Mill-Quelle erstellen
- [ ] feste, skalierende und wiederholbare Mill-Quellen unterscheiden
- [ ] legalen Dimir-Kartenpool nach der zentralen Definition auswerten
- [ ] maximal verfügbare Kopien und Kurvenverteilung dokumentieren
- [ ] Mindestdichte erst nach der Kapazitätsanalyse festlegen

### Mill-Zyklus 2 – Komposition und Optimierer

- [ ] dedizierte Mill-Quellenrolle oder gleichwertigen maschinenlesbaren Marker einführen
- [ ] Mill-Profil erhält kapazitätsgeprüfte Mindestdichte
- [ ] Optimierer darf die Startdichte nicht unterschreiten
- [ ] Eligibility bevorzugt echte Millquellen, ohne Schutz und Interaktion vollständig auszuschließen
- [ ] gezielte Regressionstests für `target player mills`, `target opponent mills`, wiederholbare und skalierende Quellen

### Mill-Zyklus 3 – Gemeinsame Messdefinition

- [ ] Benchmark `mill_sources` nutzt dieselbe zentrale Definition
- [ ] Opening-Hand-Analyse nutzt dieselbe Definition
- [ ] Fast-Validator schreibt Mill-Quellen-Diagnose mit Namen, Mengen und Kategorie
- [ ] genau 100 Hände mit Seed `1701`
- [ ] Vergleich gegen Run 50

### Fachliche Erfolgskriterien

- [ ] legales 60/15-Deck
- [ ] finales Mainboard besitzt eine belegte Mill-Quellendichte
- [ ] Benchmark meldet nicht länger 0 Mill-Quellen
- [ ] Planfähigkeit steigt über 0 %
- [ ] fehlender Enabler-/Payoff-Zugang sinkt deutlich unter 72 %
- [ ] Keepability und Manafehler verschlechtern sich nicht unbegründet
- [ ] Deck bleibt nicht überwiegend Draw/Counter/Removal ohne Wincondition
- [ ] Mill gegen Tokens und mindestens einen Control-/Engine-Plan geprüft

### Fallback innerhalb des Entwicklungsbudgets, maximal 20 Minuten

Falls der legale Kartenpool die geplante Mindestdichte nicht ermöglicht:

- [ ] exakte Poolkapazität dokumentieren
- [ ] keinen künstlichen Mindestwert setzen
- [ ] Eligibility-, Oracle-Text- oder Rollenweitergabe als isolierte Ursache bestimmen
- [ ] produktiven No-Change-Zyklus mit genau einem nächsten Schritt abschließen

### Abschlussreserve, mindestens 30 Minuten

- [ ] letzter Workflow vollständig beendet
- [ ] Jobs und Logs einmal vollständig gelesen
- [ ] Artefakt einmal heruntergeladen und maschinenlesbar ausgewertet
- [ ] Evidenztabelle vorher/nachher/Delta/Interpretation/Confidence
- [ ] Logbook, Roadmap und KGB-Entscheidung aktualisiert
- [ ] kein neuer Zyklus mehr begonnen

## Danach

1. relevante Control-Antworten aus konkreten Gegnerdecks ableiten
2. Token-Subarchetypen als separate Referenzdecks benchmarken
3. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
4. Finish Density allgemein modellieren
5. belastbare Regression-Baseline statt `baseline: none`
6. erste vollständig qualifizierte v2-KGB
7. Meta- und Club-Benchmark

## Definition of Done für den ersten Mill-Meilenstein

- zentrale Mill-Quellen-Definition in Builder, Optimierer, Benchmark und Handanalyse identisch
- Kartenpoolkapazität dokumentiert
- keine Grenzwertsenkung nur zum Bestehen
- vollständige Testsuite und Fast-Validierung grün
- Fast-Lauf unter zehn Minuten
- fünf Referenzarchetypen und sechs priorisierte Matchups
- genau 100 Hände je Deck mit dokumentiertem Seed
- Mill-Metriken gegen Run 50 verglichen
- keine unbegründete Regression bei Burn, Tokens, Artifacts oder Control
- genau ein weiterer priorisierter Schritt dokumentiert
