# Roadmap

## Token Go Wide

- [x] Go-Wide-Profil und Pflichtdichten
- [x] Full-Pool-Test und drei Bestätigungsläufe
- [x] `{C}`-Castability mit zentraler Zahlungsdefinition und echten Quellen
- [x] 23-Land-Experiment verworfen
- [x] Immediate-Maker-Scoring
- [x] reine Opfer-Outlets entfernt
- [x] Lethal-Race-Modell mit abnehmendem Überkill-Nutzen
- [x] Burn-Stabilisierungsoptionen im Sideboard
- [x] Postboard-Lebensgewinn im Burn-Modell
- [x] Burn-Cuts rollenbasiert absichern
- [x] Arena-Import und 100 Hände final bewerten
- [x] Root-`AGENTS.md` als dauerhafte Repository-Einstiegsanweisung validieren
- [x] Quellenspannung strikter `{C}`-Kosten im Candidate Scoring modellieren
- [x] Engine-Pflicht und Engine-Warnung planabhängig kalibrieren
- [x] Go-Wide-Planfähigkeit an einen bis Zug 2 castbaren Maker binden
- [x] Engine-Pflicht zentral im Opening-Hand-Bericht kontextualisieren
- [x] transformationsgesperrte Rückseiteneffekte aus Sofortrollen entfernen
- [x] Sideboard-Suche über Mehrkopien-Schwellen führen und zielabhängigen
  Lebensgewinn abgrenzen
- [x] Trigger-, Saga-, Modal- und Anthem-Kontext bis in Goldfish-Dauersemantik
  vereinheitlichen
- [x] zusätzliche Kreaturen-Opferkosten zentral erkennen und im Goldfish
  Verfügbarkeit sowie Boardverbrauch modellieren
- [x] SQLite-Integritätsprüfung vor atomarem Datenbankersatz unter Windows
  schließen
- [x] Token-spezifische Outlet-Rollen und -Synergien gemeinsam präzisieren
- [x] globale Outlet-Tags, Opfer-Cast-Kosten und exakte Burn-Lebensfenster
  gemeinsam modellieren
- [x] Mill-Einmalquellen, wiederholbare Engines und simulierten Durchsatz
  zentral trennen
- [x] Control-Antworten, echten Kartenvorteil und Winconditions als zentrale
  Stabilisierungssequenz modellieren
- [x] Artifact-Enabler, Payoffs, Engines und Produktionskapazitäten zentral
  trennen und in Benchmark/Opening Hands/Goldfish vereinheitlichen
- [x] reale Matchup-Beobachtungen versioniert und an beide Deck-Hashes binden
- [x] read-only Kalibrierungsartefakt mit ehrlichem Null-Evidenz-Status

## Stabiler Stand – Run 78

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate
- Game One Burn/Artifacts/Mill: 0/64/100 %
- Burn Postboard 62 %, modellierte Matchwinrate 48 %
- Burn-Plan: 3 `Dawnbringer Cleric` hinein; 2 `Descendant of Storms`, 1 `Duty Beyond Death` heraus
- Mainboard-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`

## Aktueller Zyklus – Empirical Matchup Calibration Contract

1. [x] strikt versioniertes Beobachtungsschema definieren.
2. [x] Daten an beide vollständigen Deck-Hashes binden.
3. [x] umgekehrte Orientierung und veraltete Hashes korrekt behandeln.
4. [x] Abdeckung und Fehler nur berichten, nicht Simulation reweighten.
5. [x] Null-Evidenz explizit als `NO_EMPIRICAL_DATA` ausweisen.

## Prioritäten danach

1. Regression-Baseline statt `baseline: none`.
2. Mindestens 20 echte hashgleiche Spiele für ein extremes Matchup erfassen.

## Genau ein nächster ausführbarer Schritt

Den letzten erfolgreichen `global-report.json` als versionierten
Regression-Snapshot einchecken und in Fast-Validierung beweisen, dass ein
unveränderter Folgelauf `baseline: restored` statt `baseline: none` meldet.
