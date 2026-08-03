# Development Logbook

Detaillierte frühere Einträge bleiben über die Git-Historie erhalten. Ab Development System v2.0 dokumentiert jeder Zyklus Ausgangs-Head, Vergleichsstand, Hypothese, Änderungen, Tests/CI, 100-Hand-Seed, KGB-Entscheidung, Reflexion und genau einen nächsten Schritt.

## KGB-Status

### Voll qualifizierte v2-KGB

Noch nicht vorhanden.

### v2-Bootstrap-Vergleichsstand

- Commit `31f6c1e053976435481c07ab2098430bc2a45471`
- Run `30792560878`, erfolgreich
- 240 Tests; Fast ungefähr 3:36 Minuten
- Einschränkungen: Shrines statt Control, `baseline: none`, keine 100 planabhängigen Rohhände
- Status: technischer Bootstrap-Vergleichsstand, keine v2-KGB

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
- Tests: 250 bestanden in 23,49 Sekunden
- Fast: ungefähr 2:51 Minuten
- Artefakt: `8848391256`, 38 Dateien
- Seed: `1701`, exakt 100 Hände je erzeugtem Deck
- Ergebnis: deterministische Rohhände, Deck-Hash, Manaquellen, T1/T2/T3, Rollen-Zugänge, Planfähigkeitsklassen
- Befund: Manafehler konnten fälschlich planfähig sein
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 2: Manafehler-Invariante

- Ausgangs-Head: `43fa53d1766b05327eae5880bacb05905923f21c`
- Commit: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Run: `30795368803`, erfolgreich
- Tests: 251 bestanden in 23,30 Sekunden
- Fast: ungefähr 2:50 Minuten
- Artefakt: `8848730571`, 38 Dateien
- 500 Rohhände geprüft; 0 Fälle `mana_error` plus `planfaehig`
- Burn: Keepability/Planfähigkeit 78/78 %
- Tokens/Aristocrats: 73/73 %
- Artifacts: 71/70 %
- Mill: 77/0 %, marginal 100 %
- KGB: keine neue v2-KGB; Control fehlte noch

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 3: Control-Referenzarchetyp

- Ausgangs-Head: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Commit: `380eba398fd27c30579f92da9c1d9d20372e626e`
- Hypothese: Dimir Control ist als allgemeiner Referenzfall wertvoller als Shrines.
- Änderungen: Control-Scoring/Strategie/Sideboard, Benchmark, v2-Validator mit Burn/Tokens/Artifacts/Control/Mill, sechs Fast-Matchups und Tests.
- Run `30796392816`: rot wegen genau eines veralteten Tests; Fast-Validierung selbst PASS.
- Tests: 256 bestanden, 1 fehlgeschlagen in 30,50 Sekunden.
- Fast insgesamt ungefähr 3:20 Minuten; Artefakt `8849106044`, 38 Dateien.
- Control: legal 60/15, Benchmark 72, Antworten 33, Finisher 0, Keepability 73 %, Planfähigkeit 68 %, fehlender Finisher-Zugang 100 %.
- Matchups: 0 % gegen Burn, 99 % gegen Tokens, 66 % gegen Artifacts; BO3 0/100/95 %.
- KGB: keine neue v2-KGB; Run rot und Control kann die Partie nicht belastbar beenden.
- Reflexion: Antwortdichte überdeckt fehlende Wincondition; Matchup-Simulation bewertet situativ tote Antworten noch nicht zuverlässig.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 4: Veralteter Unknown-Archetype-Test

- Ausgangs-Head: `380eba398fd27c30579f92da9c1d9d20372e626e`
- Commit: `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07`
- Änderung: Unknown-Archetype-Test verwendet `combo` statt des nun unterstützten `control`.
- Run: `30796896850`, erfolgreich.
- Tests: 257 bestanden in 31,87 Sekunden.
- Fast: 5 Referenzarchetypen, 6 Matchups, 0 Regressionen; Test-/Fast-Schritt ungefähr 3:28 Minuten.
- Artefakt: `8849302790`, 38 Dateien, 46.145 Byte.
- Seed: `1701`, je Deck exakt 100 Hände.
- Control unverändert: Benchmark 72, 0 Finisher, 100 % fehlender Finisher-Zugang.
- KGB: keine neue v2-KGB, da die spielerische Control-Wincondition fehlt und `baseline: none` fortbesteht.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 5: Control-Finisher-Mindestdichte

