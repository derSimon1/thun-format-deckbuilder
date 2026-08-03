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

Der einzige Testfehler entstand durch gemischte Enum- und String-Repräsentationen der Rollen.

### Run 65

- Commit `a9dc0ea54a842f2b50547768a185abd49b2062cb`
- Workflow `30820717373`, fehlgeschlagen
- 300 Tests bestanden, 1 Test fehlgeschlagen
- Fast-Validierung und Artefakte gegenüber Run 64 unverändert
- Artefakt `global-calibration-pr-65`, ID `8858844642`

Die Annahme, `str(CardRole)` liefere den kanonischen Rollenwert, war falsch. Der Test muss den Enum-Wert verwenden und bei Strings zurückfallen.

## Aktueller Hotfix-Zyklus

- Ursache: gemischte Enum-/String-Rollen im Full-Pool-Test
- Hypothese: `getattr(role, "value", str(role))` normalisiert beide Repräsentationen
- Änderung: nur Testnormalisierung und Dokumentation
- Erfolg: 301 Tests und Fast-Validierung grün; Deck und Metriken unverändert
- KGB-Entscheidung vor Push: keine neue KGB

## Reflexion

- Benchmark 96 belegt bessere Rollenerfüllung, aber nicht automatisch bessere Club-Performance.
- Das Burn-Matchup bleibt die stärkste offene spielerische Warnung.
- Die Go-Wide-Liste enthält eine Karte mit erforderlichem farblosem Mana, während die aktuelle Basismana-Analyse nur W/U/B/R/G verarbeitet. Dieser Castability-Fall muss nach grünem Gate geprüft werden.

## Nächster ausführbarer Schritt

Den Enum-Wert-Hotfix veröffentlichen und den Workflow vollständig auswerten. Bei grünem Gate anschließend die farblose Manaanforderung global absichern.
