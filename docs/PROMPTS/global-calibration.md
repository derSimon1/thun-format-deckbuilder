# Global Calibration Prompt

**Version:** 1.3  
**Verbindliche Grundlage:** `docs/SPECIFICATION.md`

## Verwendung

Der externe Auftrag nennt nur Repository, Branch/PR und die verfügbare Laufzeit `X` in Stunden. Diese Datei enthält die vollständige Arbeitsanweisung.

Beispiel:

> Arbeite 3 Stunden im Repository `derSimon1/thun-format-deckbuilder` auf Branch `codex/global-deckbuilder-calibration` und PR #14 gemäß `docs/PROMPTS/global-calibration.md`. PR #13 bleibt unangetastet.

## Auftrag

Arbeite für die im externen Auftrag genannte Laufzeit im Repository `derSimon1/thun-format-deckbuilder` auf Branch `codex/global-deckbuilder-calibration` und PR #14. PR #13 bleibt unangetastet.

Führe innerhalb der verfügbaren Laufzeit so viele **vollständige produktive Kalibrierungszyklen** wie sinnvoll möglich durch. Ein Zyklus ist nur abgeschlossen, wenn Hypothese, Änderung oder belegter No-Change-Befund, Validierung, Reflexion und Dokumentation vollständig vorliegen.

Starte keinen neuen Zyklus, wenn er innerhalb der verbleibenden Laufzeit voraussichtlich nicht mehr sauber validiert, dokumentiert und abgeschlossen werden kann. Nutze die Restzeit stattdessen für Abschlussvalidierung, CI-Auswertung, Artefaktprüfung, Logbook, Roadmap und Abschlussbericht.

Es werden **keine separaten 15-Minuten-Aufgaben** benötigt. Arbeite im selben Lauf kontinuierlich weiter. GitHub Actions ist Validator und kein Entwicklungsagent.

## 1. Verbindliche Repository-Dokumente

Lies zu Beginn vollständig die aktuelle Version von:

- `docs/SPECIFICATION.md`
- `docs/PROMPTS/global-calibration.md`
- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/META.md`

Diese Repository-Dokumente sind verbindlich und haben Vorrang vor älteren Aufgabenformulierungen und vor allgemeinen Annahmen.

Vor jedem weiteren Zyklus lies mindestens den zuletzt geänderten Teil von Logbook und Roadmap erneut und beginne mit dem dort priorisierten nächsten ausführbaren Schritt, sofern keine neue belegte Evidenz eine andere Priorität rechtfertigt.

## 2. Start- und Zyklusprüfung

Prüfe zu Beginn des Laufs und unmittelbar vor jeder Änderung:

- aktuellen Branch- und PR-Head
- Mergeability
- aktive CI-Runs
- letzten erfolgreichen Workflow
- enthaltene Jobs
- relevante Logs
- verfügbare Artefakte
- Änderungen seit dem letzten dokumentierten Zyklus

Halte den Ausgangs-Head jedes Zyklus fest.

Stoppe den betroffenen Änderungsschritt ohne Commit, wenn aktive CI, ein veränderter Head, Parallelität oder eine unklare Ursache eine sichere Änderung verhindert. Dokumentiere dann den exakten Stopgrund, die Erkenntnis, Confidence und den nächsten ausführbaren Schritt. Ein solcher Befund darf den gesamten mehrstündigen Lauf nicht unnötig beenden, sofern ein anderer Roadmap-Punkt sicher bearbeitet werden kann.

## 3. Priorisierung

Wähle pro Zyklus genau eine testbare Hypothese mit hohem erwartetem globalem Qualitätsgewinn.

Aktuelle Priorität:

1. belastbare Token-Subarchetyp-Erkennung für Go Wide, Value Tokens und Aristocrats
2. Control als allgemeiner Referenzarchetyp für das Verhindern gegnerischer Pläne
3. Burn als Referenz für frühen Druck und Reach
4. Artifacts als Referenz für Synergie- und Engine-Erkennung
5. Mill als alternative Wincondition
6. Strategy Commitment
7. Engine Density
8. Finish Density
9. Baseline und Meta-Benchmark

Die fünf verbindlichen Referenzarchetypen sind:

- Burn
- Tokens
- Artifacts
- Control
- Mill

Shrines ist kein Pflicht- oder Referenzarchetyp mehr. Es darf höchstens optional als spezieller Regressionstest für mehrfarbige Engine-Decks verwendet werden, wenn konkrete Evidenz dies begründet.

Wiederhole nicht lediglich Statusprüfungen. Nach zwei dokumentierten No-Change-Zyklen derselben Ursache musst du zum nächsten Roadmap-Punkt wechseln.

Setze pro Zyklus höchstens drei eng gekoppelte Code-, Test- oder Berichtsänderungen derselben Ursache um. Keine Dummy-Commits, keine unbegründeten Grenzwertverschiebungen und keine Änderungen an PR #13.

## 4. Aktuell stärkste Hypothese

Implementiere beziehungsweise vervollständige einen reproduzierbaren `OpeningHandPlanReport`, der für jedes erzeugte oder als aktuelle Referenz verwendete Deck genau 100 Sieben-Karten-Starthände mit dokumentiertem festem Zufallsseed erzeugt und maschinenlesbar speichert.

Die Analyse darf nicht nur Landzahl oder irgendeinen frühen spielbaren Spell bewerten. Sie muss prüfen, ob der deklarierte Hauptplan realistisch anlaufen kann.

Für jede Hand sind mindestens zu erfassen:

- gezogene sieben Karten
- verfügbare und farblich passende Manaquellen
- mögliche Spielzüge in Zug 1, 2 und 3
- frühe Bedrohung oder Enabler
- Engine-, Payoff- und Finisher-Zugang
- notwendige frühe Interaktion
- tote oder widersprüchliche Karten
- deklarierter Hauptplan
- Klassifikation `planfähig`, `marginal` oder `nicht planfähig`
- konkrete Klassifikations- und Ausfallgründe

### Archetypabhängige Kriterien

**Burn:** frühe Pressure- oder Burn-Dichte, realistische Schadenssequenz, passende Farben und keine Hand aus ausschließlich teuren oder reaktiven Karten.

**Tokens – Go Wide:** frühe Maker oder Boardentwicklung plus realistisches Fenster für Anthem, Pump, Evasion oder einen anderen Go-Wide-Payoff.

**Tokens – Value Tokens:** frühe Token-Erzeugung plus wiederholbare Value-Engine oder belastbarer Ressourcen- und Kartenvorteil.

**Tokens – Aristocrats:** Opfermaterial oder wiederholbare Token-Erzeugung plus Sacrifice Outlet oder gleichwertiger Enabler plus Drain-, Death- oder Sacrifice-Payoff. Unterscheide Material, Outlet und Payoff einzeln sowie alle unvollständigen Kombinationen.

**Artifacts:** früher Artifact-Enabler plus nutzbares Synergy-Piece, Engine oder Payoff.

**Control:** relevante frühe Interaktion gegen den konkreten gegnerischen Plan, anschließende Stabilisierung, Kartenvorteil und belastbare Wincondition. Eine hohe Zahl reaktiver Karten allein genügt nicht. Prüfe Removal, Countermagic, Sweeper-Zugang, situativ tote Antworten, Tap-out-/Draw-go-Widersprüche und ob die Partie tatsächlich beendet werden kann.

**Mill:** frühe Mill-Engine oder wiederholbare Mill-Quelle plus Schutz, Interaktion oder Tempo und eine realistische Mill-Clock.

## 5. Reproduzierbarkeit und Rohdaten

Der Seed muss:

- im Bericht stehen
- in den maschinenlesbaren Rohdaten enthalten sein
- bei gleichem Deck und Code dieselben 100 Hände erzeugen
- durch automatisierte Tests reproduzierbar geprüft werden

Speichere vollständige Rohdaten als JSON oder JSONL unter `artifacts/global` oder `docs/reports` und ergänze eine kompakte Markdown-Zusammenfassung.

Die Rohdaten enthalten mindestens Deck-ID, Decklisten-Hash, Seed, Simulationsversion, Handnummer, Karten, Sequenz bis Zug 3, Klassifikation, Gründe und Ausfallgründe.

Erfinde keine Einzelhände aus aggregierten Workflow-Daten. Falls eine echte Simulation nicht möglich ist, dokumentiere den exakten technischen Stopgrund und behaupte nicht, die 100-Hand-Prüfung durchgeführt zu haben.

## 6. Pflichtmetriken

Berichte je Deck mindestens:

- Keepability-Rate
- planfähige, marginale und nicht-planfähige Rate
- frühe-Play-Rate bis Zug 2 und 3
- Mana- und Farbfehlerquote
- fehlende Enabler-, Engine-, Payoff- und gegebenenfalls Finisher-Quote
- Quote widersprüchlicher oder toter Karten
- drei häufigste Problemtypen

Für Control zusätzlich:

- relevante Interaktionsrate bis Zug 2
- Abdeckung gegen Kreaturen- und Nichtkreaturen-Pläne
- Stabilisierungschance bis Zug 4 oder 5
- Kartenvorteil-Zugang nach früher Interaktion
- Wincondition-Zugang nach Stabilisierung
- Quote situativ toter Antworten je Matchup

Keepability, Early Play und Planfähigkeit müssen getrennte Metriken bleiben. Eine allgemeine Early-Play-Rate oder bloße Anzahl von Antworten ist kein Beweis für einen funktionierenden Hauptplan.

## 7. Tests und Validierung je Zyklus

Ergänze fachlich eindeutige Tests für die jeweilige Ursache. Für den Opening-Hand-Report mindestens:

- identischer Seed erzeugt identische Ergebnisse
- anderer Seed verändert die Stichprobe
- exakt 100 Hände pro Deck
- klar planfähige und klar nicht-planfähige Fixtures
- Go Wide, Value Tokens und Aristocrats
- Control mit relevanter sowie matchup-toter Interaktion
- Trennung von Early Play, Keepability und Planfähigkeit
- vollständige maschinenlesbare Ausgabe

Vor jedem Commit:

1. vollständige Testsuite ausführen
2. Fast-Validierung ausführen
3. Burn, Tokens, Artifacts, Control und Mill vergleichen
4. drei Token-Matchups prüfen
5. Control gegen Aggro, Tokens und einen Nichtkreaturen- oder Engine-Plan prüfen
6. BO3-Berichte prüfen
7. Laufzeit unter zehn Minuten bestätigen
8. unbegründete Regressionen ausschließen
9. Branch-Head, PR-Head, Mergeability und aktive CI erneut prüfen

## 8. Commit- und CI-Regel

Bei erfolgreicher Validierung erstelle pro abgeschlossenem Zyklus genau einen sinnvollen Commit. Aktualisiere `docs/DEVELOPMENT_LOGBOOK.md` und `docs/ROADMAP.md` im selben Commit.

Nach jedem Push:

- verifiziere innerhalb von zehn Minuten die neue Workflow-Run-ID
- prüfe Commit-SHA, Status und Conclusion
- prüfe alle Jobs, Schritte und Logs
- prüfe erzeugte Artefakte und deren Inhalt

Während ein Workflow läuft, darfst du nur an einem nachweislich unabhängigen nächsten Schritt arbeiten. Besteht Abhängigkeit zum laufenden Ergebnis, warte nicht passiv, sondern nutze die Zeit für Artefaktanalyse, Dokumentation, Testdesign oder einen unabhängigen Roadmap-Punkt. Erzeuge keinen Dummy-Commit zum Triggern.

Grüne CI ist kein automatischer Beweis für bessere spielerische Qualität.

## 9. Reflexion nach jedem Zyklus

Stelle jedes Ergebnis ausdrücklich in Frage:

- Welche zentrale Annahme könnte falsch sein?
- Welche alternative Erklärung passt ebenfalls zu den Messwerten?
- Wurde auf Fixtures, Tests oder Simulationen überangepasst?
- Welche Mess- oder Datenlücke bleibt?
- Bedeutet grüne CI tatsächlich bessere spielerische Qualität?
- Welche unbeabsichtigte Regression könnte unentdeckt sein?
- Sind Klassifikationsregeln zu streng oder zu locker?
- Sind Referenzdecks echte Builder-Ausgaben oder kuratierte Beispiele?
- Werden Kartentexte, Rollen und Synergien zuverlässig erkannt?
- Werden Control-Antworten gegen den konkreten Plan bewertet?
- Wird eine kontrollierte Partie beendet oder nur verzögert?

Bewerte die Erkenntnis danach neu mit expliziter Confidence.

Leite mindestens zwei mögliche Folgeschritte ab und bewerte sie nach erwartetem globalem Qualitätsgewinn, Evidenz, Aufwand und Risiko. Wähle genau einen logisch stärksten nächsten Schritt und schreibe ihn konkret und ausführbar in Logbook und Roadmap.

Der nächste Zyklus beginnt mit diesem Schritt, sofern keine neue belegte Evidenz eine andere Priorität rechtfertigt.

## 10. No-Change-Regel

Falls kein sinnvoller Commit möglich ist, dokumentiere:

- geprüfte Hypothese
- verwendete Daten und gegebenenfalls Seed
- exakten Stopgrund
- gewonnene Erkenntnis
- Confidence
- mindestens zwei Folgeschritte
- genau einen priorisierten nächsten ausführbaren Schritt

Nach zwei aufeinanderfolgenden No-Change-Zyklen derselben Ursache wechsle zum nächsten priorisierten Roadmap-Punkt.

## 11. Abschluss des mehrstündigen Laufs

Beende den Lauf mit:

- vollständiger Testsuite und Full-Validierung, sofern innerhalb der Laufzeit sauber möglich
- Liste aller Commits und Workflow-Run-IDs
- Status, Jobs, Logs und Artefakte des letzten relevanten Runs
- Qualitätsentwicklung je Referenzarchetyp
- bestätigten und widerlegten Hypothesen
- Regressionen, Risiken und Datenlücken
- aktualisiertem Logbook und aktualisierter Roadmap
- genau einem priorisierten nächsten ausführbaren Schritt

Beginne keinen unvollständigen letzten Zyklus nur, um die Laufzeit auszuschöpfen.

Erfinde keine Ergebnisse, Workflow-Runs, Artefakte oder simulierten Hände.
