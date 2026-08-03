# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Ab Development System v2.0 dokumentiert jeder Zyklus Ausgangs-Head, Hypothese, Änderungen, CI/Artefakte, 100-Hand-Seed, KGB-Entscheidung, Reflexion und genau einen nächsten Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht.

### v2-Bootstrap-Vergleichsstand

- Commit `31f6c1e053976435481c07ab2098430bc2a45471`
- Run `30792560878`, erfolgreich
- Einschränkungen: Shrines statt Control, `baseline: none`, keine planabhängigen 100 Rohhände

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

- Commit `43fa53d1766b05327eae5880bacb05905923f21c`
- Run `30794553679`, erfolgreich
- 250 Tests; Fast ungefähr 2:51 Minuten; Artefakt `8848391256`
- Seed `1701`, exakt 100 Hände je erzeugtem Deck
- Ergebnis: Rohhände mit Deck-Hash, Manaquellen, T1/T2/T3, Rollen-Zugängen und Planfähigkeitsklassen
- Befund: Manafehler konnten fälschlich planfähig sein
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 2: Manafehler-Invariante

- Commit `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Run `30795368803`, erfolgreich
- 251 Tests; Fast ungefähr 2:50 Minuten; Artefakt `8848730571`
- 500 Rohhände; 0 Fälle `mana_error` plus `planfaehig`
- Burn 78 %, Tokens 73 %, Artifacts 70 %, Mill 0 % planfähig
- KGB: keine neue v2-KGB; Control fehlte

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 3: Control-Referenzarchetyp

- Commit `380eba398fd27c30579f92da9c1d9d20372e626e`
- Änderungen: Control-Scoring/Strategie/Sideboard, Benchmark, v2-Validator mit fünf Referenzarchetypen, sechs Fast-Matchups und Tests
- Run `30796392816`: rot wegen eines veralteten Unknown-Archetype-Tests; Fast-Validierung selbst PASS
- Control: legal 60/15, Benchmark 72, Antworten 33, Finisher 0, Keepability 73 %, Planfähigkeit 68 %
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 4: Veralteter Unknown-Archetype-Test

- Commit `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07`
- Run `30796896850`, erfolgreich
- 257 Tests; Fast ungefähr 3:28 Minuten; Artefakt `8849302790`
- Control weiterhin ohne Finisher
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 5: Control-Finisher-Mindestdichte

- Commit `2ef72a092db8de4717ec1d474a380c0b2c0d63dc`
- Run `30797591719`, erfolgreich
- 258 Tests; Fast ungefähr 3:39 Minuten; Artefakt `8849580550`
- Control Benchmark 72 → 85; Finisher 0 → 6; Finisher-Zugang 0 → 53 %; Keepability 73 → 78 %; Planfähigkeit 68 → 72 %
- keine Mana- oder Laufzeitregression
- KGB: keine neue v2-KGB; Sideboard-Pläne weiterhin fachlich falsch

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 6: Erste Sideboard-Relevanzregel

- Commit `f3ea0f48e5cdeac422a5bb29f6864fb203745c3d`
- Run `30798351806`, erfolgreich
- 260 Tests in 31,68 Sekunden; Test-/Fast-Schritt ungefähr 3:49 Minuten
- Fast PASS: Burn 83, Tokens 90, Artifacts 90, Control 85, Mill 78; fünf Archetypen; sechs Matchups; 0 Regressionen
- Artefakt `8849876514`, 38 Dateien, 46.205 Byte
- Seed `1701`; 100 Hände je Deck; Control-Metriken unverändert stabil

### Widerlegung der Hypothese

Trotz grüner CI boardeten die realen BO3-Artefakte Control weiterhin mit drei `Tormod's Crypt` gegen Burn und Tokens. Die reine Auswertung der menschenlesbaren `reasons` war damit im realen Pfad nicht ausreichend belastbar. Grüne CI bedeutete erneut nicht automatisch bessere spielerische Qualität.

### KGB-Entscheidung

Keine neue v2-KGB. Die behauptete Sideboardverbesserung ist durch die Artefakte widerlegt.

### Reflexion

