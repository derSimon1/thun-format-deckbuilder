# Global Calibration Prompt

**Version:** 1.2  
**Verbindliche Grundlage:** `docs/SPECIFICATION.md`

## Verwendung

Der externe Auftrag soll nur Repository, Branch/PR und Laufzeit nennen. Diese Datei enthält die vollständige Arbeitsanweisung.

## Auftrag

Führe genau einen produktiven Kalibrierungszyklus im Repository `derSimon1/thun-format-deckbuilder` auf Branch `codex/global-deckbuilder-calibration` und PR #14 aus. PR #13 bleibt unangetastet.

Lies zu Beginn vollständig die aktuelle Version von:

- `docs/SPECIFICATION.md`
- `docs/PROMPTS/global-calibration.md`
- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/META.md`

Diese Repository-Dokumente sind verbindlich und haben Vorrang vor älteren Aufgabenformulierungen.

## 1. Startprüfung

Prüfe vor jeder Änderung:

- aktuellen PR-Head
- Mergeability
- aktive CI-Runs
- letzten erfolgreichen Workflow
- enthaltene Jobs
- relevante Logs
- verfügbare Artefakte

Halte den Ausgangs-Head fest. Stoppe ohne Commit, wenn aktive CI, ein veränderter Head, Parallelität oder eine unklare Ursache vorliegt. Dokumentiere dann den exakten Stopgrund und den nächsten ausführbaren Schritt.

## 2. Priorisierung

Wähle anhand der aktuellen Roadmap genau eine testbare Hypothese mit hohem erwartetem globalem Qualitätsgewinn.

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

Die fünf verbindlichen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Shrines ist kein Pflicht- oder Referenzarchetyp mehr. Es darf höchstens optional als spezieller Regressionstest für mehrfarbige Engine-Decks verwendet werden, wenn dies durch konkrete Evidenz begründet ist.

Wiederhole nicht lediglich Statusprüfungen. Nach zwei dokumentierten No-Change-Zyklen derselben Ursache musst du zum nächsten Roadmap-Punkt wechseln.

Setze höchstens drei eng gekoppelte Code-, Test- oder Berichtsänderungen um, die dieselbe Ursache behandeln. Keine Dummy-Commits, keine unbegründeten Grenzwertverschiebungen und keine Änderungen an PR #13.

## 3. Verbindliche Hypothese für den nächsten Zyklus

Implementiere einen reproduzierbaren `OpeningHandPlanReport`, der für jedes geprüfte Referenzdeck genau 100 Sieben-Karten-Starthände mit einem dokumentierten festen Zufallsseed erzeugt und die einzelnen Hände beziehungsweise ihre maschinenlesbaren Ergebnisse speichert.

Die Analyse darf nicht nur Landzahl oder irgendeinen frühen spielbaren Spell bewerten. Sie muss prüfen, ob der deklarierte Hauptplan des Decks realistisch anlaufen kann.

Für jede Hand sind mindestens zu erfassen:

- gezogene sieben Karten
- verfügbare Manaquellen
- farblich passende Manaquellen
- mögliche Spielzüge in Zug 1, Zug 2 und Zug 3
- frühe Bedrohung oder Enabler
- Engine-Zugang
- Payoff-Zugang
- Finisher-Zugang
- notwendige frühe Interaktion
- tote Karten
- widersprüchliche Karten oder Kartenpakete
- deklarierter Hauptplan
- Klassifikation `planfähig`, `marginal` oder `nicht planfähig`
- konkrete Klassifikationsgründe
- konkrete Ausfallgründe

Die Bewertung muss archetypen- und planabhängig erfolgen.

### Burn

Eine Hand ist nur dann planfähig, wenn sie ausreichend frühe Pressure- oder Burn-Dichte besitzt und ihre relevanten Karten mit den vorhandenen Farben rechtzeitig wirken kann.

Prüfe insbesondere:

- Zug-1- oder Zug-2-Pressure
- mehrere frühe Schadensquellen
- Verhältnis aus Kreaturen, Burn und Mana
- Hände mit nur teuren oder reaktiven Karten
- Hände, die zwar einen frühen Spell, aber keinen realistischen Schadensplan besitzen

### Tokens – Go Wide

Eine Hand ist nur dann planfähig, wenn sie frühe Token Maker oder gleichwertige Board-Entwicklung besitzt und ein realistisches Fenster für Anthem, Pump, Evasion oder einen anderen Go-Wide-Payoff erreicht.

Prüfe insbesondere:

- früher Token Maker
- zweiter Maker oder Board-Verbreiterung
- passender Go-Wide-Payoff
- Mana für Maker und Payoff
- Hände mit ausschließlich Payoffs ohne Board
- Hände mit ausschließlich kleinen Bodies ohne Scaling

### Tokens – Value Tokens

Eine Hand ist nur dann planfähig, wenn sie frühe Token-Erzeugung mit einer wiederholbaren Value-Engine oder einem belastbaren Ressourcenvorteil verbinden kann.

Prüfe insbesondere:

- früher Token Maker
- wiederholbare Engine
- Kartenfluss, Mana-, Lebens- oder Board-Vorteil
- realistisches Engine-Fenster
- Hände mit vielen Token-Karten, aber ohne Value-Konversion
- Hände mit Engine, aber ohne verwertbares Material

### Tokens – Aristocrats

Eine Hand ist nur dann planfähig, wenn sie in einem realistischen Zeitfenster mehrere notwendige Funktionsgruppen zusammenbringt:

- Opfermaterial oder wiederholbare Token-Erzeugung
- Sacrifice Outlet oder gleichwertiger Opfer-Enabler
- Drain-, Death- oder Sacrifice-Payoff
- ausreichendes Mana und passende Farben

Ein einzelnes formal passendes Element reicht nicht aus.

Unterscheide mindestens:

- nur Material
- nur Outlet
- nur Payoff
- Material plus Outlet ohne Payoff
- Material plus Payoff ohne Outlet
- Outlet plus Payoff ohne Material
- vollständiger oder realistisch vervollständigbarer Aristocrats-Core

### Artifacts

Eine Hand ist nur dann planfähig, wenn sie einen frühen Artifact-Enabler und mindestens ein nutzbares Synergy-Piece oder Payoff besitzt.

Prüfe insbesondere:

- frühes Artefakt oder Artifact-Enabler
- Synergie-Piece
- Payoff oder Engine
- Mana und Farbzugang
- Hände mit generischen Artefakten ohne Synergie
- Hände mit Payoffs ohne ausreichende Artefaktbasis

### Control

Eine Hand ist nur dann planfähig, wenn sie den gegnerischen frühen Plan realistisch verlangsamen oder beantworten, anschließend Ressourcen aufholen und schließlich über eine belastbare Wincondition gewinnen kann.

Control wird nicht anhand einer hohen Anzahl reaktiver Karten allein bewertet. Die Hand muss eine sinnvolle zeitliche Abfolge aus Mana, früher Interaktion, Stabilisierung, Kartenvorteil und späterem Abschluss ermöglichen.

Prüfe insbesondere:

- belastbare und farblich passende Manaquellen
- verfügbare Interaktion in Zug 1 oder 2
- Removal gegen frühe Kreaturen
- Countermagic oder andere Antworten gegen Nichtkreaturen-Pläne
- Schutz vor mehreren Bedrohungen oder Go-Wide-Boards
- Sweeper-Zugang, wenn er im Matchup notwendig ist
- Kartenvorteil oder Selection nach der ersten Interaktion
- realistische Stabilisierung bis Zug 4 oder 5
- Zugang zu einer Wincondition nach der Stabilisierung
- Hände mit nur Countern gegen frühes Creature-Aggro
- Hände mit nur Removal gegen Engines, Combo oder alternative Winconditions
- Hände mit vielen Antworten, aber ohne Kartenfluss
- Hände mit Kartenvorteil und Finishern, aber ohne frühe Antworten
- zu viele teure Karten oder situative Antworten
- widersprüchliche Tap-out- und Draw-go-Pakete

Die Control-Bewertung muss matchupsensitiv sein. Eine Antwort gilt nur dann als relevante Interaktion, wenn sie den erwarteten gegnerischen Plan tatsächlich beeinflussen kann.

### Mill

Eine Hand ist nur dann planfähig, wenn sie eine frühe Mill-Engine oder belastbare wiederholbare Mill-Quelle besitzt und ausreichenden Schutz, Interaktion oder Tempozugang hat.

Prüfe insbesondere:

- frühe Mill-Engine
- wiederholbare Mill-Quelle
- Schutz oder Interaktion
- Mana und Farben
- Hände mit einmaligem Mill ohne Folgedruck
- Hände mit Interaktion, aber ohne realistische Mill-Clock

## 4. Reproduzierbarkeit und Rohdaten

Verwende einen explizit dokumentierten Zufallsseed.

Der Seed muss:

- im Bericht stehen
- in den maschinenlesbaren Rohdaten enthalten sein
- bei gleichem Deck und gleichem Code dieselben 100 Hände erzeugen
- in automatisierten Tests reproduzierbar geprüft werden

Speichere die Ergebnisse unter `artifacts/global` oder `docs/reports`.

Bevorzugtes Format:

- JSON oder JSONL für vollständige Rohdaten
- Markdown für die kompakte menschlich lesbare Zusammenfassung

Die Rohdaten müssen mindestens enthalten:

- Deck-ID oder Archetyp
- Decklisten-Hash oder eindeutige Deckreferenz
- Seed
- Simulationsversion
- Handnummer
- Karten der Starthand
- relevante Sequenz bis Zug 3
- Klassifikation
- Klassifikationsgründe
- Ausfallgründe

Erfinde keine Einzelhände aus bereits aggregierten Workflow-Daten. Falls bestehende Artefakte nur Zusammenfassungen enthalten, muss die Simulation aus der tatsächlichen Deckliste und den verfügbaren Kartenmetadaten neu ausgeführt werden. Ist das nicht möglich, dokumentiere den exakten technischen Stopgrund und behaupte nicht, die 100-Hand-Prüfung durchgeführt zu haben.

## 5. Pflichtmetriken je Deckliste

Berichte mindestens:

- Keepability-Rate
- planfähige Rate
- marginale Rate
- nicht-planfähige Rate
- frühe-Play-Rate bis Zug 2
- frühe-Play-Rate bis Zug 3
- Manafehlerquote
- Farbfehlerquote
- fehlende-Enabler-Quote
- fehlende-Engine-Quote
- fehlende-Payoff-Quote
- fehlende-Finisher-Quote, sofern archetypenrelevant
- Quote widersprüchlicher oder toter Karten
- drei häufigste Problemtypen

Für Control sind zusätzlich mindestens zu berichten:

- frühe relevante Interaktionsrate bis Zug 2
- Abdeckungsrate gegen Kreaturenpläne
- Abdeckungsrate gegen Nichtkreaturen-Pläne
- Stabilisierungschance bis Zug 4 oder 5
- Kartenvorteil-Zugang nach früher Interaktion
- Wincondition-Zugang nach Stabilisierung
- Quote situativ toter Antworten je Matchup

Keepability und Planfähigkeit müssen getrennte Metriken bleiben. Eine Hand kann formal keepbar sein und trotzdem den Hauptplan nicht zuverlässig unterstützen.

Eine allgemeine Early-Play-Rate darf nicht als Beweis für einen funktionierenden Matchplan verwendet werden. Bei Control darf die reine Anzahl verfügbarer Antworten nicht mit tatsächlicher Matchup-Abdeckung gleichgesetzt werden.

Falls sinnvoll, simuliere zusätzlich Ziehschritte bis Zug 4 oder 5. Trenne diese Ergebnisse klar von der reinen Sieben-Karten-Starthandbewertung.

## 6. Tests

Ergänze gezielte Tests für mindestens:

- deterministische Wiederholbarkeit mit identischem Seed
- unterschiedliche Ergebnisse mit anderem Seed
- exakt 100 Hände pro Deck
- korrekte Klassifikation klar planfähiger Hände
- korrekte Klassifikation klar nicht planfähiger Hände
- Tokens Go Wide
- Tokens Value Tokens
- Tokens Aristocrats
- Control mit früher relevanter Interaktion und späterem Kartenvorteil
- Control mit formal vorhandenen, aber im Matchup toten Antworten
- Trennung von Early Play und Planfähigkeit
- Trennung von Keepability und Planfähigkeit
- vollständige maschinenlesbare Ausgabe

Vermeide Tests, die ausschließlich die aktuelle Implementierung spiegeln. Verwende kleine, kontrollierte Deck- oder Hand-Fixtures mit fachlich eindeutigem erwarteten Ergebnis.

## 7. Gesamtvalidierung

Führe nach der Implementierung aus:

- vollständige Testsuite
- Fast-Validierung
- Vergleich von fünf Archetypen
- Vergleich der drei Token-Subarchetypen
- drei relevante Token-Matchups
- Control-Berichte gegen mindestens Aggro, Tokens und einen Nichtkreaturen- oder Engine-Plan
- BO3-Berichte
- Laufzeitprüfung unter zehn Minuten
- Prüfung auf unbegründete Regressionen

Vergleiche mindestens:

- Burn
- Tokens
- Artifacts
- Control
- Mill

Innerhalb Tokens müssen Go Wide, Value Tokens und Aristocrats getrennt ausgewertet werden.

Prüfe, ob sich bestehende Kennzahlen wie Strategy Commitment oder Engine Density scheinbar verbessern, während die planfähige Starthandrate unverändert schlecht bleibt. Dokumentiere solche Widersprüche ausdrücklich.

Prüfe bei Control zusätzlich, ob eine hohe Interaktionsdichte nur durch situative oder im jeweiligen Matchup tote Antworten entsteht. Eine grüne Control-Kennzahl darf nicht allein aus der Anzahl von Removal- oder Counter-Karten abgeleitet werden.

## 8. Vor dem Commit

Prüfe unmittelbar vor dem Commit erneut:

- Branch-Head
- PR-Head
- aktive CI
- zwischenzeitliche Änderungen
- Mergeability
- ob der lokale Stand noch auf dem aktuellen PR-Head basiert

Bei erfolgreicher Validierung:

- erstelle genau einen sinnvollen Commit
- aktualisiere `docs/DEVELOPMENT_LOGBOOK.md`
- aktualisiere `docs/ROADMAP.md`
- nimm beide Dokumentationsänderungen in denselben Commit auf

Ändere `docs/DECISIONS.md`, `docs/KNOWN_ISSUES.md`, `docs/META.md` oder `docs/SPECIFICATION.md` nur gemäß den dort definierten Regeln.

## 9. Nach dem Push

Verifiziere innerhalb von zehn Minuten die neue Workflow-Run-ID der PR.

Prüfe:

- Run-ID
- Commit-SHA
- Status
- Conclusion
- alle Jobs
- fehlgeschlagene oder übersprungene Schritte
- relevante Logs
- erzeugte Artefakte
- Inhalt und Verwendbarkeit der Artefakte

Grüne CI darf nicht automatisch als Beweis für bessere spielerische Qualität gewertet werden.

## 10. Verbindliche Reflexion

Stelle das Ergebnis am Ende ausdrücklich in Frage.

Beantworte mindestens:

- Welche zentrale Annahme könnte falsch sein?
- Welche alternative Erklärung passt ebenfalls zu den Messwerten?
- Wurde auf Fixtures, Tests oder Simulationen überangepasst?
- Welche Mess- oder Datenlücke bleibt?
- Bedeutet grüne CI tatsächlich bessere spielerische Qualität?
- Welche unbeabsichtigte Regression könnte unentdeckt sein?
- Sind die Klassifikationsregeln möglicherweise zu streng oder zu locker?
- Bilden die Referenzdecks echte Deckbuilder-Ausgaben oder nur kuratierte Beispiele ab?
- Werden Kartentexte, Rollen und Synergien zuverlässig genug erkannt?
- Ist eine gute Starthandrate möglicherweise nur Folge einer schwachen oder zu allgemeinen Planbeschreibung?
- Werden Control-Antworten gegen den konkreten gegnerischen Plan bewertet oder nur generisch als Interaktion gezählt?
- Wird eine kontrollierte Partie tatsächlich beendet oder lediglich verzögert?

Bewerte danach die Erkenntnis neu mit einer expliziten Confidence-Angabe.

Leite mindestens zwei mögliche Folgeschritte ab und bewerte sie nach:

- erwartetem globalem Qualitätsgewinn
- Evidenz
- Aufwand
- Risiko

Wähle genau einen logisch stärksten nächsten Schritt für den folgenden Zyklus. Schreibe ihn konkret und ausführbar in:

- `docs/DEVELOPMENT_LOGBOOK.md`
- `docs/ROADMAP.md`

Der nächste Zyklus beginnt mit diesem Schritt, außer neue belegte Evidenz rechtfertigt eine andere Priorität.

## 11. Dauerhafte Verankerung

Sobald CI inaktiv und der Branch-Head stabil ist, verankere dauerhaft in:

- `docs/SPECIFICATION.md`
- `docs/PROMPTS/global-calibration.md`

folgende Regeln:

1. Für jede erzeugte oder als Referenz verwendete Deckliste sind 100 reproduzierbare Sieben-Karten-Starthände mit dokumentiertem Seed zu analysieren.
2. Die Bewertung muss archetypen- und planabhängig sein.
3. Keepability, Early Play und Planfähigkeit müssen getrennt ausgewiesen werden.
4. Aggregierte Daten dürfen nicht nachträglich als simulierte Einzelhände dargestellt werden.
5. Jeder Kalibrierungszyklus endet mit einer kritischen Reflexion und einem eindeutig priorisierten nächsten Schritt.
6. Die fünf allgemeinen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill; spezielle Engine-Decks wie Shrines sind keine verpflichtende globale Referenz.
7. Control-Interaktion muss gegen den konkreten gegnerischen Plan und nicht nur anhand der Kartenzahl bewertet werden.

Dokumentiere diese Spezifikationsänderung in `docs/CHANGELOG_SPECIFICATION.md`.

## 12. No-Change- und Abbruchfall

Falls kein sinnvoller Commit möglich ist, dokumentiere im Repository oder im Abschlussprotokoll:

- geprüfte Hypothese
- verwendete Daten
- verwendeten Seed, falls eine Simulation möglich war
- exakten Stopgrund
- gewonnene Erkenntnis
- Confidence
- mindestens zwei mögliche Folgeschritte
- genau einen priorisierten nächsten ausführbaren Schritt

Nach zwei aufeinanderfolgenden No-Change-Zyklen mit derselben Ursache wechsle zum nächsten priorisierten Roadmap-Punkt.

Erfinde keine Ergebnisse, keine Workflow-Runs, keine Artefakte und keine simulierten Hände.
