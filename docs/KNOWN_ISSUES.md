# Known Issues

## KI-001 – Token-Subarchetypen sind noch nicht spielerisch kalibriert

**Status:** teilweise gelöst  
**Priorität:** hoch

Go Wide, Value Tokens und Aristocrats werden vor der Kartenauswahl unterschieden und planabhängig bewertet. Noch offen ist der belastbare Vergleich realer Builder-Ausgaben anhand planfähiger Starthände, Matchups und Clubdaten.

## KI-002 – Strategy Commitment ist noch tokenspezifisch

**Status:** teilweise gelöst  
**Priorität:** mittel

Ein kopiengewichteter Commitment-Bericht erkennt planprägende, planfremde und neutrale Token-Karten. Die Metrik ist noch nicht archetypenübergreifend in den allgemeinen Qualitätsbericht integriert.

## KI-003 – Engine Density ist teilweise vorhanden; Finish Density fehlt

**Status:** teilweise gelöst  
**Priorität:** hoch

Token-Engines werden von einmaligem Material getrennt. Eine archetypenübergreifende Engine-Abstraktion und eine robuste Finish-/Wincondition-Erkennung fehlen weiterhin.

## KI-004 – Keine vollständig qualifizierte v2-KGB

**Status:** offen  
**Priorität:** hoch

Run `30792560878` auf Commit `31f6c1e053976435481c07ab2098430bc2a45471` dient als v2-Bootstrap-Vergleichsstand. Die 100-Hand-Auswertung ist inzwischen technisch vorhanden und durch Runs 42/43 verifiziert. Eine v2-KGB ist dennoch erst nach erfolgreicher Control-Pflichtvalidierung, wiederhergestelltem Baseline-Vergleich und vollständiger Reflexion zulässig.

## KI-005 – Matchups sind teilweise unrealistisch extrem

**Status:** offen  
**Priorität:** mittel

Token-Matchups zeigten unter anderem 0 % gegen Burn und 100 % gegen Mill. Das kann echte Schwächen anzeigen, muss aber gegen Simulationsvereinfachungen und echte Clubtests geprüft werden.

Die mengenbewusste Sideboard-Suche findet inzwischen echte Dreierpakete, kann
aber mit sechs selbständig nutzbaren Schutzkarten intern weiterhin an die
0-/100-%-Grenzen geraten. Diese Werte sind Modellgrenzen und keine realen
Matchprognosen; Stabilisierungseffekt und Draw-/Cast-Wahrscheinlichkeit müssen
gegen reale Spiele kalibriert werden.

Nach der Kontext-/Dauerkorrektur fällt Token gegen Artifacts modelliert von
60 % auf 0 % und Control gegen Tokens steigt von 65 % auf 100 %. Diese
gegenläufigen Extreme bestätigen, dass das Matchupmodell relative Schwäche
anzeigt, aber absolute Prozentwerte weiterhin nicht belastbar sind.

## KI-006 – Zeitgesteuerte GitHub-Runs sind nicht zuverlässig genug

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

Cron darf nicht als Entwicklungsantrieb verwendet werden. Mehrstundenläufe arbeiten kontinuierlich; GitHub Actions validiert Commits.

## KI-007 – Zu defensive Automationsaufträge können Fortschritt blockieren

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

No-Change-Zyklen müssen Stopgrund, Erkenntnis und nächsten ausführbaren Schritt dokumentieren. Nach zwei gleichen Ursachen wird die Priorität gewechselt.

## KI-008 – Dokumentation kann hinter Code zurückbleiben

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

Development System v2.0 verlangt Logbook-, Roadmap- und KGB-Entscheidungen pro Zyklus. Der Konsistenz-Check bleibt dennoch Pflicht.

## KI-009 – Pflichtvalidator verwendete Shrines statt Control

**Status:** Umsetzung in Zyklus 3, CI ausstehend  
**Priorität:** hoch

Der v2-Validator wird auf Burn, Tokens, Artifacts, Control und Mill umgestellt. Shrines-Code bleibt für optionale Regressionstests erhalten, ist aber nicht mehr Teil der Pflichtvalidierung. Die reale Kartenpool-, 60/15-, Benchmark-, Matchup- und Laufzeitprüfung muss der neue PR-Workflow bestätigen.

## KI-010 – Planabhängige Starthandrollen beruhen teilweise auf Rollen und Auswahlgründen

**Status:** offen  
**Priorität:** mittel

`DeckEntry` enthält derzeit keinen vollständigen Oracle-Text. Der `OpeningHandPlanReport` muss deshalb Rollen, Typzeile und Auswahlgründe verwenden. Ungewöhnlich formulierte Karten oder falsch erkannte Rollen können dadurch als Enabler, Engine, Payoff, Finisher oder Interaktion übersehen werden.

## KI-011 – Mill-Starthände werden derzeit nie als planfähig klassifiziert

**Status:** offen  
**Priorität:** mittel

Runs 42 und 43 zeigen für Mill 0 % planfähige und 100 % marginale Hände. Das kann auf zu wenige erkannte Mill-Enabler in der erzeugten Liste, unzureichende Oracle-Text-Weitergabe oder eine zu strenge Mill-Heuristik zurückgehen. Keine Schwellenwerte ändern, bevor die Ursache anhand der Rohhände belegt ist.

## KI-012 – Globales Outlet-Tagging verdeckt eng bedingten Burn

**Status:** offen
**Priorität:** hoch

Die globale Legacy-Erkennung markiert zusätzliche Opferkosten weiterhin als
`sacrifice_outlet`. Ein versuchsweiser globaler Präzisionsfix änderte Burn von
Benchmark 83 auf 100, senkte aber Goldfish-Schaden/Killrate von 45,99/98 % auf
42,41/96 %, weil unter anderem `Hidetsugu's Second Rite` überbewertet wurde.
Die globale Korrektur darf erst zusammen mit einer realistischen Bewertung und
Simulation des „genau 10 Leben“-Gates erfolgen; der Benchmarkanstieg allein ist
kein Qualitätsnachweis.
