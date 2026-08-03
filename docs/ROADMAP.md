# Roadmap

## Development System v2.0

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Shrines bleibt nur optionaler Regressionstest. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten Schritt.

## Erledigt

- [x] Fast-Validierung, Cache, Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] genau 100 reproduzierbare Starthände je Referenzdeck
- [x] Keepability, Early Play und Planfähigkeit getrennt
- [x] Manafehler dürfen nicht als planfähige Hände gelten
- [x] Token-Planerkennung: Go Wide, Value Tokens und Aristocrats
- [x] Strategy Commitment und Token Engine Density
- [x] Control-Scoring, Dimir-Strategie, Sideboard, Benchmark und v2-Validator
- [x] fünf Pflichtarchetypen und sechs priorisierte Fast-Matchups
- [x] Control-Benchmark 85, sechs Finisher und 53 % Finisher-Zugang
- [x] Sideboard-Marker als maschinenlesbare Rollen eingeführt
- [x] Root Cause der falschen `Tormod's Crypt`-Einwechslung identifiziert: breite `removal`-Rolle erzeugte einen falschen zweiten Marker

## Aktueller Abschlusszyklus – Sideboard

- [ ] Phrase-first-Klassifikation im PR-Workflow bestätigen
- [ ] pro Archetyp neues `<archetype>-sideboard.json` prüfen
- [ ] kein Graveyard-Hate gegen Burn, Tokens oder Artifacts
- [ ] relevante Sideboardkarten bleiben verfügbar
- [ ] danach unabhängig vom Ergebnis keine weitere Sideboard-Kalibrierung ohne neue externe Evidenz

## Nächste Entwicklungspriorität – Mill

- [ ] echte Mill-Quellen maschinenlesbar erkennen
- [ ] Kartenpoolkapazität für Gegner-Mill bestimmen
- [ ] kapazitätsgeprüfte Mindestdichte an Mill-Quellen definieren
- [ ] Optimierer darf die Mindestdichte nicht entfernen
- [ ] Benchmark `mill_sources` muss reale Builder-Auswahl messen
- [ ] Planfähigkeitsrate muss über 0 % steigen, ohne Keepability/Mana künstlich zu verschlechtern
- [ ] 100 Rohhände auf Enabler, Engine, Interaktion und tote Karten prüfen
- [ ] Mill gegen Tokens sowie mindestens einen Control-/Engine-Plan validieren

## Danach

1. relevante Control-Antworten aus dem konkreten Gegnerdeck statt nur aus Archetyp-Matrix ableiten
2. Token-Subarchetypen als separate Referenzdecks benchmarken
3. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
4. Finish Density allgemein modellieren
5. belastbare Regressionsbaseline statt `baseline: none` einführen
6. erste vollständig qualifizierte v2-KGB erzeugen
7. Meta- und Club-Benchmark aufbauen

## Definition of Done für den Sideboard-Abschlusszyklus

- vollständige Testsuite und Fast-Validierung grün
- Laufzeit unter zehn Minuten
- fünf Referenzarchetypen und sechs Matchups vorhanden
- je Deck exakt 100 Hände mit Seed `1701`
- Diagnoseartefakte enthalten finale Sideboardrollen und Gründe
- `Tormod's Crypt` besitzt nur den Graveyard-Hate-Marker
- kein `Tormod's Crypt` gegen Burn, Tokens oder Artifacts
- Logbook enthält KGB-Entscheidung und Mill als nächsten ausführbaren Schritt

## Definition of Done für den ersten Mill-Zyklus

- reale Mill-Quellen werden anhand Oracle-Text oder einer dedizierten Rolle erkannt
- aktuelle Kartenpoolkapazität ist dokumentiert
- finales 60/15-Deck enthält eine belegte, kapazitätsgeprüfte Mill-Quellendichte
- vollständige Testsuite und Fast-Validierung grün
- genau 100 Mill-Hände mit Seed `1701`
- Planfähigkeit, Keepability, Early Play, Manafehler und tote Karten gegen Run 48 verglichen
- keine Grenzwertsenkung nur zum Bestehen
- genau ein weiterer priorisierter Schritt dokumentiert