- Falsche Annahme: Menschenlesbare Auswahlgründe seien ein stabiler maschinenlesbarer Vertrag.
- Alternative Erklärung: Sideboard-Einträge verlieren oder verändern Gründe in einem späteren Transformationsschritt.
- Overfitting-Risiko: Kartennamen zu sperren wäre unzulässig und nicht global.
- Messlücke: Artefakte enthielten bislang keine maschinenlesbaren Sideboard-Kategorien je Karte.
- Unentdeckte Regression: Ein Filter kann relevante Nischenkarten ausschließen.

### Priorisierter nächster Schritt

Sideboard-Kategorien als explizite maschinenlesbare Rollenmarker im `DeckEntry` speichern und die Relevanzlogik ausschließlich auf diese Marker stützen; danach BO3-Artefakte erneut prüfen.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 7: Maschinenlesbare Sideboard-Kategorien

### Ziel und Hypothese

Die Kategorie einer Sideboardkarte muss einen stabilen maschinenlesbaren Vertrag bilden und alle Expand-/Compress-/BO3-Schritte überstehen. Marker wie `sideboard_graveyard_hate` sollen verhindern, dass generische Wörter oder verlorene Gründe Graveyard-Hate als Anti-Aggro-Karte einstufen.

### Ausgangs-Head

`f3ea0f48e5cdeac422a5bb29f6864fb203745c3d`

### Änderungen

1. `SideboardBuilder` kodiert jede getroffene Regel zusätzlich als `sideboard_<kategorie>` in `DeckEntry.roles`.
2. `_sideboard_relevant` verwendet Rollenmarker autoritativ; Gründe bleiben Legacy-Fallback, unmarkierte Fixtures nutzen konservative Textsignale.
3. Tests sichern Marker-Erzeugung und verhindern `Tormod's Crypt` gegen Burn, Tokens und Artifacts.

### Validierung vor Commit

- kontrollierte Markerfälle bestehen konzeptionell: Graveyard-Hate nur gegen Mill, Anti-Aggro-Removal gegen Burn/Tokens
- keine Kartennamen-Sonderregel, keine Benchmark- oder Pass/Fail-Grenze
- vollständige Suite, Fast-Lauf und reale BO3-Artefakte durch neuen PR-Workflow zu verifizieren

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Der reale Artefaktpfad muss den Marker-Vertrag bestätigen.

### Confidence

- hoch für die technische Persistenz in `roles`
- mittel für die Kategorien-Matrix
- niedrig bis mittel für echte Sideboardqualität ohne Gegnerdeck-Analyse

### Kritische Reflexion

- Falsche Annahme: Eine Archetyp-Matrix könne alle Matchupvarianten abdecken.
- Alternative Erklärung: Manche Mill-Decks profitieren vom Graveyard und manche nicht; `graveyard_hate → mill` bleibt vereinfachend.
- Overfitting: Marker sind global und nicht kartennamenspezifisch, aber die Matrix ist auf die aktuellen Referenzarchetypen zugeschnitten.
- Datenlücke: Relevante Ziele im konkreten Gegnerdeck werden noch nicht gezählt.
- Grüne CI genügt nicht; entscheidend sind BO3-Karten-in-Pläne.
- Mögliche Regression: Sideboards können gegen bestimmte Gegner keine relevante Karte besitzen und korrekt `none` melden.

### Mögliche Folgeschritte

1. Workflow und BO3-Pläne prüfen – höchste Evidenz, geringer Aufwand.
2. Relevanz aus dem konkreten Gegnerdeck ableiten – hoher globaler Gewinn, mittlerer Aufwand.
3. Mill-0-%-Planfähigkeitsbefund untersuchen – hoher Messgewinn, geringer bis mittlerer Aufwand.

### Priorisierter nächster ausführbarer Schritt

Den neuen Workflow und alle sechs BO3-Pläne vollständig auswerten. Falls Marker funktionieren, den Lauf abschließen und Mill als nächsten ausführbaren Roadmap-Punkt festhalten. Falls nicht, exakten Transformationspunkt der Rollenmarker diagnostizieren; nach zwei gescheiterten Sideboard-Zyklen danach zwingend zum Mill-Punkt wechseln.
