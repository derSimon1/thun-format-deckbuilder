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
- [ ] planfremde bedingte, Death- und aktivierte Maker reduzieren
- [ ] Arena-Import und 100 Hände final bewerten

## Aktuelle Pflichtdichten

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems

## Evidenz

- bestätigter 24-Land-Stand aus Run 70: Benchmark 96, T2/T3 94/96 %, Schaden 23,58, Killrate 62 %
- 23-Land-Run 71: Benchmark 94, T2/T3 92/94 %, Mana-Screw 16 statt 13 Hände, Schaden 23,66, Killrate 63 %
- Entscheidung: 24 Plains bleiben wegen klar besserer Starthand- und Kurvenstabilität

## Prioritäten

1. Rollback auf 24 Länder vollständig grün bestätigen.
2. Go-Wide-Auswahl auf garantierte Sofortproduktion, effiziente Multi-Maker und echte Anthems optimieren.
3. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
4. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
5. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
6. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

24-Land-Rollback veröffentlichen, CI und Artefakt bestätigen und anschließend bedingte, Death- und teure aktivierte Maker im Go-Wide-Scoring gegenüber sofortigen Multi-Makern abwerten.
