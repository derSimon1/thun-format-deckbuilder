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

### Runs 57/58 – Sparse-Pool-Hotfix

- Run 57, Commit `dfa5bf4cccf21d2eee782191097b8ed894f6f36a`: rot; 280/281 Tests grün
- Run-57-Artefakt `8854353437`: neutrale Füller wurden auch im Full-Pool aufgenommen; Benchmark 91→87, Schaden 18,97→16,80, Killrate 66→28 %, Artifacts 7→0 %
- Commit `1a4618ed3eaed910632eba526b550d8abf9ed905` beschränkt Füller auf echte Gesamtkopienlücken
- Run 58 `30810553137`: erfolgreich
- 283 Tests in 30,85 Sekunden
- Test-/Fast-/Diagnoseschritt ungefähr 3:59 Minuten
- Artefakt `global-calibration-pr-58`, ID `8854683264`, 47 Dateien
- Benchmarks: Burn 83, Tokens 91, Artifacts 90, Control 85, Mill 80
- Value Tokens, Material 33, wiederholbare Maker 12, Fehlpositive 0
- Keepability/Planfähigkeit 77/76 %, Schaden/Killrate 18,97/66 %
- Matchups: 0 % Burn, 7 % Artifacts, 100 % Mill

### KGB-Entscheidung

Keine neue v2-KGB. Der Builder ist technisch grün, aber Goldfish und Matchups verwendeten weiterhin eine pauschale Zwei-Token-Annahme.

## Token-Zyklus 3 – Produktionsmodi und Goldfish

### Commit und Run 59

- Commit `3863d851efbf5704f84ce29b6897d638bb5d0bb9`
- Run `30811810037`, rot
- 292 Tests bestanden, 1 Test fehlgeschlagen
- Fast-Validierung selbst PASS
- Artefakt `global-calibration-pr-59`, ID `8855172586`
- kombinierter Test-/Fast-Schritt ungefähr 4:04 Minuten
- Benchmarks unverändert: Burn 83, Tokens 91, Artifacts 90, Control 85, Mill 80
- Builderprofil, Paketrollen und 100 Hände unverändert

### Fachliche Messkorrektur

| Metrik | Run 58 | Run 59 | Delta | Interpretation |
|---|---:|---:|---:|---|
| Goldfish-Schaden | 18,97 | 10,47 | -8,50 | bisherige Pauschalproduktion blähte Schaden stark auf |
| Killrate bis Zug 5 | 66 % | 7 % | -59 pp | neue Zahl ist konservative Messkorrektur, keine Builderregression |
| durchschnittliches Tokenboard | nicht gemessen | 3,15 | neu | reales Board im Modell deutlich kleiner |
| aktive unbedingte Engines | nicht gemessen | 0,00 | neu | nominelle Engine-Dichte entsprach keinen im Goldfish sicher auslösbaren Engines |
| Tokens vs Artifacts | 7 % | 1 % | -6 pp | Matchup hängt direkt an korrigiertem Abschlussdruck |

Die Workflow-Diagnose meldete 26 Kopien mit bedingter und 7 Kopien mit Death-Produktion. Keine der 33 Maker-Kopien erzeugt im leeren Solitaire garantiert sofort oder über einen unbedingten wiederholbaren Trigger Kreatur-Tokens. Damit ist die frühere `token_repeatable_maker`-Metrik fachlich zu breit.

### Rote Ursachen

1. Produktionsmarker wie `token_output_2` und `token_production_conditional` wurden als dynamische Knowledge-Rollen gespeichert. `CardContribution` versuchte sie als kanonische Funktionsrollen zu normalisieren. Die Fast-Validierung konnte zwar einen Produktionsstand erzeugen, aber direkte Token-Generierungstests scheiterten an unbekannten Rollen.
2. Ein Regressionstest erwartete, dass ein wiederholbarer Ein-Token-Maker bereits bis Zug 5 zwingend mehr Schaden als ein gleich teurer einmaliger Maker erzeugt. Run 59 zeigte 4,02 gegenüber 4,04; die Setup-Verzögerung macht diese Annahme für den kurzen Horizont ungültig.

### KGB-Entscheidung

Regression festgestellt. Die Messhypothese ist fachlich bestätigt, das technische Gate ist rot.

### Reflexion

- Produktionsmetadaten sind kein funktionaler Deckrollenbeitrag.
- „Repeatable“ bedeutet nicht automatisch, dass der Trigger im leeren Goldfish auslöst.
- Die neue niedrige Killrate darf nicht durch Lockerung des Modells „repariert“ werden.
- Der Builder priorisiert derzeit bedingte Engines, ohne garantierte Produktion zu messen.
- Grüne Fast-Validierung allein hätte die rote Testintegration und die falsche Repeatable-Annahme nicht ersetzt.

## Token-Hotfix 3 – Metadaten von Funktionsrollen trennen

### Zyklusvertrag

- **Ursache:** dynamische Produktionsmarker werden fälschlich als `CardContribution`-Rollen normalisiert; der Engine-Test verwendet einen ungeeigneten Fünf-Züge-Vergleich.
- **Hypothese:** Metadata-Prefixe werden aus funktionalen Beiträgen gefiltert, bleiben aber auf finalen `DeckEntry`-Rollen für Diagnose und Goldfish erhalten. Engine-Skalierung wird über denselben Decktyp bei längerem Horizont geprüft.
- **Änderungen:** Metadata-Filter in `contribution_from_knowledge`; Regressionstest; korrigierter Goldfish-Test.
- **Erfolg:** alle Tests und Fast grün; Buildermetriken unverändert; Produktionsdiagnose vorhanden; Goldfish bleibt bei der konservativen Messung.
- **Invarianten:** Benchmark 91, Material 33, Fehlpositive 0, Keepability/Planfähigkeit 77/76 %, andere Benchmarks unverändert.
- **Rollback:** Produktionsmarker fehlen im finalen Artefakt oder beeinflussen erneut Komposition/Benchmark.

### KGB-Entscheidung vor Push

Keine neue KGB. Der Hotfix bleibt bis CI- und Artefaktauswertung vorläufig.

### Priorisierter nächster ausführbarer Schritt

Den Hotfix-Workflow vollständig auswerten. Bei Grün die Full-Pool-Kapazität garantiert sofortiger und im Solitaire unbedingter wiederholbarer Produktion messen; erst danach die Value-Planrolle oder Kartenauswahl verändern.
