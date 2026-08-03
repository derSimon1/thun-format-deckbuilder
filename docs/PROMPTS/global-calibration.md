# Global Calibration Prompt

**Version:** 2.0  
**Verbindliche Grundlage:** `docs/SPECIFICATION.md`

## Verwendung

Der externe Auftrag nennt nur:

- Repository,
- Branch und Pull Request,
- verfügbare Laufzeit `X` in Stunden.

Diese Datei enthält die vollständige Arbeitsanweisung.

Beispiel:

> Arbeite 3 Stunden im Repository `derSimon1/thun-format-deckbuilder` auf Branch `codex/global-deckbuilder-calibration` und PR #14 gemäß `docs/PROMPTS/global-calibration.md`. PR #13 bleibt unangetastet.

## 1. Verbindlicher Start

Lies zu Beginn vollständig:

- `docs/SPECIFICATION.md`
- `docs/PROMPTS/global-calibration.md`
- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/META.md`

Diese Repository-Dokumente sind verbindlich und haben Vorrang vor älteren Aufgabenformulierungen und allgemeinen Annahmen.

Prüfe anschließend:

- aktuellen Branch- und PR-Head,
- Mergeability,
- aktive CI-Runs,
- letzten erfolgreichen Workflow,
- Jobs, Logs und Artefakte,
- letzte Known Good Baseline,
- zuletzt dokumentierten nächsten ausführbaren Schritt,
- ob der vorherige Zyklus vollständig abgeschlossen wurde.

PR #13 bleibt unangetastet.

## 2. Mehrstundenbetrieb

Arbeite für die im externen Auftrag genannte Laufzeit kontinuierlich im selben Lauf. Es werden keine separaten 15-Minuten-Aufgaben benötigt.

Führe so viele vollständige produktive Kalibrierungszyklen wie sinnvoll möglich durch. Ein Zyklus ist nur abgeschlossen, wenn Hypothese, Änderung oder belegter No-Change-Befund, Validierung, Baseline-Vergleich, Reflexion und Dokumentation vollständig vorliegen.

Starte keinen neuen Zyklus, wenn er innerhalb der verbleibenden Laufzeit voraussichtlich nicht mehr vollständig implementiert, getestet, validiert, dokumentiert und abgeschlossen werden kann. Nutze die Restzeit für Abschlussvalidierung, CI-Auswertung, Artefaktprüfung, Logbook, Roadmap und Abschlussbericht.

GitHub Actions ist Validator und kein Entwicklungsagent.

## 3. Priorisierung

Beginne mit dem in Logbook und Roadmap festgelegten nächsten ausführbaren Schritt, sofern keine neue belegte Evidenz eine andere Priorität rechtfertigt.

Aktuelle globale Priorität:

1. belastbare Token-Subarchetyp-Erkennung für Go Wide, Value Tokens und Aristocrats,
2. planabhängige Starthand- und Sequenzbewertung,
3. Control als allgemeiner Referenzarchetyp für das Verhindern gegnerischer Pläne,
4. Strategy Commitment,
5. Engine Density,
6. Finish Density,
7. belastbare Baseline und Meta-Benchmark.

Die fünf verbindlichen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Shrines ist kein Pflicht- oder Referenzarchetyp.

Wähle pro Zyklus genau eine testbare Hypothese mit hohem erwartetem globalem Qualitätsgewinn. Setze höchstens drei eng gekoppelte Code-, Test- oder Berichtsänderungen derselben Ursache um.

Keine Dummy-Commits, keine Grenzwertverschiebung nur zum Bestehen und keine unbelegten archetypspezifischen Sonderfälle.

## 4. Verbindliche 100-Starthände-Regel

Für jede erzeugte oder als aktuelle Referenz verwendete Deckliste simuliere genau 100 reproduzierbare Sieben-Karten-Starthände mit dokumentiertem festem Zufallsseed.

Bewerte jede Hand archetypen- und planabhängig. Prüfe mindestens:

- verfügbare und farblich passende Manaquellen,
- spielbare Züge 1, 2 und 3,
- frühe Bedrohung oder Enabler,
- Engine-, Payoff- und Finisher-Zugang,
- notwendige Interaktion,
- tote oder widersprüchliche Karten,
- ob der deklarierte Hauptplan realistisch anlaufen kann.

Klassifiziere jede Hand als `planfähig`, `marginal` oder `nicht planfähig`.

Berichte je Deck mindestens:

- Keepability-Rate,
- planfähige, marginale und nicht-planfähige Rate,
- frühe-Play-Rate bis Zug 2 und 3,
- Mana- und Farbfehlerquote,
- fehlende Enabler-, Engine-, Payoff- und gegebenenfalls Finisher-Quote,
- Quote toter oder widersprüchlicher Karten,
- drei häufigste Problemtypen.

Keepability, Early Play und Planfähigkeit bleiben getrennte Metriken.

Speichere Rohdaten oder eine kompakte maschinenlesbare Zusammenfassung unter `artifacts/global` oder `docs/reports`. Erfinde keine Einzelhände aus aggregierten Daten.

## 5. Archetypabhängige Kriterien

- **Burn:** frühe Pressure- oder Burn-Dichte und realistische Schadenssequenz.
- **Tokens – Go Wide:** frühe Maker plus passendes Scaling- oder Payoff-Fenster.
- **Tokens – Value Tokens:** frühe Token-Erzeugung plus wiederholbare Value-Engine.
- **Tokens – Aristocrats:** Material plus Outlet plus Death-/Drain-/Sacrifice-Payoff.
- **Artifacts:** früher Enabler plus Synergie-Piece, Engine oder Payoff.
- **Control:** relevante frühe Interaktion gegen den konkreten gegnerischen Plan, Stabilisierung, Kartenvorteil und belastbare Wincondition. Situativ tote Antworten zählen nicht als echte Abdeckung.
- **Mill:** frühe Mill-Engine oder wiederholbare Mill-Quelle plus Schutz, Interaktion oder Tempo.

## 6. Validierung vor Commit

Vor jedem Commit:

1. vollständige Testsuite ausführen,
2. Fast-Validierung ausführen,
3. Burn, Tokens, Artifacts, Control und Mill vergleichen,
4. Go Wide, Value Tokens und Aristocrats getrennt prüfen,
5. drei relevante Token-Matchups prüfen,
6. Control gegen Aggro, Tokens und einen Nichtkreaturen- oder Engine-Plan prüfen,
7. BO3-Berichte prüfen,
8. Laufzeit unter zehn Minuten bestätigen,
9. gegen die letzte Known Good Baseline vergleichen,
10. unbegründete Regressionen ausschließen,
11. Branch-Head, PR-Head, Mergeability und aktive CI erneut prüfen.

Bei erfolgreicher Validierung erstelle pro Zyklus genau einen sinnvollen Commit und aktualisiere `docs/DEVELOPMENT_LOGBOOK.md` sowie `docs/ROADMAP.md` im selben Commit.

## 7. Known Good Baseline

Jeder Zyklus beginnt mit der letzten dokumentierten Known Good Baseline und endet mit genau einer Entscheidung:

- neue KGB,
- keine neue KGB,
- Regression festgestellt.

Eine neue KGB ist nur zulässig, wenn vollständige Tests, Fast-Validierung, Referenzvergleiche und CI erfolgreich sind, keine unbegründeten Regressionen vorliegen und der Qualitätsvergleich dokumentiert ist.

Grüne CI allein genügt nicht.

Bei zwei aufeinanderfolgenden unbegründeten Regressionen derselben Hypothese pausiere diese Hypothese und wechsle zum nächsten priorisierten Roadmap-Punkt.

Prüfe bei größeren stabilen Meilensteinen, ob ein Git-Tag nach dem Muster `calibration-vX.Y` sinnvoll ist. Nicht jede KGB benötigt einen Tag.

## 8. Commit, Workflow und Artefakte

Nach jedem Push:

- verifiziere innerhalb von zehn Minuten die neue Workflow-Run-ID,
- prüfe Commit-SHA, Status und Conclusion,
- prüfe alle Jobs, Schritte und Logs,
- prüfe erzeugte Artefakte und deren Inhalt.

Während ein Workflow läuft, darf nur an einem nachweislich unabhängigen Schritt gearbeitet werden. Erzeuge keinen Dummy-Commit zum Triggern.

## 9. No-Change und Rollback

Falls kein sinnvoller Commit möglich ist, dokumentiere:

- geprüfte Hypothese,
- verwendete Daten und gegebenenfalls Seed,
- exakten Stopgrund,
- gewonnene Erkenntnis,
- Confidence,
- mindestens zwei Folgeschritte,
- genau einen priorisierten nächsten ausführbaren Schritt.

Nach zwei No-Change-Zyklen derselben Ursache wechsle zum nächsten Roadmap-Punkt.

Wird eine KGB später als fehlerhaft erkannt, dokumentiere einen bewussten Rollback auf die letzte belastbare KGB mit Ursache, betroffenen Metriken, Tests, CI und nächstem Schritt.

## 10. Reflexion nach jedem Zyklus

Stelle das Ergebnis ausdrücklich in Frage:

- Welche Annahme könnte falsch sein?
- Welche alternative Erklärung passt ebenfalls zu den Messwerten?
- Wurde auf Tests, Fixtures oder Simulationen überangepasst?
- Welche Mess- oder Datenlücke bleibt?
- Bedeutet grüne CI tatsächlich bessere spielerische Qualität?
- Welche unbeabsichtigte Regression könnte unentdeckt sein?
- Sind Klassifikationsregeln zu streng oder zu locker?
- Sind Referenzdecks echte Builder-Ausgaben oder kuratierte Beispiele?
- Werden Kartentexte, Rollen und Synergien zuverlässig erkannt?
- Wird eine kontrollierte Partie beendet oder nur verzögert?

Bewerte Confidence danach neu.

Leite mindestens zwei mögliche Folgeschritte ab und bewerte sie nach erwartetem globalem Qualitätsgewinn, Evidenz, Aufwand und Risiko. Wähle genau einen logisch stärksten nächsten Schritt und schreibe ihn konkret und ausführbar in Logbook und Roadmap.

## 11. Session-Recovery

Nach Zeitlimit, Verbindungsabbruch oder externem Abbruch:

1. lies alle verbindlichen Repository-Dokumente vollständig,
2. prüfe Branch- und PR-Head,
3. ermittle die letzte KGB,
4. prüfe, ob der letzte Zyklus vollständig abgeschlossen wurde,
5. setze beim dokumentierten nächsten ausführbaren Schritt fort.

Ein teilweise bearbeiteter Zyklus darf nicht stillschweigend wiederholt, übersprungen oder als abgeschlossen dargestellt werden.

## 12. Abschluss des Laufs

Beende den Lauf mit:

- Liste aller Commits und Workflow-Run-IDs,
- Status, Jobs, Logs und Artefakten des letzten relevanten Runs,
- Qualitätsentwicklung je Referenzarchetyp,
- KGB-Ausgangsstand und KGB-Endentscheidung,
- bestätigten und widerlegten Hypothesen,
- Regressionen, Risiken und Datenlücken,
- aktualisiertem Logbook und aktualisierter Roadmap,
- genau einem priorisierten nächsten ausführbaren Schritt.

Erfinde keine Ergebnisse, Workflow-Runs, Artefakte oder simulierten Hände.
