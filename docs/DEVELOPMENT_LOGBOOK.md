# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

Run 63 zeigte, dass der Mono-White-Pool nur drei mögliche Kopien einer automatisch wiederholbaren Tokenquelle besitzt. Deshalb wurde Value Tokens zugunsten des besser versorgten Go-Wide-Plans pausiert.

### Run 64

- Commit `03dfbc385f252cdd08b1160dab08a02a3b4cabd4`
- Workflow `30819019117`, fehlgeschlagen
- 300 Tests bestanden, 1 Test fehlgeschlagen
- Fast-Validierung erfolgreich
- Artefakt `global-calibration-pr-64`, ID `8858133949`
- Benchmarks: Burn 83, Tokens 96, Artifacts 90, Control 85, Mill 80
- Go-Wide-Paket: 36 Kreatur-Token-Maker, 25 sofortige Maker, 21 Multi-Maker, 6 Anthems
- 100 Hände: Keepability 77 %, Planfähigkeit 77 %, Early Play T2/T3 94/96 %
- Goldfish: 23,72 Schaden, 63 % Killrate, Board 9,30
- Matchups: Burn 0 %, Artifacts 58 %, Mill 100 %

### Runs 65 und 66

- Run 65: Commit `a9dc0ea54a842f2b50547768a185abd49b2062cb`, Workflow `30820717373`, fehlgeschlagen
- Run 66: Commit `50c174413f42d6a185631e6d1ae6fd0d5bf69257`, Workflow `30821482441`, fehlgeschlagen
- in beiden Runs: Fast-Validierung und Token-Diagnose erfolgreich; nur derselbe Full-Pool-Test rot
- Run-66-Artefakt `global-calibration-pr-66`, ID `8859139442`
- Run 66: 300 Tests bestanden, 1 fehlgeschlagen
- Qualitätsbericht belegt 21 `token_multi_maker`-Kopien bei Minimum 6

### Belegte Ursache

Der Produktionscode und die Artefakte erfüllen das Go-Wide-Paket. Der Test zählte rohe `DeckEntry.roles`, deren Enum-/String-Repräsentation kein stabiler öffentlicher Vertrag ist. Zwei Normalisierungsvarianten änderten daran nichts. Der kanonische Vertrag ist `deck.quality_report.role_quality`, denn genau dieser Bericht steuert und dokumentiert die erfüllten Profilrollen.

## Aktueller Hotfix-Zyklus

- **Ursache:** Test prüft eine interne Rollenrepräsentation statt des kanonischen Qualitätsberichts.
- **Hypothese:** Prüfung von `quality_report.role_quality` beseitigt den repräsentationsabhängigen Fehler, ohne Produktionscode oder Deckliste zu ändern.
- **Änderung:** nur Full-Pool-Test sowie Logbook und Roadmap.
- **Erfolg:** vollständige Testsuite und Fast-Validierung grün; Deck-Hash, Benchmark 96 und Go-Wide-Dichten unverändert.
- **Rollback:** Produktionsmetriken oder Referenzbenchmarks verändern sich.
- **KGB-Entscheidung vor Push:** keine neue KGB.

## Reflexion

- Zwei aufeinanderfolgende Test-Hotfixes scheiterten, weil weiterhin die falsche Abstraktionsebene geprüft wurde.
- Der Qualitätsbericht ist stabiler als rohe Rollenobjekte und entspricht dem fachlichen Ziel des Tests.
- Benchmark 96 belegt Rollenerfüllung, aber noch nicht automatisch bessere Club-Performance.
- Das Burn-Matchup bleibt die stärkste offene spielerische Warnung.
- Die Go-Wide-Liste enthält eine Karte mit erforderlichem farblosem Mana; dieser Castability-Fall folgt erst nach grünem Gate.

## Nächster ausführbarer Schritt

Den Qualitätsbericht-Hotfix veröffentlichen und den Workflow vollständig auswerten. Bei grünem Gate die farblose Manaanforderung global absichern.
