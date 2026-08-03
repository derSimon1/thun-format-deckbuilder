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
- [ ] Full-Pool-Test über repräsentationsunabhängige finale Deckrollen grün machen
- [ ] zustandsabhängige Qualitätsberichtabweichung separat reproduzieren
- [ ] Arena-Import und 100 Hände final bewerten

## Aktuelle Pflichtdichten

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems

## Aktuelle Evidenz

- 36 Kreatur-Token-Maker
- 25 sofortige Maker
- 21 garantierte Multi-Maker
- 6 Anthems
- Keepability/Planfähigkeit 77/77 %
- Goldfish 23,72 Schaden und 63 % Killrate
- Matchups Burn/Artifacts/Mill: 0/58/100 %
- Runs 64–67 scheiterten ausschließlich am Full-Pool-Test; Fast und Diagnose waren jeweils erfolgreich

## Prioritäten nach grünem Testgate

1. Farblose Pflichtmanaanforderungen in Manabasis und Castability berücksichtigen.
2. Zustandsabhängige Abweichung des Qualitätsberichts zwischen wiederholter Testsession und isoliertem Fast-Prozess reproduzieren.
3. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
4. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
5. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
6. Go Wide, Value Tokens und Aristocrats getrennt erzeugen.
7. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Den Full-Pool-Test gegen die finalen `DeckEntry.roles` mit repräsentationsunabhängiger Rollenprüfung ausführen, CI und Artefakte auswerten und erst bei grünem Gate die Fortsetzungsaufgaben starten.
