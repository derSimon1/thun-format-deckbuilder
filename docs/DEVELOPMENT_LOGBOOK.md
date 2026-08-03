# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte Development-System-v2-KGB existiert noch nicht.

- v2-Bootstrap: `31f6c1e053976435481c07ab2098430bc2a45471`, Run `30792560878`
- letzter Sideboard-Sicherungspunkt: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- letzter grüner Mill-Messstand: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- aktueller grüner Token-Diagnosestand: `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`, Run `30808101416`
- keine v2-KGB, da der Vergleich weiterhin `baseline: none` meldet und externe Club-/Meta-Evidenz fehlt

## Bisherige Meilensteine

| Bereich | Commit / Run | Ergebnis |
|---|---|---|
| 100 Starthände | `43fa53d…` / `30794553679` | reproduzierbare Einzelhände, Seed 1701 |
| Mana-Invariante | `5a040f9…` / `30795368803` | Manafehler nicht mehr planfähig |
| Control | `2ef72a0…` / `30797591719` | Benchmark 85, sechs Finisher |
| Sideboard | `937f10f…` / `30801497068` | Phrase-first, kein Graveyard-Hate gegen Aggro/Artifacts |
| Mill-Messung | `397d989…` / `30803643342` | 40 legale Quellen, Benchmark 80, 55 % planfähig |
| Token-Paketdiagnose | `6aa952f…` / `30808101416` | echte Paketbestandteile und 43 Rollen-Fehlpositive sichtbar |

## Vier-Stunden-Lauf – Token-Fokus

### Session-Snapshot

