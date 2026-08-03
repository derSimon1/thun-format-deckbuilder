# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort; externe Club-/Meta-Evidenz fehlt.

Aktuelle Sicherungspunkte:

- Sideboard: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- Mill-Messung: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- Token-Diagnose: `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`, Run `30808101416`
- Token-Builder: `1a4618ed3eaed910632eba526b550d8abf9ed905`, Run `30810553137`

## Vier-Stunden-Lauf – Token-Fokus

### Ausgangsstand Run 54

- Plan Aristocrats
- Benchmark 90
- Keepability/Planfähigkeit 73/73 %
- Commitment 100 %, Engine Density 64 %
- Goldfish 18,69 Schaden, 66 % Killrate bis Zug 5
- Matchups: 0 % Burn, 2 % Artifacts, 100 % Mill

## Token-Zyklus 1 – Paketdiagnose

- Commit `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`
- Run `30808101416`, erfolgreich
- 274 Tests; ungefähr 3:58 Minuten
- Artefakt `global-calibration-pr-55`, ID `8853712704`
- echte Kopien: Material 14, Outlets 9, Death-/Drain-Payoffs 3
- 43 breite Fehlpositive: 19 Nichtkreatur-Token-Maker, 23 One-Shot-Sacrifices, 1 unspezifischer Payoff
- Poolkapazität ausreichend: 169 Kreatur-Token-Karten, 20 wiederholbare Maker, 34 Outlets, 13 Death-Payoffs
- Hypothese bestätigt; keine neue KGB

## Token-Zyklus 2 – Präzise Planrollen und Komposition

### Run 56

- Commit `676da07f56abc55651c2d1e1cb25b423ba1a6088`
- Run `30809079933`, rot: 274 Tests grün, 5 Sparse-Pool-Generierungstests rot
- Fast-Validierung selbst PASS
- Artefakt `8854099893`

Full-Pool-Ergebnis:

| Metrik | Run 55 | Run 56 | Delta |
|---|---:|---:|---:|
| Plan | Aristocrats | Value Tokens | geändert |
| Benchmark | 90 | 91 | +1 |
| echtes Material | 14 | 33 | +19 |
| wiederholbare Maker | 0 | 12 | +12 |
| Rollen-Fehlpositive | 43 | 0 | -43 |
| Keepability | 73 % | 77 % | +4 pp |
| Planfähigkeit | 73 % | 76 % | +3 pp |
| Schaden | 18,69 | 18,97 | +0,28 |
| Killrate | 66 % | 66 % | 0 |
| vs Artifacts | 2 % | 7 % | +5 pp |

Die Rollenbereinigung war fachlich bestätigt; das rote Gate entstand durch unerreichbare Produktionsminimums in kleinen Fixture-Pools.

### Runs 57/58 – Sparse-Pool-Hotfix

- Run 57, Commit `dfa5bf4cccf21d2eee782191097b8ed894f6f36a`: rot; 280/281 Tests grün
- Run-57-Artefakt `8854353437`: neutrale Füller wurden auch im Full-Pool aufgenommen; Benchmark 91→87, Schaden 18,97→16,80, Killrate 66→28 %, Artifacts 7→0 %
- Commit `1a4618ed3eaed910632eba526b550d8abf9ed905` beschränkt Füller auf echte Gesamtkopienlücken
- Run 58 `30810553137`: erfolgreich
- 283 Tests in 30,85 Sekunden
- Test-/Fast-/Diagnoseschritt ungefähr 3:59 Minuten
- Artefakt `global-calibration-pr-58`, ID `8854683264`, 47 Dateien, 62.499 Byte
- Benchmarks: Burn 83, Tokens 91, Artifacts 90, Control 85, Mill 80
- fünf Archetypen, sechs Matchups, 0 gemeldete Regressionen

Run 58 stellt den Full-Pool-Stand von Run 56 exakt wieder her und hält Sparse-Pools generierbar:

- Value Tokens
- 33 Materialkopien
- 12 wiederholbare Maker
- 0 breite Fehlpositive
- Keepability/Planfähigkeit 77/76 %
- Schaden/Killrate 18,97/66 %
- Matchups: 0 % Burn, 7 % Artifacts, 100 % Mill

### KGB-Entscheidung

Keine neue v2-KGB. Der Token-Builder ist nun ein technischer Sicherungspunkt, aber Goldfish und Matchups verwenden weiterhin eine nachweislich grobe Produktionsannahme.

### Reflexion

- Präzise Planrollen verbessern Kohärenz und Starthände.
- Full-Pool-Ziele dürfen nicht unbesehen auf Sparse-Pools übertragen werden.
- Neutrale Füller müssen ausschließlich eine tatsächliche Kopienlücke schließen.
- Der aktuelle Goldfish-Wert ist nicht belastbar: jeder Maker erzeugt pauschal zwei Tokens, auch Death-, Ziel- und variable Trigger.
- Grüne CI bestätigt die Builderintegration, nicht die simulierte Killrate.

## Token-Zyklus 3 – Produktionsmodi und Goldfish

### Ausgangs-Head

`1a4618ed3eaed910632eba526b550d8abf9ed905`

### Zyklusvertrag

- **Ursache:** alle Token-Maker werden als zwei sofort erzeugte Kreatur-Tokens behandelt.
- **Hypothese:** Immediate-, Repeatable-, Conditional- und Death-Produktion mit konservativer Mindestmenge liefert realistischere Board-, Schaden- und Killdaten.
- **Änderungen:** zentrale Produktionsanalyse; Rollenmarker und Diagnoseartefakt; Goldfish-Modell und Regressionstests.
- **Erfolg:** Ein-/Zwei-Maker unterscheiden sich; echte Engines skalieren über Züge; Death-/zielabhängige Effekte erzeugen im leeren Solitaire nicht automatisch Tokens; Builderdeck bleibt identisch.
- **Invarianten:** Benchmark 91, Material 33, wiederholbare Maker 12, Fehlpositive 0, Legalität und Opening-Hand-Werte unverändert.
- **Abbruch:** Builderausgabe ändert sich, andere Benchmarks regressieren oder Fast überschreitet zehn Minuten.
- **geschätzte Zeit:** 60–80 Minuten inklusive Artefaktauswertung.

### Änderungen vor Push

1. `token_production.py` erkennt konservative Mindestmenge und Produktionsmodus aus Oracle-Text.
2. Der Token-Builder speichert stabile `token_output_*`- und `token_production_*`-Marker; die Diagnose listet Modi und Karten.
3. Goldfish zählt Kartenkörper, garantierte Sofortproduktion und echte unbedingte Engines getrennt; Conditional-/Death-Ausgabe ist im leeren Solitaire nicht kostenlos.

### KGB-Entscheidung vor Push

Keine neue KGB. Die Änderung korrigiert Messung, nicht Kartenauswahl, und bleibt bis CI-/Artefaktauswertung vorläufig.

### Priorisierter nächster ausführbarer Schritt

Den neuen Workflow vollständig auswerten. Danach prüfen, ob der Builder wegen der korrigierten Produktionsdaten andere Karten priorisieren muss oder ob zuerst separate Go-Wide-/Value-/Aristocrats-Referenzdecks benötigt werden.
