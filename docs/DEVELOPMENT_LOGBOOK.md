# Development Logbook

Detaillierte frühere Einträge bleiben über die Git-Historie erhalten. Ab Development System v2.0 dokumentiert jeder Zyklus Ausgangs-Head, Vergleichsstand, Hypothese, Änderungen, Tests/CI, 100-Hand-Seed, KGB-Entscheidung, Reflexion und genau einen nächsten Schritt.

## KGB-Status

### Voll qualifizierte v2-KGB

Noch nicht vorhanden.

### v2-Bootstrap-Vergleichsstand

- Commit `31f6c1e053976435481c07ab2098430bc2a45471`
- Run `30792560878`, erfolgreich
- 240 Tests; Fast ungefähr 3:36 Minuten
- noch Shrines statt Control, `baseline: none`, keine 100 planabhängigen Rohhände
- keine v2-KGB

### Legacy-Kandidat

- Commit `3fa9b104d8e38a260ab1240df97bec206a17a1df`
- Run `30762470833`, erfolgreich
- historischer Wiederanlaufpunkt, keine v2-KGB

## Historische Kernlektionen

- Rollenpunkte allein erzeugen keine kohärenten Decks.
- Token-Pläne müssen vor Kartenauswahl unterschieden werden.
- Harte Mindestwerte erst nach Kapazitätsprüfung.
- Strategy Commitment trennt neutrale Interaktion von Planbruch.
- Engine Density trennt wiederholbare Engines von einmaligem Material.
- GitHub Actions ist Validator, nicht Entwicklungsagent.
- Grüne CI beweist keine spielerische Qualität.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 1: OpeningHandPlanReport

- Ausgangs-Head: `31f6c1e053976435481c07ab2098430bc2a45471`
- Commit: `43fa53d1766b05327eae5880bacb05905923f21c`
- Run: `30794553679`, erfolgreich
- Tests: 250 bestanden in 23,49 Sekunden
- Fast: ungefähr 2:51 Minuten
- Artefakt: `8848391256`, 38 Dateien
- Seed: `1701`, exakt 100 Hände je erzeugtem Deck
- Ergebnis: deterministische Rohhände, Deck-Hash, Manaquellen, T1/T2/T3, Rollen-Zugänge, Planfähigkeitsklassen
- Befund: Manafehler konnten fälschlich planfähig sein
- KGB: keine neue v2-KGB

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 2: Manafehler-Invariante

- Ausgangs-Head: `43fa53d1766b05327eae5880bacb05905923f21c`
- Commit: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Run: `30795368803`, erfolgreich
- Tests: 251 bestanden in 23,30 Sekunden
- Fast: ungefähr 2:50 Minuten
- Artefakt: `8848730571`, 38 Dateien
- 500 Rohhände geprüft; 0 Fälle `mana_error` plus `planfaehig`
- Burn: Keepability/Planfähigkeit 78/78 %
- Tokens/Aristocrats: 73/73 %
- Artifacts: 71/70 %
- Mill: 77/0 %, marginal 100 %
- KGB: keine neue v2-KGB; Control fehlte noch

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 3: Control-Referenzarchetyp

### Ausgangs-Head und Hypothese

- Ausgangs-Head: `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1`
- Hypothese: Dimir Control mit günstigen Countern, Removal, Sweepern, Kartenvorteil und wenigen Finishers ist ein allgemeinerer Referenzfall als Shrines.

### Änderungen

1. Control-Scoring, Dimir-Profil, Sideboardregeln und Deckbuilderregistrierung.
2. Control-Benchmark und v2-Validator für Burn, Tokens, Artifacts, Control und Mill; sechs Fast-Matchups.
3. Tests für Scoring, Farbpflicht und Benchmark.

### Commit und Run 44

- Commit: `380eba398fd27c30579f92da9c1d9d20372e626e`
- Run: `30796392816`, rot
- Tests: 256 bestanden, 1 fehlgeschlagen in 30,50 Sekunden
- Fast-Validierung selbst: PASS
- Referenzarchetypen: 5
- Matchups: 6
- Regressionen: 0
- Benchmark: Burn 83, Tokens 90, Artifacts 90, Control 72, Mill 78
- Test-/Fast-Schritt: 08:11:08 bis 08:14:29, ungefähr 3:20 Minuten
- Artefakt: `8849106044`, 38 Dateien, 46.851 Byte

