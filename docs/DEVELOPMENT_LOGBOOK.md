# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte Development-System-v2-KGB existiert noch nicht.

- v2-Bootstrap-Vergleichsstand: Commit `31f6c1e053976435481c07ab2098430bc2a45471`, Run `30792560878`
- aktueller technischer Sicherungspunkt: Commit `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- der aktuelle Sicherungspunkt ist keine v2-KGB, weil der Vergleich weiterhin `baseline: none` meldet und Mill keinen belastbaren Hauptplan besitzt

## Laufübersicht 2026-08-03

| Zyklus | Commit | Workflow | Kernergebnis |
|---|---|---|---|
| OpeningHandPlanReport | `43fa53d1766b05327eae5880bacb05905923f21c` | `30794553679` | 100 reproduzierbare Hände je Deck |
| Manafehler-Invariante | `5a040f9db39b740d1f1cb72bfcfdb221fcd061d1` | `30795368803` | Manafehler-Hände nicht mehr planfähig |
| Control-Integration | `380eba398fd27c30579f92da9c1d9d20372e626e` | `30796392816` | Control integriert; alter Test rot |
| Control-Basis | `9c4426e8bcdd8177d5cce3722484b2d9ceec3b07` | `30796896850` | grüner Control-Basislauf |
| Control-Finisher | `2ef72a092db8de4717ec1d474a380c0b2c0d63dc` | `30797591719` | Benchmark 72→85, Finisher 0→6 |
| Sideboard-Relevanz v1 | `f3ea0f48e5cdeac422a5bb29f6864fb203745c3d` | `30798351806` | technisch grün, fachlich widerlegt |
| Sideboard-Marker v2 | `84c82fc4a795b5d14ef30ecc7debd24f0cef4478` | `30799228495` | technisch grün, falsche BO3-Pläne |
| Phrase-first + Diagnose | `3e6b23067d5811f12b0f6dae2325fb777776d5df` | `30800668838` | Produktion fachlich korrekt, Testannahme rot |
| Test-Invariante | `937f10f699814e271dd7f8b11b874b0a8f64270c` | `30801497068` | vollständiger grüner Sideboard-Abschluss |

## Abgeschlossener Sideboard-Zyklus – Run 50

### Technische Validierung

- Workflow: `30801497068`, erfolgreich
- Tests: 262 bestanden in 31,82 Sekunden
- Test-/Fast-Schritt: ungefähr 3 Minuten 44 Sekunden
- Artefakt: `global-calibration-pr-50`, ID `8851073096`, 43 Dateien, 50.063 Byte
- fünf Referenzarchetypen
- sechs priorisierte Matchups
- Benchmarks: Burn 83, Tokens 90, Artifacts 90, Control 85, Mill 78
- Seed `1701`, je Deck exakt 100 Hände

### Fachliche Artefaktprüfung

- Control gegen Burn: 3 Disfigure hinein
- Control gegen Tokens: 3 Disfigure hinein
- Control gegen Artifacts: keine ungeeignete Karte hinein
- kein `Tormod's Crypt` gegen Burn, Tokens oder Artifacts
- `control-sideboard.json` enthält finale Mengen, Scores, Gründe und Rollenmarker
- Sideboard-Diagnoseartefakte liegen für alle fünf Referenzarchetypen vor

### Ergebnis

Phrase-first-Klassifikation ist als globale Regel bestätigt. Spezifische Oracle-Text-Phrasen werden vor breiten Rollen ausgewertet; Rollen bleiben Fallback. Der Regressionstest injiziert die breite Rolle bewusst und prüft nur die relevante Invariante.

### KGB-Entscheidung

Keine neue v2-KGB.

Begründung:

- `baseline: none` besteht fort
- Mill hat weiterhin 0 % planfähige Hände
- Sideboard-Relevanz wird noch über Archetyp-Matrix statt konkretes Gegnerdeck bestimmt

### Reflexion

- Zwei grüne Sideboard-Runs waren fachlich falsch; erst maschinenlesbare Artefakte und eine Root-Cause-Invariante schlossen die Ursache.
- Direkte Diagnoseartefakte sind wirksamer als Rückschlüsse aus aggregierten BO3-Werten.
- Phrase-first kann ungewöhnliche Kartentexte übersehen; der Rollenfallback bleibt notwendig.
- Weitere Sideboard-Kalibrierung wird pausiert, solange keine neue Evidenz eine konkrete andere Ursache zeigt.

## Prozesszyklus – Global Calibration Prompt 2.1

### Ziel

Den nächsten Drei-Stunden-Lauf produktiver machen: weniger wiederholte Statusprüfung, früherer Artefaktvergleich, verbindliche Abschlussreserve und ein klar begrenztes Mill-Ziel.

### Änderungen

1. Einmaliger Session-Snapshot statt vollständigem Neustart vor jedem Zyklus.
2. Echtes 180-Minuten-Budget: maximal 20 Minuten Start, bis zu 120 Minuten produktive Zyklen einschließlich Fallback, mindestens 30 Minuten Abschluss und 10 Minuten Puffer.
3. Artifact-first-Evidenztabelle mit vorher/nachher/Delta/Interpretation/Confidence.
4. Zyklusvertrag vor Code: Ursache, Hypothese, Metriken, Invarianten, Erfolg, Abbruch und Zeitschätzung.
5. Connector-only-Regel: Commit bleibt bis vollständiger CI- und Artefaktauswertung vorläufig.
6. Schleifenschutz: keine dritte Variante derselben gescheiterten Heuristik ohne neue Root-Cause-Evidenz.
7. Mill-Komposition wird das einzige primäre Entwicklungsziel des nächsten Drei-Stunden-Laufs.

### Erwarteter Nutzen

- weniger identische CI-Abfragen
- keine neuen Zyklen ohne ausreichenden Abschluss- und Workflowpuffer
- fachliche Fehler werden über Artefakte früher erkannt
- klarere Ursache-Wirkungs-Zuordnung je Commit
- mehr Zeit für echte Deckqualität statt Prozesswiederholung

### KGB-Entscheidung

Keine neue v2-KGB. Der Prozess verbessert Reproduzierbarkeit und Sicherheit, verändert aber noch keine Mill-Qualität und stellt keine Regression-Baseline wieder her.

## Priorisierter nächster ausführbarer Schritt

Die Mill-Komposition reparieren. Eine zentrale Definition für Gegner-Mill-Quellen einführen, die reale Kartenpoolkapazität messen und erst danach eine kapazitätsgeprüfte Mindestdichte festlegen. Komposition, Optimierer, Benchmark und 100-Hand-Analyse müssen dieselbe Definition verwenden. Keine Schwellenwertsenkung nur zum Bestehen.
