# Roadmap

## Development System v2.0

Jeder Kalibrierungszyklus beginnt mit der letzten Known Good Baseline und endet mit einer expliziten Entscheidung: neue KGB, keine neue KGB oder Regression.

Bei zwei aufeinanderfolgenden No-Change-Zyklen derselben Ursache oder zwei unbegründeten Regressionen derselben Hypothese wird zum nächsten priorisierten Roadmap-Punkt gewechselt. Eine Rückkehr erfolgt erst bei neuer belegter Evidenz.

Die fünf verbindlichen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Shrines ist kein Pflicht- oder Referenzarchetyp.

## Phase 1 – Stabilität und Messbarkeit

- [x] globale Fast-Validierung
- [x] fünf repräsentative Archetypen
- [x] Datenbankcache
- [x] Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] grundlegende Regressionserkennung
- [x] Token-Combat realistischer modellieren
- [ ] letzte belastbare Known Good Baseline eindeutig bestimmen und dokumentieren
- [ ] reproduzierbaren `OpeningHandPlanReport` mit genau 100 gespeicherten Händen je Referenzdeck implementieren
- [ ] Keepability, Early Play und Planfähigkeit getrennt ausweisen
- [ ] eindeutiges Zyklusprotokoll mit Stopgrund, KGB-Entscheidung und Run-ID

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

- [ ] Control als fünften allgemeinen Referenzarchetyp vollständig integrieren
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

1. letzte belastbare Known Good Baseline bestimmen und dokumentieren
2. `OpeningHandPlanReport` mit genau 100 reproduzierbaren Händen je Referenzdeck implementieren
3. Token-Subarchetypen Go Wide, Value Tokens und Aristocrats anhand planfähiger Hände vergleichen
4. Control als Referenzarchetyp integrieren
5. Strategy Commitment in den allgemeinen Qualitätsbericht integrieren
6. Engine Density archetypenübergreifend abstrahieren
7. Finish Density und klare Wincondition-Erkennung
8. Meta-Benchmark

## Definition of Done für den nächsten Zyklus

- Ausgangs-KGB ist mit Commit-SHA und Evidenz dokumentiert.
- Genau 100 reproduzierbare Hände je verwendeter Referenzdeckliste werden mit Seed gespeichert.
- Burn, Tokens, Artifacts, Control und Mill werden verglichen.
- Go Wide, Value Tokens und Aristocrats werden getrennt ausgewertet.
- Keepability, Early Play und Planfähigkeit bleiben getrennt.
- Vollständige Testsuite und Fast-Validierung sind erfolgreich.
- Fast-Validierung bleibt unter zehn Minuten.
- Keine unbegründete Regression gegenüber der KGB.
- Logbook enthält Reflexion, Confidence, KGB-Entscheidung und genau einen nächsten Schritt.
