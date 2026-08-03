# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Ab Development System v2.0 dokumentiert jeder Zyklus Ausgangs-Head, Hypothese, Änderungen, CI/Artefakte, 100-Hand-Seed, KGB-Entscheidung, Reflexion und genau einen nächsten Schritt.

## KGB-Status

### Voll qualifizierte v2-KGB

Noch nicht vorhanden.

### v2-Bootstrap-Vergleichsstand

- Commit `31f6c1e053976435481c07ab2098430bc2a45471`
- Run `30792560878`, erfolgreich
- 240 Tests; Fast ungefähr 3:36 Minuten
- Einschränkungen: Shrines statt Control, `baseline: none`, keine planabhängigen 100 Rohhände
- keine v2-KGB

### Legacy-Kandidat

- Commit `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- Run `30762470833`, erfolgreich
- historischer Wiederanlaufpunkt, keine v2-KGB

## Historische Kernlektionen

- Rollenpunkte allein erzeugen keine kohärenten Decks.
- Token-Pläne müssen vor Kartenauswahl unterschieden werden.
- Harte Mindestwerte erst nach Kapazitätsprüfung.
- Strategy Commitment trennt neutrale Interaktion von Planbruch.
- Engine Density trennt wiederholbare Engines von einmaligem Material.
- GitHub Actions ist Validator, nicht Entwicklungsagent.
- Grüne CI beweist keine spielerische Qualität.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 1: OpeningHandPlanReport

- Ausgangs-Head: `31f6c1e053976435481c07ab2098430bc2a45471`
- Commit: `43fa53d1766b05327eae5880bacb05905923f21c`
- Run: `30794553679`, erfolgreich
- Tests: 250 bestanden; Fast ungefähr 2:51 Minuten
- Artefakt: `8848391256`, 38 Dateien
- Seed `1701`, exakt 100 Hände je erzeugtem Deck
- Ergebnis: Rohhände mit Deck-Hash, Manaquellen, T1/T2/T3, Rollen-Zugängen und Planfähigkeitsklassen
- Befund: Manafehler konnten fälschlich planfähig sein
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 2: Manafehler-Invariante

- Ausgangs-Head: `43fa53d1766b05327eae5880bacb05905923f21c`
- Commit: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Run: `30795368803`, erfolgreich
- Tests: 251 bestanden; Fast ungefähr 2:50 Minuten
- Artefakt: `8848730571`, 38 Dateien
- 500 Rohhände geprüft; 0 Fälle `mana_error` plus `planfaehig`
- Burn: Keepability/Planfähigkeit 78/78 %
- Tokens/Aristocrats: 73/73 %
- Artifacts: 71/70 %
- Mill: 77/0 %, marginal 100 %
- KGB: keine neue v2-KGB; Control fehlte

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 3: Control-Referenzarchetyp

- Ausgangs-Head: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Commit: `380eba398fd27c30579f92da9c1d9d20372e626e`
- Änderungen: Control-Scoring/Strategie/Sideboard, Benchmark, v2-Validator mit Burn/Tokens/Artifacts/Control/Mill, sechs Fast-Matchups und Tests
- Run `30796392816`: rot wegen eines veralteten Unknown-Archetype-Tests; Fast-Validierung selbst PASS
- 256 Tests bestanden, 1 fehlgeschlagen; Fast ungefähr 3:20 Minuten
- Control: legal 60/15, Benchmark 72, Antworten 33, Finisher 0, Keepability 73 %, Planfähigkeit 68 %, fehlender Finisher-Zugang 100 %
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 4: Veralteter Unknown-Archetype-Test

- Ausgangs-Head: `380eba398fd27c30579f92da9c1d9d20372e626e`
- Commit: `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07`
- Änderung: Unknown-Archetype-Test verwendet `combo` statt des nun unterstützten `control`
- Run `30796896850`: erfolgreich
- Tests: 257 bestanden; Fast ungefähr 3:28 Minuten
- Artefakt: `8849302790`, 38 Dateien
- Control unverändert ohne Finisher
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 5: Control-Finisher-Mindestdichte

- Ausgangs-Head: `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07`
- Commit: `2ef72a092db8de4717ec1d474a380c0b2c0d63dc`
- Hypothese: Die vorhandene globale Rolle `finisher` wird durch `RoleTarget("finisher", minimum=3, target=3)` kapazitätsgeprüft reserviert.
- Run `30797591719`: erfolgreich
- Tests: 258 bestanden in 30,81 Sekunden
- Test-/Fast-Schritt: ungefähr 3:39 Minuten
- Artefakt: `8849580550`, 38 Dateien, 46.155 Byte
- Referenzarchetypen: 5; Matchups: 6; Regressionen: 0; Seed `1701`

### Vergleich Control Run 45 → Run 46

- Benchmark: 72 → 85
- Mainboard-Finisher: 0 → 6
- fehlender Finisher-Zugang: 100 % → 47 %
- Keepability: 73 % → 78 %
- Planfähigkeit: 68 % → 72 %
- Early Play T2/T3: 79/87 % → 80/87 %
- Manafehler: 19 % → 18 %
- Farbfehler: 5 % → 4 %
- Control vs Burn: 0 % → 0 %
- Control vs Tokens: 99 % → 86 %
- Control vs Artifacts: 66 % → 51 %
- BO3 vs Tokens: 100 % → 100 %; vs Artifacts: 95 % → 80 %

### Ergebnis und KGB-Entscheidung

Die kapazitätsgeprüfte Mindestdichte bleibt nach Optimierung erhalten. Die niedrigeren Token-/Artifact-Werte sind als erwarteter Trade-off durch sechs teurere Abschlusskarten plausibel, aber wegen der vereinfachten Matchup-Simulation noch nicht spielerisch belastbar. Keine neue v2-KGB: `baseline: none` bleibt bestehen und Sideboard-Pläne sind fachlich falsch.

### Kritische Reflexion

- Sechs Finisher sind mehr als das Mindestziel drei, da zwei Kartennamen je dreifach gewählt wurden; dies kann bereits zu viel sein.
- Kreaturen ab Manawert 5 sind nicht automatisch gute Control-Finisher.
- Goldfish bleibt bei 0 % Killrate, weil Control-Abschlussdruck nicht realistisch modelliert wird.
- Grüne CI bestätigt technische Mindestdichte, nicht die Qualität der Winconditions.
- Unbeabsichtigte Regression: weniger Antworten können Matchups verschlechtern; aktuelle Werte sind durch das heuristische Modell verzerrt.

### Nächster Schritt

Die belegte matchupfremde Sideboard-Nutzung korrigieren: `Tormod's Crypt` darf nicht gegen Burn, Tokens oder Artifacts eingewechselt werden.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 6: Matchupabhängige Sideboard-Relevanz

