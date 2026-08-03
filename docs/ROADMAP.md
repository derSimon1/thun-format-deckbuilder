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

## Token-Fokus – Buildermeilenstein erreicht

- [x] Kreatur-Token von Food/Clue/Blood/Treasure getrennt
- [x] echte Outlets von One-Shot-Sacrifice getrennt
- [x] Other-Creature-Death-Payoffs von Self-Death getrennt
- [x] 43 breite Rollen-Fehlpositive diagnostiziert und entfernt
- [x] präzise Planrollen und planabhängige Mindestpakete
- [x] Full-Pool wechselt von Aristocrats zu Value Tokens
- [x] Sparse-Pool-Ziele kapazitätsgeprüft
- [x] neutrale Füller nur bei echter Kopienlücke
- [x] Run 58: 283 Tests grün, Fast unter vier Minuten
- [x] Run 58: Benchmark 91, Material 33, wiederholbare Maker 12, Fehlpositive 0
- [x] Run 58: Keepability/Planfähigkeit 77/76 %

## Aktueller Token-Zyklus – realistische Produktion

- [x] Immediate-, Repeatable-, Conditional- und Death-Modi definieren
- [x] konservative Mindestmenge je Creature-Token-Ereignis erkennen
- [x] stabile Produktionsmarker im finalen Deck vorbereiten
- [x] Token-Diagnose um Modus, Menge und Kartennamen erweitern
- [x] Goldfish trennt Kartenkörper, Sofortproduktion und unbedingte Engines
- [x] Conditional-/Death-Ausgabe wird im leeren Solitaire nicht automatisch erzeugt
- [x] Regressionstests für 1 vs 2 Tokens, Death, Conditional, Engine und Kartenkörper vorbereiten
- [ ] vollständige CI und Artefakte auswerten

## Erfolgskriterien Produktionszyklus

- [ ] alle Tests grün
- [ ] Fast unter zehn Minuten
- [ ] Builderdeck und Benchmark 91 unverändert
- [ ] Material 33, wiederholbare Maker 12, Fehlpositive 0
- [ ] Opening-Hand-Werte unverändert
- [ ] Diagnose nennt Kopien je Produktionsmodus
- [ ] Goldfish meldet Boardgröße und aktive Engines
- [ ] Schaden/Killrate werden als Messkorrektur interpretiert, nicht als automatische Deckregression
- [ ] andere vier Benchmarks unverändert

## Danach nach Artefaktevidenz

### A – Kartenauswahl an garantierter Produktion ausrichten

- [ ] Anteil garantiert sofortiger und unbedingter wiederholbarer Produktion bewerten
- [ ] Conditional-/Death-lastige Listen nicht über nominale Maker-Dichte überschätzen
- [ ] nur bei belegter Unterversorgung Scoring/Komposition ändern

### B – separate Token-Referenzdecks

- [ ] Go Wide, Value Tokens und Aristocrats jeweils erzwungen erzeugen
- [ ] Paketdichte, 100 Hände, Goldfish und Matchups getrennt vergleichen
- [ ] automatische Planwahl gegen die drei Referenzdecks validieren

### C – Matchupmodell

- [ ] Burn-/Artifact-Extremwerte gegen Boardentwicklung und Interaktion prüfen
- [ ] keine Kartenauswahl allein anhand heuristischer Matchup-Prozente verändern

## Pausierter Mill-Rückkehrpunkt

- [ ] mindestens 18 Mill-Quellen, Ziel 20
- [ ] mindestens 6 echte Engines, Ziel 8
- [ ] Komposition und Optimierer erhalten diese Dichte
- [ ] 100 Hände und Benchmark erneut vergleichen

## Spätere Schritte

1. relevante Control-Antworten aus konkreten Gegnerdecks ableiten
2. Mill-Kompositionsschritt abschließen
3. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
4. Finish Density allgemein modellieren
5. belastbare Regression-Baseline statt `baseline: none`
6. erste v2-KGB
7. Meta- und Club-Benchmark

## Definition of Done für den aktuellen Token-Meilenstein

- zentrale Paket- und Produktionsdefinition in Diagnose, Builder und Simulation identisch
- Full- und Sparse-Pool funktionieren
- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs Matchups
- genau 100 Hände je Deck mit Seed 1701
- Buildermetriken gegen Run 58 unverändert
- Goldfish-Metriken transparent neu kalibriert
- keine unbegründete Regression anderer Referenzarchetypen
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
