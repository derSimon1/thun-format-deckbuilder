# Development Logbook

Dieses Dokument ist das chronologische Projektgedächtnis. Es hält Änderungen, Hypothesen, Ergebnisse, Baseline-Entscheidungen und Lessons Learned fest. Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten.

## Verbindliches Eintragsformat ab Development System v2.0

```text
Datum / Lauf / Zyklus
Ziel
Ausgangs-Head
Ausgangs-KGB oder Legacy-KGB-Kandidat
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
- Fast-Validierung: erfolgreich; Gesamtzeit des Test-/Fast-Schritts ungefähr 3 Minuten 36 Sekunden
- Benchmarks: Burn 83, Tokens 90, Artifacts 90, Shrines 78, Mill 78
- bestehende Opening-Hand-Werte nach Mulligan: Burn 96 %, Tokens 94 %, Artifacts 96 %, Shrines 94 %, Mill 96 %
- Einschränkungen: Validator enthält Shrines statt Control; Vergleich meldet `baseline: none`; keine gespeicherten planabhängigen 100 Rohhände
- Status: technischer und quantitativer Bootstrap-Vergleichsstand, keine voll qualifizierte v2-KGB
- Confidence: hoch für Reproduzierbarkeit des technischen Stands, niedrig bis mittel für globale spielerische Aussagekraft

### Historischer Legacy-KGB-Kandidat

- Commit: `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- Workflow: Run `30762470833`, erfolgreich
- Evidenz: 225 Tests bestanden; Fast-Lauf ungefähr drei Minuten; Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte vorhanden
- Einschränkung: damalige Referenzgruppe enthielt Shrines statt Control; die v2.0-Starthand- und KGB-Regeln waren noch nicht vollständig umgesetzt
- Status: historischer Wiederanlaufpunkt, keine voll qualifizierte v2.0-KGB
- Confidence: mittel

## Historische Lessons Learned

### 2026-08-02 – Globale Kalibrierung und Token-Combat

- robuste Scryfall-Bulkdatenbank und Cache aufgebaut
- Opening-Hand-, Goldfish-, Benchmark-, Matchup- und BO3-Berichte etabliert
- Token-Combat realistischer modelliert
- Summoning Sickness, leere Anthem-Boards und Payoff-Wirkung durch Regressionstests abgesichert
- zentrale Erkenntnis: Rollenpunkte allein erzeugen noch kein gutes Tokendeck

### 2026-08-02/03 – Fehlgeschlagene Nachtkalibrierung

- GitHub Actions und Cron wurden fälschlich als Entwicklungsantrieb behandelt
- Statusprüfungen wurden wiederholt, ohne neue Entwicklungsergebnisse zu erzeugen
- daraus folgten Single Source of Truth, produktive No-Change-Regel und kontinuierlicher Mehrstundenbetrieb ohne separate 15-Minuten-Aufgaben

### 2026-08-03 – Token-Plan-Erkennung

- Go Wide, Value Tokens und Aristocrats werden vor der Kartenauswahl unterschieden
- planabhängige Kartenbewertung integriert
- technische Integration bestätigt; spielerische Kalibrierung weiterhin benchmarkabhängig

### 2026-08-03 – Planspezifische Dichteziele und Sparse-Pool-Hotfix

- harte Mindestdichten blockierten sparse Kartenpools
- Supportrollen wurden auf weiche Ziele zurückgeführt
- zentrale Erkenntnis: harte Mindestwerte dürfen erst nach Kapazitätsprüfung aktiviert werden

### 2026-08-03 – Strategy Commitment

- Commitment-Score, planprägende, planfremde und neutrale Kopien sowie Mischmasch-Warnungen eingeführt
- neutrale Interaktion wird nicht fälschlich als Planbruch gewertet

### 2026-08-03 – Token Engine Density

- wiederholbare planrelevante Engines von einmaligem Material getrennt
- Null-Engine- und Single-Engine-Abhängigkeit werden transparent gewarnt
- noch offen: archetypenübergreifende Abstraktion

## 2026-08-03 – Development System v2.0 Konsolidierung

### Ziel

Eine konsistente, selbstbeschreibende Arbeitsgrundlage für mehrstündige Kalibrierung mit Sicherungspunkten und Wiederanlaufregeln schaffen.

### Ausgangslage

