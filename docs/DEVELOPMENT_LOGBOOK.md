# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

Run 63 zeigte, dass der Mono-White-Pool nur drei mögliche Kopien einer automatisch wiederholbaren Tokenquelle besitzt. Deshalb wurde Value Tokens zugunsten des besser versorgten Go-Wide-Plans pausiert.

### Stabiler Bestätigungsstand

- Commit `2bd921c1688c72d4b5949bd0f93cb65a9d1d206c` beseitigte den Full-Pool-Test-Leak.
- Workflow `30824779542`, Run 69, wurde dreimal vollständig auf demselben Head ausgeführt.
- alle drei Durchgänge grün; jeweils 301 Tests, Fast-Validierung und Token-Diagnose erfolgreich.
- Artefakte: `8860492462`, `8860710216`, `8860887986`.
- Benchmarks: Burn 83, Tokens 96, Artifacts 90, Control 85, Mill 80.
- Go Wide: 36 Kreatur-Token-Maker, 25 sofortige Maker, 21 Multi-Maker, 6 Anthems.
- 100 Hände: Keepability 77 %, Planfähigkeit 77 %, Early Play T2/T3 94/96 %.
- Goldfish: 23,72 Schaden, 63 % Killrate, Board 9,30.
- Matchups: Burn 0 %, Artifacts 58 %, Mill 100 %.

## Aktueller Castability-Zyklus

- **Ursache:** Das bestätigte Deck enthält `Warping Wail` mit expliziter `{C}`-Anforderung, obwohl der aktuelle Mana-Builder ausschließlich farbige Standardländer erzeugt und 24 Plains ausgibt.
- **Hypothese:** Ein globales Eligibility-Gate für explizite `{C}`-Kosten verhindert unspielbare Deckeinträge, bis farblose Quellen als echte Manabasisfunktion unterstützt werden.
- **Änderungen:** generisches Candidate-Eligibility-Gate, Regressionstest, Logbook und Roadmap.
- **Erwartung:** `Warping Wail` verschwindet aus dem Token-Deck; alle fünf Archetypen bleiben legal und die Token-Planpflichtdichten bleiben erfüllt.
- **Invarianten:** keine Benchmarksenkung, Seed 1701, 60/15, Kopienlimit, Fast unter zehn Minuten.
- **Rollback:** Produktionspool kann 36 Spells nicht füllen, Token-Benchmark fällt unbegründet oder ein anderer Archetyp regressiert.
- **KGB-Entscheidung vor Push:** keine neue KGB.

## Nächster ausführbarer Schritt

Castability-Gate veröffentlichen und das neue Artefakt gegen Run 69 auswerten. Bei grünem Gate anschließend die tatsächliche Go-Wide-Kartenauswahl anhand garantierter Tokenproduktion, Anthems, Kurve und Burn-Matchup optimieren.
