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

---

## 2026-08-02/03 – Nachtkalibrierung fehlgeschlagen

### Tatsächliches Ergebnis

- über Nacht liefen nur drei sichtbare GitHub-Workflows
- auf PR #14 entstand kein neuer Code- oder Testcommit
- die Aufgaben wiederholten überwiegend Status- und Sicherheitsprüfungen
- der Abschlussjob deaktivierte den automatischen Zeitplan planmäßig

### Ursachenanalyse

1. GitHub Actions validierte nur vorhandenen Code und konnte selbst keine Verbesserungen entwickeln.
2. Der Cron-Zeitplan wurde fälschlich als Entwicklungsantrieb behandelt.
3. Die ChatGPT-Aufgaben waren zu defensiv und stoppten häufig ohne Commit.
4. Es fehlte eine Fortschrittsregel gegen wiederholte No-Change-Zyklen.
5. Es fehlte ein persistentes Logbuch mit exaktem Stopgrund und nächster ausführbarer Hypothese.

### Zentrale Entscheidung

GitHub Actions ist künftig Validator, nicht Entwicklungsagent. Ein produktiver Zyklus beginnt mit einer konkreten Hypothese und endet entweder mit einem sinnvollen Commit plus verifiziertem Workflow oder mit einem dokumentierten Stopgrund plus nächstem ausführbarem Schritt.

### Confidence

Hoch.

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 1: Token-Plan-Erkennung

### Ziel

Den Token-Hauptplan vor der Kartenauswahl explizit bestimmen und die Kartenbewertung an diesen Plan binden.

### Ausgangslage

- Ausgangs-Head: `ec0748574e639d3902f356b2872d0ebe6c730b57`
- PR #14 offen, mergeable und Draft
- letzter PR-Workflow: Run `30784219809`, erfolgreich

### Hypothese

Eine konservative, kartenname-unabhängige Signalerkennung kann Go Wide, Value Tokens und Aristocrats unterscheiden. Wird genau ein Plan vor der Komposition ausgewählt und in der Bewertung verwendet, sinkt das Risiko von Rollen-Mischmasch.

### Änderungen

1. Neuer Token-Plan-Detektor mit strukturierten Signalen, Supportwerten und Confidence.
2. Planabhängige Token-Kartenbewertung.
3. Token-Generator bestimmt den Plan vor der Auswahl.
4. Vier gezielte Regressionstests.

### Validierung

- vollständiger PR-Workflow: Run `30785153345`, erfolgreich

### Ergebnis

Der Hauptplan wird vor der Komposition gewählt und die Bewertung bevorzugt Karten, die diesen Plan unterstützen.

### Confidence

Hoch für die technische Integration, mittel für die spielerische Kalibrierung bis zum externen Pioneer- und Club-Benchmark.

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 2: Planspezifische Dichteziele

### Ziel

Den erkannten Token-Hauptplan in verbindliche Rollenminimums übersetzen.

### Ausgangslage

- Ausgangs-Head: `5a1db8d9d83bca0ff639d72d9c8884551097cdfc`
- vorheriger Workflow: Run `30785153345`, erfolgreich

### Hypothese

Konservative planspezifische Mindestdichten erzwingen die definierenden Pakete.

### Ergebnis

Die harte Form war zu optimistisch. Der Kompositionsalgorithmus reservierte die letzten vier Slots für eine planprägende Pflichtrolle, konnte aber im Testkartenpool keine weiteren geeigneten Kopien mehr wählen.

### Validierung

- Workflow Run `30786201567`, fehlgeschlagen
- 228 Tests bestanden, 5 fehlgeschlagen
- Fast-Validierung selbst grün, fünf Archetypen und drei Matchups, keine Regressionen

### Confidence

Hoch.

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 3: CI-Hotfix für sparse Rollenpools

### Ziel

Die durch Zyklus 2 verursachte rote CI beheben, ohne Planerkennung oder Scoring zurückzunehmen.

### Ausgangslage

- Ausgangs-Head: `85b146f22118e43cc01c1cc7080c9c66b5be4b15`
- Workflow Run `30786201567`: fehlgeschlagen

### Hypothese

Wenn nur `token_maker` als harte Mindestrolle bleibt und planprägende Supportrollen weiche Zielwerte besitzen, bleibt die Planpräferenz erhalten, ohne sparse Kartenpools zu blockieren.

### Änderungen

1. Planprägende Supportrollen auf weiche Ziele umgestellt.
2. Profiltests unterscheiden harte Maker-Mindestwerte von weichen Supportzielen.
3. Roadmap dokumentiert die spätere kapazitätsbewusste Mindestprüfung.

### Validierung

- Workflow Run `30786777460`, erfolgreich
- vollständige Testsuite und Fast-Validierung grün

### Ergebnis

Die konkret belegte Deadlock-Ursache wurde beseitigt, ohne Planerkennung, Scoring oder weiche Dichteziele zu entfernen.

