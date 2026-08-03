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
- [ ] planspezifische Rollenminimums und Dichteziele
- [ ] Rollen-Mischmasch im Qualitätsbericht negativ bewerten
- [ ] Engine Density modellieren
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

1. PR-Validierung der Token-Plan-Erkennung und Artefaktprüfung
2. planspezifische Rollenminimums und Strategy-Commitment-Bericht
3. Engine Density
4. Finish Density
5. belastbare Vergleichsbaseline
6. Meta-Benchmark

## Definition of Done für den nächsten Sprint

- Token-Hauptplan wird vor Kartenauswahl bestimmt.
- Mindestens drei gezielte Regressionstests decken Subarchetyp-Kohärenz ab.
- Der gewählte Token-Plan ist im erzeugten Profil und Bericht sichtbar.
- Planspezifische Rollenminimums verhindern Rollen-Mischmasch.
- Fast-Validierung bleibt unter zehn Minuten.
- Keine unbegründete Regression bei Burn, Artifacts, Shrines oder Mill.
- Logbuch, Entscheidungen und bekannte Probleme sind aktualisiert.
