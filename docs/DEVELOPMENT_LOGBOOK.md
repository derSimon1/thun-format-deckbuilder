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

### Legacy-KGB-Kandidat

- Commit: `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- Workflow: Run `30762470833`, erfolgreich
- Evidenz: 225 Tests bestanden; Fast-Lauf ungefähr drei Minuten; Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte vorhanden
- Einschränkung: damalige Referenzgruppe enthielt Shrines statt Control; die v2.0-Starthand- und KGB-Regeln waren noch nicht vollständig umgesetzt
- Status: nur Vergleichs- und Wiederanlaufpunkt, keine voll qualifizierte v2.0-KGB
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
- die nachfolgenden Konsistenz-Commits müssen durch ihren eigenen PR-Workflow verifiziert werden
- grüne CI allein würde weiterhin keine v2.0-KGB begründen

### Ergebnis

Die Repository-Dokumente verwenden nun dieselbe Referenzgruppe und dasselbe Mehrstunden-, Baseline- und Wiederanlaufmodell.

### KGB-Entscheidung

Keine neue v2.0-KGB.

Grund: Der dokumentierte grüne Stand enthält noch keinen vollständigen v2.0-Qualitätsvergleich mit Control und keine gespeicherten 100-Starthände je Referenzdeck.

### Confidence

Hoch für die Prozesskonsistenz; mittel für den Legacy-KGB-Kandidaten; keine Aussage über eine neue spielerische Baseline.

### Kritische Reflexion

- Annahme, die falsch sein könnte: Der Legacy-KGB-Kandidat ist möglicherweise spielerisch schwächer als ein späterer Commit, obwohl er der letzte breit dokumentierte grüne Stand ist.
- Alternative Erklärung: Fehlende v2.0-KGB bedeutet primär eine Messlücke und nicht zwingend fehlende Deckqualität.
- Overfitting-Risiko: Die neuen Regeln könnten zunächst mehr Reporting als tatsächliche spielerische Verbesserung erzeugen.
- Datenlücke: Control ist noch nicht vollständig als Builder- und Matchup-Referenz integriert.
- Unentdeckte Regression: Bestehende Validierungsskripte können weiterhin Shrines voraussetzen oder Control noch nicht vollständig abdecken.

### Mögliche Folgeschritte

1. **KGB-Bootstrap und OpeningHandPlanReport** – höchster erwarteter globaler Qualitätsgewinn, hohe Evidenz, mittlerer Aufwand, mittleres Implementierungsrisiko.
2. **Control sofort vollständig integrieren** – hoher globaler Qualitätsgewinn, mittlere Evidenz, hoher Aufwand, höheres Risiko wegen fehlender Starthand-Basis.

### Priorisierter nächster ausführbarer Schritt

Bestimme den letzten belastbaren Vergleichsstand als Legacy-KGB-Kandidaten und implementiere beziehungsweise vervollständige anschließend den reproduzierbaren `OpeningHandPlanReport` mit genau 100 gespeicherten Händen je verwendeter Referenzdeckliste, dokumentiertem Seed, getrennten Keepability-/Early-Play-/Planfähigkeitsmetriken und archetypenabhängigen Kriterien für Burn, Tokens, Artifacts, Control und Mill.
