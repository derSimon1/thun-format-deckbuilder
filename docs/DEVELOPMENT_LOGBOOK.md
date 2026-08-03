# Development Logbook

Dieses Dokument ist das chronologische Projektgedächtnis. Es hält Änderungen, Hypothesen, Ergebnisse, Baseline-Entscheidungen und Lessons Learned fest. Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten.

## Verbindliches Eintragsformat ab Development System v2.0

```text
Datum / Lauf / Zyklus
Ziel
Ausgangs-Head
Ausgangs-KGB oder Vergleichsstand
Hypothese
Änderungen oder No-Change-Befund
Validierung und Laufzeit
Workflow-Run-ID, Jobs, Logs und Artefakte
Qualitätsvergleich: Burn, Tokens, Artifacts, Control, Mill
Starthand-Seed und Rohdatenpfad
Ergebnis
KGB-Entscheidung: neue KGB / keine neue KGB / Regression
Confidence
Kritische Reflexion
Mindestens zwei Folgeschritte mit Bewertung
Genau ein priorisierter nächster ausführbarer Schritt
```

## Known-Good-Baseline-Status

### Voll qualifizierte Development-System-v2.0-KGB

Noch nicht vorhanden.

Eine v2.0-KGB benötigt vollständige Tests, Fast-Validierung, erfolgreiche CI, Vergleich von Burn, Tokens, Artifacts, Control und Mill, die verbindliche 100-Starthände-Auswertung, dokumentierte Reflexion und keine unbegründeten Regressionen.

### v2-Bootstrap-Vergleichsstand

- Commit: `31f6c1e053976435481c07ab2098430bc2a45471`
- Workflow: Run `30792560878`, erfolgreich
- Tests: 240 bestanden in 30,10 Sekunden
- Fast-Validierung: ungefähr 3 Minuten 36 Sekunden
- Benchmarks: Burn 83, Tokens 90, Artifacts 90, Shrines 78, Mill 78
- Einschränkungen: Shrines statt Control, `baseline: none`, keine gespeicherten planabhängigen 100 Rohhände
- Status: technischer Bootstrap-Vergleichsstand, keine v2-KGB
- Confidence: hoch für technische Reproduzierbarkeit, niedrig bis mittel für globale spielerische Aussagekraft

### Historischer Legacy-KGB-Kandidat

