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
- [ ] Lethal-Race-Modell mit abnehmendem Überkill-Nutzen kalibrieren
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

## Run-75-Lernpunkt

- harte Kappung bei 20 reduzierte Tokens–Artifacts auf 0 % und machte Control–Burn zu 100 %
- Fast und Diagnose waren grün; ein Test scheiterte nur an 0,001 Monte-Carlo-Rundung
- die harte Kappung wird verworfen, bevor weitere Deckoptimierung beginnt

## Aktueller Zyklus

1. Schaden bis 20 linear bewerten.
2. Überkill oberhalb 20 nur logarithmisch gutschreiben.
3. Killrate als kleinen Konsistenzbonus ergänzen.
4. Fortschrittsfunktion direkt und deterministisch testen.
5. Workflow sichtbar `Token Go Wide – Lethal Race Diminishing Returns` benennen.
6. Deck-Hash, Benchmarks und Deckmetriken müssen unverändert bleiben.

## Prioritäten danach

1. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
2. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
3. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
4. Arena-Import und 100 Hände final bewerten.
5. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Diminishing-Returns-Fix veröffentlichen, den sprechend benannten Workflow samt Artefakt vollständig auswerten und erst nach grünem Gate weiter optimieren.
