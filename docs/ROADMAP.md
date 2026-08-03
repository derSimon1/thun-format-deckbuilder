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
- [x] Prompt 2.1 mit Artifact-first, Zyklusvertrag und Abschlussreserve
- [x] zentrale Mill-Quellen-Definition und Poolkapazität: 40 Quellen / 120 Kopien
- [x] Mill-Benchmark 80 und 55 % planfähige Hände im Messstand Run 54

## Aktueller Vier-Stunden-Lauf – Token-Fokus

### Ausgangsbefund Run 54

- Token-Plan: Aristocrats
- Benchmark 90
- Keepability/Planfähigkeit 73/73 %
- Strategy Commitment 100 %
- Engine Density 64 %
- Goldfish bis Zug 5: 66 % Killrate
- Matchups: 0 % Burn, 2 % Artifacts, 100 % Mill
- Deckliste enthält starke Food-/Artefakt- und breite Sacrifice-Anteile

### Token-Zyklus 1 – Paketdiagnose

- [x] zentrale Oracle-Text-Signale für Kreatur-Token-Material definieren
- [x] echte wiederholbare Creature-Sacrifice-Outlets von One-Shot-Sacrifice trennen
- [x] Other-Creature-Death-/Drain-Payoffs von Self-Death-Value trennen
- [x] gezielte Regressionstests vorbereiten
- [x] Workflow-Diagnose `tokens/token-packages.json` vorbereiten
- [ ] CI, Laufzeit und Artefakt vollständig auswerten

### Entscheidung nach Zyklus 1

Falls breite Rollen das Paket überzählen:

- [ ] Planerkennung nutzt echte Creature-Material-/Outlet-/Death-Payoff-Signale
- [ ] Aristocrats-Profil erhält kapazitätsgeprüfte Paketminimums
- [ ] Strategy Commitment verwendet dieselbe Paketdefinition
- [ ] Opening-Hand-Klassifikation verwendet dieselbe Paketdefinition
- [ ] Builderausgabe und 100 Hände gegen Run 54 vergleichen

Falls ein vollständiger echter Kern belegt ist:

- [ ] keine künstlichen Paketminimums setzen
- [ ] Token-Combat-/Matchupmodell gegen Burn und Artifacts diagnostizieren
- [ ] echte Boardentwicklung, Opfersequenzen und Payoff-Schaden getrennt messen

### Fachliche Token-Erfolgskriterien

- [ ] legales 60/15-Deck und Fast-Lauf unter zehn Minuten
- [ ] Go Wide, Value Tokens und Aristocrats werden anhand echter Planbestandteile unterschieden
- [ ] Food/Clue/Blood/Treasure zählen nicht automatisch als Kreatur-Token-Material
- [ ] One-Shot-Sacrifice zählt nicht automatisch als Outlet
- [ ] Self-Death-Value zählt nicht automatisch als Death-Payoff
- [ ] Commitment und 100-Hand-Klassifikation verwenden dieselbe Definition wie der Builder
- [ ] Matchupverbesserung wird nicht nur aus einem höheren Benchmark abgeleitet
- [ ] Burn, Artifacts, Control und Mill zeigen keine unbegründeten Regressionen

## Pausierter Mill-Rückkehrpunkt

Der Mill-Messzyklus ist grün abgeschlossen. Nach dem aktuellen Token-Fokus bleibt folgender nächste Mill-Schritt offen:

- [ ] mindestens 18 Mill-Quellen, Ziel 20
- [ ] mindestens 6 echte wiederholbare Engines, Ziel 8
- [ ] Komposition und Optimierer erhalten diese kapazitätsgeprüfte Dichte
- [ ] Benchmark und Opening-Hand-Analyse bleiben auf der zentralen Definition

## Danach

1. Token-Subarchetypen als separate Referenzdecks benchmarken
2. relevante Control-Antworten aus konkreten Gegnerdecks ableiten
3. Mill-Kompositionsschritt abschließen
4. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
5. Finish Density allgemein modellieren
6. belastbare Regression-Baseline statt `baseline: none`
7. erste vollständig qualifizierte v2-KGB
8. Meta- und Club-Benchmark

## Definition of Done für den Token-Diagnosemeilenstein

- zentrale Token-Paketdefinition ist getestet
- reales Deck und legaler Mono-White-Pool werden maschinenlesbar ausgewertet
- vollständige Testsuite und Fast-Validierung grün
- Fast-Lauf unter zehn Minuten
- fünf Referenzarchetypen und sechs priorisierte Matchups
- genau 100 Hände je Deck mit dokumentiertem Seed
- Token-Metriken gegen Run 54 verglichen
- keine unbegründete Regression bei Burn, Artifacts, Control oder Mill
- KGB-Entscheidung und genau ein weiterer priorisierter Schritt dokumentiert
