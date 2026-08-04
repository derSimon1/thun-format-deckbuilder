# Deckbuilder Development Specification

**Version:** 2.0  
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

Bei Widersprüchen gilt: Spezifikation vor Prompt, Prompt vor Roadmap, dokumentierte Entscheidungen vor offenen Ideen. Ältere externe Aufgabenformulierungen treten hinter den aktuellen Repository-Dokumenten zurück.

## 2. Entwicklungsprinzipien

- Spielplan vor Kartenauswahl.
- Globale Regeln vor archetypspezifischen Sonderfällen.
- Keine Grenzwerte nur zum Bestehen von Tests verschieben.
- Keine unbelegten Optimierungen.
- Keine Dummy-Commits nur zum Auslösen von CI.
- Offene Izzet-Prowess-Arbeiten in PR #13 bleiben getrennt und unangetastet.
- Ein technischer Erfolg ist nicht automatisch ein spielerisch überzeugendes Deck.
- Grüne CI allein beweist weder höhere Deckqualität noch eine neue Baseline.
- Jede Verbesserung wird gegen die letzte Known Good Baseline bewertet.

## 3. Referenzarchetypen

Die fünf verbindlichen allgemeinen Referenzarchetypen sind:

- Burn
- Tokens
- Artifacts
- Control
- Mill

Tokens werden zusätzlich in Go Wide, Value Tokens und Aristocrats getrennt bewertet.

Shrines ist kein Pflicht- oder Referenzarchetyp. Es darf nur optional als spezieller Regressionstest für mehrfarbige Engine-Decks verwendet werden, wenn konkrete Evidenz dies begründet.

## 4. Mehrstundenbetrieb

Der externe Auftrag nennt Repository, Branch/PR und die verfügbare Laufzeit `X` in Stunden.

Während dieser Laufzeit werden so viele vollständige produktive Kalibrierungszyklen wie sinnvoll möglich durchgeführt. Es werden keine separaten 15-Minuten-Aufgaben benötigt. GitHub Actions ist Validator und kein Entwicklungsagent.

Ein neuer Zyklus darf nur begonnen werden, wenn er innerhalb der verbleibenden Laufzeit voraussichtlich vollständig implementiert, getestet, validiert, dokumentiert und abgeschlossen werden kann. Restzeit wird für Abschlussvalidierung, CI-Auswertung, Artefaktprüfung, Logbook, Roadmap und Abschlussbericht verwendet.

## 5. Arbeitsmodell eines Kalibrierungszyklus

Ein vollständiger Zyklus besteht aus:

1. Repository-, Branch-, PR-, Mergeability- und CI-Status prüfen.
2. Letzten erfolgreichen Workflow, Jobs, Logs und Artefakte prüfen.
3. Letzte Known Good Baseline und offenen nächsten Schritt lesen.
4. Genau eine konkrete, testbare Hypothese mit hohem erwartetem globalem Qualitätsgewinn wählen.
5. Höchstens drei eng gekoppelte Änderungen derselben Ursache umsetzen.
6. Vollständige Testsuite, Fast-Validierung und Referenzvergleiche ausführen.
7. Gegen die letzte Known Good Baseline vergleichen.
8. Vor Commit Branch-Head, PR-Head, Mergeability und aktive CI erneut prüfen.
9. Genau einen zusammenhängenden Commit erstellen.
10. Neue Workflow-Run-ID verifizieren und Status, Jobs, Logs und Artefakte auswerten.
11. Kritische Reflexion durchführen.
12. Logbook und Roadmap aktualisieren und genau einen nächsten ausführbaren Schritt bestimmen.
13. Entscheiden, ob eine neue Known Good Baseline entstanden ist.

Zusätzliche Cast-Kosten sind Teil der Castability-Invariante. Eine Karte darf
in einer Simulation nur gewirkt werden, wenn neben Mana auch die verlangten
Boardressourcen vorhanden sind; bezahlte Ressourcen werden vor Anwendung des
Karteneffekts verbraucht. Maschinenlesbare Kostenmarker bleiben am finalen
Deckeintrag erhalten, zählen aber nicht als funktionale Deckrolle.

