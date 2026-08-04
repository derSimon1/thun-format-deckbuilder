# Global Calibration Prompt

**Prompt-Version:** 2.1  
**Verbindliche Grundlage:** `docs/SPECIFICATION.md` Version 2.0

## Verwendung

Der externe Auftrag nennt nur Repository, Branch/Pull Request und verfügbare Laufzeit `X`.

Beispiel:

> Arbeite 3 Stunden im Repository `derSimon1/thun-format-deckbuilder` auf Branch `codex/global-deckbuilder-calibration` und PR #14 gemäß `docs/PROMPTS/global-calibration.md`. PR #13 bleibt unangetastet.

## 1. Einmaliger Session-Start

Lies vollständig:

- `docs/SPECIFICATION.md`
- `docs/PROMPTS/global-calibration.md`
- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/META.md`

Erstelle anschließend einen kompakten Session-Snapshot mit:

- Branch- und PR-Head,
- Mergeability und aktiver CI,
- letzter abgeschlossener Workflow-Run-ID,
- letztem relevanten Artefakt,
- KGB- beziehungsweise Vergleichsstatus,
- genau einem primären nächsten Schritt,
- genau einem Fallback-Schritt,
- bekannten Stopbedingungen.

Unveränderte Repository-Dokumente werden innerhalb derselben Session nicht vor jedem Zyklus erneut vollständig gelesen. Vor jedem Commit werden nur Head, PR, Mergeability und aktive CI erneut geprüft.

PR #13 bleibt unangetastet.

## 2. Zeitbudget für einen Drei-Stunden-Lauf

Für andere Laufzeiten werden die Anteile entsprechend skaliert.

- maximal 20 Minuten: Recovery, Session-Snapshot und letzte Artefaktauswertung
- bis zu 120 Minuten: produktive Entwicklungszyklen einschließlich eines optionalen Fallback-Zyklus von höchstens 20 Minuten
- mindestens 30 Minuten: letzter Workflow, Artefaktprüfung, Dokumentation und Abschlussbericht
- 10 Minuten bleiben als ungeplanter Puffer für Connector-, Runner- oder Merge-Verzögerungen

Ein neuer Zyklus darf nur begonnen werden, wenn Restzeit mindestens aus geschätzter Implementierungszeit plus CI-/Artefaktpuffer plus 30 Minuten Abschlussreserve besteht.

CI-Wartezeit zählt nicht als produktiver Zyklus. Während CI läuft, darf nur ein nachweislich unabhängiger Analyse- oder Dokumentationsschritt vorbereitet werden.

## 3. Artifact-first statt Status-first

Zu Beginn und nach jedem Commit:

1. Workflowstatus einmal prüfen.
2. Nach Abschluss Jobs und Logs einmal vollständig lesen.
3. Relevantes Artefakt einmal herunterladen und maschinenlesbar auswerten.
4. Ergebnisse in einer Evidenztabelle mit `vorher`, `nachher`, `Delta`, `Interpretation` und `Confidence` festhalten.

Keine Folge identischer Statusabfragen ohne neue erwartbare Information. Bei normaler Laufzeit wird nicht fortlaufend gepollt; es wird zwischenzeitlich unabhängig gearbeitet oder bis zum erwartbaren Abschluss gewartet.

Grüne CI ist nur ein technisches Gate. Die Artefakte entscheiden über die fachliche Hypothese.

## 4. Zyklusvertrag vor Codeänderung

Jeder Zyklus definiert vor der Implementierung:

- eine konkrete Ursache,
- eine testbare Hypothese,
- höchstens drei eng gekoppelte Änderungen,
- erwartete verbesserte Metriken,
- explizite Invarianten, die unverändert bleiben müssen,
- fachliches Erfolgskriterium,
- Abbruch- oder Rollbackkriterium,
- geschätzte Gesamtzeit inklusive Workflow und Artefaktauswertung.

Keine Grenzwertsenkung nur zum Bestehen, keine Dummy-Commits und keine kartennamenspezifische Sonderregel ohne belegte Notwendigkeit.

## 5. Test- und Commitstrategie

Bei verfügbarem lokalem Checkout:

1. gezielte Regressionstests,
2. vollständige Testsuite,
3. Fast-Validierung,
4. Commit.

In einer Connector-only-Umgebung ohne lokalen Checkout:

1. Syntax- und kontrollierte Regressionstests soweit technisch möglich,
2. atomarer Commit mit Tests und Dokumentation,
3. vollständige Testsuite und Fast-Validierung zwingend in CI,
4. Commit bleibt bis zur Artefaktauswertung vorläufig und darf nicht als KGB gelten.

Pro Zyklus genau ein zusammenhängender Commit. Logbook und Roadmap werden im selben Commit aktualisiert.

## 6. Verbindliche fachliche Gates

Jeder relevante Fast-Lauf prüft:

- Burn, Tokens, Artifacts, Control und Mill,
- Legalität, 60/15, Kopienlimit, Farben und Manabasis,
- genau 100 reproduzierbare Hände je Deck mit dokumentiertem Seed,
- Keepability, Early Play und Planfähigkeit getrennt,
- Benchmark und Rollen-/Strategiedichte,
- priorisierte Matchups und BO3,
- finale Sideboardrollen, Gründe und Karten-in-Pläne,
- Laufzeit unter zehn Minuten,
- unbegründete Regressionen.

Für bekannte Fehler werden maschinenlesbare Invarianten und Diagnoseartefakte bevorzugt. Ein Fehler darf nicht nur über manuelles Lesen eines Berichts abgesichert werden, wenn eine direkte Assertion möglich ist.

## 7. Aktuelles primäres Ziel des nächsten Drei-Stunden-Laufs

### Primär: Mill-Komposition

Run 48 zeigte:

- Benchmark 78, aber 0 erkannte Mill-Quellen,
- nur zwei klare Millkarten im finalen Mainboard,
- 77 % Keepability,
- 0 % planfähige und 100 % marginale Hände,
- 72 % fehlender Enabler-/Payoff-/Finisher-Zugang,
- überwiegend Draw-, Counter- und Removal-Karten statt eines Millplans.

Der nächste Lauf beginnt daher mit:

1. reale Gegner-Mill-Quellen anhand Oracle-Text maschinenlesbar erkennen,
2. verfügbare Kartenpoolkapazität bestimmen,
3. kapazitätsgeprüfte Mindestdichte definieren,
4. sicherstellen, dass Komposition und Optimierer diese Dichte erhalten,
5. Benchmark und Opening-Hand-Analyse auf dieselbe Definition ausrichten,
6. 100 Mill-Hände und Matchups gegen den Ausgangsstand vergleichen.

Erfolg bedeutet nicht nur einen höheren Benchmark. Das finale Deck muss tatsächlich einen realistisch anlaufenden Millplan besitzen.

### Fallback

Falls die Kartenpoolkapazität keine belastbare Mindestdichte erlaubt:

- keine künstliche Schwelle setzen,
- exakte Kapazität und fehlende Kartentypen dokumentieren,
- Oracle-Text-/Rollenweitergabe oder Eligibility als nächste Ursache isolieren,
- einen vollständigen No-Change-Zyklus abschließen.

Sideboard-Tuning wird im nächsten Lauf nicht erneut priorisiert, sofern keine neue externe oder artefaktbasierte Evidenz eine andere Ursache zeigt.

## 8. Pflichtanalyse der 100 Hände

Je Referenzdeck genau 100 Sieben-Karten-Hände mit festem Seed. Jede Hand wird als `planfähig`, `marginal` oder `nicht planfähig` klassifiziert.

Für Mill insbesondere:

- frühe Gegner-Mill-Quelle,
- wiederholbare Engine oder ausreichende Mill-Dichte,
- Schutz, Interaktion oder Tempo,
- Mana- und Farbzugang,
- tote Draw-/Counter-/Removal-Hände ohne Millplan,
- realistischer Sequenzstart bis Zug 3.

Aggregierte Daten dürfen nicht als Einzelhände erfunden werden.

## 9. Prioritätswechsel und Schleifenschutz

Nach zwei fachlich gescheiterten Zyklen derselben Ursache wird die Hypothese pausiert. Ein weiterer Versuch ist nur zulässig, wenn neue Evidenz eine klar andere Root Cause belegt. Diese Evidenz muss vor der Änderung im Logbook stehen.

Keine dritte Variante derselben Heuristik nur mit anderen Wörtern oder Schwellenwerten.

## 10. KGB-Entscheidung

Jeder Zyklus endet mit genau einer Entscheidung:

- neue KGB,
- keine neue KGB,
- Regression festgestellt.

Eine neue KGB erfordert vollständige Tests, Fast-Validierung, erfolgreiche CI, Artefaktprüfung, Vergleich aller fünf Referenzarchetypen, dokumentierte Reflexion und keine unbegründeten Regressionen. `baseline: none` muss vor einer voll qualifizierten v2-KGB durch einen belastbaren Vergleichsmechanismus ersetzt sein.

## 11. Reflexion

Nach jedem Zyklus beantworten:

- Welche Annahme könnte falsch sein?
- Welche alternative Erklärung passt zu den Daten?
- Wurde auf Fixtures oder Simulationen überangepasst?
- Welche Mess- oder Datenlücke bleibt?
- Belegt grüne CI bessere spielerische Qualität?
- Welche unbeabsichtigte Regression könnte fehlen?
- Sind Builderausgabe, Benchmark und Handklassifikation auf dieselbe Plan-Definition ausgerichtet?

Danach Confidence neu bewerten und mindestens zwei Folgeschritte nach Qualitätsgewinn, Evidenz, Aufwand und Risiko vergleichen. Genau einen nächsten ausführbaren Schritt dokumentieren.

## 12. Abschluss

Der Lauf endet mit:

- Commits und Workflow-Run-IDs,
- Status, Jobs, Logs und Artefakten des letzten Runs,
- Evidenztabelle vorher/nachher,
- Qualitätsentwicklung der fünf Referenzarchetypen,
- bestätigten und widerlegten Hypothesen,
- KGB-Entscheidung,
- Risiken und Datenlücken,
- aktualisiertem Logbook und Roadmap,
- genau einem priorisierten nächsten ausführbaren Schritt.

Erfinde keine Ergebnisse, Workflow-Runs, Artefakte oder Hände.