- Ausgangs-Head: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`
- PR #14: offen, Draft, mergeable
- Ausgangsrun: `30803643342`, erfolgreich
- Ausgangsartefakt: `global-calibration-pr-54`, ID `8851950460`
- Token-Plan: Aristocrats
- Benchmark 90
- Keepability/Planfähigkeit 73/73 %
- Strategy Commitment 100 %
- Engine Density 64 %
- Goldfish bis Zug 5: 66 % Killrate, 18,69 Schaden
- Matchups: 0 % Burn, 2 % Artifacts, 100 % Mill
- Mill-Kompositionsschritt bleibt als dokumentierter Rückkehrpunkt offen

## Token-Zyklus 1 – Paketdiagnose

### Ursache und Hypothese

Die globale Rollenlogik zählte jedes erzeugte Token als Material, jedes Vorkommen von `sacrifice` als Outlet-Nähe und Self-Death-Effekte als Aristocrats-Payoff. Eine zentrale Oracle-Text-Diagnose sollte echte Kreatur-Token, wiederholbare Creature-Sacrifice-Outlets und Other-Creature-Death-/Drain-Payoffs getrennt ausweisen.

### Commit und Workflow

- Commit: `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`
- Workflow: `30808101416`, erfolgreich
- Tests: 274 bestanden in 31,27 Sekunden
- Test-/Fast-/Diagnoseschritt: ungefähr 3 Minuten 58 Sekunden
- Artefakt: `global-calibration-pr-55`, ID `8853712704`, 47 Dateien, 62.043 Byte
- Benchmarks unverändert: Burn 83, Tokens 90, Artifacts 90, Control 85, Mill 80
- fünf Referenzarchetypen, sechs Matchups, 0 gemeldete Regressionen

### Fachliche Artefaktauswertung

| Metrik | Run 54 | Run 55 | Delta | Interpretation | Confidence |
|---|---:|---:|---:|---|---|
| echtes Kreatur-Token-Material | unbekannt | 14 | neu | nur ein Teil der 33 breiten Maker ist echtes Boardmaterial | hoch |
| echte wiederholbare Outlets | unbekannt | 9 | neu | drei Outlet-Kartennamen zu je drei Kopien | hoch |
| echte Death-/Drain-Payoffs | unbekannt | 3 | neu | Paket hängt vollständig von Relic Vial ab | hoch |
| Nichtkreatur-Token als Maker | unbekannt | 19 | neu | Food/Blood und ähnliche Tokens blähen Material auf | hoch |
| One-Shot-Sacrifice als Outlet | unbekannt | 23 | neu | zusätzliche Kosten und Self-Sacrifice blähen Outletdichte auf | hoch |
| breite Fehlpositive gesamt | unbekannt | 43 | neu | Commitment und Handklassifikation sind stark überzählt | hoch |

Das reale Deck besitzt zwar alle drei Aristocrats-Komponenten, aber nur drei Death-/Drain-Payoff-Kopien. Der legale Mono-White-Pool ist nicht der Engpass: 169 Kreatur-Token-Karten, 41 Multi-Maker, 20 wiederholbare Maker, 34 Outlets und 13 Death-Payoffs sind vorhanden.

### KGB-Entscheidung

Keine neue v2-KGB. Der Zyklus verbessert Messbarkeit, ändert aber noch keine Deckauswahl. Die bisherigen 100-%-Commitment- und 73-%-Planfähigkeitswerte sind fachlich nicht mehr belastbar.

### Reflexion

- Die Annahme „jedes Token ist Kampfmaterial“ ist widerlegt.
- Die Annahme „jedes sacrifice ist ein Outlet“ ist widerlegt.
- Alternative Erklärung für extreme Matchups bleibt ein vereinfachtes Combat-/Matchupmodell.
- Die Diagnose erkennt Copy-Token ohne das Wort `creature` möglicherweise zu konservativ; reale Deck- und Pooldaten müssen nach dem Rollenumbau erneut geprüft werden.
- Grüne CI bestätigt nur die Diagnose, nicht bessere Token-Decks.

## Token-Zyklus 2 – Präzise Planrollen und Komposition

### Ausgangs-Head

`6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`

### Zyklusvertrag

- **Ursache:** 43 breite Rollen-Fehlpositive steuern Planwahl, Komposition, Commitment, Handklassifikation und Goldfish.
- **Hypothese:** Token-spezifisch bereinigte Rollen und kapazitätsgeprüfte Planminimums erzeugen ein Deck, dessen deklarierter Plan tatsächlich erfüllt ist.
- **Änderungen:** präzise Tokenrollen; zentrale Planerkennung/Eligibility/Scoring; profilespezifische Mindestpakete.
- **Erwartung:** Nichtkreatur-Token und One-Shot-Sacrifices verlieren ihre planprägenden Rollen; der gewählte Plan erfüllt seine echten Paketminimums.
- **Invarianten:** legal 60/15, Seed 1701, Fast unter zehn Minuten, andere vier Benchmarks ohne unbegründete Regression.
- **Erfolg:** finales Diagnoseartefakt zeigt keine breiten Paket-Fehlpositive; Commitment und Hände verwenden die bereinigten Rollen; Token-Kohärenz steigt.
- **Rollback:** roter Lauf, nicht erfüllbare Mindestpakete oder schlechtere Planfähigkeit ohne belegten Kohärenzgewinn.
- **geschätzte Zeit:** 60–80 Minuten inklusive Workflow und Artefaktauswertung.

### Änderung vor Push

1. Neue Rollen `token_creature_maker`, `token_repeatable_maker`, `sacrifice_outlet`, `death_payoff`, `drain_payoff` und `token_value_payoff`.
2. Token-Planerkennung und Kandidatenpool verwenden die zentrale Paketdefinition; breite Fehlrollen werden in der Token-spezifischen Knowledge-Ansicht entfernt.
3. Go Wide, Value Tokens und Aristocrats erhalten anhand der gemessenen Poolkapazität eigene harte Planminimums.

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Der Commit bleibt bis vollständiger CI- und Artefaktauswertung vorläufig.

### Priorisierter nächster ausführbarer Schritt

Den neuen Workflow und insbesondere Deckliste, `token-packages.json`, 100 Hände, Commitment, Goldfish sowie die Matchups gegen Burn, Artifacts und Mill auswerten. Danach nur die durch Artefakte belegte nächste Ursache bearbeiten.