## 6. Produktivität, No-Change und Regressionen

Ein Zyklus darf ohne Codeänderung enden, wenn eine Sicherheitsbedingung greift oder keine belegte Verbesserung möglich ist. Dann sind zwingend zu dokumentieren:

- geprüfte Hypothese,
- verwendete Daten,
- exakter Stopgrund,
- gewonnene Erkenntnis,
- Confidence,
- mindestens zwei Folgeschritte,
- genau ein priorisierter nächster ausführbarer Schritt.

Nach zwei aufeinanderfolgenden No-Change-Zyklen derselben Ursache muss zum nächsten priorisierten Roadmap-Punkt gewechselt werden.

Nach zwei aufeinanderfolgenden unbegründeten Regressionen derselben Hypothese wird diese Hypothese pausiert. Der nächste priorisierte Roadmap-Punkt wird bearbeitet; zur pausierten Hypothese darf erst bei neuer belegter Evidenz zurückgekehrt werden.

## 7. CI- und Workflow-Regeln

GitHub Actions validiert Änderungen; GitHub-Cron ist nicht der Motor der Entwicklung.

- Ein neuer PR-Workflow wird nach einem sinnvollen Commit erwartet.
- Nach Commit muss innerhalb von zehn Minuten geprüft werden, ob eine neue Run-ID entstanden ist.
- Fehlt ein erwarteter Lauf, sind Workflow-Aktivierung, Trigger, Branch-/Pfadfilter, Workflowdatei auf `main`, `concurrency` und Trigger-Commit zu prüfen.
- Es darf höchstens eine eindeutig belegte Infrastrukturursache pro Zyklus behoben werden.
- Fast-Validierung soll unter zehn Minuten bleiben.
- Full-Validierung erfolgt manuell oder als Abschlusslauf.
- Bei aktiver CI, verändertem Head oder unklarer Ursache wird nicht committed.
- Während ein Workflow läuft, darf nur an einem nachweislich unabhängigen Schritt gearbeitet werden.

## 8. Qualitätsmodell

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

Sideboard-Optimierung muss zusammenhängende Mengen von eins bis zur legal
verfügbaren Kopienzahl prüfen. Ein Paket darf nicht verworfen werden, nur weil
seine erste Einzelkopie einen gerundeten Matchupwert noch nicht verbessert.
Zielabhängiger Lebensgewinn nach „destroy/exile target“ ist kein
eigenständiger Schutz; ein modaler, ohne Ziel wählbarer Lebensgewinn dagegen
schon. Nicht gecachte Goldfish-Berichte verwenden das explizite Sample- und
Seed-Budget des aufrufenden Matchup-Laufs.

Bei mehrflächigen Karten dürfen Effekte einer durch Transformieren, Craft,
Daybound oder eine besiegte Battle gesperrten Rückseite nicht als beim normalen
Cast sofort verfügbare Produktion, Engine oder Payoff gewertet werden. Modal
castbare Flächen wie Adventures und Rooms bleiben davon getrennt.

Oracle-Effektanalyse bewahrt den Kontext einer Fähigkeit über Folgesätze,
Reminder-Text und modale Aufzählungspunkte. Spätere Saga-Kapitel sind ohne
Read-ahead verzögert; mit Read-ahead darf ein gewähltes späteres Kapitel beim
Eintritt auslösen. Attack-, Payment-, Landfall-, Leave- und andere Trigger sind
keine garantierte Cast-Sofortproduktion. Self-ETB-Erzeugung bleibt sofort.

Als sofortiger Go-Wide-Anthem zählt nur ein beim Cast verfügbarer globaler
Power-Buff oder ein globaler +1/+1-Counter-Effekt. Ziele, Kartennamen,
Kreaturen-Unterklassen, Aktivierungskosten, Spree, Solved- und andere
Freischaltungen zählen nicht. Temporäre Anthems gelten nur im aktuellen Zug
und dürfen im Goldfish nicht über mehrere Züge gestapelt werden.

## 9. Verbindliche Starthand- und Sequenzanalyse

