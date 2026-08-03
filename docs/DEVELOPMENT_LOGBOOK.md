# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

Run 63 zeigte, dass der Mono-White-Pool nur drei mögliche Kopien einer automatisch wiederholbaren Tokenquelle besitzt. Deshalb wurde Value Tokens zugunsten des besser versorgten Go-Wide-Plans pausiert.

### Runs 64 bis 68

- Runs 64–68 scheiterten jeweils an genau einem Full-Pool-Test.
- Fast-Validierung und Token-Diagnose waren in allen Läufen erfolgreich.
- Run 68: Commit `43cc6a5b1376e9b212d6998a1c014c13b13671f2`, Workflow `30823466044`, 300 Tests bestanden und 1 fehlgeschlagen.
- Artefakt `global-calibration-pr-68`, ID `8859954895`.

### Stabiler Produktionsbefund

- Benchmarks: Burn 83, Tokens 96, Artifacts 90, Control 85, Mill 80.
- Go-Wide-Profil: 36 Kreatur-Token-Maker, 25 sofortige Maker, 21 Multi-Maker, 6 Anthems.
- 100 Hände: Keepability 77 %, Planfähigkeit 77 %, Early Play T2/T3 94/96 %.
- Goldfish: 23,72 Schaden, 63 % Killrate, Board 9,30.
- Matchups: Burn 0 %, Artifacts 58 %, Mill 100 %.

### Belegte Root Cause

`tests/conftest.py` setzt `THUN_DATABASE_FILE` für die gesamte Testsitzung absichtlich auf eine synthetische Datenbank. Der als Full-Pool bezeichnete Test öffnete `CardDatabase()` ohne expliziten Pfad und prüfte deshalb Karten wie `Test Token 1` statt `data/cards.db`. Die Rollen- und Qualitätsberichtabweichungen waren Folge dieses falschen Testinputs, nicht eines instabilen Produktionsbuilders.

## Aktueller Reparaturzyklus

- **Ursache:** Full-Pool-Test verwendet durch die Session-Umgebung den synthetischen Fixture-Pool.
- **Hypothese:** `CardDatabase(DATABASE_FILE)` bindet das Integrationsgate explizit an die kanonische Repository-Datenbank und umgeht den Test-Fixture-Pfad.
- **Änderung:** expliziter Datenbankpfad plus Pfadassertion; Logbook und Roadmap im selben Commit.
- **Erfolg:** 301 Tests, Fast-Validierung und Token-Diagnose grün; drei anschließende CI-Durchgänge auf demselben Head bleiben grün und metrisch identisch.
- **Rollback:** Test verwendet weiterhin `Test Token`-Karten, Produktionsmetriken verändern sich oder einer der drei Bestätigungsläufe ist rot.
- **KGB-Entscheidung vor Validierung:** keine neue KGB.

## Nächster ausführbarer Schritt

Reparaturcommit veröffentlichen, den ersten Workflow artifact-first auswerten und anschließend denselben Head zweimal über fehlgeschlagene-Job-Neustarts beziehungsweise erneute CI-Ausführungen bestätigen, insgesamt drei vollständige grüne Durchgänge.
