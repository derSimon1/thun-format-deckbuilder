# Roadmap

## Development System v2.0 / Prompt 2.1

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill.

## Token-Grundlagen

- [x] Kreatur-Token von Nichtkreatur-Tokens getrennt
- [x] echte Outlets und Death-Payoffs getrennt
- [x] Immediate-, Conditional-, Death-, Activated- und Repeatable-Produktion getrennt
- [x] Goldfish auf Produktionsmodi umgestellt
- [x] Mono-White-Poolkapazität gemessen
- [x] Value-Mindestdichte automatischer Engines als unerreichbar widerlegt

## Token Go Wide

- [x] Go-Wide-Planwahl auf sofortige Maker, Multi-Maker und Anthems ausgerichtet
- [x] Go-Wide-Profil mit kapazitätsgeprüften Mindestdichten
- [x] drei vollständige grüne Bestätigungsläufe auf demselben Head
- [x] explizite `{C}`-Kosten ohne farblose Quellen aus der Komposition ausgeschlossen
- [x] 23-Land-Variante gemessen und wegen schlechterer Stabilität verworfen
- [x] bedingte und aktivierte Maker durch modusspezifisches Scoring entfernt
- [x] reine Opfer-Outlets aus Go Wide entfernt
- [ ] Lethal-Race-Modell ohne Überkill-Doppelzählung kalibrieren
- [ ] Arena-Import und 100 Hände final bewerten

## Aktuelle Pflichtdichten

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems

## Run-74-Evidenz

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Kreatur-Token-Maker, 30 sofortige Maker, 22 Multi-Maker und 7 Anthems
- reine Opfer-Outlets: 0
- Keepability/Planfähigkeit 77/77 %, Early Play T2/T3 94/96 %
- Goldfish 24,94 Schaden, 66 % Killrate, Board 9,10
- Matchups Burn/Artifacts/Mill: 0/76/100 %
- Burn erreicht im Goldfish 45,99 Durchschnittsschaden und 98 % Killrate; das bisherige Matchupmodell zählt den Überkill linear als 230 % Fortschritt

## Aktueller Zyklus

1. Schadensfortschritt für Burn und Tokens bei lethal 20 deckeln.
2. Killrate als Konsistenzkomponente in den Rennfortschritt aufnehmen.
3. Überkill- und Killraten-Regressionsfälle testen.
4. Workflow sichtbar `Token Go Wide – Lethal Race Calibration` benennen.
5. Deck-Hash, Benchmarks und Deckmetriken müssen unverändert bleiben; nur das Diagnosemodell darf sich ändern.

## Prioritäten danach

1. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
2. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
3. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
4. Arena-Import und 100 Hände final bewerten.
5. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Lethal-Race-Kalibrierung veröffentlichen, den sprechend benannten Workflow samt Artefakt vollständig auswerten und danach behalten oder evidenzbasiert zurückrollen.
