# Roadmap

## Development System v2.0 / Prompt 2.1

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill.

## Token Go Wide

- [x] Go-Wide-Profil und kapazitätsgeprüfte Mindestdichten
- [x] drei grüne Full-Pool-Bestätigungsläufe
- [x] `{C}`-Castability korrigiert
- [x] 23-Land-Variante gemessen und verworfen
- [x] Immediate-Maker-Scoring verbessert
- [x] reine Opfer-Outlets entfernt
- [x] Lethal-Race-Modell mit abnehmendem Überkill-Nutzen kalibriert
- [ ] Burn-Stabilisierung im Sideboard ergänzen
- [ ] Arena-Import und 100 Hände final bewerten

## Aktueller stabiler Stand – Run 76

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Kreatur-Token-Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, T2/T3 94/96 %
- Goldfish 24,94 Schaden, 66 % Killrate, Board 9,10
- Matchups Burn/Artifacts/Mill: 0/64/100 %
- Deck-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`
- Sideboard bisher: 15 Artifact-/Enchantment-Antworten, keine Burn-Stabilisierung

## Aktueller Zyklus

1. Token-Schutzregel um präzise Lebensgewinn- und Schadensverhinderungsphrasen ergänzen.
2. Diese Optionen über redundante Artifact-/Enchantment-Antworten priorisieren.
3. Maschinenlesbaren Marker `sideboard_protection` beibehalten, damit BO3 sie gegen Burn erkennt.
4. Sideboard-Auswahl mit Regressionstest absichern.
5. Workflow `Token Go Wide – Burn Stabilization Sideboard` nennen.
6. Mainboard-Hash, Benchmarks und Kernmetriken müssen unverändert bleiben.

## Prioritäten danach

1. BO3-Burn-Plan und konkrete Kartenwechsel auswerten.
2. Strategy Commitment und Opening-Hand-Klassifikation prüfen.
3. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
4. Arena-Import und 100 Hände final bewerten.
5. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Burn-Stabilisierungsregel veröffentlichen, den sprechend benannten Workflow samt Sideboard- und BO3-Artefakten vollständig auswerten und danach behalten oder zurückrollen.
