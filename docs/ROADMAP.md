# Roadmap

## Token Go Wide

- [x] Go-Wide-Profil und Pflichtdichten
- [x] Full-Pool-Test und drei Bestätigungsläufe
- [x] `{C}`-Castability
- [x] 23-Land-Experiment verworfen
- [x] Immediate-Maker-Scoring
- [x] reine Opfer-Outlets entfernt
- [x] Lethal-Race-Modell mit abnehmendem Überkill-Nutzen
- [x] Burn-Stabilisierungsoptionen im Sideboard
- [ ] Postboard-Lebensgewinn im Burn-Modell abbilden
- [ ] Arena-Import und 100 Hände final bewerten

## Stabiler Stand – Run 77

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate
- Matchups Burn/Artifacts/Mill: 0/64/100 %
- Sideboard: Dawnbringer Cleric, Light of Hope, Lucky Offering, Sanctify, Decommission – jeweils 3
- Mainboard-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`

## Aktueller Zyklus

1. `sideboard_protection`-Dichte im postboard Mainboard erkennen.
2. Bonus ausschließlich anwenden, wenn der Gegner Burn ist.
3. Drei Schutzkarten als ungefähr sechs zusätzliche Lebenspunkte konservativ mit Faktor 3 abbilden.
4. Test: Burn-Winrate steigt, Artifact-Score bleibt identisch.
5. Workflow `Token Go Wide – Postboard Burn Stabilization` nennen.
6. Game One, Deck-Hash, Benchmarks und andere Matchups müssen unverändert bleiben.

## Prioritäten danach

1. Konkreten BO3-Burn-Plan und Kartenwechsel bewerten.
2. Strategy Commitment und Opening Hands prüfen.
3. Anthem-/Combatmodell verbessern.
4. Arena-Import final validieren.
5. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Postboard-Stabilisierungsmodell veröffentlichen und CI sowie BO3-Artefakt vollständig auswerten.
