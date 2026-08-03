# Global Calibration Prompt

**Version:** 1.0  
**Verbindliche Grundlage:** `docs/SPECIFICATION.md`

## Verwendung

Der externe Auftrag soll nur Repository, Branch/PR und Laufzeit nennen. Diese Datei enthält die vollständige Arbeitsanweisung.

## Auftrag

Arbeite im Repository `derSimon1/thun-format-deckbuilder` gemäß der aktuellen Version von:

- `docs/SPECIFICATION.md`
- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/META.md`

Arbeite auf dem im externen Auftrag genannten Branch und Pull Request. Falls nichts anderes genannt ist, verwende `codex/global-deckbuilder-calibration` und PR #14. PR #13 und Izzet-Prowess-spezifische Arbeiten bleiben unangetastet.

## 1. Startprüfung

Zu Beginn jedes Zyklus:

1. Verifiziere GitHub-Zugriff.
2. Lies Spezifikation, Logbuch, Roadmap, Entscheidungen und bekannte Probleme.
3. Prüfe Branch-Head, PR-Status, Mergeability und aktive CI.
4. Prüfe den letzten erfolgreichen Workflow, Jobs, Logs und Artefakte.
5. Prüfe, ob seit dem letzten dokumentierten Zyklus neue Commits oder Erkenntnisse entstanden sind.
6. Halte den Ausgangs-Head fest.

Stoppe ohne Commit, wenn aktive CI, ein veränderter Head, Parallelität oder eine unklare Ursache vorliegt. Dokumentiere dann den exakten Stopgrund und den nächsten ausführbaren Schritt.

## 2. Priorisierung

Arbeite in dieser Reihenfolge, solange die Dokumentation nichts Neueres vorgibt:

1. Token-Subarchetyp-Erkennung
2. Strategy Commitment
3. Engine Density
4. Finish Density
5. belastbare Baseline und Regressionserkennung
6. Meta-Benchmark

Wähle pro Zyklus die Hypothese mit dem höchsten erwarteten globalen Qualitätsgewinn pro Entwicklungsaufwand. Tokens haben Priorität; Shrines dienen nur als Regressionstest.

## 3. Token-Regeln

Bestimme vor der Kartenauswahl einen Hauptplan:

- Go Wide
- Value Tokens
- Aristocrats

Bewerte anschließend planabhängig:

- frühe Maker
- passende Payoffs
- wiederholbare Engines
- Finisher
- Card Advantage
- Interaktion
- Manakurve
- realistische Combat-Performance

Ein hoher Token-Maker-, Payoff- oder Rollenwert allein genügt nicht. Rollen-Mischmasch ohne Hauptplan ist negativ zu bewerten. Standard- und Pioneer-Konzepte dürfen als Referenz für allgemeine Regeln genutzt werden, aber nicht blind kopiert werden.

## 4. Änderungspaket

Pro Zyklus darfst du höchstens drei eng gekoppelte Änderungen oder Tests derselben Ursache umsetzen. Beispiele für zulässige Pakete:

- Erkennung + Scoring + Regressionstests eines Token-Subarchetyps
- Engine-Density-Metrik + Bericht + Tests
- belegter CI-Fix + zugehöriger Test

Nicht zulässig:

- mehrere unabhängige Themen in einem Commit
- Grenzwerte nur zum Bestehen verändern
- Dummy-Commits
- unbelegte archetypspezifische Sonderfälle
- Änderungen an PR #13

## 5. Validierung

Vor Commit:

1. vollständige Testsuite ausführen
2. Fast-Validierung ausführen
3. alle fünf Archetypen vergleichen
4. drei Token-priorisierte Matchups und schnelle BO3-Berichte prüfen
5. Laufzeit unter zehn Minuten halten
6. unbegründete Regressionen ausschließen
7. Branch-Head und aktive CI erneut prüfen

Fast bleibt kurz und entwicklungsnah. Full bleibt unverändert und wird manuell oder am Abschluss ausgeführt.

## 6. Commit und Workflow

Bei erfolgreicher Validierung:

1. Erstelle genau einen klar benannten Commit.
2. Verifiziere innerhalb von zehn Minuten eine neue Workflow-Run-ID.
3. Prüfe Status, Jobs, Logs und Artefakte.
4. Bei roter CI behebe in einem späteren Zyklus höchstens eine eindeutig belegte Ursache.
5. Fehlt ein erwarteter Lauf, prüfe Workflow-Aktivierung, Trigger, Branch-/Pfadfilter, Workflowdatei auf `main`, `concurrency` und Trigger-Commit.
6. Erzeuge keinen Dummy-Commit zum Triggern.

GitHub Actions ist Validator. Ein Zeitplanlauf ohne neuen Code gilt nicht als Entwicklungsfortschritt.

## 7. No-Change-Regel

Wenn keine sichere Änderung möglich ist, liefere zwingend:

- geprüfte Hypothese
- exakten Stopgrund
- gewonnene Erkenntnis
- Confidence
- nächsten ausführbaren Schritt

Nach zwei aufeinanderfolgenden No-Change-Zyklen mit derselben Ursache wechsle zum nächsten priorisierten Roadmap-Punkt. Wiederhole nicht endlos dieselben Statusprüfungen.

Ein No-Change-Zyklus darf stattdessen produktiv nutzen:

- gezielte Tests vorbereiten
- technische Schulden dokumentieren
- Referenzkonzepte analysieren
- offene Hypothesen präzisieren
- Baseline- oder Berichtslücken untersuchen

Ohne belegte Änderung wird nicht committed.

## 8. Dokumentation

Nach jedem Zyklus aktualisiere bei Bedarf:

- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/ROADMAP.md`
- `docs/META.md`

Ändere `docs/SPECIFICATION.md` nur bei belegten neuen Erkenntnissen und dokumentiere jede Änderung in `docs/CHANGELOG_SPECIFICATION.md`.

Jeder Logbucheintrag beantwortet:

1. Was wurde verbessert?
2. Was wurde gelernt?
3. Was ist der nächste Schritt?

Zusätzlich festhalten:

- Ausgangs- und Ziel-Head
- Commit-SHA
- Workflow-Run-ID
- Tests und Laufzeit
- Regressionen
- Confidence
- Stopgrund, falls kein Commit entstand

## 9. Laufzeitsteuerung

Der externe Auftrag gibt `X` Stunden vor. Beginne sofort mit dem ersten Zyklus. Verwende die verfügbare Zeit für mehrere aufeinanderfolgende, abgeschlossene Entwicklungszyklen. Starte keinen neuen Änderungsschritt, wenn er vor Ablauf der Laufzeit nicht mehr sauber validiert und dokumentiert werden kann.

Empfohlener unbeaufsichtigter Rahmen im aktuellen Reifegrad: 8 bis 12 Stunden. Längere Läufe erst nach stabiler Baseline, Meta-Benchmark und nachgewiesener produktiver Zyklussteuerung.

## 10. Abschlussbericht

Am Ende der Laufzeit:

- vollständigen Testsatz und Full-Validierung ausführen, sofern zeitlich möglich
- alle Commits und Run-IDs auflisten
- Qualitätsentwicklung je Archetyp zusammenfassen
- bestätigte und widerlegte Hypothesen nennen
- Regressionen und offene Risiken nennen
- Roadmap aktualisieren
- Spezifikationslücken als Vorschläge dokumentieren
- einen kurzen Folgeauftrag für die nächste Runde formulieren

Erfinde keine Ergebnisse. Trenne Fakten, Schlussfolgerungen und offene Hypothesen klar.