### Ziel

Sideboard-Pläne nach tatsächlicher gegnerischer Strategie statt nach unspezifischen Worttreffern bewerten.

### Ausgangs-Head

`2ef72a092db8de4717ec1d474a380c0b2c0d63dc`

### Evidenz und Hypothese

Run 46 boardet gegen Burn, Tokens und Artifacts jeweils drei `Tormod's Crypt` ein. Ursache: Das generische Wort `exile` lässt Graveyard-Hate als Removal beziehungsweise Artifact-Antwort erscheinen. Verbindliche SideboardBuilder-Kategorien wie `graveyard hate`, `anti-aggro removal` und `countermagic` ermöglichen eine präzisere matchupabhängige Relevanz.

### Änderungen

1. Neue `_sideboard_relevant`-Logik verwendet autoritative Sideboard-Kategorien; unspezifische Wörter wie `exile` reichen nicht mehr.
2. Fast-Boarding und Full-Sideboard-Optimierung filtern Kandidaten auf echte Matchup-Relevanz.
3. Regressionstests sichern: Graveyard-Hate nur gegen Mill; `Disfigure` statt `Tormod's Crypt` gegen Burn.

### Validierung vor Commit

- kontrollierte Relevanzfälle bestanden
- keine Pass/Fail-, Benchmark- oder Deckbaugrenze verändert
- vollständige Suite, sechs BO3-Berichte, Laufzeit und Artefakte müssen durch den neuen PR-Workflow bestätigt werden

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Zuerst müssen die neuen Sideboard-Pläne und mögliche Matchupänderungen ausgewertet werden.

### Confidence

- hoch für die konkrete Graveyard-Hate-Fehlzuordnung
- mittel für die vollständige Kategorien-Matrix
- niedrig bis mittel für spielerische Matchupwerte, da die Matchup-Simulation weiterhin stark vereinfacht ist

### Kritische Reflexion

- Falsche Annahme: Mill ist nicht automatisch ein Graveyard-Matchup; selbst die Zuordnung `graveyard hate → mill` benötigt spätere Decklisten-Evidenz.
- Alternative Erklärung: `Tormod's Crypt` wurde nicht wegen Relevanz, sondern wegen Artefakt-Threat-Density im Simulator bevorzugt. Der Filter behebt beide Pfade, kann aber nützliche ungewöhnliche Karten ausschließen.
- Overfitting: Kategorien stammen aus dem SideboardBuilder und gelten global; dennoch sind sie derzeit auf wenige Referenzarchetypen zugeschnitten.
- Datenlücke: Der Gegnerdeck-Inhalt wird nicht direkt auf relevante Ziele untersucht.
- Grüne CI würde nur konsistente Kategorien, nicht echte Sideboardqualität beweisen.
- Mögliche Regression: Zu strenge Filter können zu `cards in: none` führen, obwohl eine Karte situativ nützlich wäre.

### Mögliche Folgeschritte

1. **Workflow-/BO3-Artefakte auswerten** – höchste Evidenz, geringer Aufwand.
2. **Relevanz aus konkretem Gegnerdeck statt Archetyp ableiten** – hoher globaler Gewinn, mittlerer bis hoher Aufwand.
3. **Control-Basisfortschritt im Matchupmodell an Finisher koppeln** – hoher Messgewinn, mittlerer Aufwand und Overfitting-Risiko.
4. **Mill-0-%-Planfähigkeitsbefund untersuchen** – hoher Messgewinn, geringer bis mittlerer Aufwand.

### Priorisierter nächster ausführbarer Schritt

Den neuen Workflow vollständig auswerten. Danach anhand der Artefakte entscheiden, ob die konkrete Gegnerdeck-Relevanz oder der Mill-Messfehler den höheren globalen Qualitätsgewinn bietet.
