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
- [x] Run 58: 283 Tests grün, Benchmark 91, Material 33, Fehlpositive 0
- [x] Run 58: Keepability/Planfähigkeit 77/76 %

## Produktionsmessung – Run 59

- [x] Immediate-, Repeatable-, Conditional- und Death-Modi definiert
- [x] konservative Mindestmenge je Creature-Token-Ereignis erkannt
- [x] Produktionsmarker und Diagnoseartefakt implementiert
- [x] Goldfish trennt Kartenkörper, Sofortproduktion und unbedingte Engines
- [x] Conditional-/Death-Ausgabe wird nicht kostenlos erzeugt
- [x] Messkorrektur belegt: Schaden 18,97→10,47; Killrate 66→7 %
- [x] finales Deck enthält 26 bedingte und 7 Death-Maker-Kopien
- [x] aktive unbedingte Engines im Goldfish: 0,00
- [ ] technisches Gate wieder grün herstellen

## Aktueller Hotfix

- [x] Produktionsmetadaten von funktionalen `CardContribution`-Rollen trennen
- [x] Metadaten auf finalen `DeckEntry`-Rollen erhalten
- [x] Regressionstest für Metadata-Filter vorbereiten
- [x] Repeatable-Test auf langfristiges Wachstum statt Fünf-Züge-Vergleich umstellen
- [ ] vollständige Testsuite und Fast-Validierung grün
- [ ] Produktionsdiagnose und konservative Goldfishwerte bestätigen
- [ ] Buildermetriken gegen Run 58 unverändert bestätigen

## Erfolgskriterien des Hotfixes

- [ ] alle Tests grün
- [ ] Fast unter zehn Minuten
- [ ] Builderprofil Value Tokens und Benchmark 91 unverändert
- [ ] Material 33, Fehlpositive 0, Keepability/Planfähigkeit 77/76 %
- [ ] Produktionsmarker im finalen Deck vorhanden
- [ ] Produktionsmodi im Diagnoseartefakt sichtbar
- [ ] Goldfish-Schaden/Killrate bleiben als korrigierte Messwerte dokumentiert
- [ ] andere vier Benchmarks unverändert

## Nächste Token-Hypothese nach grünem Hotfix

### Garantierte Produktionskapazität messen

- [ ] Mono-White-Pool nach garantierter sofortiger, unbedingter wiederholbarer, bedingter und Death-Produktion auswerten
- [ ] unterschiedliche Karten und maximale Kopien je Modus dokumentieren
- [ ] prüfen, ob Value Tokens überhaupt mindestens sechs unbedingte Engines tragen kann
- [ ] erst nach Kapazitätsmessung `token_repeatable_maker` enger definieren
- [ ] automatische Planwahl und Profile auf dieselbe Produktionsdefinition ausrichten

### Danach mögliche Pfade

1. Bei ausreichender garantierter Kapazität Kartenauswahl auf diese Produktion verpflichten.
2. Bei fehlender Value-Kapazität automatische Planwahl auf Go Wide oder Aristocrats zurückführen.
3. Danach Go Wide, Value Tokens und Aristocrats als separate Referenzdecks erzeugen.
4. Matchupmodell erst auf Basis belastbarer Produktionsdaten weiterentwickeln.

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

- Paket- und Produktionsdefinition in Diagnose, Builder und Simulation konsistent
- Full- und Sparse-Pool funktionieren
- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs Matchups
- genau 100 Hände je Deck mit Seed 1701
- Buildermetriken gegen Run 58 unverändert
- Goldfish-Metriken transparent neu kalibriert
- keine unbegründete Regression anderer Referenzarchetypen
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
