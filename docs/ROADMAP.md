# Roadmap

## Development System v2.0

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Shrines bleibt nur optionaler Regressionstest. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten Schritt.

## Erledigt

- [x] Fast-Validierung, Cache, Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] Token-Planerkennung: Go Wide, Value Tokens und Aristocrats
- [x] Strategy Commitment und Token Engine Density
- [x] genau 100 reproduzierbare Starthände je erzeugtem Referenzdeck
- [x] Keepability, Early Play und Planfähigkeit getrennt
- [x] Manafehler dürfen nicht als planfähige Hände gelten
- [x] Control-Scoring, Dimir-Strategie, Sideboard, Benchmark und v2-Validator implementiert
- [x] Pflichtvalidator erzeugt Burn, Tokens, Artifacts, Control und Mill
- [x] Fast-Validator prüft drei Token- und drei Control-Matchups
- [x] veralteten Unknown-Archetype-Test aktualisiert; Run `30796896850` grün

## Offen – Control

- [ ] mindestens drei belastbare Control-Finisher im final optimierten Mainboard sicherstellen
- [ ] Wincondition-Zugang nach Stabilisierung messen
- [ ] relevante Antworten matchupabhängig statt nur über Dichte bewerten
- [ ] Stabilisierung bis Zug 4 oder 5 explizit modellieren

## Offen – globale Qualität

- [ ] Mill-Befund 0 % planfähig / 100 % marginal anhand Rohhänden prüfen
- [ ] Token-Subarchetypen mit separaten Referenzdecks vergleichen
- [ ] Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
- [ ] Finish Density allgemein modellieren
- [ ] erste vollständig qualifizierte v2-KGB erzeugen
- [ ] Meta- und Club-Benchmark aufbauen

## Aktuelle Priorität

1. Workflow der Control-Finisher-Mindestdichte vollständig auswerten
2. falls nötig Optimierer-Guardrail für drei Finisher ergänzen
3. Control-Hände, Early Play, Mana, Benchmark und BO3 gegen Run 45 vergleichen
4. matchupabhängige Control-Antwortabdeckung modellieren
5. Mill-Messauffälligkeit untersuchen
6. Token-Subarchetypen separat benchmarken
7. erste v2-KGB dokumentieren

## Definition of Done für den nächsten Zyklus

- vollständige Testsuite und Fast-Validierung grün
- Burn, Tokens, Artifacts, Control und Mill erzeugt
- sechs priorisierte Matchups und BO3-Berichte vorhanden
- Fast-Lauf unter zehn Minuten
- je Deck exakt 100 Hände mit Seed `1701`
- Control ist legal 60/15
- finales Control-Mainboard enthält mindestens drei Finisher
- Control-Finisher-Zugang ist größer als 0 %
- Early Play, Mana und Matchups zeigen keine unbegründete Regression
- Logbook enthält KGB-Entscheidung und nächsten Schritt