Für jede erzeugte oder als aktuelle Referenz verwendete Deckliste sind genau 100 reproduzierbare Sieben-Karten-Starthände mit dokumentiertem festem Zufallsseed zu analysieren.

Die Bewertung muss archetypen- und planabhängig sein und mindestens prüfen:

- verfügbare und farblich passende Manaquellen,
- spielbare Züge 1, 2 und 3,
- frühe Bedrohung oder Enabler,
- Engine-, Payoff- und Finisher-Zugang,
- notwendige frühe Interaktion,
- tote oder widersprüchliche Karten,
- ob der deklarierte Hauptplan realistisch anlaufen kann.

Jede Hand wird als `planfähig`, `marginal` oder `nicht planfähig` klassifiziert. Keepability, Early Play und Planfähigkeit werden getrennt ausgewiesen.

Aggregierte Daten dürfen niemals nachträglich als simulierte Einzelhände dargestellt werden. Wenn eine echte Simulation nicht möglich ist, muss der exakte technische Stopgrund dokumentiert werden.

Maschinenlesbare Rohdaten oder eine kompakte Zusammenfassung werden unter `artifacts/global` oder `docs/reports` gespeichert.

## 10. Archetypabhängige Mindestlogik

- **Burn:** frühe Pressure- oder Burn-Dichte und realistische Schadenssequenz.
- **Tokens – Go Wide:** frühe Maker plus realistisches Payoff- oder Scaling-Fenster.
- **Tokens – Value Tokens:** frühe Token-Erzeugung plus wiederholbare Value-Engine.
- **Tokens – Aristocrats:** Material plus Outlet plus Death-/Drain-/Sacrifice-Payoff.
- **Artifacts:** früher Enabler plus Synergie-Piece, Engine oder Payoff.
- **Control:** relevante frühe Interaktion gegen den konkreten gegnerischen Plan, anschließende Stabilisierung, Kartenvorteil und belastbare Wincondition.
- **Mill:** frühe Mill-Engine oder wiederholbare Mill-Quelle plus Schutz, Interaktion oder Tempo.

Control-Antworten dürfen nicht nur generisch als Interaktion gezählt werden. Sie müssen gegen den konkreten gegnerischen Plan wirksam sein. Ein Control-Deck muss eine Partie nicht nur verzögern, sondern nach Stabilisierung auch beenden können.

## 11. Known Good Baseline Policy

Eine **Known Good Baseline (KGB)** ist ein ausdrücklich dokumentierter Commit, der als letzter belastbarer Vergleichsstand gilt.

Ein Commit darf nur als neue KGB akzeptiert werden, wenn:

- vollständige Testsuite erfolgreich,
- Fast-Validierung erfolgreich,
- erforderliche Referenzvergleiche erfolgreich,
- CI erfolgreich,
- keine unbegründeten Regressionen gegenüber der bisherigen KGB,
- Qualitätsvergleich für Burn, Tokens, Artifacts, Control und Mill dokumentiert,
- Reflexion und Confidence dokumentiert.

Grüne CI allein reicht nicht aus.

Jeder Zyklus beginnt mit der Ermittlung der letzten KGB und endet mit einer expliziten Entscheidung:

- neue KGB,
- keine neue KGB,
- Regression festgestellt.

Ist der neue Stand insgesamt nur gleichwertig, darf er nur dann KGB werden, wenn er Messbarkeit, Reproduzierbarkeit, Wartbarkeit oder Sicherheit nachweislich verbessert und keine spielerische Verschlechterung verursacht.

## 12. Baseline-Vergleich und Regression

Jeder neue Zyklus vergleicht mindestens:

- Commit-SHA der KGB,
- Tests und Laufzeit,
- Referenzarchetypen,
- Starthandmetriken,
- Matchups und BO3,
- Strategy Commitment,
- Engine Density,
- Finish Density, sofern vorhanden,
- bekannte Risiken.

Unbegründete signifikante Verschlechterungen verhindern die Ernennung zur neuen KGB und müssen im Logbook dokumentiert werden. Es darf nicht auf einer nachweislich schlechteren Version einfach weiterentwickelt werden, solange kein klarer experimenteller Grund und kein Rückkehrpfad dokumentiert ist.