- Branch: `codex/global-deckbuilder-calibration`
- PR: #14
- PR #13 bleibt unangetastet
- letzter vor der Konsolidierung verifizierter Head: `82b5aafead442103837f735ae1a66413462ba15c`
- zugehöriger Workflow: Run `30791354202`, erfolgreich
- PR war offen, Draft und mergeable

### Änderungen

- `docs/SPECIFICATION.md` auf Version 2.0 konsolidiert
- Mehrstundenbetrieb ohne separate 15-Minuten-Aufgaben verbindlich gemacht
- Burn, Tokens, Artifacts, Control und Mill als Referenzarchetypen festgelegt
- Shrines aus den Pflicht- und Referenzarchetypen entfernt
- 100 reproduzierbare Starthände je verwendeter Deckliste verbindlich gemacht
- Keepability, Early Play und Planfähigkeit getrennt
- Known Good Baseline, Git-Tag, Rollback und Session-Recovery eingeführt
- Prompt-Priorität an Roadmap und KGB-Bootstrap angepasst
- D-007 ausdrücklich ersetzt; Control und KGB als dauerhafte Entscheidungen dokumentiert
- META auf Control statt Shrines ausgerichtet

### Validierung

- Run `30791354202` bestätigt den unmittelbar vorherigen Dokumentationsstand als technisch grün
- Run `30792560878` bestätigt Head `31f6c1e053976435481c07ab2098430bc2a45471` mit 240 Tests und Fast-Validierung als technisch grün
- grüne CI allein begründet weiterhin keine v2.0-KGB

### Ergebnis

Die Repository-Dokumente verwenden dieselbe Referenzgruppe und dasselbe Mehrstunden-, Baseline- und Wiederanlaufmodell. Die ausführbare Validierung ist jedoch noch nicht vollständig angepasst und verwendet weiterhin Shrines statt Control.

### KGB-Entscheidung

Keine neue v2.0-KGB.

### Confidence

Hoch für die Prozesskonsistenz; keine Aussage über eine neue spielerische Baseline.

### Priorisierter nächster ausführbarer Schritt

Den reproduzierbaren `OpeningHandPlanReport` mit genau 100 gespeicherten Händen je verwendeter Deckliste, dokumentiertem Seed und getrennten Keepability-/Early-Play-/Planfähigkeitsmetriken implementieren und im Fast-Workflow als Rohdatenartefakt ausgeben.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 1: OpeningHandPlanReport und v2-Bootstrap

### Ziel

Die Messlücke zwischen formal spielbaren Händen und realistisch anlaufendem Hauptplan schließen, ohne die bestehende aggregierte London-Mulligan-Simulation zu brechen.

### Ausgangs-Head

`31f6c1e053976435481c07ab2098430bc2a45471`

### Ausgangs-KGB oder Vergleichsstand

- keine voll qualifizierte v2-KGB
- v2-Bootstrap-Vergleichsstand: Head `31f6c1e053976435481c07ab2098430bc2a45471`, Run `30792560878`
- Run 41: 240 Tests bestanden; Fast-Validierung erfolgreich; 0 gemeldete Regressionen, jedoch `baseline: none`
- bestehender Pflichtvalidator: Burn, Tokens, Artifacts, Shrines, Mill

### Hypothese

Ein reproduzierbarer Einzelhandbericht mit archetypen- und planabhängiger Klassifikation trennt Keepability, Early Play und Planfähigkeit und macht halbe Engines beziehungsweise widersprüchliche Hände sichtbar. Der globale Qualitätsgewinn ist höher als eine weitere Schwellenwertanpassung, weil die neue Messung alle späteren Token-, Control-, Engine- und Finish-Entscheidungen absichert.

### Änderungen

1. `OpeningHandSimulator.simulate_plan` erzeugt exakt 100 reproduzierbare Sieben-Karten-Hände mit Seed, Deck-Hash, farbigen Manaquellen, Zug-1/2/3-Spielbarkeit, Sequenzvorschlag, Rollen-Zugängen, Klassifikation und Ausfallgründen. Die bestehende Methode `simulate` bleibt kompatibel.
2. 15 gezielte Tests decken Reproduzierbarkeit, anderen Seed, exakt 100 Hände, Early-Play-/Planfähigkeits-Trennung, Go Wide, Value Tokens, Aristocrats, Artifacts, Mill, Control und Farbfehler ab.
3. Der Fast-Validator schreibt pro erzeugtem Archetyp `<archetype>-opening-hands.json` mit vollständigen Rohdaten und ergänzt die kompakte Zusammenfassung in den Validierungsbericht.

