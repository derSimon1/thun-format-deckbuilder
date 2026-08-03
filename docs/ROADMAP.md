# Roadmap

## Development System v2.0 / Prompt 2.1

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten ausführbaren Schritt.

## Globale Grundlagen

- [x] Fast-Validierung und Cache
- [x] genau 100 reproduzierbare Starthände je Deck, Seed 1701
- [x] Opening-Hand-, Goldfish-, Benchmark-, Matchup- und BO3-Berichte
- [x] Manafehler-Invariante
- [x] Control als fünfter Referenzarchetyp, Benchmark 85
- [x] Phrase-first-Sideboardklassifikation und Diagnoseartefakte
- [x] zentrale Mill-Quellendefinition und Poolkapazität

## Token-Grundlagen

- [x] Kreatur-Token von Nichtkreatur-Tokens getrennt
- [x] echte Outlets und Death-Payoffs getrennt
- [x] 43 Rollen-Fehlpositive entfernt
- [x] präzise Planrollen und kapazitätsgeprüfte Mindestpakete
- [x] Immediate-, Conditional-, Death-, Activated- und Repeatable-Produktion getrennt
- [x] Goldfish auf reale Produktionsmodi umgestellt
- [x] Mono-White-Poolkapazität je Produktionsmodus gemessen
- [x] Aktivierungsmetadaten aus Funktionsrollen ausgeschlossen

## Run-63-Evidenz

| Produktionsmodus | Karten | maximale Kopien |
|---|---:|---:|
| sofort | 88 | 264 |
| aktiviert | 16 | 48 |
| bedingt | 50 | 150 |
| Death | 14 | 42 |
| automatisch wiederholbar | 1 | 3 |

- [x] Run `30817765040` vollständig grün
- [x] 297 Tests
- [x] Fast ungefähr 4:14 Minuten
- [x] Benchmarks 83/91/90/85/80
- [x] Value-Mindestdichte von sechs automatischen Engines als unerreichbar widerlegt

## Aktueller Fokus – Token Go Wide

### Builder

- [x] kanonische Rolle `token_immediate_maker` vorbereiten
- [x] kanonische Rolle `token_multi_maker` vorbereiten
- [x] `token_repeatable_maker` nur automatischen Triggern zuweisen
- [x] Value-Planwahl an mindestens sechs erreichbare automatische Enginekopien binden
- [x] Go-Wide-Planwahl auf garantierte Sofort-/Multi-Maker und Team-Payoffs ausrichten
- [x] Go-Wide-Profil mit kapazitätsgeprüften Pflichtdichten vorbereiten
- [ ] vollständige Testsuite und Fast-Validierung auswerten
- [ ] finale Go-Wide-Deckliste und Arena-Import prüfen

### Pflichtdichten des ersten Go-Wide-Zyklus

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems
- Ziele: 20 / 12 / 9 / 6

### Erfolgskriterien

- [ ] Profilname enthält `Go Wide`
- [ ] Legalität 60/15 und Kopienlimit
- [ ] genau 100 Hände mit Seed 1701
- [ ] Keepability, Early Play und Planfähigkeit vollständig ausgewertet
- [ ] Goldfish mit korrigierter Produktionsmessung
- [ ] Token gegen Burn, Artifacts und Mill sowie BO3 ausgewertet
- [ ] Fast unter zehn Minuten
- [ ] Burn 83, Artifacts 90, Control 85 und Mill 80 ohne unbegründete Regression
- [ ] keine Token-Rollen-Fehlpositive

## Nach erfolgreichem Go-Wide-Builderzyklus

1. Strategy Commitment auf sofortige Maker, Multi-Maker und Team-Payoffs ausrichten.
2. Opening-Hand-Klassifikation auf dieselben präzisen Go-Wide-Rollen umstellen.
3. Anthem-Wirkung und Boardaufbau im Goldfish/Combatmodell prüfen.
4. Go Wide, Value Tokens und Aristocrats als getrennte Referenzdecks erzeugen.
5. Mill-Kompositionsschritt mit 18 Quellen und 6 echten Engines abschließen.
6. relevante Control-Antworten aus konkreten Gegnerdecks ableiten.
7. belastbare Regression-Baseline statt `baseline: none`.
8. erste v2-KGB und Club-/Meta-Benchmark.

## Definition of Done für den aktuellen Zyklus

- Code, Tests, Logbook und Roadmap in einem Commit
- vollständige CI und Artefaktauswertung
- Go-Wide-Pflichtrollen erfüllt
- andere vier Referenzbenchmarks stabil
- KGB-Entscheidung und kritische Reflexion dokumentiert
- genau ein nächster ausführbarer Schritt
