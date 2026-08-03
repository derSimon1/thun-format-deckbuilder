# Decisions

Dauerhafte Architektur- und Prozessentscheidungen. Neue Einträge werden nicht überschrieben, sondern ergänzt oder ausdrücklich ersetzt.

## D-001 – GitHub Actions ist Validator, nicht Entwicklungsagent

**Datum:** 2026-08-03  
**Status:** akzeptiert

GitHub Actions führt Tests und Validierungen aus, entwickelt aber keine Verbesserungen. Produktiver Fortschritt entsteht durch einen konkreten Entwicklungszyklus mit Hypothese, Änderung, Commit und anschließender CI.

## D-002 – Kein Cron als primärer Entwicklungsantrieb

**Datum:** 2026-08-03  
**Status:** akzeptiert

Zeitgesteuerte GitHub-Workflows dürfen ergänzend validieren, gelten aber weder als Entwicklungsfortschritt noch als zuverlässiger Motor einer Kalibrierung.

## D-003 – Versionierte Spezifikation als Single Source of Truth

**Datum:** 2026-08-03  
**Status:** akzeptiert

Kalibrierungsregeln leben im Repository. Chat-Aufträge referenzieren auf Spezifikation und Prompt, statt lange Anweisungen zu kopieren.

## D-004 – Ein zusammenhängendes Änderungspaket pro Zyklus

**Datum:** 2026-08-03  
**Status:** akzeptiert

Pro Zyklus werden höchstens drei eng gekoppelte Änderungen derselben Ursache in genau einem Commit gebündelt.

## D-005 – No-Change-Zyklen müssen produktiv sein

**Datum:** 2026-08-03  
**Status:** akzeptiert

Ein Zyklus ohne Commit muss Stopgrund, geprüfte Hypothese, Erkenntnis und nächsten ausführbaren Schritt festhalten. Nach zwei gleichen No-Change-Zyklen wird die Priorität gewechselt.

## D-006 – Tokens werden über Subarchetypen modelliert

**Datum:** 2026-08-03  
**Status:** akzeptiert

Token-Decks werden nicht nur über Rollenanzahlen bewertet. Vor Kartenauswahl wird ein Hauptplan aus Go Wide, Value Tokens oder Aristocrats bestimmt.

## D-007 – Shrines bleiben vorerst Regressionstest

**Datum:** 2026-08-03  
**Status:** ersetzt durch D-009

Diese frühere Entscheidung führte Shrines noch als wiederkehrenden Regressionstest. Sie ist für Development System v2.0 nicht mehr maßgeblich.

## D-008 – Fast und Full bleiben getrennt

**Datum:** 2026-08-03  
**Status:** akzeptiert

Fast dient kurzen Entwicklungszyklen und soll unter zehn Minuten bleiben. Full wird manuell oder am Ende einer Runde ausgeführt.

## D-009 – Control ersetzt Shrines als allgemeinen Referenzarchetyp

**Datum:** 2026-08-03  
**Status:** akzeptiert

Die fünf allgemeinen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Control prüft relevante Interaktion, Stabilisierung und eine belastbare Wincondition. Shrines ist kein Pflicht- oder Referenzarchetyp mehr.

**Ersetzt:** D-007.

## D-010 – Known Good Baseline ist der verbindliche Sicherungspunkt

**Datum:** 2026-08-03  
**Status:** akzeptiert

Jeder Zyklus beginnt mit der letzten dokumentierten Known Good Baseline und endet mit `neue KGB`, `keine neue KGB` oder `Regression`.

Grüne CI allein qualifiziert keinen Commit als KGB. Solange keine v2-KGB existiert, wird ein belegter grüner Stand nur als Bootstrap- oder Legacy-Vergleichsstand geführt.

## D-011 – Mehrstundenbetrieb ohne separate 15-Minuten-Aufgaben

**Datum:** 2026-08-03  
**Status:** akzeptiert

Ein externer Auftrag setzt die Laufzeit `X` in Stunden. Innerhalb desselben Laufs werden so viele vollständige Kalibrierungszyklen wie sinnvoll möglich durchgeführt.

Ein neuer Zyklus wird nur begonnen, wenn er innerhalb der Restzeit vollständig implementiert, getestet, validiert und dokumentiert werden kann.

## D-012 – Artifact-first-Auswertung vor weiterer Optimierung

**Datum:** 2026-08-03  
**Status:** akzeptiert

Nach jedem Workflow werden nicht nur Status und Testzahl geprüft. Das relevante Artefakt wird einmal heruntergeladen und maschinenlesbar ausgewertet. Fachliche Aussagen stützen sich auf Decklisten, Rohhände, Rollen, Sideboard-Pläne, Matchups und BO3, nicht allein auf eine grüne Conclusion.

Wiederholte identische Statusabfragen ohne neue erwartbare Information gelten nicht als produktive Arbeit.

**Begründung:** Mehrere grüne Runs enthielten weiterhin 0 Control-Finisher beziehungsweise falsche `Tormod's Crypt`-Einwechslungen.

## D-013 – Verbindliche Abschlussreserve und Zyklusvertrag

**Datum:** 2026-08-03  
**Status:** akzeptiert

Bei einem Drei-Stunden-Lauf werden mindestens 30 Minuten für letzten Workflow, Artefaktprüfung, Logbook, Roadmap und Abschlussbericht reserviert.

Vor jeder Codeänderung werden Ursache, Hypothese, erwartete Metriken, Invarianten, Erfolgskriterium, Abbruchkriterium und Zeitbedarf festgelegt. Ein Zyklus wird nicht gestartet, wenn Implementierung plus CI-/Artefaktpuffer plus Abschlussreserve nicht mehr in die Restzeit passen.

## D-014 – Spezifische Signale vor breiten Rollen

**Datum:** 2026-08-03  
**Status:** akzeptiert

Bei fachlicher Klassifikation haben spezifische Oracle-Text-Signale Vorrang vor breiten Rollen wie `removal`, `card_draw` oder `finisher`. Breite Rollen dienen als Fallback, wenn keine spezifische Kategorie erkannt wurde.

**Begründung:** `Tormod's Crypt` wurde aufgrund des Wortes `exile` global als Removal erkannt und dadurch zusätzlich fälschlich als Anti-Aggro-Sideboardkarte klassifiziert.

## D-015 – Echte farblose Manaanforderungen bleiben eigenständig

**Datum:** 2026-08-03
**Status:** akzeptiert

`{C}` ist eine eigene Zahlungsanforderung und darf weder durch farbiges Mana noch durch eine generische Wildcard-Quelle erfüllt werden. Mana-Parser, Candidate Eligibility, Basic-Land-Verteilung und Opening-Hand-Castability verwenden dieselbe zentrale Definition.

Eine `{C}`-Karte ist nur zulässig, wenn der konfigurierte Mana-Builder echte farblose Quellen erzeugen kann. Die Basic-Land-Manabasis verwendet dafür `Wastes` und reserviert mindestens so viele passende Quellen, wie ein einzelner Zauber an strikten gleichartigen Symbolen verlangt.

**Begründung:** Das frühere pauschale Verbot verhinderte legale, castbare Kandidaten. Eine bloße Entfernung des Verbots hätte dagegen unspielbare Karten ohne echte farblose Quellen zugelassen.
