# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. Der Vergleich meldet weiterhin `baseline: none`; externe Club-/Meta-Evidenz fehlt.

Aktuelle Sicherungspunkte:

- Sideboard: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- Mill-Messung: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- Token-Diagnose: `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`, Run `30808101416`

## Vier-Stunden-Lauf – Token-Fokus

### Ausgangsstand Run 54

- Plan Aristocrats
- Benchmark 90
- Keepability/Planfähigkeit 73/73 %
- Commitment 100 %, Engine Density 64 %
- Goldfish 18,69 Schaden, 66 % Killrate bis Zug 5
- Matchups: 0 % Burn, 2 % Artifacts, 100 % Mill

## Token-Zyklus 1 – Paketdiagnose

### Commit und Workflow

- Commit `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`
- Run `30808101416`, erfolgreich
- 274 Tests in 31,27 Sekunden
- Fast-/Diagnoseschritt insgesamt ungefähr 3:58 Minuten
- Artefakt `global-calibration-pr-55`, ID `8853712704`, 47 Dateien
- Benchmarks: Burn 83, Tokens 90, Artifacts 90, Control 85, Mill 80

### Evidenz

| Paketmetrik | Run 55 |
|---|---:|
| echtes Kreatur-Token-Material | 14 |
| echte wiederholbare Outlets | 9 |
| Death-/Drain-Payoffs | 3 |
| Nichtkreatur-Token fälschlich als Material | 19 |
| One-Shot-Sacrifice fälschlich als Outlet | 23 |
| breite Rollen-Fehlpositive gesamt | 43 |

Der reale Pool ist nicht knapp: 169 Kreatur-Token-Karten, 41 Multi-Maker, 20 wiederholbare Maker, 34 Outlets und 13 Death-Payoffs.

### Entscheidung

Hypothese bestätigt. Keine neue KGB: Der Zyklus verbesserte Messbarkeit, nicht die Builderausgabe.

## Token-Zyklus 2 – Präzise Planrollen und Komposition

### Commit und Run 56

- Commit `676da07f56abc55651c2d1e1cb25b423ba1a6088`
- Run `30809079933`, rot
- Tests: 274 bestanden, 5 fehlgeschlagen
- Fast-Validierung selbst: PASS
- Artefakt `global-calibration-pr-56`, ID `8854099893`, 47 Dateien
- Laufzeit des Test-/Fast-/Diagnoseschritts: ungefähr 4:02 Minuten

### Produktionsartefakt trotz rotem Testgate

Der vollständige Pool erzeugte erfolgreich ein neues Value-Tokens-Deck:

- Benchmark 90 → 91
- Plan Aristocrats → Value Tokens
- 33 echte Materialkopien
- 12 wiederholbare Maker
- 0 breite Rollen-Fehlpositive
- Keepability 73 → 77 %
- Planfähigkeit 73 → 76 %
- Goldfish-Schaden 18,69 → 18,97
- Killrate unverändert 66 %
- Artifacts-Matchup 2 → 7 %
- Burn unverändert 0 %, Mill unverändert 100 %
- Commitment weiterhin 100 %
- Engine Density 64 → 33 %, nun 12 echte wiederholbare Maker statt breite Sacrifice-„Engines“

Deckkern: 33 Kreatur-Token-Maker, 24 Kreaturen, 13 Multi-Maker, 3 Anthems, 5 Removal. `token_value_payoff` ist noch 0/4 und wird als offene Rolle gewarnt.

### Belegte rote Ursache

Kleine Testdatenbanken enthalten nach präziser Eligibility nur 33 verfügbare Kopien. Die statischen Produktionsminimums werden nicht gegen den tatsächlich übergebenen Pool geprüft. Die Kompositionsengine bleibt deshalb drei Slots vor Deckende ohne zulässigen Kandidaten. Im vollständigen Pool sind alle Minimums erfüllbar.

### KGB-Entscheidung

Regression festgestellt: rotes Testgate. Der Produktionsbefund ist fachlich vielversprechend, darf aber nicht als neuer Sicherungspunkt gelten.

### Reflexion

- Die Hypothese zur Rollenbereinigung ist bestätigt.
- Die Annahme, Full-Pool-Kapazität gelte für jede Test-/Sparse-Datenbank, ist falsch.
- Schwellenwerte werden nicht global gesenkt; sie müssen poolabhängig begrenzt werden.
- Value Tokens besitzt noch keinen erkannten direkten Value-Payoff. Die Planwahl beruht auf wiederholbaren Makern und Card Draw.
- Goldfish bleibt pauschal und zählt nicht die tatsächliche Tokenmenge je Karte.
- Extreme Matchups zeigen weiterhin Simulationsgrenzen.

## Token-Hotfix – Poolabhängige Mindestwerte

### Zyklusvertrag

- **Ursache:** unerreichbare harte Minimums und nur 33 planrelevante Kopien im Sparse-Pool.
- **Hypothese:** Kapazitätsprüfung je Candidate-Pool plus niedrig priorisierte kleine Kreaturen als Füllmaterial stellt Sparse-Pool-Fähigkeit wieder her, ohne Full-Pool-Ziele anzutasten.
- **Änderungen:** `capacity_checked_token_profile`; getrennte Plan- und Composition-Pools; neutrale Kreaturen nur als Fallback.
- **Erfolg:** alle Tests und Fast grün; Full-Pool-Value-Deck behält 33 Material- und mindestens 6 wiederholbare Maker-Kopien; 0 Fehlpositive.
- **Invarianten:** keine Benchmarksenkung, keine Änderung der Produktionsziele bei ausreichender Kapazität.
- **Rollback:** Full-Pool-Pflichtrollen oder Kohärenz gehen verloren.

### KGB-Entscheidung vor Push

Keine neue KGB. Der Hotfix ist bis CI-/Artefaktauswertung vorläufig.

### Priorisierter nächster ausführbarer Schritt

Hotfix-Workflow auswerten. Bei Grün anschließend den fehlenden `token_value_payoff` und die tatsächliche Tokenzahl im Goldfish als zwei getrennte mögliche Ursachen nach Qualitätsgewinn vergleichen.
