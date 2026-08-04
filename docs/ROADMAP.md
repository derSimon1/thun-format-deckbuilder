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

## Stabiler Stand – Run 78

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate
- Game One Burn/Artifacts/Mill: 0/64/100 %
- Burn Postboard 62 %, modellierte Matchwinrate 48 %
- Burn-Plan: 3 `Dawnbringer Cleric` hinein; 2 `Descendant of Storms`, 1 `Duty Beyond Death` heraus
- Mainboard-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`

## Aktueller Zyklus – Early Maker Path

1. Die 23 marginalen Hände nach tatsächlicher Ursache clustern.
2. Planfähige Hände auf reale T1-bis-T3-Sequenzen gegenprüfen.
3. Go Wide nur mit bis Zug 2 castbarem Maker als planfähig werten.
4. Workflow `Token Go Wide – Early Maker Path` und Artefakt auswerten.

## Prioritäten danach

1. Engine-Pflicht im Opening-Hand-Bericht planabhängig ausweisen.
2. Opening-Hand-Klassifikation und Builderausgabe weiter abgleichen.
3. Anthem-/Combatmodell verbessern.
4. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Die planabhängige Engine-Pflicht zentralisieren und im
`OpeningHandPlanReport` explizit als required/optional ausweisen, ohne den
rohen Engine-Zugang zu verbergen.
