# Development Logbook

Dieses Dokument ist das chronologische Projektgedächtnis. Es hält nicht nur Änderungen, sondern vor allem Hypothesen, Ergebnisse und Lessons Learned fest.

## Eintragsformat

```text
Datum / Zyklus
Ziel
Ausgangslage
Hypothese
Änderungen
Validierung
Ergebnis
Confidence
Lessons Learned
Offene Risiken
Nächster Schritt
```

---

## 2026-08-02 – Globale Kalibrierung und Token-Combat

### Ziel

Archetypenübergreifende Kalibrierung für Burn, Tokens, Artifacts, Shrines und Mill; Tokens als priorisierter Problemfall.

### Ausgangslage

- Branch: `codex/global-deckbuilder-calibration`
- PR: #14
- Izzet-Prowess-Arbeiten in PR #13 getrennt
- Fast-Validierung mit fünf Archetypen und drei Token-Matchups

### Bestätigte Verbesserungen

- robuste Scryfall-Bulkdatenbank und Cache
- vollständige Testsuite im Fast-Lauf
- Opening-Hand-, Goldfish-, Benchmark-, Matchup- und BO3-Berichte
- realistischere Token-Combat-Simulation
- Regressionstests für Summoning Sickness, leere Anthem-Boards und Payoff-Wirkung

### Letzter bestätigter Stand

- Branch-Head: `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- letzter bestätigter PR-Workflow: Run `30762470833`, erfolgreich
- 225 Tests bestanden
- Fast-Lauf ungefähr drei Minuten
- Tokens: durchschnittlicher Schaden bis Zug 5 etwa 19,54; Killrate bis Zug 5 etwa 72 %; Benchmark 94; Qualität 95
- Token-Matchups: Burn 0/0, Artifacts 20/35, Mill 100/100 für BO1/BO3

### Lessons Learned

1. Rollenpunkte allein erzeugen noch kein gutes Tokendeck.
2. Combat-Simulation brachte einen deutlich größeren Erkenntnisgewinn als zusätzliche oberflächliche Matchups.
3. Token-Payoffs dürfen ohne vorhandenes Board keinen fiktiven Schaden erzeugen.
4. Token-Maker müssen Summoning Sickness korrekt berücksichtigen.
5. Ein klarer Token-Subarchetyp muss vor der Kartenauswahl feststehen.
6. Strategy Commitment, Engine Density und Finish Density sind zentrale nächste Bausteine.

### Offene Fragen

- Wie werden Go Wide, Value Tokens und Aristocrats zuverlässig erkannt?
- Wie wird verhindert, dass der Builder Rollen-Mischmasch als hohe Qualität bewertet?
- Wie werden Engine- und Finisher-Dichten archetypenübergreifend modelliert?
- Wie werden Referenzdecks und Thun-Meta-Benchmarks sauber integriert?

### Nächster Schritt

Token-Subarchetyp-Erkennung und planabhängige Rollenpriorisierung implementieren und mit gezielten Regressionstests absichern.

---

## 2026-08-02/03 – Nachtkalibrierung fehlgeschlagen

### Ziel

Mehrstündige autonome Kalibrierung mit vier ChatGPT-Aufgaben pro Stunde und einem GitHub-Zeitplan-Workflow.

### Erwartung

- etwa 24 ChatGPT-Zyklen
- regelmäßig neue, belegte Verbesserungen
- Commit nach sinnvoller Änderung
- anschließende CI-Verifikation
- fortlaufendes Lernen und Dokumentieren

### Tatsächliches Ergebnis

- über Nacht liefen nur drei sichtbare GitHub-Workflows
- auf PR #14 entstand kein neuer Code- oder Testcommit
- der Branch-Head blieb auf `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- die Aufgaben wiederholten überwiegend Status- und Sicherheitsprüfungen
- die geplante Dokumentationsstruktur wurde in der Nacht nicht erstellt
- der Abschlussjob deaktivierte den automatischen Zeitplan planmäßig

### Ursachenanalyse

1. GitHub Actions validierte nur vorhandenen Code und konnte selbst keine Verbesserungen entwickeln.
2. Der Cron-Zeitplan wurde fälschlich als Entwicklungsantrieb behandelt.
3. Die ChatGPT-Aufgaben waren zu defensiv und stoppten häufig ohne Commit.
4. Es fehlte eine Fortschrittsregel gegen wiederholte No-Change-Zyklen.
5. Es fehlte ein persistentes Logbuch mit exaktem Stopgrund und nächster ausführbarer Hypothese.
6. Die Anzahl der Workflowläufe wurde mit Produktivität verwechselt.

### Zentrale Entscheidung

GitHub Actions ist künftig Validator, nicht Entwicklungsagent. Ein produktiver Zyklus beginnt mit einer konkreten Hypothese und endet entweder mit einem sinnvollen Commit plus verifiziertem Workflow oder mit einem dokumentierten Stopgrund plus nächstem ausführbarem Schritt.

### Neue Schutzregeln

- keine Dummy-Commits
- nach zwei gleichen No-Change-Zyklen Priorität wechseln
- nach Commit Run-ID innerhalb von zehn Minuten prüfen
- jeder No-Change-Zyklus muss Erkenntnis und nächsten Schritt liefern
- Zeitplan-Workflows gelten nicht als Beleg für Entwicklungsfortschritt

### Confidence

Hoch. Branch-Historie, PR-Head und Workflowverhalten bestätigen die Diagnose.

### Nächster Schritt

Development System v1.0 im Repository verankern und den nächsten Lauf ausschließlich über die versionierte Spezifikation und den versionierten Kalibrierungsprompt steuern.
