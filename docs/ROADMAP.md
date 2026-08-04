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

## Stabiler Stand – Run 78

- Benchmarks Burn/Tokens/Artifacts/Control/Mill: 83/98/90/85/80
- 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets
- Keepability/Planfähigkeit 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate
- Game One Burn/Artifacts/Mill: 0/64/100 %
- Burn Postboard 62 %, modellierte Matchwinrate 48 %
- Burn-Plan: 3 `Dawnbringer Cleric` hinein; 2 `Descendant of Storms`, 1 `Duty Beyond Death` heraus
- Mainboard-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`

## Aktueller Zyklus – Outlet Synergy Precision

1. falschen Legacy-Outletbonus aus dem `Duty`-Auswahltrace entfernen.
2. Rollen und Synergie-Tags in derselben Token-Präzisionssicht verfeinern.
3. selbstopferndes Equipment von echten Kreaturen-Outlets unterscheiden.
4. breite globale Änderung gegen Benchmarks und Goldfish gegenprüfen.

## Prioritäten danach

1. globales Outlet-Tagging zusammen mit eng bedingtem Burn korrekt modellieren.
2. Bedingte/dead-on-board Kandidaten unter korrekter Semantik vergleichen.
3. Modellierte Matchups gegen reale Spiele kalibrieren.
4. Regression-Baseline statt `baseline: none`.

## Genau ein nächster ausführbarer Schritt

Das globale Outlet-Tagging nur gemeinsam mit der Bewertung und Simulation von
„genau 10 Leben“-Burn korrigieren; die Änderung darf den Burn-Goldfish nicht
durch Benchmark-Gaming verschlechtern.
