# Roadmap

## Development System v2.0 / Prompt 2.1

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten ausführbaren Schritt.

## Globale Grundlagen

- [x] Fast-Validierung und Cache
- [x] genau 100 reproduzierbare Starthände je Deck, Seed 1701
- [x] Opening-Hand-, Goldfish-, Benchmark-, Matchup- und BO3-Berichte
- [x] Manafehler-Invariante
- [x] Control als fünfter Referenzarchetyp, Benchmark 85
- [x] Phrase-first-Sideboardklassifikation und Diagnoseartefakte
- [x] zentrale Mill-Quellendefinition und Poolkapazität

## Token-Fokus – aktueller Stand

### Diagnose abgeschlossen

- [x] Kreatur-Token von Food/Clue/Blood/Treasure getrennt
- [x] echte Outlets von One-Shot-Sacrifice getrennt
- [x] Other-Creature-Death-Payoffs von Self-Death getrennt
- [x] Run 55: 43 Rollen-Fehlpositive belegt
- [x] Full-Pool-Kapazität für alle drei Token-Pläne belegt

### Präzise Planrollen – Produktionsbefund Run 56

- [x] präzise Rollen eingeführt
- [x] Planerkennung und Eligibility auf zentrale Paketdefinition gestellt
- [x] planabhängige Mindestpakete definiert
- [x] Full-Pool-Deck wechselt zu Value Tokens
- [x] breite Rollen-Fehlpositive 43 → 0
- [x] Material 14 → 33; wiederholbare Maker 12
- [x] Benchmark 90 → 91; Keepability 73 → 77 %; Planfähigkeit 73 → 76 %
- [ ] Testgate wieder grün herstellen

### Aktueller Hotfix

- [x] tatsächliche Rollen-Kapazität je Candidate-Pool berechnen
- [x] nur unerreichbare Sparse-Pool-Minimums begrenzen
- [x] generische kleine Kreaturen als niedrig priorisierte Füller zulassen
- [x] Produktionsziele bei ausreichender Kapazität unverändert lassen
- [ ] vollständige Testsuite und Fast-Validierung bestätigen
- [ ] Full-Pool-Deck und Token-Artefakte gegen Run 56 vergleichen

### Nach grünem Hotfix anhand Evidenz priorisieren

Option A – **fehlender Value-Payoff**

- [ ] klären, warum die zentrale Definition 0 verfügbare `token_value_payoff`-Karten meldet
- [ ] Oracle-Phrasen gegen reale Mono-White-Karten prüfen
- [ ] keine Rolle erzwingen, falls der Pool tatsächlich keinen direkten Value-Payoff enthält

Option B – **realistische Token-Goldfish-Messung**

- [ ] tatsächliche Tokenanzahl je Karte statt pauschal zwei verwenden
- [ ] wiederholbare Quellen über Züge getrennt modellieren
- [ ] Kreatur-Token und Nichtkreatur-Token strikt trennen
- [ ] Schaden/Boardgröße gegen Run 56 vergleichen

Option C – **Matchupmodell**

- [ ] Burn-/Artifact-Extremwerte gegen Boardentwicklung und Interaktion prüfen
- [ ] keine Matchupschwellen allein anhand heuristischer Prozentwerte ändern

## Pausierter Mill-Rückkehrpunkt

- [ ] mindestens 18 Mill-Quellen, Ziel 20
- [ ] mindestens 6 echte Engines, Ziel 8
- [ ] Komposition und Optimierer erhalten diese Dichte
- [ ] 100 Hände und Benchmark erneut vergleichen

## Spätere Schritte

1. Go Wide, Value Tokens und Aristocrats als separate Referenzdecks erzeugen
2. relevante Control-Antworten aus konkreten Gegnerdecks ableiten
3. Mill-Kompositionsschritt abschließen
4. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
5. Finish Density allgemein modellieren
6. belastbare Regressionsbaseline statt `baseline: none`
7. erste v2-KGB
8. Meta- und Club-Benchmark

## Definition of Done für den aktuellen Hotfix

- alle Tests grün
- Fast-Validierung unter zehn Minuten
- fünf Referenzarchetypen und sechs Matchups
- Value-Tokens-Deck legal 60/15
- mindestens 10 echte Material- und 6 wiederholbare Maker-Kopien
- 0 breite planprägende Fehlpositive
- andere Benchmarks ohne unbegründete Regression
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
