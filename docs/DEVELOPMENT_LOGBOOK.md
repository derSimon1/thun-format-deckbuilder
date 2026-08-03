# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte Development-System-v2-KGB existiert noch nicht.

- v2-Bootstrap-Vergleichsstand: Commit `31f6c1e053976435481c07ab2098430bc2a45471`, Run `30792560878`
- letzter vollständig dokumentierter technischer Sicherungspunkt: Commit `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- aktueller grüner Messstand: Commit `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- keiner dieser Stände ist eine v2-KGB, weil der Vergleich weiterhin `baseline: none` meldet und externe Club-/Meta-Evidenz fehlt

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
| Mill-Definition | `70f538ce52593e4ab7485f59bf801081cc069601` | `30803091071` | zentrale Mill-Messung; ausgeschriebene Zahlen fehlten |
| Mill-Messkompatibilität | `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4` | `30803643342` | 40 legale Quellen; Benchmark 80; 55 % planfähige Hände |

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

### Ergebnis und KGB-Entscheidung

Phrase-first-Klassifikation ist als globale Regel bestätigt. Keine neue v2-KGB: `baseline: none` besteht fort und die Sideboard-Relevanz wird noch über Archetyp-Matrizen statt konkrete Gegnerdecks bestimmt.

## Mill-Messzyklus – Runs 53/54

### Ursache und Hypothese

Vier voneinander abweichende Mill-Erkennungen führten zu 0 erkannten Quellen im Benchmark und 0 % planfähigen Händen. Eine zentrale Oracle-Text-Definition sollte Builder, Rollen, Benchmark und Handanalyse ausrichten.

### Ergebnis

- Commit `70f538ce52593e4ab7485f59bf801081cc069601`, Run 53: rot; ausgeschriebene Mengen wie `two` und `three` wurden unterschätzt
- Commit `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run 54: erfolgreich
- 267 Tests bestanden
- Artefakt `global-calibration-pr-54`, ID `8851950460`, 45 Dateien
- 40 unterschiedliche legale Dimir-Millquellen, maximal 120 Kopien bei drei Kopien je Karte
- aktuelles Milldeck: 15 Quellenkopien
- Mill-Benchmark: 78 → 80
- Planfähigkeit: 0 % → 55 %
- marginale Hände: 100 % → 45 %
- Keepability: 74 %
- fehlender Mill-Zugang: 13 %

### KGB-Entscheidung

Keine neue v2-KGB. Die Messdefinition ist verbessert, aber die geplante kapazitätsgeprüfte Mill-Komposition mit mindestens 18 Quellen und sechs echten Engines ist noch nicht veröffentlicht.

### Prioritätsentscheidung für den aktuellen Lauf

Der veröffentlichte Mill-Messzyklus ist vollständig abgeschlossen und grün. Der verbleibende Kompositionsschritt wird nicht als erledigt dargestellt, aber aufgrund des ausdrücklich vorgegebenen Token-Fokus für diesen Vier-Stunden-Lauf pausiert. Der Rückkehrpunkt bleibt dokumentiert.

## 2026-08-03 – Vier-Stunden-Lauf, Token-Zyklus 1: Paketdiagnose

### Session-Snapshot

- Ausgangs-Head: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`
- PR #14: offen, Draft, mergeable
- letzter Run: `30803643342`, erfolgreich
- Ausgangsartefakt: `global-calibration-pr-54`, ID `8851950460`
- Token-Benchmark: 90
- Token-Plan: Aristocrats
- Keepability/Planfähigkeit: 73/73 %
- Goldfish bis Zug 5: 66 % Killrate, 18,69 durchschnittlicher Schaden
- Matchups: 0 % gegen Burn, 2 % gegen Artifacts, 100 % gegen Mill
- Strategy Commitment: 100 %
- Engine Density: 64 %

### Belegte Auffälligkeit

Das finale Deck enthält viele Food-, Artefakt- und allgemeine Sacrifice-Karten. Die aktuelle Rollenlogik zählt jedes erzeugte Token als Material, jedes Vorkommen von `sacrifice` als Outlet-Nähe und auch Self-Death-Effekte als Aristocrats-Payoff. Damit können Commitment und Handklassifikation einen vollständigen Material/Outlet/Death-Payoff-Kern vortäuschen.

### Zyklusvertrag

- **Ursache:** breite Token-/Sacrifice-Rollen unterscheiden keine Kreatur-Tokens, echten wiederholbaren Creature-Sacrifice-Outlets und Other-Creature-Death-Payoffs
- **Hypothese:** eine zentrale paketbezogene Oracle-Text-Diagnose zeigt, welche der hohen Aristocrats-Metriken echte Paketbestandteile und welche breite Rollen-Fehlpositive sind
- **Änderungen:** zentrale Token-Paketsignale; maschinenlesbares Deck-/Pool-Artefakt; Regressionstests
- **Erwartete Metriken:** reale Material-, Outlet-, Death-/Drain-Payoff- und False-Positive-Kopien
- **Invarianten:** keine Kartenauswahl- oder Schwellenwertänderung; fünf Referenzarchetypen, Seed 1701 und bestehende Benchmarks bleiben unverändert
- **Erfolg:** `tokens/token-packages.json` enthält Namen, Mengen, Kategorien, Poolkapazität und breite Rollen-Fehlpositive
- **Abbruch:** zeigt die Diagnose bereits einen belastbaren Aristocrats-Kern, wird nicht künstlich umgebaut; dann ist Matchup-/Combatmodell die nächste Ursache
- **geschätzte Zeit:** 45–60 Minuten inklusive Workflow und Artefaktauswertung

### Änderung vor Push

1. `token_packages.py` trennt Kreatur-Token von Food/Clue/Blood/Treasure, echte aktivierte Creature-Sacrifice-Outlets von One-Shot-Sacrifice sowie Other-Creature-Death-Payoffs von Self-Death-Value.
2. Der PR-Workflow erzeugt nach erfolgreicher Globalvalidierung `tokens/token-packages.json` und behandelt einen Diagnosefehler als roten Lauf.
3. Gezielte Tests sichern die zentralen Abgrenzungen und eine vollständige Fixture-Diagnose.

### KGB-Entscheidung vor Push

Keine neue v2-KGB. Dieser Zyklus verbessert zunächst Messbarkeit; eine Deckverbesserung darf erst nach CI- und Artefaktauswertung behauptet werden.

### Priorisierter nächster ausführbarer Schritt

Den neuen Workflow vollständig auswerten. Bei bestätigter Rollenüberzählung Planerkennung, Komposition, Commitment und Handklassifikation in einem zweiten Zyklus auf dieselbe zentrale Paketdefinition umstellen. Bei vollständigem echtem Paket stattdessen Token-Combat und Matchupmodell untersuchen.
