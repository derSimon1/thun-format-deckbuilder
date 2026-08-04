# Roadmap

## Token Go Wide

- [x] Go-Wide-Profil und Pflichtdichten
- [x] Full-Pool-Test und drei Bestätigungsläufe
- [x] `{C}`-Castability mit zentraler Zahlungsdefinition und echten Quellen
- [x] 23-Land-Experiment verworfen
- [x] Immediate-Maker-Scoring
- [x] reine Opfer-Outlets entfernt
- [x] Lethal-Race-Modell mit abnehmendem Überkill-Nutzen
- [x] Burn-Stabilisierungsoptionen im Sideboard
- [x] Postboard-Lebensgewinn im Burn-Modell
- [x] Burn-Cuts rollenbasiert absichern
- [x] Arena-Import und 100 Hände final bewerten
- [x] Root-`AGENTS.md` als dauerhafte Repository-Einstiegsanweisung validieren
- [x] Quellenspannung strikter `{C}`-Kosten im Candidate Scoring modellieren
- [x] Engine-Pflicht und Engine-Warnung planabhängig kalibrieren
- [x] Go-Wide-Planfähigkeit an einen bis Zug 2 castbaren Maker binden
- [x] Engine-Pflicht zentral im Opening-Hand-Bericht kontextualisieren
- [x] transformationsgesperrte Rückseiteneffekte aus Sofortrollen entfernen
- [x] Sideboard-Suche über Mehrkopien-Schwellen führen und zielabhängigen
  Lebensgewinn abgrenzen

## Stabiler Stand – Run 78

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate
- Game One Burn/Artifacts/Mill: 0/64/100 %
- Burn Postboard 62 %, modellierte Matchwinrate 48 %
- Burn-Plan: 3 `Dawnbringer Cleric` hinein; 2 `Descendant of Storms`, 1 `Duty Beyond Death` heraus
- Mainboard-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`

## Aktueller Zyklus – Threshold-Aware Sideboarding

1. Sechs reale Ersatzpakete über mehrere Seeds verwerfen: kein Burn-Gewinn.
2. Greedy-Einzelkartenfalle bei drei `Dawnbringer Cleric` korrigieren.
3. Zielabhängigen Lifegain von selbständigem Schutz trennen.
4. Workflow `Token Go Wide – Threshold-Aware Sideboarding` auswerten.

## Prioritäten danach

1. Weitere verzögerte Tokenproduktion (Trigger/Sagas) prüfen.
2. Modellierte Matchups gegen reale Spiele kalibrieren.
3. Burn-/Artifact-Ersatzpaket erst mit präziserer Simulation erneut prüfen.
4. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Trigger- und Saga-Text zentral so segmentieren, dass bedingte oder verzögerte
Tokenproduktion und begrenzte Buffs nicht als sofortige Go-Wide-Effekte gelten.
