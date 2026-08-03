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

## Token-Fokus – erreichte Evidenz

### Paketdiagnose

- [x] Kreatur-Token von Food/Clue/Blood/Treasure getrennt
- [x] echte Outlets von One-Shot-Sacrifice getrennt
- [x] Other-Creature-Death-Payoffs von Self-Death getrennt
- [x] Run 55: 43 breite Rollen-Fehlpositive belegt
- [x] ausreichende Full-Pool-Kapazität für Go Wide, Value und Aristocrats belegt

### Präzise Planrollen

- [x] präzise Tokenrollen eingeführt
- [x] Planerkennung und Eligibility auf zentrale Paketdefinition gestellt
- [x] planabhängige Mindestpakete definiert
- [x] Full-Pool wechselt zu Value Tokens
- [x] Fehlpositive 43 → 0
- [x] Benchmark 90 → 91; Keepability 73 → 77 %; Planfähigkeit 73 → 76 %

### Sparse-Pool-Hotfix

- [x] statische Minimums gegen tatsächliche Poolkapazität begrenzt
- [x] kleine Testdatenbanken erzeugen wieder 60 Karten
- [x] erkannt: neutrale Füller verschlechtern Full-Pool, wenn sie immer zugelassen werden
- [x] Füllerlogik auf echte Gesamtkopienlücke beschränkt
- [x] Tests für Full-Pool-Ausschluss und Sparse-Pool-Zulassung vorbereitet
- [ ] vollständige Testsuite und Fast-Validierung grün bestätigen
- [ ] Full-Pool-Werte mindestens auf Run-56-Niveau bestätigen

## Erfolgskriterien des aktuellen Hotfixes

- [ ] alle Tests grün
- [ ] Fast unter zehn Minuten
- [ ] Sparse-Pool-Generierung erfolgreich
- [ ] Full-Pool-Plan Value Tokens
- [ ] Benchmark mindestens 91
- [ ] 33 echte Materialkopien
- [ ] mindestens 12 wiederholbare Maker
- [ ] 0 breite Rollen-Fehlpositive
- [ ] Keepability mindestens 77 % und Planfähigkeit mindestens 76 %
- [ ] Schaden mindestens 18,97 und Killrate mindestens 66 % im aktuellen Modell
- [ ] andere vier Benchmarks ohne unbegründete Regression

## Nächste Token-Hypothesen nach grünem Hotfix

### A – Value-Payoff-Erkennung

- [ ] reale Mono-White-Karten prüfen, die Token- oder kleine Kreatur-ETBs in Kartenvorteil umwandeln
- [ ] direkte Token-Payoffs von allgemeinem Card Draw trennen
- [ ] keine Rolle erzwingen, falls der legale Pool tatsächlich keinen geeigneten Payoff besitzt

### B – realistische Token-Goldfish-Messung

- [ ] tatsächliche Tokenanzahl je Karte statt pauschal zwei verwenden
- [ ] wiederholbare Quellen über mehrere Züge modellieren
- [ ] Kreatur-Token und Nichtkreatur-Token strikt trennen
- [ ] Boardgröße, Schaden und Killrate gegen Run 56 vergleichen

### C – Matchupmodell

- [ ] Burn-/Artifact-Extremwerte gegen Boardentwicklung und Interaktion prüfen
- [ ] keine Kartenauswahl allein anhand heuristischer Matchup-Prozente verändern

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
6. belastbare Regression-Baseline statt `baseline: none`
7. erste v2-KGB
8. Meta- und Club-Benchmark

## Definition of Done für den aktuellen Token-Meilenstein

- zentrale Token-Paketdefinition in Diagnose, Planerkennung und Komposition identisch
- Full- und Sparse-Pool funktionieren
- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs Matchups
- genau 100 Hände je Deck mit Seed 1701
- Token-Metriken gegen Runs 55–57 verglichen
- keine unbegründete Regression anderer Referenzarchetypen
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
