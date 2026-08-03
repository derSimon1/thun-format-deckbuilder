# Roadmap

## Development System v2.0

Jeder Kalibrierungszyklus beginnt mit der letzten Known Good Baseline und endet mit einer expliziten Entscheidung: neue KGB, keine neue KGB oder Regression.

Bei zwei aufeinanderfolgenden No-Change-Zyklen derselben Ursache oder zwei unbegründeten Regressionen derselben Hypothese wird zum nächsten priorisierten Roadmap-Punkt gewechselt. Eine Rückkehr erfolgt erst bei neuer belegter Evidenz.

Die fünf verbindlichen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Shrines ist kein Pflicht- oder Referenzarchetyp.

## Phase 1 – Stabilität und Messbarkeit

- [x] globale Fast-Validierung
- [x] Datenbankcache
- [x] Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] grundlegende Regressionserkennung
- [x] Token-Combat realistischer modellieren
- [x] v2-Bootstrap-Vergleichsstand mit Commit, Workflow und Einschränkungen dokumentieren
- [x] reproduzierbaren `OpeningHandPlanReport` mit genau 100 gespeicherten Händen je im Fast-Lauf verwendeter Deckliste implementieren
- [x] Keepability, Early Play und Planfähigkeit getrennt ausweisen
- [x] Manafehler dürfen nicht als planfähige Hände gelten
- [ ] Control-Pflichtvalidator und sechs priorisierte Matchups im PR-Workflow verifizieren
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

- [x] Dimir Control als allgemeine Builder-Strategie registrieren
- [x] Control-Scoring für Counter, Removal, Sweeper, Kartenvorteil und Finisher implementieren
- [x] Control-Benchmark und v2-Validatorregistrierung vorbereiten
- [ ] reale Control-Generierung mit 60/15, Legalität und Manabasis im Workflow bestätigen
- [ ] matchupabhängige relevante Interaktion statt bloßer Antwortenzahl messen
- [ ] Stabilisierung bis Zug 4 oder 5 bewerten
- [ ] Kartenvorteil nach früher Interaktion messen
- [ ] Wincondition-Zugang nach Stabilisierung prüfen
- [ ] Control gegen Burn, Tokens und Artifacts benchmarken

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

1. neuen Control-Workflow vollständig auswerten: Tests, 60/15, Benchmark, 100 Hände, sechs Matchups, BO3, Laufzeit und Artefakte
2. bei roter CI genau eine belegte Control-Ursache beheben; keine Grenzwerte nur zum Bestehen verschieben
3. bei grüner CI Control-Handmetriken auf relevante Interaktion, Kartenvorteil und Finisher-Zugang prüfen
4. Mill-Befund 0 % planfähig / 100 % marginal anhand Rohhänden und Oracle-Textdaten untersuchen
5. Go Wide, Value Tokens und Aristocrats anhand planfähiger Hände getrennt benchmarken
6. erste vollständig qualifizierte v2-KGB dokumentieren
7. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
8. Finish Density und klare Wincondition-Erkennung
9. Meta-Benchmark

## Definition of Done für den nächsten Zyklus

- PR-Workflow des Control-Commits ist vollständig ausgewertet
- Pflichtvalidierung verwendet Burn, Tokens, Artifacts, Control und Mill; Shrines ist daraus entfernt
- Control erzeugt ein legales 60/15-Deck mit ausreichender Manabasis
- Control-Hände berichten relevante frühe Interaktion, Engine-/Kartenvorteil- und Finisher-Zugang
- Control wird gegen Burn, Tokens und Artifacts sowie die drei Token-Matchups geprüft
- genau 100 reproduzierbare Hände je verwendeter Referenzdeckliste werden mit Seed gespeichert
- vollständige Testsuite und Fast-Validierung sind erfolgreich
- Fast-Validierung bleibt unter zehn Minuten
- keine unbegründete Regression gegenüber dem v2-Bootstrap-Vergleichsstand
- Logbook enthält Reflexion, Confidence, KGB-Entscheidung und genau einen nächsten Schritt
