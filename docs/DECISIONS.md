# Decisions

Dauerhafte Architektur- und Prozessentscheidungen. Neue Einträge werden nicht überschrieben, sondern ergänzt oder ausdrücklich ersetzt.

## D-001 – GitHub Actions ist Validator, nicht Entwicklungsagent

**Datum:** 2026-08-03  
**Status:** akzeptiert

GitHub Actions führt Tests und Validierungen aus, entwickelt aber keine Verbesserungen. Produktiver Fortschritt entsteht durch einen konkreten Entwicklungszyklus mit Hypothese, Änderung, Commit und anschließender CI.

**Begründung:** Der Nachtlauf erzeugte trotz zahlreicher geplanter Zyklen keinen neuen Entwicklungscommit.

## D-002 – Kein Cron als primärer Entwicklungsantrieb

**Datum:** 2026-08-03  
**Status:** akzeptiert

Zeitgesteuerte GitHub-Workflows dürfen ergänzend validieren, gelten aber weder als Entwicklungsfortschritt noch als zuverlässiger Motor einer Kalibrierung.

## D-003 – Versionierte Spezifikation als Single Source of Truth

**Datum:** 2026-08-03  
**Status:** akzeptiert

Kalibrierungsregeln leben im Repository. Chat-Aufträge referenzieren auf die aktuelle Spezifikation und den aktuellen Prompt, statt lange Anweisungen zu kopieren.

## D-004 – Ein zusammenhängendes Änderungspaket pro Zyklus

**Datum:** 2026-08-03  
**Status:** akzeptiert

Pro Zyklus werden höchstens drei eng gekoppelte Änderungen derselben Ursache in genau einem Commit gebündelt. Dadurch bleiben Ursache und Wirkung nachvollziehbar.

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
**Status:** akzeptiert

Shrines werden nur verändert, wenn eine globale Ursache dies rechtfertigt. Zielgerichtete Shrine-Optimierung ist nicht Teil der aktuellen Kalibrierung.

## D-008 – Fast und Full bleiben getrennt

**Datum:** 2026-08-03  
**Status:** akzeptiert

Fast dient kurzen Entwicklungszyklen und soll unter zehn Minuten bleiben. Full wird manuell oder am Ende einer Runde ausgeführt.
