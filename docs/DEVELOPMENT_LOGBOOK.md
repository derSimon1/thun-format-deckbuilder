# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort; externe Club-/Meta-Evidenz fehlt.

Aktuelle Sicherungspunkte:

- Sideboard: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- Mill-Messung: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- Token-Builder: `1a4618ed3eaed910632eba526b550d8abf9ed905`, Run `30810553137`
- Token-Produktion: `e246e8d86b0872aec05232d43b9ea87c57f77ae6`, Run `30812706366`

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
- Artefakt `8853712704`
- echtes Material 14, Outlets 9, Death-/Drain-Payoffs 3
- 43 breite Rollen-Fehlpositive
- Full-Pool-Kapazität für alle drei Token-Pakete ausreichend
- Hypothese bestätigt; keine neue KGB

## Token-Zyklus 2 – Präzise Planrollen und Komposition

- Commit `676da07f56abc55651c2d1e1cb25b423ba1a6088`, Run 56 rot wegen Sparse-Pool-Tests; Full-Pool fachlich erfolgreich
- Runs 57/58 beheben Sparse-Pool-Ziele und begrenzen Füller auf echte Kopienlücken
- finaler grüner Builder-Stand Run `30810553137`, Artefakt `8854683264`

| Metrik | Run 55 | Run 58 | Delta |
|---|---:|---:|---:|
| Plan | Aristocrats | Value Tokens | geändert |
| Benchmark | 90 | 91 | +1 |
| echtes Material | 14 | 33 | +19 |
| nominell wiederholbare Maker | 0 | 12 | +12 |
| Rollen-Fehlpositive | 43 | 0 | -43 |
| Keepability | 73 % | 77 % | +4 pp |
| Planfähigkeit | 73 % | 76 % | +3 pp |
| bisheriger Goldfish-Schaden | 18,69 | 18,97 | +0,28 |
| bisherige Killrate | 66 % | 66 % | 0 |

## Token-Zyklus 3 – Produktionsmodi und Goldfish

### Run 59 – rotes Integrationsgate

- Commit `3863d851efbf5704f84ce29b6897d638bb5d0bb9`
- Run `30811810037`, rot
- 292 Tests bestanden, 1 Test fehlgeschlagen; Fast selbst PASS
- Produktionsmetadaten wurden fälschlich als Funktionsrollen normalisiert
- ein Test erwartete einen ungeeigneten Fünf-Züge-Vergleich für wiederholbare Engines
- Messhypothese bestätigt, technisches Gate rot

### Run 60 – erfolgreicher Produktionsmeilenstein

- Commit `e246e8d86b0872aec05232d43b9ea87c57f77ae6`
- Workflow `30812706366`, erfolgreich
- 295 Tests bestanden in 49,55 Sekunden
- Test-/Fast-/Diagnoseschritt ungefähr 4 Minuten 10 Sekunden
- Artefakt `global-calibration-pr-60`, ID `8855522460`, 47 Dateien, 63.190 Byte
- Benchmarks unverändert: Burn 83, Tokens 91, Artifacts 90, Control 85, Mill 80
- fünf Archetypen, sechs Matchups, 0 gemeldete Regressionen
- Builderprofil, Deck-Hash und 100 Hände gegenüber Run 58 unverändert

### Produktionsartefakt Run 60

| Produktionsmodus | Kopien im Mainboard |
|---|---:|
| garantiert sofort | 4 |
| unbedingte wiederholbare Engine | 0 |
| bedingt | 21 |
| Death-Trigger | 8 |

- garantierte sofortige Mindestproduktion über alle Deckkopien: 8 Tokens
- Goldfish-Schaden: 14,66 statt zuvor pauschal 18,97
- Killrate bis Zug 5: 27 % statt 66 %
- durchschnittliche Tokenboardgröße: 5,30
- aktive unbedingte Engines: 0,00
- durchschnittlich 4,50 gewirkte Spells und 4,58 ungenutztes Mana
- Keepability/Planfähigkeit weiterhin 77/76 %

Die niedrigeren Werte sind eine Messkorrektur, keine Builderregression. Die aktuelle Rolle `token_repeatable_maker` ist dennoch fachlich zu breit: zwölf nominelle Maker entsprechen im konservativen Produktionsmodell keiner einzigen unbedingten Engine.

### KGB-Entscheidung

Keine neue v2-KGB. Run 60 ist ein grüner technischer Token-Sicherungspunkt, aber die automatische Value-Planwahl beruht noch auf einer zu breiten Repeatable-Definition.

### Reflexion

- Produktionsmetadaten müssen auf finalen DeckEntries sichtbar bleiben, dürfen aber keine funktionalen Kompositionsrollen sein.
- Bedingte Trigger können im echten Spiel wertvoll sein, sind aber keine garantierten Goldfish-Engines.
- Die korrigierte Killrate darf nicht durch ein lockeres Simulationsmodell angehoben werden.
- Vor einer Rollen- oder Planänderung fehlt die Poolkapazität je Produktionsmodus.
- Grüne CI bestätigt Messkonsistenz, nicht automatisch die optimale Token-Kartenauswahl.

## Token-Zyklus 4 – Produktionskapazität des Mono-White-Pools

### Zyklusvertrag

- **Ursache:** Das Deck besitzt 0 unbedingte Engines, aber der Builder meldet 12 `token_repeatable_maker`; die verfügbare echte Produktionskapazität ist unbekannt.
- **Hypothese:** Eine deduplizierte Poolmessung zeigt, ob Mono-White genügend garantierte Sofort- oder unbedingte wiederholbare Quellen für Value Tokens besitzt.
- **Änderungen:** zentrale Kapazitätsfunktion; Diagnoseartefakt; Regressionstest.
- **Erwartete Metriken:** unterschiedliche Karten, maximale Kopien und konservative Mindestoutput-Kapazität je Immediate/Repeatable/Conditional/Death-Modus.
- **Invarianten:** keine Kartenauswahl; Benchmark 91, Material 33, Starthände 77/76 %, Goldfishwerte und andere Archetypen unverändert.
- **Erfolg:** `token-packages.json` enthält vollständige Mono-White-Poolkapazität je Modus.
- **Abbruch:** Builderausgabe oder andere Benchmarks ändern sich.
- **geschätzte Zeit:** 35–50 Minuten inklusive Workflow und Artefaktauswertung.

### KGB-Entscheidung vor Push

Keine neue KGB. Dieser Zyklus misst nur die Voraussetzung für eine spätere Rollenänderung.

### Priorisierter nächster ausführbarer Schritt

Den Kapazitätsworkflow auswerten. Bei mindestens sechs unbedingten Engine-Kopien `token_repeatable_maker` auf den Repeatable-Modus begrenzen und Value Tokens kapazitätsgeprüft neu bauen. Andernfalls die automatische Planwahl auf den bestversorgten garantierten Plan umstellen.