### Validierung vor Commit

- Syntaxprüfung der geänderten Python-Dateien: bestanden
- gezielte Tests in einer kontrollierten, API-kompatiblen Testumgebung: 15 bestanden in 0,77 Sekunden
- identischer Seed erzeugte identische 100 Hände; anderer Seed veränderte die Stichprobe
- bestehende aggregierte Simulator-Tests blieben in der kontrollierten Suite enthalten
- vollständige Repository-Testsuite und Fast-Validierung müssen durch den neuen PR-Workflow verifiziert werden, da im lokalen Ausführungscontainer kein direkter GitHub-Checkout möglich war

### Starthand-Seed und Rohdatenpfad

- Seed: `1701`
- Stichprobe: exakt 100 Hände je im Fast-Lauf erzeugter Deckliste
- Rohdaten: `artifacts/global/<archetype>/<archetype>-opening-hands.json`

### Qualitätsvergleich vor der Änderung

- Burn: Benchmark 83; Early Play 100 %; Core bis Zug 3 0 %
- Tokens: Benchmark 90; Early Play 98 %; Core bis Zug 3 0 %
- Artifacts: Benchmark 90; Early Play 99 %; Core bis Zug 3 100 %
- Mill: Benchmark 78; Early Play 99 %; Core bis Zug 3 31 %
- Control: nicht im ausführbaren Validator vorhanden

Diese Werte bestätigen die Messlücke: hohe Early-Play-Raten beweisen insbesondere bei Burn und Tokens keinen erkannten Hauptplan.

### Ergebnis vor Push

Die Messung ist implementiert und gezielt getestet. Eine spielerische Verbesserung wird noch nicht behauptet; der Zyklus verbessert zunächst Messbarkeit und Reproduzierbarkeit.

### KGB-Entscheidung

Keine neue v2-KGB in diesem Commit.

Gründe:

- Control fehlt weiterhin als erzeugter Pflichtarchetyp
- die neue vollständige Testsuite, Fast-Laufzeit und Rohdatenartefakte müssen post-push verifiziert werden
- der bisherige Regressionsvergleich besitzt keine wiederhergestellte Baseline

### Confidence

- hoch für deterministische Datenerzeugung und Rohdatenstruktur
- mittel für die rollen-/gründe-basierte Planerkennung
- niedrig bis mittel für globale spielerische Aussagekraft vor echten Builder-/Clubbenchmarks

### Kritische Reflexion

- Falsche Annahme: Rollen und Auswahlgründe könnten den tatsächlichen Kartentext nicht zuverlässig genug repräsentieren.
- Alternative Erklärung: Schlechte Planfähigkeitsraten könnten von zu strengen Heuristiken statt von schlechten Decklisten stammen.
- Overfitting-Risiko: Die kontrollierten Fixtures sind fachlich eindeutig, aber einfacher als reale Kartenpakete.
- Messlücke: Matchupsensitivität von Control-Antworten ist noch nicht vollständig modelliert.
- Grüne CI würde nur technische Stabilität zeigen, nicht automatisch bessere Decks.
- Unentdeckte Regression: Die zusätzliche 100-Hand-Auswertung könnte die Fast-Laufzeit oder Artefaktgröße erhöhen; dies muss im Workflow geprüft werden.

### Mögliche Folgeschritte

1. **Control als fünften Builder-/Validator-Archetyp integrieren** – sehr hoher globaler Qualitätsgewinn, hohe Evidenz aus der v2-Inkonsistenz, mittlerer bis hoher Aufwand, mittleres Risiko.
2. **Oracle-Text in `DeckEntry` beziehungsweise Handrollen durchreichen** – hoher Messqualitätsgewinn, mittlere Evidenz, mittlerer Aufwand, Risiko breiter Datenmodelländerungen.
3. **Token-Grenzwerte anhand der neuen Rohhände kalibrieren** – hoher möglicher Spielgewinn, aber erst nach erfolgreicher Workflow- und Control-Basis sinnvoll; mittlerer Aufwand, höheres Overfitting-Risiko.

### Priorisierter nächster ausführbarer Schritt

Nach erfolgreicher Auswertung des neuen Workflows Control als fünften allgemeinen Builder- und Validator-Archetyp integrieren, Shrines aus der Pflichtvalidierung entfernen und Control-Starthände sowie Matchups gegen Aggro, Tokens und einen Nichtkreaturen-/Engine-Plan mit denselben 100-Hand-Rohdaten prüfen.
