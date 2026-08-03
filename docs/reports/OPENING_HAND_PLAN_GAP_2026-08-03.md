# Opening-Hand Plan Validation – Messlückenbericht

**Datum:** 2026-08-03  
**Branch:** `codex/global-deckbuilder-calibration`  
**Ausgangs-Head:** `851b0e605f53fd70468ba4cd814e7fa37f88d569`  
**Workflow:** Run `30788304533`, erfolgreich

## Ziel

Prüfen, ob die erzeugten Decklisten ihren deklarierten Hauptplan aus realistischen Starthänden beginnen können, und die verbindliche Anforderung von 100 reproduzierbaren, planabhängig bewerteten Sieben-Karten-Händen vorbereiten.

## Verwendete Evidenz

Der aktuelle Workflow erzeugte für Burn, Tokens, Artifacts, Shrines und Mill bereits je 2.000 Opening-Hand-Samples. Die Artefakte enthalten aggregierte Kennzahlen, jedoch weder die einzelnen gezogenen Hände noch vollständige Kartenmetadaten pro Hand. Deshalb wäre eine nachträgliche Rekonstruktion von exakt 100 planabhängigen Händen aus diesen Artefakten nicht reproduzierbar und würde Ergebnisse erfinden.

## Aktuelle Messwerte

| Archetyp | Profil | Samples | spielbare Hände | nach Mulligan spielbar | früher Play | Core bis Zug 3 | Mana Screw | Benchmark | Qualität |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Burn | Mono-Red Burn | 2.000 | 79 % | 96 % | 100 % | 0 % | 3 % | 83 | 93 |
| Tokens | Mono-White Tokens — Aristocrats | 2.000 | 75 % | 94 % | 98 % | 0 % | 4 % | 90 | 95 |
| Artifacts | Artifact Synergy | 2.000 | 78 % | 96 % | 99 % | 100 % | 3 % | 90 | 94 |
| Shrines | Five-Color Shrines | 2.000 | 73 % | 94 % | 97 % | 100 % | 3 % | 78 | 89 |
| Mill | Dimir Mill | 2.000 | 77 % | 96 % | 99 % | 31 % | 3 % | 78 | 97 |

Tokens meldet zusätzlich:

- Strategy Commitment Aristocrats: 100 %; 36 committed, 0 conflicting, 0 neutral
- Engine Density Aristocrats: 64 %; 23 von 36 Zauberkopien, acht unterschiedliche Engines

## Kritische Prüfung

### Welche Annahme könnte falsch sein?

Die bisherige Opening-Hand-Metrik setzt offenbar „früher Play“ teilweise mit einem funktionierenden Spielplan gleich. Burn und Tokens erreichen 100 beziehungsweise 98 % frühe Plays, aber 0 % „Core bis Zug 3“. Mindestens eine der beiden Metriken ist für diese Archetypen nicht korrekt auf den Hauptplan kalibriert.

### Alternative Erklärungen

1. Die Core-Kartenerkennung kennt die neuen Token-Subarchetypen und die Burn-Rollen nicht.
2. Die Decks besitzen tatsächlich viele billige Karten, aber zu wenig planprägende Sequenzen.
3. Die aggregierte Metrik betrachtet einzelne Karten, nicht die notwendige Kombination aus Enabler, Engine und Payoff.
4. Bei Tokens kann die hohe Engine Density durch Karten entstehen, die zwar einzeln als Engine erkannt werden, aber in einer konkreten Hand nicht gemeinsam funktionieren.

### Overfitting-Risiko

Grüne CI, hohe Qualitätswerte und gute Early-Play-Raten beweisen nicht, dass der Matchplan in einer Starthand funktioniert. Eine neue 100-Hand-Prüfung darf deshalb nicht nur bestehende Rollen- und Benchmarkwerte erneut zusammenzählen.

### Unentdeckte Regression

Die neue Aristocrats-Erkennung könnte ein formal kohärentes Deck bevorzugen, dessen Starthände zu häufig nur Opfermaterial, nur Sacrifice-Outlets oder nur Payoffs enthalten. Die aktuellen aggregierten Artefakte können dieses Sequenzproblem nicht erkennen.

## Abgeleitete nächste Schritte

### Option A – Planabhängige 100-Hand-Sequenzanalyse

Erweitere den Opening-Hand-Simulator so, dass jede einzelne Hand mit festem Seed gespeichert und anhand eines Archetyp-Plans klassifiziert wird. Für Tokens muss mindestens unterschieden werden zwischen Material/Enabler, Sacrifice-Outlet beziehungsweise Engine und Death-/Drain-Payoff. Ausgabe: planfähig, marginal oder nicht planfähig sowie konkrete Ausfallgründe.

**Nutzen:** sehr hoch  
**Evidenz:** hoch  
**Aufwand:** mittel  
**Risiko:** niedrig bis mittel

### Option B – Finish Density zuerst implementieren

Modelliere vor der Starthandprüfung Finisher separat und verwende sie anschließend als weiteres Handmerkmal.

**Nutzen:** hoch  
**Evidenz:** mittel  
**Aufwand:** mittel  
**Risiko:** mittel, weil eine Finish-Metrik allein das Sequenzproblem nicht löst

## Priorisierter nächster Schritt

**Option A ist der logisch stärkste nächste Schritt.**

Implementiere einen reproduzierbaren `OpeningHandPlanReport` mit genau 100 Händen je Referenzdeck und dokumentiertem Seed. Er muss Rohklassifikationen oder maschinenlesbare Zähler ausgeben und darf planfähig nur melden, wenn Mana, frühe Spielbarkeit und die für den Hauptplan erforderlichen Komponenten beziehungsweise ein realistischer Zug-1-bis-Zug-3-Pfad gemeinsam vorhanden sind.

Erst danach sollte Finish Density als eigener Baustein ergänzt werden, weil die Handanalyse zeigen kann, ob Finisher überhaupt früh genug erreichbar sind oder ob Enabler-/Engine-Konsistenz das größere Problem ist.

## Confidence

**Hoch** für die Diagnose der Messlücke, da die widersprüchlichen Artefaktwerte direkt aus dem erfolgreichen Workflow stammen.  
**Mittel** für die Annahme, dass die neue Sequenzanalyse unmittelbar die Deckqualität verbessert; dafür sind Implementierung, Regressionstests und spätere Clubspiele erforderlich.

## Nicht durchgeführt

Es wurden keine künstlichen 100 Hände aus Prozentwerten zurückgerechnet. Ohne einzelne Hände und Kartenmetadaten wäre dies keine echte Simulation gewesen. PR #13 wurde nicht verändert.
