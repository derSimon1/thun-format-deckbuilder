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
- [x] Run 64/65: Benchmark 96 und stabile andere Referenzbenchmarks
- [ ] Full-Pool-Rollentest auf kanonischen Enum-Wert normalisieren
- [ ] vollständigen grünen Workflow bestätigen
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

## Prioritäten nach grünem Testgate

1. Farblose Pflichtmanaanforderungen in Manabasis und Castability berücksichtigen.
2. Strategy Commitment und Opening-Hand-Klassifikation auf präzise Go-Wide-Rollen prüfen.
3. Anthem-Wirkung und Boardaufbau im Combatmodell prüfen.
4. Burn-Matchup anhand realer Sequenzen und relevanter Schutz-/Tempooptionen untersuchen.
5. Go Wide, Value Tokens und Aristocrats getrennt erzeugen.
6. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Den Full-Pool-Test mit `getattr(role, "value", str(role))` auf den kanonischen Rollenwert umstellen, CI und Artefakte auswerten und danach die farblose Manaanforderung bearbeiten.
