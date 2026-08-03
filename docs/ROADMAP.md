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
- [x] Control-Scoring, Dimir-Strategie, Sideboard, Benchmark und v2-Validator
- [x] Pflichtvalidator erzeugt Burn, Tokens, Artifacts, Control und Mill
- [x] Fast-Validator prüft drei Token- und drei Control-Matchups
- [x] Control enthält mindestens drei Finisher; Run `30797591719` behält sechs
- [x] Control-Benchmark 85 und Finisher-Zugang 53 %

## Offen – Control und Sideboard

- [ ] matchupabhängige Sideboard-Relevanz im neuen Workflow bestätigen
- [ ] relevante Antworten aus konkretem Gegnerdeck statt nur Archetyp ableiten
- [ ] Wincondition-Zugang nach Stabilisierung messen
- [ ] Stabilisierung bis Zug 4 oder 5 explizit modellieren
- [ ] Control-Basisfortschritt im Matchupmodell an tatsächliche Finisher koppeln

## Offen – globale Qualität

- [ ] Mill-Befund 0 % planfähig / 100 % marginal anhand Rohhänden prüfen
- [ ] Token-Subarchetypen mit separaten Referenzdecks vergleichen
- [ ] Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
- [ ] Finish Density allgemein modellieren
- [ ] belastbare Regressionsbaseline statt `baseline: none`
- [ ] erste vollständig qualifizierte v2-KGB
- [ ] Meta- und Club-Benchmark

## Aktuelle Priorität

1. Workflow der matchupabhängigen Sideboard-Relevanz vollständig auswerten
2. prüfen, dass Control gegen Burn/Tokens/Artifacts kein Graveyard-Hate mehr einwechselt
3. Matchup- und BO3-Änderungen auf unbegründete Regressionen prüfen
4. Mill-Messauffälligkeit anhand der 100 Rohhände untersuchen
5. relevante Control-Antworten aus dem konkreten Gegnerdeck ableiten
6. Token-Subarchetypen separat benchmarken
7. Regressionsbaseline und erste v2-KGB aufbauen

## Definition of Done für den nächsten Zyklus

- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs priorisierte Matchups vorhanden
- Fast-Lauf unter zehn Minuten
- je Deck exakt 100 Hände mit Seed `1701`
- kein `Tormod's Crypt` gegen Burn, Tokens oder Artifacts
- relevante Sideboardkarten werden weiterhin eingewechselt, sofern im Sideboard vorhanden
- BO3-Berichte und Laufzeit zeigen keine unbegründete Regression
- Logbook enthält KGB-Entscheidung, Reflexion und genau einen nächsten Schritt
