# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, Tests/CI, Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte Development-System-v2-KGB existiert noch nicht.

### v2-Bootstrap-Vergleichsstand

- Commit: `31f6c1e053976435481c07ab2098430bc2a45471`
- Workflow: `30792560878`, erfolgreich
- Einschränkungen: Shrines statt Control, keine planabhängigen 100 Rohhände und `baseline: none`
- Status: technischer Vergleichsstand, keine v2-KGB

## Drei-Stunden-Lauf vom 2026-08-03 – Zyklusübersicht

| Zyklus | Commit | Workflow | Ergebnis |
|---|---|---|---|
| OpeningHandPlanReport | `43fa53d1766b05327eae5880bacb05905923f21c` | `30794553679` | 100 reproduzierbare Hände je Deck |
| Manafehler-Invariante | `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1` | `30795368803` | keine Manafehler-Hand mehr planfähig |
| Control-Integration | `380eba398fd27c30579f92da9c1d9d20372e626e` | `30796392816` | Validator grün, veralteter Test rot |
| Test-Hotfix | `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07` | `30796896850` | vollständiger grüner Control-Basislauf |
| Control-Finisher | `2ef72a092db8de4717ec1d474a380c0b2c0d63dc` | `30797591719` | Benchmark 72→85, Finisher 0→6 |
| Sideboard-Relevanz v1 | `f3ea0f48e5cdeac422a5bb29f6864fb203745c3d` | `30798351806` | CI grün, Artefakte fachlich falsch |
| Sideboard-Marker v2 | `84c82fc4a795b5d14ef30ecc7debd24f0cef4478` | `30799228495` | CI grün, Artefakte weiterhin fachlich falsch |

## Bestätigte globale Messwerte auf Run 48

- Tests: 261 bestanden in 31,29 Sekunden
- Test-/Fast-Schritt: 08:55:32 bis 08:59:18 UTC, ungefähr 3 Minuten 46 Sekunden
- Artefakt: `global-calibration-pr-48`, ID `8850209535`, 38 Dateien, 46.202 Byte
- Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill
- Benchmarks: Burn 83, Tokens 90, Artifacts 90, Control 85, Mill 78
- Matchups: sechs
- gemeldete Regressionen: null, weil weiterhin keine wiederhergestellte Vergleichsbaseline existiert
- Starthand-Seed: `1701`; je Referenzdeck exakt 100 Rohhände

## Run-48-Artefaktbefunde

### Control

- legal 60/15
- Benchmark 85
- Keepability 78 %
- Planfähigkeit 72 %
- Finisher-Zugang 53 %
- Manafehler 18 %, Farbfehler 4 %

### Mill

- Benchmark meldet 0 Mill-Quellen
- Builderliste enthält nur zwei Kopien `Weight of Memory` als klar erkennbare Millkarte
- Keepability 77 %, Planfähigkeit 0 %, marginal 100 %
- fehlender Enabler-/Payoff-/Finisher-Zugang jeweils 72 %
- 31 % tote oder widersprüchliche Hände
- der erzeugte Build ist faktisch überwiegend Dimir Draw/Counter/Removal und kein belastbares Milldeck

### Sideboard

Die Marker-Hypothese aus Zyklus 7 ist widerlegt. `best-of-three.json` enthält weiterhin:

- Control gegen Burn: 3 `Tormod's Crypt` hinein
- Control gegen Tokens: 3 `Tormod's Crypt` hinein
- Control gegen Artifacts: keine Control-Karten hinein

## Exakte Ursache

`SideboardBuilder` wertete pro Regel `phrase_match OR role_match` aus. `Tormod's Crypt` trifft zwar spezifisch die Phrase für `graveyard hate`, erhält durch die globale Kartentextanalyse aber zugleich die breite Rolle `removal`, weil der Text `exile` enthält. Dadurch wurde zusätzlich die Control-Regel `anti-aggro removal` getroffen und der Marker `sideboard_anti_aggro_removal` vergeben.

Der Marker wurde nicht verloren. Er war bereits bei der Erzeugung falsch mehrfach klassifiziert.

## Zyklus 8 – Phrase-first Sideboard-Klassifikation und Diagnoseartefakt

### Ausgangs-Head

`84c82fc4a795b5d14ef30ecc7debd24f0cef4478`

### Hypothese

Spezifische Oracle-Text-Phrasen müssen Vorrang vor breiten funktionalen Rollen haben. Rollen dürfen nur als Fallback dienen, wenn keine spezifische Sideboardregel per Text erkannt wurde.

### Änderungen

1. Sideboardregeln werden zweistufig ausgewertet: zuerst alle Phrasentreffer; nur ohne Phrasentreffer werden Rollen als Fallback verwendet.
2. Ein realitätsnaher Regressionstest erzeugt `Tormod's Crypt` mit automatisch erkannter Rolle `removal` und verbietet den zusätzlichen Anti-Aggro-Marker.
3. Der Fast-Validator schreibt pro Archetyp `<archetype>-sideboard.json` mit finalen Namen, Mengen, Scores, Gründen und Rollen. Dadurch kann die Klassifikation künftig direkt geprüft werden, ohne aus BO3-Plänen rückzuschließen.

### Validierung vor Commit

- kontrollierter Root-Cause-Test vorbereitet
- keine Kartennamen-Sperre im Produktionscode
- keine Benchmark-, Pass/Fail- oder Matchupschwelle verändert
- vollständige Testsuite, Fast-Lauf, Diagnoseartefakte und sechs BO3-Pläne müssen durch den neuen Workflow bestätigt werden

### KGB-Entscheidung vor Push

Keine neue v2-KGB.

### Kritische Reflexion

- Phrase-first kann Karten mit ungewöhnlichem Oracle-Wording übersehen; der Rollenfallback bleibt deshalb erhalten.
- Eine Karte kann legitim mehrere spezifische Phrasen treffen und mehrere Marker erhalten.
- Die Archetyp-Matrix bleibt eine Vereinfachung und prüft noch nicht das konkrete Gegnerdeck.
- Grüne CI genügt weiterhin nicht; die BO3-Karten-in-Pläne und neuen Sideboard-Diagnoseartefakte sind entscheidend.
- Zwei vorherige Sideboard-Hypothesen waren fachlich falsch. Unabhängig vom Ergebnis dieses Root-Cause-Fixes wird danach zum Mill-Punkt gewechselt, sofern keine technische Regression den Commit selbst blockiert.

### Priorisierter nächster ausführbarer Schritt

Nach vollständiger Workflow- und Artefaktauswertung die Mill-Komposition reparieren. Zuerst eine maschinenlesbare Mill-Quellenrolle beziehungsweise Mill-Dichte ableiten und anhand der realen Kartenpoolkapazität sicherstellen, dass die erzeugte Liste tatsächlich genügend Gegner-Mill-Quellen enthält. Keine bloße Benchmark-Schwellenwertsenkung.
