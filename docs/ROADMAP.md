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
- [x] Fast-Validierung erzeugt Profil Go Wide
- [x] Benchmark 96 und stabile andere Referenzbenchmarks
- [x] Artefakte bestätigen 36 Kreatur-Token-Maker, 25 sofortige Maker, 21 Multi-Maker und 6 Anthems
- [ ] Full-Pool-Test explizit an `data/cards.db` binden
- [ ] drei vollständige grüne Bestätigungsläufe auf demselben Head abschließen
- [ ] Arena-Import und 100 Hände final bewerten

## Aktuelle Pflichtdichten

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems

## Root Cause der roten Runs 64–68

Die autouse Session-Fixture setzt `THUN_DATABASE_FILE` auf eine synthetische Testdatenbank. Der Full-Pool-Test verwendete dadurch nicht den realen Pool, sondern `Test Token`-Karten. Das Produktionsartefakt war in allen Runs korrekt und stabil.

## Prioritäten nach drei grünen Bestätigungsläufen

1. Farblose Pflichtmanaanforderungen in Manabasis und Castability berücksichtigen.
2. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
3. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
4. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
5. Go Wide, Value Tokens und Aristocrats getrennt erzeugen.
6. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Den Full-Pool-Test mit `CardDatabase(DATABASE_FILE)` gegen die kanonische Repository-Datenbank ausführen und anschließend drei vollständige CI-Durchgänge samt Artefakten auf demselben Head bestätigen.
