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
- [x] Trigger-, Saga-, Modal- und Anthem-Kontext bis in Goldfish-Dauersemantik
  vereinheitlichen

## Stabiler Stand – Run 78

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate
- Game One Burn/Artifacts/Mill: 0/64/100 %
- Burn Postboard 62 %, modellierte Matchwinrate 48 %
- Burn-Plan: 3 `Dawnbringer Cleric` hinein; 2 `Descendant of Storms`, 1 `Duty Beyond Death` heraus
- Mainboard-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`

## Aktueller Zyklus – Context-Gated Effects

1. Triggerkontext über Folgesätze und modale Bullets bewahren.
2. Read-ahead von verzögerten Saga-Kapiteln unterscheiden.
3. begrenzte/aktivierte Buffs aus globalen Anthems entfernen.
4. temporäre Anthems im Goldfish am Zugende auslaufen lassen.

## Prioritäten danach

1. Zusätzliche Cast-Kosten und Boardverbrauch im Token-Goldfish modellieren.
2. Bedingte/dead-on-board Kandidaten unter korrekter Semantik neu gewichten.
3. Modellierte Matchups gegen reale Spiele kalibrieren.
4. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Zusätzliche Opferkosten wie bei `Duty Beyond Death` zentral erkennen und im
Token-Goldfish nur bei vorhandenem, tatsächlich verbrauchtem Board bezahlen.
