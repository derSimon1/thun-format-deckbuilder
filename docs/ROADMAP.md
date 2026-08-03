# Roadmap

## Development System v2.0

Jeder Kalibrierungszyklus beginnt mit der letzten Known Good Baseline und endet mit einer expliziten Entscheidung: neue KGB, keine neue KGB oder Regression.

Bei zwei aufeinanderfolgenden No-Change-Zyklen derselben Ursache oder zwei unbegründeten Regressionen derselben Hypothese wird zum nächsten priorisierten Roadmap-Punkt gewechselt. Eine Rückkehr erfolgt erst bei neuer belegter Evidenz.

Die fünf verbindlichen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Shrines ist kein Pflicht- oder Referenzarchetyp.

## Phase 1 – Stabilität und Messbarkeit

- [x] globale Fast-Validierung
- [x] fünf repräsentative Archetypen im Legacy-Validator
- [x] Datenbankcache
- [x] Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] grundlegende Regressionserkennung
- [x] Token-Combat realistischer modellieren
- [x] v2-Bootstrap-Vergleichsstand mit Commit, Workflow und Einschränkungen dokumentieren
- [x] reproduzierbaren `OpeningHandPlanReport` mit genau 100 gespeicherten Händen je im Fast-Lauf verwendeter Deckliste implementieren
- [x] Keepability, Early Play und Planfähigkeit getrennt ausweisen
- [ ] Fast-Report-Artefakte und Laufzeit im neuen PR-Workflow verifizieren
- [ ] vollständigen Validator auf Burn, Tokens, Artifacts, Control und Mill umstellen
- [ ] erste vollständig qualifizierte v2-KGB erzeugen

## Phase 2 – Strategy Commitment und Engines

- [x] Token-Hauptplan vor der Kartenauswahl bestimmen
- [x] Go Wide, Value Tokens und Aristocrats unterscheiden
- [x] Token-Karten planabhängig bewerten
- [x] planspezifische weiche Dichteziele
- [ ] kapazitätsgeprüfte harte Mindestdichten für planprägende Rollen
- [x] Rollen-Mischmasch im Strategy-Commitment-Bericht negativ bewerten
- [x] Strategy-Commitment-Bericht mit Plan, Dichten und Warnungen
- [ ] Strategy Commitment in den allgemeinen Qualitätsbericht integrieren
- [x] Engine Density für Token-Pläne messen und berichten
- [ ] Engine Density archetypenübergreifend abstrahieren
- [ ] Finish Density modellieren
- [ ] klare Wincondition-Erkennung

## Phase 3 – Control und allgemeine Interaktion

- [ ] Control als fünften allgemeinen Referenzarchetyp im Builder und Validator integrieren
- [ ] matchupabhängige relevante Interaktion statt bloßer Antwortenzahl messen
- [ ] Stabilisierung bis Zug 4 oder 5 bewerten
- [ ] Kartenvorteil nach früher Interaktion messen
- [ ] Wincondition-Zugang nach Stabilisierung prüfen
- [ ] Control gegen Aggro, Tokens und Nichtkreaturen-/Engine-Pläne benchmarken

## Phase 4 – Meta-Benchmark

- [ ] Referenzbibliothek erfolgreicher Standard-/Pioneer-Konzepte
- [ ] Thun-Meta-Referenzdecks
- [ ] Benchmark gegen Burn, Tokens, Artifacts, Control und Mill
- [ ] Schwachstellenanalyse und Sideboard-Wirkung
- [ ] Clubtests als externe Validierung dokumentieren

## Phase 5 – Adaptive Optimierung

- [ ] Hypothesenregister mit Confidence
- [ ] automatische Priorisierung nach erwartetem Qualitätsgewinn
- [ ] kontrollierte Experimente
- [ ] Lernprotokoll gegen wiederholte Fehlversuche
- [ ] KGB-Historie und Meilenstein-Tags
- [ ] Rollback-Protokoll
- [ ] Selbstverbesserung der Spezifikation nur mit belegter Evidenz

## Aktuelle Priorität

1. neuen Workflow, 100-Hand-Rohdaten und Laufzeit des `OpeningHandPlanReport` verifizieren
2. Control als fünften Builder- und Validator-Archetyp integrieren und Shrines aus der Pflichtvalidierung entfernen
3. Burn, Tokens, Artifacts, Control und Mill mit denselben 100-Hand-Metriken vergleichen
4. Go Wide, Value Tokens und Aristocrats anhand planfähiger Hände getrennt benchmarken
5. erste vollständig qualifizierte v2-KGB dokumentieren
6. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
7. Finish Density und klare Wincondition-Erkennung
8. Meta-Benchmark

## Definition of Done für den nächsten Zyklus

- aktueller PR-Workflow und dessen Rohdatenartefakte sind vollständig ausgewertet
- Control kann als legaler 60/15-Referenzarchetyp erzeugt werden
- Pflichtvalidierung verwendet Burn, Tokens, Artifacts, Control und Mill; Shrines ist daraus entfernt
- Control-Hände unterscheiden relevante frühe Interaktion, Stabilisierung, Kartenvorteil und Wincondition-Zugang
- Control wird gegen Aggro, Tokens und einen Nichtkreaturen-/Engine-Plan geprüft
- genau 100 reproduzierbare Hände je verwendeter Referenzdeckliste werden mit Seed gespeichert
- vollständige Testsuite und Fast-Validierung sind erfolgreich
- Fast-Validierung bleibt unter zehn Minuten
- keine unbegründete Regression gegenüber dem v2-Bootstrap-Vergleichsstand
- Logbook enthält Reflexion, Confidence, KGB-Entscheidung und genau einen nächsten Schritt
