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

## Offen – Control

- [ ] veralteten Unknown-Archetype-Test aktualisieren und grünen Control-Basislauf bestätigen
- [ ] mindestens drei belastbare Control-Finisher im Mainboard sicherstellen
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

1. Run nach dem Test-Hotfix vollständig auswerten
2. Control-Finisher-Dichte ohne künstliche Schwellenwertverschiebung korrigieren
3. Control-Hände und BO3 erneut prüfen
4. Mill-Messauffälligkeit untersuchen
5. Token-Subarchetypen separat benchmarken
6. erste v2-KGB dokumentieren

## Definition of Done für den nächsten Zyklus

- vollständige Testsuite und Fast-Validierung grün
- Burn, Tokens, Artifacts, Control und Mill erzeugt
- sechs priorisierte Matchups und BO3-Berichte vorhanden
- Fast-Lauf unter zehn Minuten
- je Deck exakt 100 Hände mit Seed `1701`
- Control ist legal 60/15
- Control-Finisher-Befund ist dokumentiert
- keine unbegründeten Regressionen
- Logbook enthält KGB-Entscheidung und nächsten Schritt