## 13. Git-Tag-Policy

Nicht jede KGB benötigt einen Git-Tag. Ein Tag wird geprüft, wenn ein größerer Meilenstein erreicht ist, beispielsweise:

- neue allgemeine Qualitätsmetrik,
- neuer Referenzarchetyp vollständig integriert,
- Baseline- oder Reporting-System grundlegend verbessert,
- bedeutende stabile Version vor einem neuen Entwicklungsabschnitt.

Tags folgen dem Muster `calibration-vX.Y`. Tag, Anlass und referenzierter Commit werden im Logbook dokumentiert.

## 14. Rollback-Policy

Wird eine KGB später als fehlerhaft erkannt, wird bewusst auf die letzte belastbare KGB zurückgegangen oder von ihr weiterentwickelt.

Ein Rollback muss dokumentieren:

- fehlerhafte KGB,
- Ziel-KGB,
- konkrete Ursache,
- betroffene Metriken oder Funktionen,
- Tests und CI des Rückkehrstands,
- nächsten Schritt.

Ein Rollback ist eine bewusste Qualitätsentscheidung und kein Entwicklungsfehler.

## 15. Session-Recovery

Nach Zeitlimit, Verbindungsabbruch oder externem Abbruch beginnt der nächste Lauf mit:

1. vollständigem Lesen der verbindlichen Repository-Dokumente,
2. Prüfung des aktuellen Branch- und PR-Heads,
3. Ermittlung der letzten KGB,
4. Prüfung, ob der zuletzt begonnene Zyklus vollständig abgeschlossen wurde,
5. Fortsetzung beim im Logbook und in der Roadmap dokumentierten nächsten ausführbaren Schritt.

Ein teilweise bearbeiteter Zyklus darf nicht stillschweigend wiederholt, übersprungen oder als abgeschlossen dargestellt werden.

## 16. Reflexionspflicht

Jeder Zyklus endet mit einer kritischen Reflexion:

- Welche Annahme könnte falsch sein?
- Welche alternative Erklärung passt ebenfalls zu den Messwerten?
- Wurde auf Tests, Fixtures oder Simulationen überangepasst?
- Welche Mess- oder Datenlücke bleibt?
- Bedeutet grüne CI tatsächlich bessere spielerische Qualität?
- Welche unbeabsichtigte Regression könnte unentdeckt sein?
- Welche Klassifikationsregel könnte zu streng oder zu locker sein?

Danach wird Confidence neu bewertet. Mindestens zwei Folgeschritte werden nach erwartetem globalem Qualitätsgewinn, Evidenz, Aufwand und Risiko verglichen. Genau ein nächster ausführbarer Schritt wird in Logbook und Roadmap festgeschrieben.

## 17. Dokumentationspflicht

Nach jedem produktiven Zyklus sind mindestens zu aktualisieren:

- `DEVELOPMENT_LOGBOOK.md` bei neuen Erkenntnissen und KGB-Entscheidungen,
- `ROADMAP.md` bei nächstem Schritt und geänderter Priorität,
- `DECISIONS.md` bei dauerhaften Architektur- oder Prozessentscheidungen,
- `KNOWN_ISSUES.md` bei neu entdeckten Problemen,
- `CHANGELOG_SPECIFICATION.md` bei Änderungen dieser Spezifikation.

Keine stillen Regeländerungen.

## 18. Abschluss eines mehrstündigen Laufs

Der Abschlussbericht enthält:

1. alle Commits und Workflow-Run-IDs,
2. Status, Jobs, Logs und Artefakte des letzten relevanten Runs,
3. Qualitätsentwicklung je Referenzarchetyp,
4. KGB-Ausgangsstand und KGB-Endentscheidung,
5. bestätigte und widerlegte Hypothesen,
6. Regressionen, Risiken und Datenlücken,
7. aktualisiertes Logbook und aktualisierte Roadmap,
8. genau einen priorisierten nächsten ausführbaren Schritt.

Ergebnisse, Schlussfolgerungen und offene Hypothesen sind klar zu trennen. Es dürfen keine Ergebnisse, Workflow-Runs, Artefakte oder simulierten Hände erfunden werden.