### Confidence

Hoch.

### Nächster Schritt

Strategy-Commitment-Bericht und Mischmasch-Warnungen implementieren.

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 4: Strategy-Commitment-Bericht

### Ziel

Den gewählten Token-Plan nach der Komposition messbar machen und reines Rollen-Mischmasch explizit warnen, ohne neutrale Interaktion zu bestrafen.

### Ausgangslage

- Ausgangs-Head: `c500e3dced798403f1bc4bddd30464748bc47285`
- PR #14 offen, mergeable und Draft
- Workflow Run `30786777460`: erfolgreich
- Planerkennung und weiche Dichteziele waren vorhanden, aber das erzeugte Deck meldete keine nachvollziehbare Planbindung.

### Hypothese

Ein kopiengewichteter Commitment-Bericht kann planprägende, planfremde und neutrale Karten unterscheiden. Utility wie Removal und Protection muss neutral bleiben; ausschließlich planfremde Rollen ohne gleichzeitig planprägende Rolle sollen den Score senken.

### Änderungen

1. Neuer `StrategyCommitmentReport` mit Plan, Commitment-Score, Rollen-Dichten, committed/conflicting/neutral Kopien und Warnungen.
2. Token-Generator berechnet den Bericht nach der Komposition und schreibt eine kompakte Zusammenfassung sowie Mischmasch-Warnungen in die Deckwarnungen.
3. Drei Regressionstests sichern Go-Wide-Neutralität, planfremde Sacrifice-Pakete und Aristocrats-Rollenbindung.

### Validierung

- Workflow Run `30787546422`, erfolgreich
- vollständige Testsuite und Fast-Validierung grün
- fünf Archetypen, drei Token-Matchups und BO3-Berichte ohne unbegründete Regression

### Ergebnis

Strategy Commitment ist als explizites, kopiengewichtetes Ergebnis sichtbar. Planfremde Rollen erzeugen eine Warnung und senken den Score, während neutrale Interaktion nicht negativ bewertet wird.

### Confidence

Hoch für die technische Integration; spielerische Grenzwerte bleiben bis zum Pioneer- und Club-Benchmark offen.

### Nächster Schritt

Engine Density als nächstes unabhängiges Qualitätsmerkmal modellieren.

---

## 2026-08-03 – Zwei-Stunden-Kalibrierung, Zyklus 5: Token Engine Density

### Ziel

Wiederholbare, planrelevante Engines von einmaligem Token-Material trennen und kopiengewichtet sichtbar machen.

### Ausgangslage

- Ausgangs-Head: `fb6a84440700c72d4e74ee33ef693b3e5d5c3db6`
- PR #14 offen, mergeable und Draft
- Workflow Run `30787546422`: erfolgreich
- Strategy Commitment war messbar; Engine Density fehlte weiterhin als eigener Befund.

### Hypothese

Oracle-Text-Signale können konservativ unterscheiden, ob eine Karte den gewählten Token-Plan wiederholt antreibt oder nur einmal Material erzeugt. Eine kopiengewichtete Dichte plus Zahl unterschiedlicher Engines ist aussagekräftiger als reine Rollenanzahl.

### Änderungen

1. Neuer `EngineDensityReport` mit Engine-Kopien, Zauberkopien, Dichte, unterschiedlichen Engine-Namen und Warnungen.
2. Token-Generator berichtet die Engine Density neben Strategy Commitment; One-shot-Maker zählen nicht als Engines.
3. Drei Regressionstests sichern One-shot-Abgrenzung, wiederholbare Value-Quellen und Aristocrats-Death-Payoffs.

### Validierung

- vollständige Testsuite und Fast-Validierung: durch den neuen PR-Workflow zu verifizieren
- fünf Archetypen, drei Token-Matchups und BO3-Berichte: durch Workflow-Artefakte zu prüfen

### Vorläufiges Ergebnis

Engine Density wird ohne künstlichen Mindestgrenzwert berichtet. Null Engines und Abhängigkeit von nur einer unterschiedlichen Engine erzeugen transparente Warnungen. Damit wird ein hoher Maker- oder Commitment-Wert nicht mehr mit nachhaltigem Kartenvorteil beziehungsweise wiederholbarer Planprogression verwechselt.

### Confidence

Mittel bis zur grünen vollständigen CI und Artefaktprüfung.

### Offene Risiken

- Die Engine-Erkennung ist zunächst tokenspezifisch und muss später archetypenübergreifend abstrahiert werden.
- Planabhängige Engine-Signale sind konservativ; einzelne ungewöhnlich formulierte Karten können unentdeckt bleiben.
- Es wird bewusst noch kein universeller Mindestwert erzwungen, bevor externe Pioneer- und Clubdaten vorliegen.

### Nächster Schritt

PR-Workflow und Artefakte prüfen. Danach Finish Density als getrenntes Qualitätsmerkmal modellieren.
