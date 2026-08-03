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

### Confidence

Hoch. Branch-Historie, PR-Head und Workflowverhalten bestätigen die Diagnose.

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
- vollständiger PR-Workflow: Run `30785153345`, erfolgreich

### Ergebnis

Der Hauptplan wird vor der Komposition gewählt und die Bewertung bevorzugt Karten, die diesen Plan unterstützen. Der bisherige Standard bleibt bei Gleichstand konservativ Go Wide.

### Confidence

Hoch für die technische Integration, mittel für die spielerische Kalibrierung bis zum externen Pioneer- und Club-Benchmark.

### Lessons Learned

- Subarchetypen lassen sich über wiederverwendbare Oracle-Text- und Rollensignale modellieren, ohne konkrete Kartenlisten fest zu codieren.
- Ein einzelnes Sacrifice- oder Draw-Wording darf nicht den gesamten Plan umleiten; deshalb werden Pläne ohne mehrere Supportsignale abgewertet.
- Planerkennung allein reicht nicht: Die Rollenminimums des Deckprofils müssen den gewählten Plan ebenfalls ausdrücken.

### Nächster Schritt

Planspezifische Rollenminimums ergänzen und danach Strategy Commitment explizit berichten.

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 2: Planspezifische Dichteziele

### Ziel

Den erkannten Token-Hauptplan in verbindliche Rollenminimums übersetzen, damit die Komposition nicht trotz korrekter Planerkennung in ein Rollen-Mischmasch zurückfällt.

### Ausgangslage

- Ausgangs-Head: `5a1db8d9d83bca0ff639d72d9c8884551097cdfc`
- PR #14 offen und mergeable
- vorheriger Workflow: Run `30785153345`, erfolgreich
- alle drei Token-Pläne verwendeten weiterhin das unveränderte Go-Wide-Profil

### Hypothese

Konservative planspezifische Mindestdichten erzwingen die definierenden Pakete, ohne die 36 Zauberslots vollständig zu blockieren: Go Wide braucht Maker plus Board-Payoffs, Value Tokens braucht Maker plus Card Advantage, Aristocrats braucht Fodder plus Sacrifice-Outlets plus Death-Payoffs.

### Änderungen

1. Zentrale `token_profile_for_plan`-Funktion mit unterschiedlichen Rollenminimums und Dichtezielen.
2. Token-Generator verwendet das ausgewählte Planprofil direkt bei der Komposition.
3. Vier Regressionstests sichern definierende Mindestpakete und abweichende Landzahlen.

### Validierung

- statische Plausibilitätsprüfung: Mindestpakete bleiben unter den verfügbaren Zauberslots
- vollständige Testsuite und Fast-Validierung: durch den neuen PR-Workflow zu verifizieren
- fünf Archetypen, Token-Matchups und BO3-Berichte: durch die Workflow-Artefakte zu prüfen

### Vorläufiges Ergebnis

Die Planentscheidung beeinflusst nun nicht nur das Scoring, sondern auch die zwingend zu erfüllenden Rollen. Damit wird Strategy Commitment erstmals strukturell in der Komposition verankert.

### Confidence

Mittel bis zum vollständigen grünen Workflow und zur Artefaktprüfung.

### Offene Risiken

- Rollen können überlappen; erfüllte Mindestzahlen sind deshalb noch kein vollständiger Strategy-Commitment-Score.
- Die Mono-White-Kartenmenge könnte für Aristocrats nicht genug echte Outlets enthalten; ein Workflowfehler wäre hier ein nützlicher Kapazitätshinweis statt ein Grund, Mindestwerte blind zu senken.
- Engine Density und Finish Density bleiben separat zu modellieren.

### Nächster Schritt

Workflow und erzeugte Token-Artefakte prüfen. Danach einen expliziten Strategy-Commitment-Bericht ergänzen, der Plan, Soll-/Ist-Dichten, Rollenüberlappung und Mischmasch-Warnungen ausweist.