### Ziel

Den belegten Control-Befund 0 Finisher beheben, ohne Benchmark-Grenzwerte zu senken oder einzelne Kartennamen zu erzwingen.

### Ausgangs-Head

`9c4426e8bcdd8177d5cce3722484b2d9ceec3b07`

### Hypothese

Die globale Rollenerkennung markiert Kreaturen ab Manawert 5 bereits als `finisher`. Eine kapazitätsgeprüfte Profilanforderung von drei Finishern sollte deshalb eine belastbare Abschlussdichte herstellen. Der reale Workflow entscheidet, ob der Kartenpool und der nachgelagerte Optimierer diese Mindestdichte erhalten.

### Änderungen

1. `CONTROL_PROFILE` fordert `RoleTarget("finisher", minimum=3, target=3)`.
2. Regressionstest dokumentiert die verbindliche Control-Finisher-Dichte.

### Validierung vor Commit

- Run 45 bestätigt die grüne Control-Basis mit 257 Tests und Fast-Lauf unter zehn Minuten.
- Rollenerkennung und Kompositionsengine unterstützen `finisher` bereits global.
- keine Benchmark- oder Pass/Fail-Grenze verändert.
- vollständige Testsuite, reale 60/15-Generierung, Optimiererhalt, 100 Hände und Matchups müssen durch den neuen PR-Workflow verifiziert werden.

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Erst der Workflow kann bestätigen, ob tatsächlich mindestens drei Finisher im final optimierten Mainboard verbleiben.

### Confidence

- hoch für die belegte Ursache im Profil
- mittel für den Erhalt der Mindestdichte durch den nachgelagerten Optimierer
- mittel für spielerischen Gewinn; Finisher-Zugang allein beweist noch keine realistische Control-Clock

### Kritische Reflexion

- Falsche Annahme: Jede Kreatur ab Manawert 5 könnte als guter Control-Finisher gelten; manche sind ohne Schutz oder unmittelbaren Wert zu schwach.
- Alternative Erklärung: 0 Finisher entstand nicht nur durch das Profil, sondern durch den Optimierer oder zu schwache Finisher-Scores.
- Overfitting: Die Zahl drei folgt dem bereits definierten Control-Benchmark und nicht einem einzelnen Workflowwert, benötigt aber Club-/Meta-Evidenz.
- Messlücke: Goldfish und Matchups modellieren Control-Winconditions weiterhin nur grob.
- Grüne CI würde nur Mindestdichte und technische Stabilität bestätigen.
- Mögliche Regression: Drei teure Karten können Early Play, Mana oder Burn-Matchup verschlechtern.

### Mögliche Folgeschritte

1. **Workflow und finale Deckliste auswerten** – höchste Evidenz, geringer Aufwand, niedriges Risiko.
2. **Optimierer-Guardrail für Finisher ergänzen**, falls die Mindestdichte verloren geht – hohe Evidenz nur bei tatsächlichem Verlust, mittlerer Aufwand.
3. **Matchupabhängige Control-Antwortabdeckung modellieren** – hoher globaler Gewinn, mittlerer Aufwand und Risiko.
4. **Mill-Rohhände analysieren** – hoher Messgewinn, geringerer Aufwand, aber derzeit nachrangig.

### Priorisierter nächster ausführbarer Schritt

Den neuen Workflow vollständig auswerten. Falls das finale Mainboard weniger als drei Finisher enthält, genau diese Optimierer-Ursache beheben. Falls drei Finisher erhalten bleiben, Wincondition-Zugang, Early Play, Mana, Benchmark und drei Control-Matchups gegen Run 45 vergleichen und danach die matchupabhängige Control-Abdeckung priorisieren.
