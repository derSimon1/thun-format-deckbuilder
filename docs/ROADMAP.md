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
- [x] Full-Pool-Test explizit an `data/cards.db` gebunden
- [x] drei vollständige grüne Bestätigungsläufe auf demselben Head abgeschlossen
- [ ] explizite `{C}`-Kosten ohne farblose Quellen aus der Komposition ausschließen
- [ ] Arena-Import und 100 Hände final bewerten

## Aktuelle Pflichtdichten

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems

## Aktuelle Evidenz

- stabiler Head vor Castability-Fix: `2bd921c1688c72d4b5949bd0f93cb65a9d1d206c`
- drei grüne Run-69-Ausführungen, jeweils 301 Tests
- Benchmarks 83/96/90/85/80 für Burn/Tokens/Artifacts/Control/Mill
- Token-Arena-Liste enthält `Warping Wail`, obwohl die Manabasis nur 24 Plains erzeugt

## Prioritäten

1. Farblose Pflichtmanaanforderungen in Manabasis und Castability berücksichtigen.
2. Go-Wide-Auswahl auf garantierte Sofortproduktion, effiziente Multi-Maker und echte Anthems optimieren.
3. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
4. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
5. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
6. Go Wide, Value Tokens und Aristocrats getrennt erzeugen.
7. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Das generische Eligibility-Gate für explizite `{C}`-Kosten veröffentlichen, CI und Artefakte auswerten und das neue Token-Deck exakt gegen Run 69 vergleichen.
