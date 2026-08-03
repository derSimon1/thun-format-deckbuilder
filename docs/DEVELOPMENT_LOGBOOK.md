# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte Development-System-v2-KGB existiert noch nicht.

- v2-Bootstrap-Vergleichsstand: Commit `31f6c1e053976435481c07ab2098430bc2a45471`, Run `30792560878`
- Einschränkungen des Bootstrap-Stands: Shrines statt Control, keine planabhängigen 100 Rohhände, `baseline: none`
- aktueller Status: technische Vergleichsstände vorhanden, aber noch keine belastbare v2-KGB

## Laufübersicht 2026-08-03

| Zyklus | Commit | Workflow | Kernergebnis |
|---|---|---|---|
| OpeningHandPlanReport | `43fa53d1766b05327eae5880bacb05905923f21c` | `30794553679` | 100 reproduzierbare Hände je Deck |
| Manafehler-Invariante | `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1` | `30795368803` | Manafehler-Hände nicht mehr planfähig |
| Control-Integration | `380eba398fd27c30579f92da9c1d9d20372e626e` | `30796392816` | Control technisch integriert; alter Test rot |
| Control-Basis | `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07` | `30796896850` | vollständiger grüner Control-Lauf |
| Control-Finisher | `2ef72a092db8de4717ec1d474a380c0b2c0d63dc` | `30797591719` | Benchmark 72→85, Finisher 0→6 |
| Sideboard-Relevanz v1 | `f3ea0f48e5cdeac422a5bb29f6864fb203745c3d` | `30798351806` | technisch grün, fachlich widerlegt |
| Sideboard-Marker v2 | `84c82fc4a795b5d14ef30ecc7debd24f0cef4478` | `30799228495` | technisch grün, weiterhin falsche BO3-Pläne |
| Phrase-first und Diagnose | `3e6b23067d5811f12b0f6dae2325fb777776d5df` | `30800668838` | Fast fachlich erfolgreich; neuer Test mit falscher Annahme rot |

## Referenzstand Run 48

- 261 Tests bestanden
- Fast-Lauf ungefähr 3 Minuten 46 Sekunden
- fünf Referenzarchetypen und sechs Matchups
- Benchmarks: Burn 83, Tokens 90, Artifacts 90, Control 85, Mill 78
- Seed `1701`, exakt 100 Hände je Deck
- keine wiederhergestellte Regression-Baseline

### Control

- legal 60/15
- Keepability 78 %, Planfähigkeit 72 %
- Finisher-Zugang 53 %
- Manafehler 18 %, Farbfehler 4 %

### Mill

- Benchmark meldet 0 Mill-Quellen
- finales Mainboard enthält nur zwei klar erkennbare Millkarten
- Keepability 77 %, Planfähigkeit 0 %, marginal 100 %
- fehlender Enabler-, Payoff- und Finisher-Zugang jeweils 72 %
- 31 % tote oder widersprüchliche Hände
- aktueller Build ist überwiegend Dimir Draw/Counter/Removal und kein belastbares Milldeck

## Zyklus 8 – Phrase-first Sideboard-Klassifikation

### Ausgangs-Head

`84c82fc4a795b5d14ef30ecc7debd24f0cef4478`

### Hypothese

Spezifische Oracle-Text-Phrasen müssen Vorrang vor breiten funktionalen Rollen haben. Rollen werden nur verwendet, wenn keine spezifische Sideboardregel per Text erkannt wurde.

### Änderungen

1. zweistufige Sideboard-Klassifikation: Phrasentreffer zuerst, Rollen nur als Fallback
2. Regressionstest für eine spezifische Graveyard-Phrase bei gleichzeitig vorhandener breiter Rolle
3. neues Diagnoseartefakt `<archetype>-sideboard.json` mit finalen Namen, Mengen, Scores, Gründen und Rollen

### Run 49

- Commit: `3e6b23067d5811f12b0f6dae2325fb777776d5df`
- Workflow: `30800668838`
- Fast-Validierung: erfolgreich
- Tests: 261 bestanden, 1 fehlgeschlagen
- Artefakt: `global-calibration-pr-49`, ID `8850773679`, 43 Dateien, 50.535 Byte
- Benchmarks unverändert: 83 / 90 / 90 / 85 / 78

### Fachliche Artefaktauswertung

Die Produktionsänderung funktioniert:

- Control-Sideboard enthält Disfigure, Stab, Tragic Trajectory, Desert's Due und Final Flourish
- finale Marker sind Anti-Aggro-Removal beziehungsweise Creature-Sweeper
- Control gegen Burn: 3 Disfigure hinein
- Control gegen Tokens: 3 Disfigure hinein
- Control gegen Artifacts: keine ungeeignete Karte hinein
- kein `Tormod's Crypt` gegen Burn, Tokens oder Artifacts

### Korrektur der Root-Cause-Dokumentation

Die vorherige Aussage, die automatische Rollenerkennung müsse `Tormod's Crypt` zwingend als `removal` klassifizieren, war zu stark. Der neue Test zeigte für die verwendete Fixture nur `sacrifice`.

Belegt ist dagegen:

- die alte Kombination `phrase_match OR role_match` erlaubte spezifischen Karten zusätzliche breite Kategorien, sobald eine breite Rolle vorhanden war
- Phrase-first verhindert diese Klasse von Doppelklassifikationen
- der Regressionstest muss die breite Rolle gezielt injizieren, statt eine bestimmte aktuelle Rollenerkennung vorauszusetzen

### KGB-Entscheidung

Keine neue v2-KGB. Run 49 ist wegen einer falschen Testannahme rot; außerdem bleibt `baseline: none` bestehen.

### Reflexion

- Die Produktionshypothese ist durch reale Artefakte bestätigt.
- Die Testhypothese war überangepasst an eine angenommene interne Rolle.
- Direkte Sideboard-Diagnoseartefakte waren entscheidend und sollen erhalten bleiben.
- Die Archetyp-Matrix ersetzt weiterhin keine Analyse des konkreten Gegnerdecks.
- Nach Abschluss des Test-Hotfixes wird Sideboard-Kalibrierung pausiert und zu Mill gewechselt.

## Zyklus 9 – Testannahme an belegte Invariante anpassen

### Ausgangs-Head

`3e6b23067d5811f12b0f6dae2325fb777776d5df`

### Änderung

Der Regressionstest injiziert ausdrücklich eine breite Rolle `removal` zusammen mit einer spezifischen Graveyard-Hate-Phrase. Geprüft wird ausschließlich die relevante Invariante: spezifischer Phrasentreffer erzeugt nur `sideboard_graveyard_hate` und keinen Anti-Aggro-Marker.

### Erwartete Validierung

- vollständige Testsuite grün
- Fast-Validierung grün
- Run-49-Sideboardpläne bleiben unverändert korrekt
- neue Sideboard-Diagnoseartefakte bleiben vorhanden

### KGB-Entscheidung vor Push

Keine neue v2-KGB bis zum grünen Workflow und zur Artefaktprüfung.

### Priorisierter nächster ausführbarer Schritt

Die Mill-Komposition reparieren: Gegner-Mill-Quellen maschinenlesbar erkennen, Kartenpoolkapazität bestimmen und eine kapazitätsgeprüfte Mindestdichte in Komposition, Optimierer, Benchmark und 100-Hand-Analyse konsistent durchsetzen.
