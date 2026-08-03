# Roadmap

## Phase 1 – Stabilität und Messbarkeit

- [x] globale Fast-Validierung
- [x] fünf repräsentative Archetypen
- [x] Datenbankcache
- [x] Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] grundlegende Regressionserkennung
- [x] Token-Combat realistischer modellieren
- [ ] verlässliche Baseline statt `baseline none`
- [ ] eindeutiges Zyklusprotokoll mit Stopgrund und Run-ID

## Phase 2 – Strategy Commitment

- [x] Token-Hauptplan vor der Kartenauswahl bestimmen
- [x] Signale für Go Wide, Value Tokens und Aristocrats unterscheiden
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
- [ ] Regeln archetypenübergreifend abstrahieren

## Phase 3 – Meta-Benchmark

- [ ] Referenzbibliothek erfolgreicher Standard-/Pioneer-Konzepte
- [ ] Thun-Meta-Referenzdecks
- [ ] Benchmark gegen Burn, Tokens, Artifacts, Mill und weitere relevante Decks
- [ ] Schwachstellenanalyse und Sideboard-Wirkung
- [ ] Clubtests als externe Validierung dokumentieren

## Phase 4 – Adaptive Optimierung

- [ ] Hypothesenregister mit Confidence
- [ ] automatische Priorisierung nach erwartetem Qualitätsgewinn
- [ ] kontrollierte Experimente
- [ ] Lernprotokoll gegen wiederholte Fehlversuche
- [ ] Selbstverbesserung der Spezifikation nur mit belegter Evidenz

## Aktuelle Priorität

1. PR-Validierung und Artefaktprüfung der Token-Engine-Density
2. Finish Density
3. Engine Density archetypenübergreifend abstrahieren
4. Strategy Commitment in den allgemeinen Qualitätsbericht integrieren
5. belastbare Vergleichsbaseline
6. Meta-Benchmark

## Definition of Done für den nächsten Sprint

- Token-Hauptplan wird vor Kartenauswahl bestimmt.
- Mindestens drei gezielte Regressionstests decken Subarchetyp-Kohärenz ab.
- Der gewählte Token-Plan ist im erzeugten Profil und Bericht sichtbar.
- Planprägende Rollen werden als Dichteziele bevorzugt, ohne sparse Kartenpools zu blockieren.
- Rollen-Mischmasch erzeugt eine explizite Warnung und einen nachvollziehbaren Commitment-Score.
- Wiederholbare Engines werden von einmaligem Material getrennt und kopiengewichtet berichtet.
- Harte Mindestdichten werden erst nach Kapazitätsprüfung aktiviert.
- Fast-Validierung bleibt unter zehn Minuten.
- Keine unbegründete Regression bei Burn, Artifacts, Shrines oder Mill.
- Logbuch, Entscheidungen und bekannte Probleme sind aktualisiert.
