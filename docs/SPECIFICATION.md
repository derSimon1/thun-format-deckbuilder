# Deckbuilder Development Specification

**Version:** 1.0  
**Stand:** 2026-08-03  
**Status:** verbindliche Arbeitsgrundlage

## 0. Mission

Der Thun-Format-Deckbuilder soll nicht nur legale Decklisten erzeugen, sondern spielstarke, kohärente Decks mit klarer Strategie, sinnvoller Kurve, belastbarer Manabasis, realistischen Winconditions und nachvollziehbarer Qualität. Verbesserungen müssen möglichst archetypenübergreifend wirken und durch Tests, Simulationen, Benchmarks oder belastbare Referenzen begründet sein.

## 1. Single Source of Truth

Für Kalibrierungsarbeiten sind diese Dateien verbindlich:

1. `docs/SPECIFICATION.md`
2. `docs/PROMPTS/global-calibration.md`
3. `docs/DEVELOPMENT_LOGBOOK.md`
4. `docs/ROADMAP.md`
5. `docs/DECISIONS.md`
6. `docs/KNOWN_ISSUES.md`
7. `docs/META.md`

Bei Widersprüchen gilt folgende Reihenfolge: Spezifikation vor Prompt, Prompt vor Roadmap, dokumentierte Entscheidungen vor offenen Ideen.

## 2. Entwicklungsprinzipien

- Spielplan vor Kartenauswahl.
- Globale Regeln vor archetypspezifischen Sonderfällen.
- Keine Grenzwerte nur zum Bestehen von Tests verschieben.
- Keine unbelegten Optimierungen.
- Keine Dummy-Commits nur zum Auslösen von CI.
- Shrines dienen vorerst als Regressionstest und werden nicht gezielt optimiert, solange keine globale Ursache vorliegt.
- Offene Izzet-Prowess-Arbeiten in PR #13 bleiben getrennt.
- Ein technischer Erfolg ist nicht automatisch ein spielerisch überzeugendes Deck.

## 3. Arbeitsmodell einer Kalibrierung

Ein Kalibrierungszyklus besteht aus:

1. Repository-, Branch-, PR- und CI-Status prüfen.
2. Letzten erfolgreichen Bericht und offene Prioritäten lesen.
3. Eine konkrete, testbare Hypothese wählen.
4. Höchstens drei eng gekoppelte Änderungen derselben Ursache umsetzen.
5. Vollständige Testsuite und Fast-Validierung ausführen.
6. Vor Commit Branch-Head und aktive CI erneut prüfen.
7. Genau einen zusammenhängenden Commit erstellen.
8. Neue Workflow-Run-ID verifizieren und Ergebnis auswerten.
9. Erkenntnisse, Entscheidung und nächsten Schritt dokumentieren.

## 4. Produktivität statt Leerlauf

Ein Zyklus darf ohne Codeänderung enden, wenn eine Sicherheitsbedingung greift oder keine belegte Verbesserung möglich ist. Dann sind jedoch zwingend zu dokumentieren:

- exakter Stopgrund,
- geprüfte Hypothese,
- gewonnene Erkenntnis,
- nächster ausführbarer Schritt.

Nach zwei aufeinanderfolgenden No-Change-Zyklen mit derselben Ursache muss zum nächsten priorisierten Roadmap-Punkt gewechselt werden. Dieselben Prüfungen dürfen nicht endlos wiederholt werden.

## 5. CI und Workflow-Regeln

GitHub Actions validiert Änderungen; GitHub-Cron ist nicht der Motor der Entwicklung.

- Ein neuer PR-Workflow wird nach einem sinnvollen Commit erwartet.
- Zeitgesteuerte Läufe sind optional und dürfen nicht als Beweis produktiver Entwicklung gelten.
- Nach Commit muss innerhalb von zehn Minuten geprüft werden, ob eine neue Run-ID entstanden ist.
- Fehlt ein erwarteter Lauf, sind Workflow-Aktivierung, Trigger, Branch-/Pfadfilter, Workflowdatei auf `main`, `concurrency` und Trigger-Commit zu prüfen.
- Es darf höchstens eine eindeutig belegte Infrastrukturursache pro Zyklus behoben werden.
- Fast-Validierung soll unter zehn Minuten bleiben.
- Full-Validierung erfolgt manuell oder als Abschlusslauf.
- Bei aktiver CI, verändertem Head oder unklarer Ursache wird nicht committed.

## 6. Qualitätsmodell

Ein Deck wird mindestens anhand folgender Ebenen bewertet:

- Legalität, Deckgröße, Kopienlimit und Farbidentität
- Manabasis und Kurve
- frühe Spielbarkeit
- Strategy Commitment
- Engine Density
- Finish Density
- Card Advantage und Interaktion
- realistische Goldfish-/Combat-Performance
- Matchups und BO3-Verhalten
- archetypenübergreifende Regressionen

Eine hohe Rollenzahl allein ist kein Qualitätsnachweis.

## 7. Token-Priorität

Tokens sind derzeit der priorisierte Archetyp. Vor Kartenauswahl muss ein Hauptplan erkannt werden:

- Go Wide
- Value Tokens
- Aristocrats

Zu prüfen sind insbesondere:

- frühe Token-Maker,
- passende Payoffs,
- Engine-Dichte,
- klare Finisher,
- Card Advantage,
- Interaktion,
- kohärente Rollenverteilung.

Rollen-Mischmasch ohne klaren Hauptplan ist ein Qualitätsproblem. Erfolgreiche Standard- und Pioneer-Konzepte dürfen als Referenz für allgemeine Regeln dienen, aber nicht blind kopiert werden.

## 8. Hypothesen und Confidence

Jede Optimierung erhält eine Einschätzung:

- **hoch:** durch Tests oder mehrere Datenquellen klar bestätigt
- **mittel:** mehrere belastbare Indizien
- **niedrig:** plausible, noch nicht ausreichend geprüfte Hypothese

Niedrige Confidence rechtfertigt Experimente und Tests, aber keine weitreichende Produktionsregel ohne zusätzliche Evidenz.

## 9. Dokumentationspflicht

Nach jedem produktiven Zyklus sind mindestens zu aktualisieren:

- `DEVELOPMENT_LOGBOOK.md` bei neuen Erkenntnissen,
- `DECISIONS.md` bei dauerhaften Architektur- oder Prozessentscheidungen,
- `KNOWN_ISSUES.md` bei neu entdeckten Problemen,
- `ROADMAP.md` bei geänderter Priorität,
- `CHANGELOG_SPECIFICATION.md` bei Änderungen dieser Spezifikation.

Die Spezifikation darf nur bei belegten neuen Erkenntnissen geändert werden. Keine stillen Regeländerungen.

## 10. Abschlusskriterien

Eine Kalibrierungsrunde endet mit:

1. Was wurde verbessert?
2. Was wurde gelernt?
3. Was ist der nächste priorisierte Schritt?
4. Welche Tests und Workflows liefen mit welchen Run-IDs?
5. Welche Regressionen oder offenen Risiken bleiben?

Der Abschlussbericht muss klar zwischen tatsächlichen Ergebnissen, Schlussfolgerungen und offenen Hypothesen unterscheiden.
