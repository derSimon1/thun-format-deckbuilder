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

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 1: Token-Plan-Erkennung

### Ziel

Den Token-Hauptplan vor der Kartenauswahl explizit bestimmen und die Kartenbewertung an diesen Plan binden.

### Ausgangslage

- Ausgangs-Head: `ec0748574e639d3902f356b2872d0ebe6c730b57`
- PR #14 offen, mergeable und Draft
- letzter PR-Workflow: Run `30784219809`, erfolgreich
- bisherige Token-Bewertung war faktisch auf Go Wide zugeschnitten und konnte Value Tokens oder Aristocrats nicht als eigenständige Pläne behandeln

### Hypothese

Eine konservative, kartenname-unabhängige Signalerkennung kann Go Wide, Value Tokens und Aristocrats unterscheiden. Wird genau ein Plan vor der Komposition ausgewählt und in der Bewertung verwendet, sinkt das Risiko von Rollen-Mischmasch.

### Änderungen

1. Neuer Token-Plan-Detektor mit strukturierten Signalen, Supportwerten und Confidence.
2. Planabhängige Token-Kartenbewertung für Go Wide, Value Tokens und Aristocrats.
3. Token-Generator bestimmt den Plan vor der Auswahl, lässt echte Sacrifice-Pieces zu und schreibt den gewählten Plan in den Profilnamen.
4. Vier gezielte Regressionstests für alle drei Pläne und planfremde Kartenpakete.

### Validierung

- isolierte zielgerichtete Tests der neuen Plan- und Scoringlogik: 4 bestanden
- Syntaxprüfung der neuen und geänderten Module: bestanden
- vollständige Repository-Tests und PR-Fast-Validierung: nach Commit durch den neuen PR-Workflow zu verifizieren

### Vorläufiges Ergebnis

Der Hauptplan wird jetzt vor der Komposition gewählt und die Bewertung bevorzugt Karten, die diesen Plan unterstützen. Der bisherige Standard bleibt bei Gleichstand konservativ Go Wide.

### Confidence

Mittel. Die Kernlogik ist gezielt getestet; hohe Confidence erst nach grüner vollständiger CI und Prüfung der erzeugten Token-Artefakte.

### Lessons Learned

- Subarchetypen lassen sich über wiederverwendbare Oracle-Text- und Rollensignale modellieren, ohne konkrete Kartenlisten fest zu codieren.
- Ein einzelnes Sacrifice- oder Draw-Wording darf nicht den gesamten Plan umleiten; deshalb werden Pläne ohne mehrere Supportsignale abgewertet.
- Planerkennung allein reicht noch nicht: Die Rollenminimums des Deckprofils sind weiterhin für alle Token-Pläne identisch.

### Offene Risiken

- Die Auswahl erfolgt aus der gesamten legalen Mono-White-Kandidatenmenge; die Verteilung realer Karten kann einen Plan durch reine Verfügbarkeit bevorzugen.
- Planspezifische Rollenminimums, Engine Density und Finish Density fehlen noch.
- Matchup-Extreme müssen weiterhin gegen echte Clubtests geprüft werden.

### Nächster Schritt

PR-Workflow und Artefakte prüfen. Danach planspezifische Rollenminimums sowie einen expliziten Strategy-Commitment-Bericht ergänzen.
