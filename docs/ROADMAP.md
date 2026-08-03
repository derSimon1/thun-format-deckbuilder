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
- [x] Value-Mindestdichte von sechs automatischen Engines als unerreichbar widerlegt

## Aktueller Fokus – Token Go Wide

### Builder

- [x] `token_immediate_maker` nur garantierter Sofortproduktion zuweisen
- [x] `token_multi_maker` nur garantierter Sofortproduktion von mindestens zwei Kreatur-Tokens zuweisen
- [x] `token_repeatable_maker` nur automatischen Triggern zuweisen
- [x] Value-Planwahl an mindestens sechs erreichbare automatische Enginekopien binden
- [x] Go-Wide-Planwahl auf garantierte Sofort-/Multi-Maker und Team-Payoffs ausrichten
- [x] Go-Wide-Profil mit kapazitätsgeprüften Pflichtdichten implementieren
- [x] Fast-Validierung erzeugt ein legales Go-Wide-Deck, Benchmark 96
- [ ] Rollen-Normalisierungstest grün machen
- [ ] vollständigen grünen Go-Wide-Workflow und Artefaktvergleich bestätigen
- [ ] finale Go-Wide-Deckliste und Arena-Import prüfen

### Pflichtdichten

- mindestens 15 Kreatur-Token-Maker
- mindestens 9 sofortige Maker
- mindestens 6 garantierte Multi-Maker
- mindestens 3 Anthems
- Ziele: 20 / 12 / 9 / 6

### Run-64-Evidenz

- Profil: Go Wide
- 36 Kreatur-Token-Maker
- 25 sofortige Maker
- 21 garantierte Multi-Maker
- 6 Anthems
- Token-Benchmark 96
- Burn 83, Artifacts 90, Control 85 und Mill 80 unverändert
- 300 von 301 Tests grün
- einziger Fehler: Enum-/String-Normalisierung im Full-Pool-Rollentest

### Erfolgskriterien

- [x] Profilname enthält `Go Wide`
- [x] Legalität 60/15 und Kopienlimit im Fast-Lauf
- [x] andere vier Referenzbenchmarks stabil
- [x] keine Token-Rollen-Fehlpositive
- [ ] vollständige Testsuite grün
- [ ] genau 100 Hände mit Seed 1701 ausgewertet
- [ ] Keepability, Early Play und Planfähigkeit gegen Run 63 verglichen
- [ ] Goldfish mit korrigierter Produktionsmessung verglichen
- [ ] Token gegen Burn, Artifacts und Mill sowie BO3 ausgewertet
- [ ] Fast unter zehn Minuten bestätigt

## Nach grünem Go-Wide-Builderzyklus

1. Strategy Commitment auf sofortige Maker, Multi-Maker und Team-Payoffs ausrichten.
2. Opening-Hand-Klassifikation auf dieselben präzisen Go-Wide-Rollen umstellen.
3. Anthem-Wirkung und Boardaufbau im Goldfish/Combatmodell prüfen.
4. Go Wide, Value Tokens und Aristocrats als getrennte Referenzdecks erzeugen.
5. Mill-Kompositionsschritt mit 18 Quellen und 6 echten Engines abschließen.
6. relevante Control-Antworten aus konkreten Gegnerdecks ableiten.
7. belastbare Regression-Baseline statt `baseline: none`.
8. erste v2-KGB und Club-/Meta-Benchmark.

## Genau ein nächster ausführbarer Schritt

Den Rollen-Normalisierungshotfix committen, den entstehenden Workflow vollständig auswerten und anschließend anhand der 100 Hände und Goldfish-Artefakte genau eine belegte Go-Wide-Schwäche priorisieren.

## Definition of Done für den aktuellen Zyklus

- Code, Tests, Logbook und Roadmap in einem Commit
- vollständige CI und Artefaktauswertung
- Go-Wide-Pflichtrollen erfüllt
- andere vier Referenzbenchmarks stabil
- KGB-Entscheidung und kritische Reflexion dokumentiert
- genau ein nächster ausführbarer Schritt
