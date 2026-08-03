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

## Token-Fokus – Buildermeilenstein

- [x] Kreatur-Token von Food/Clue/Blood/Treasure getrennt
- [x] echte Outlets von One-Shot-Sacrifice getrennt
- [x] Other-Creature-Death-Payoffs von Self-Death getrennt
- [x] 43 breite Rollen-Fehlpositive entfernt
- [x] präzise Planrollen und planabhängige Mindestpakete
- [x] Full-Pool wechselt zu Value Tokens
- [x] Sparse-Pool-Ziele kapazitätsgeprüft
- [x] neutrale Füller nur bei echter Kopienlücke
- [x] Benchmark 91, Material 33, Fehlpositive 0
- [x] Keepability/Planfähigkeit 77/76 %

## Produktionsmessung – Run 60 grün

- [x] Immediate-, Repeatable-, Conditional- und Death-Modi
- [x] konservative Mindestmenge je Produktionseffekt
- [x] Produktionsmarker von Funktionsrollen getrennt
- [x] Goldfish trennt Kartenkörper, Sofortproduktion und unbedingte Engines
- [x] Conditional-/Death-Ausgabe wird nicht kostenlos erzeugt
- [x] 295 Tests und Fast-Validierung grün
- [x] Buildermetriken gegenüber Run 58 unverändert
- [x] Produktionsartefakt: 4 Immediate, 0 Repeatable, 21 Conditional, 8 Death
- [x] Goldfish neu kalibriert: 14,66 Schaden, 27 % Killrate, Boardgröße 5,30

## Aktueller Zyklus – Mono-White-Produktionskapazität

- [x] deduplizierte Produktionskapazitätsfunktion vorbereiten
- [x] Off-Color-, Land- und zu teure Karten filtern
- [x] unterschiedliche Karten je Modus zählen
- [x] maximale Kopien je Modus berechnen
- [x] konservative Mindestoutput-Kapazität je Modus berechnen
- [x] Diagnoseartefakt erweitern
- [x] Regressionstest vorbereiten
- [ ] vollständige CI und Artefakte auswerten

## Erfolgskriterien Kapazitätszyklus

- [ ] alle Tests grün
- [ ] Fast unter zehn Minuten
- [ ] Builderprofil, Benchmark 91 und Deck-Hash unverändert
- [ ] 100 Hände weiterhin 77/76 %
- [ ] Goldfish weiterhin 14,66 Schaden und 27 % Killrate im aktuellen Modell
- [ ] Poolkapazität für Immediate, Repeatable, Conditional und Death dokumentiert
- [ ] andere vier Benchmarks unverändert

## Entscheidung nach der Kapazitätsmessung

### Bei mindestens sechs verfügbaren unbedingten Repeatable-Kopien

- [ ] `token_repeatable_maker` ausschließlich dem Produktionsmodus `repeatable` zuweisen
- [ ] Value-Profil weiterhin mindestens 6/8 echte Engines verlangen
- [ ] Planerkennung dieselbe Definition verwenden lassen
- [ ] Builder, Diagnose, 100 Hände und Goldfish erneut vergleichen

### Bei weniger als sechs verfügbaren unbedingten Repeatable-Kopien

- [ ] Value Tokens nicht künstlich erzwingen
- [ ] Go Wide und Aristocrats nach garantierter Produktions- und Paketkapazität vergleichen
- [ ] automatische Planwahl auf den bestversorgten belastbaren Plan umstellen

## Danach

1. Go Wide, Value Tokens und Aristocrats als separate Referenzdecks erzeugen.
2. Matchupmodell erst auf belastbaren Produktionsdaten weiterentwickeln.
3. Mill-Kompositionsschritt mit 18 Quellen und 6 echten Engines abschließen.
4. relevante Control-Antworten aus konkreten Gegnerdecks ableiten.
5. belastbare Regression-Baseline statt `baseline: none`.
6. erste v2-KGB und Club-/Meta-Benchmark.

## Definition of Done für den aktuellen Token-Meilenstein

- Paket- und Produktionsdefinition in Diagnose, Builder und Simulation konsistent
- Full- und Sparse-Pool funktionieren
- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs Matchups
- genau 100 Hände je Deck mit Seed 1701
- Buildermetriken unverändert
- Produktionskapazität evidenzbasiert dokumentiert
- keine unbegründete Regression anderer Referenzarchetypen
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