- Commit: `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- Workflow: Run `30762470833`, erfolgreich
- Evidenz: 225 Tests bestanden; Fast-Lauf ungefähr drei Minuten
- Einschränkung: alte Referenzgruppe und keine v2-Regeln
- Status: historischer Wiederanlaufpunkt, keine v2-KGB

## Historische Lessons Learned

- Rollenpunkte allein erzeugen kein gutes Tokendeck.
- Token-Combat muss Summoning Sickness und leere Anthem-Boards korrekt berücksichtigen.
- Go Wide, Value Tokens und Aristocrats müssen vor der Kartenauswahl unterschieden werden.
- Harte Rollenminimums dürfen erst nach Kapazitätsprüfung aktiviert werden.
- Strategy Commitment muss neutrale Interaktion von planfremden Paketen trennen.
- Engine Density muss wiederholbare Engines von einmaligem Material trennen.
- GitHub Actions ist Validator, nicht Entwicklungsagent.
- No-Change-Zyklen benötigen Stopgrund, Erkenntnis und nächsten Schritt.

## 2026-08-03 – Development System v2.0 Konsolidierung

- Spezifikation, Prompt, Roadmap, Decisions, Meta und PR-Beschreibung vereinheitlicht.
- Referenzgruppe: Burn, Tokens, Artifacts, Control, Mill.
- 100 reproduzierbare Starthände, KGB, Rollback und Session-Recovery verbindlich gemacht.
- Runs `30791354202` und `30792560878` technisch grün.
- KGB-Entscheidung: keine v2-KGB, da Validator noch Shrines enthielt.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 1: OpeningHandPlanReport

### Ziel und Hypothese

Eine reproduzierbare Einzelhandanalyse soll Keepability, Early Play und Planfähigkeit trennen und damit halbe Engines sowie widersprüchliche Hände sichtbar machen.

### Ausgangs-Head

`31f6c1e053976435481c07ab2098430bc2a45471`

### Änderungen

1. `OpeningHandSimulator.simulate_plan` erzeugt exakt 100 Hände mit Seed, Deck-Hash, Manaquellen, Zug-1/2/3-Spielbarkeit, Sequenz, Rollen-Zugängen, Klassifikation und Ausfallgründen.
2. Gezielte Tests für Reproduzierbarkeit, drei Token-Pläne, Artifacts, Mill, Control und Farbfehler.
3. Fast-Validator schreibt vollständige Rohdaten nach `artifacts/global/<archetype>/<archetype>-opening-hands.json`.

### Commit und Workflow

- Commit: `43fa53d1766b05327eae5880bacb05905923f21c`
- Run: `30794553679`, erfolgreich
- Tests: 250 bestanden in 23,49 Sekunden
- Fast-Schritt: ungefähr 2 Minuten 51 Sekunden
- Artefakt: ID `8848391256`, 38 Dateien, 46.181 Byte komprimiert
- Seed: `1701`
- genau 100 Hände je erzeugtem Deck bestätigt

### Erste Messwerte

- Burn: Keepability 78 %, Planfähigkeit 94 %, Manafehler 22 %
- Tokens/Aristocrats: Keepability 73 %, Planfähigkeit 92 %, Manafehler 22 %
- Artifacts: Keepability 71 %, Planfähigkeit 88 %, Manafehler 22 %
- Mill: Keepability 77 %, Planfähigkeit 0 %, marginal 100 %
- Shrines: Keepability 69 %, Planfähigkeit 51 %, Manafehler 18 %

### Erkenntnis

Grüne CI deckte eine fachliche Fehlklassifikation nicht ab: Hände mit Mana Screw oder Flood konnten als planfähig gelten.

### KGB-Entscheidung

Keine neue v2-KGB.

### Confidence und Reflexion

- hoch für Determinismus und Rohdaten
- mittel für Rollen-/Gründe-Heuristik
- Rollen und Auswahlgründe können Oracle-Text unvollständig repräsentieren
- gute Messwerte können von zu breiten Signalen stammen

### Nächster Schritt

Manafehler-Invariante korrigieren, bevor Control oder Grenzwerte kalibriert werden.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 2: Manafehler-Invariante

### Ziel und Hypothese

Eine Sieben-Karten-Hand mit höchstens einem oder mindestens fünf Ländern kann relevante Planstücke enthalten, darf aber nicht als belastbar planfähig gelten.

### Ausgangs-Head

`43fa53d1766b05327eae5880bacb05905923f21c`

### Änderungen

1. Planfähige Hände mit Mana Screw/Flood werden auf `marginal` herabgestuft und erhalten `plan_pieces_with_unstable_mana`.
2. Regressionstest: keine Hand mit `mana_error=True` darf `planfaehig` sein.

### Commit und Workflow

- Commit: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Run: `30795368803`, erfolgreich
- Tests: 251 bestanden in 23,30 Sekunden
- Test-/Fast-Schritt: ungefähr 2 Minuten 50 Sekunden
- Artefakt: ID `8848730571`, 38 Dateien, 46.166 Byte komprimiert
- Seed: `1701`
- geprüfte Rohhände: 500
- Verstöße gegen Mana-Invariante: 0

### Korrigierte Messwerte

- Burn: Keepability 78 %, Planfähigkeit 78 %, marginal 20 %, nicht planfähig 2 %
- Tokens/Aristocrats: Keepability 73 %, Planfähigkeit 73 %, marginal 23 %, nicht planfähig 4 %
- Artifacts: Keepability 71 %, Planfähigkeit 70 %, marginal 30 %
- Mill: Keepability 77 %, Planfähigkeit 0 %, marginal 100 %
- Shrines: Keepability 69 %, Planfähigkeit 48 %, marginal 49 %, nicht planfähig 3 %

### KGB-Entscheidung

Keine neue v2-KGB, da Control weiterhin nicht im Pflichtvalidator war.

### Confidence und Reflexion

- hoch für die globale Mana-Invariante
- mittel für übrige archetypenabhängige Regeln
- aggressive Ein-Land-Hände können praktisch situativ keepbar sein; `marginal` ist bewusst konservativ und kein automatisches Mulligan-Urteil
- Mill bleibt eine belegte Messauffälligkeit, darf aber nicht durch bloße Schwellenwertverschiebung repariert werden

### Nächster Schritt

Control als fünften Builder- und Validator-Archetyp integrieren.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 3: Control-Referenzarchetyp

### Ziel

Shrines aus der ausführbaren Pflichtvalidierung entfernen und Control als allgemeinen Referenzfall für das Verhindern gegnerischer Pläne integrieren.

### Ausgangs-Head

`5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`

### Hypothese

Eine konservative Dimir-Control-Strategie kann mit Oracle-Textsignalen günstige Counter, Removal, Sweeper, Kartenvorteil und wenige Finisher auswählen. Sie liefert einen allgemeineren globalen Qualitätsbenchmark als Shrines.

### Änderungen

1. Neues Control-Scoring und `ControlStrategy` mit 25 Ländern, Dimir-Farbpflicht und Control-spezifischem Sideboard; Registrierung im Deckbuilder.
2. Control-Benchmark sowie v2-Validatorwrapper für Burn, Tokens, Artifacts, Control und Mill; Fast-Matchups um Control gegen Burn, Tokens und Artifacts ergänzt; Full-Workflow auf v2-Validator gestellt.
3. Gezielte Tests für Counter, Removal, Sweeper, Kartenvorteil, Finisher, Dimir-Farbpflicht und Control-Benchmark.

### Validierung vor Commit

- statische Import- und Abhängigkeitsprüfung: keine neue zyklische Abhängigkeit erkannt
- bestehender Run 43 ist grün und Branch-Head stabil
- reale Kartenpool-, 60/15-, Manabasis-, Benchmark-, 100-Hand-, Matchup- und Laufzeitprüfung: durch neuen PR-Workflow zu verifizieren

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Eine KGB-Entscheidung ist erst nach vollständiger Workflow- und Artefaktauswertung zulässig.

### Confidence

- mittel bis hoch für Scoring-Signale und Registrierungsstruktur
- mittel für reale Poolkapazität und Sideboardfüllung
- niedrig bis mittel für spielerische Control-Qualität vor Artefakt- und Clubauswertung

### Kritische Reflexion

- Falsche Annahme: Dimir könnte als einzelner Control-Referenzfall zu eng sein; Azorius oder Esper würden andere Antworttypen abdecken.
- Alternative Erklärung für gute Benchmarks: hohe Antwortenzahl kann situativ tote Interaktion enthalten.
- Overfitting-Risiko: Gründe wie `Counter target spell` und `Control-Finisher` speisen zugleich Benchmark und Handanalyse.
- Datenlücke: Die Matchup-Simulation bewertet Counter/Removal noch nicht vollständig gegen konkrete Kartentypen.
- Grüne CI würde nur zeigen, dass ein legales Control-Deck erzeugt wird, nicht dass es gegnerische Pläne realistisch verhindert.
- Unentdeckte Regression: sechs statt drei Fast-Matchups können die Laufzeit erhöhen.

### Mögliche Folgeschritte

1. **Control-Workflow und Rohhände auswerten** – höchste Evidenz, geringer Aufwand, niedriges Risiko.
2. **Matchupabhängige Control-Antwortabdeckung modellieren** – hoher globaler Gewinn, mittlerer Aufwand, mittleres Risiko.
3. **Mill-Rohhände analysieren** – hohe Messrelevanz, geringer bis mittlerer Aufwand, Gefahr archetypspezifischer Überanpassung.

### Priorisierter nächster ausführbarer Schritt

Den neuen Control-Workflow vollständig auswerten. Bei roter CI genau eine belegte Ursache beheben. Bei grüner CI Control-Handmetriken, sechs Matchups, BO3, Artefakte und Laufzeit prüfen und danach entscheiden, ob zuerst Control-Matchupsensitivität oder der Mill-Messfehler den höheren globalen Qualitätsgewinn verspricht.