### Belegte Fehlerursache

Der bestehende Test `test_generate_deck_rejects_unknown_archetype` verwendete `control` als absichtlich unbekannten Archetyp. Nach der registrierten Control-Strategie ist diese Testannahme veraltet. Der Produktionscode erreichte korrekt die Control-Farbprüfung; der Test erwartete fälschlich weiterhin `Unbekannter Archetyp`.

### Control-Artefakte aus Run 44

- legales Mainboard/Sideboard: 60/15
- Farben: U/B
- Benchmark: 72
- Control-Antworten: 33 Kopien
- Control-Finisher: 0 Kopien
- Keepability: 73 %
- Planfähigkeit: 68 %
- marginal: 32 %
- Early Play bis T2/T3: 79/87 %
- Manafehler: 19 %
- Farbfehler: 5 %
- fehlender Finisher-Zugang: 100 %
- 0 Hände verletzen die Manafehler-Invariante
- Goldfish: 0 % Killrate; durchschnittlich 5,13 Spells, 4,13 ungenutztes Mana

### KGB-Entscheidung

Keine neue v2-KGB. Der Run ist rot und das Control-Deck kann die Partie nicht beenden.

### Confidence und Reflexion

- hoch für die konkrete Testursache
- hoch dafür, dass Control technisch generiert wird
- mittel für Interaktionsqualität
- hoch dafür, dass Finish Density aktuell fehlt
- alternative Erklärung für Benchmark 72: Antwort- und Card-Draw-Dichte überdecken die fehlende Wincondition
- grüne Validierung allein hätte dieses spielerische Problem nicht verhindert
- Dimir ist nur ein Control-Referenzfall; matchupabhängige Totkarten bleiben ungemessen

### Nächster Schritt

Den veralteten Unknown-Archetype-Test auf einen tatsächlich unbekannten Namen umstellen. Danach den grünen Control-Basislauf auswerten und in einem getrennten Zyklus die belegte fehlende Finisher-Dichte beheben.

## 2026-08-03 – Drei-Stunden-Lauf, Zyklus 4: Veralteter Unknown-Archetype-Test

### Ziel und Hypothese

Nur die durch Run 44 belegte Testannahme korrigieren. `combo` bleibt unbekannt und prüft weiterhin denselben Fehlerpfad, während `control` nun bewusst unterstützt wird.

### Ausgangs-Head

`380eba398fd27c30579f92da9c1d9d20372e626e`

### Änderung

- `test_generate_deck_rejects_unknown_archetype` verwendet `combo` statt `control`.

### Validierung vor Commit

- Run 44 belegt: 256 andere Tests bestanden; Control-Validierung PASS; nur dieser Test ist rot.
- keine Produktionsschwelle oder Control-Regel geändert
- vollständige Suite und Fast-Validierung durch neuen PR-Workflow zu bestätigen

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Der nächste Run muss grün sein; anschließend bleibt Finish Density als belegter Control-Blocker.

### Kritische Reflexion

- Annahme: `combo` bleibt absichtlich nicht unterstützt; dies ist derzeit durch STRATEGIES belegt.
- Alternative Erklärung: Der alte Test war nicht nur stale, sondern dokumentierte eine frühere Produktgrenze. Die neue Control-Entscheidung ersetzt diese Grenze ausdrücklich.
- Overfitting: keine fachliche Heuristik verändert.
- mögliche Regression: Fehlermeldungspfad bleibt identisch für tatsächlich unbekannte Archetypen.

### Priorisierter nächster ausführbarer Schritt

Run nach dem Test-Hotfix vollständig auswerten. Bei Grün die Control-Finisher-Lücke mit einer kapazitätsgeprüften Kompositionsregel lösen; nicht lediglich den Benchmark-Grenzwert senken.
