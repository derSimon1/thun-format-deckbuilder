# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide – stabiler Kern

- Run 74: Benchmark 98, 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets.
- Opening Hands 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate, Board 9,10.
- Deck-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`.

## Burn-Stabilisierung – Runs 77–78

- Run 77 ergänzte fünf legale Lebensgewinn-/Interaktionspakete im Sideboard.
- Commit `cc484ad60ecb2a47b8277d3e8b7d013ee83a6cdd`, Workflow `Token Go Wide – Postboard Burn Stabilization`, Run 78, ID `30834782059`, Artefakt `8864513611`.
- 310 Tests, Fast und Diagnose grün; Benchmarks 83/98/90/85/80; Mainboard-Hash unverändert.
- Burn Game One 0 %, Postboard 62 %, modellierte Matchwinrate 48 %.
- Plan: 3 `Dawnbringer Cleric` hinein; 2 `Descendant of Storms` und 1 `Duty Beyond Death` heraus.
- Artifacts/Mill bleiben 64/100 %; KGB: keine neue KGB.

## Castability-Zyklus – lokale Evidenz vor CI

- **Ursache:** Explizite `{C}`-Kosten wurden von Candidate Eligibility pauschal abgelehnt, weil der Basic-Land-Builder keine echte farblose Quelle modellierte. Der begonnene Ersatz verteilte die neue Semantik zunächst auf mehrere Module und ließ Eligibility ohne gemeinsame Quellengarantie durch.
- **Hypothese:** Eine zentrale Mana-Symbol- und Zahlungsdefinition sowie ein Mindestquellen-Floor erlauben `{C}` nur bei echter farbloser Quellenunterstützung, erzeugen ausreichend Wastes und verhindern, dass farbige oder Wildcard-Quellen `{C}` bezahlen.
- **Änderungen:** zentrale Parser-/Payment-Invariante in `mana_requirement`; `Wastes` und Mindestquellen in der Basic-Land-Verteilung; Candidate Eligibility und Opening-Hand-Simulation verwenden dieselbe Definition. Der Workflow heißt `Token Go Wide – Castability`.
- **Ursprünglicher Testfehler:** Der Test erwartete noch das frühere pauschale Verbot jeder `{C}`-Karte. Diese Erwartung ist nach Wastes-Unterstützung nicht mehr korrekt. Sie wurde nicht gelockert, sondern in Gegenbeispiele für fehlende echte Quellen, farbige Quellen und Wildcards sowie positive Wastes-Fälle aufgeteilt.
- **Lokale Validierung:** 33 gezielte Tests und 322 Gesamttests grün; Fast-Validierung `PASS`; Benchmarks Burn/Tokens/Artifacts/Control/Mill unverändert `83/98/90/85/80`; keine gemeldete Regression.
- **Castability:** Token-Manabasis vorher `24 Plains`, nachher `22 Plains + 2 Wastes`; W/C-Quellen jeweils 100 % ausreichend, Manaqualität unverändert 97. Von 100 Händen mit Seed `1701` enthalten 20 `Warping Wail`; 3 sind damit spielbar und keine ohne echte C-Quelle.
- **Opening Hands und Arena:** 60/15 bestanden; Keepability/Planfähigkeit unverändert 77/77 %, Mana-/Farbfehler 22/0 %. Early Play bis Zug 2/3 sinkt von 94/96 auf 93/95 %. Deck-Hash wechselt von `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815` auf `a9fbd8b2b767a92df82f564474565db1d44bbccd66c9af948869ec2375d8cced`.
- **Spielerische Deltas:** Goldfish 24,94 → 24,84 Schaden, Killrate 66 → 65 %, Board 9,10 → 9,02. Burn-Matchwinrate bleibt 48 %, Artifacts 98 %, Mill 100 %; der Fast-Regression-Validator meldet keine Regression.
- **Alternative Erklärung/Risiko:** Die kleinen Goldfish- und Early-Play-Deltas entstehen wahrscheinlich aus der nun legalen Auswahl von zwei `Warping Wail` und der zugehörigen Wastes-Manabasis, nicht aus einem Fehler der Zahlungslogik. Die Simulation modelliert andere nichtbasische echte farblose Quellen nur dann korrekt, wenn sie als Quelle `C` übergeben werden; reale Spiele bleiben ungeprüft.
- **KGB-Entscheidung vor Push:** keine neue KGB. `baseline: none` besteht fort; der Zyklus verbessert Korrektheit und Reproduzierbarkeit, bringt aber keine belegte spielerische Verbesserung.

## Agent-Instructions-Zyklus – lokale Evidenz vor CI

- **Ursache:** Im Repository fehlt `AGENTS.md`; dadurch sind verbindliche Dokumentreihenfolge, Zyklusvertrag, lokaler Testpfad, PR-Trennung und die vorgeschriebene GitHub-CLI-Ausführung am Einstieg nicht dauerhaft auffindbar.
- **Hypothese:** Eine knappe Root-Routingdatei verweist auf die bestehenden Single Sources of Truth und verhindert wiederkehrende Recovery-/Workflowfehler, ohne Runtime- oder Deckverhalten zu ändern.
- **Änderungen:** neues Root-`AGENTS.md` mit Dokumenthierarchie, Zyklus-/Validierungsregeln, lokalem Windows-Testpfad, Artefaktregeln, PR-#13-Trennung und vollständigem GitHub-CLI-Pfad; Workflow `Token Go Wide – Agent Instructions`.
- **Erwartete Invarianten:** 322 Tests, Fast-Validierung, Benchmarks `83/98/90/85/80`, Token-60/15, Seed `1701`, Deck-Hash `a9fbd8b2b767a92df82f564474565db1d44bbccd66c9af948869ec2375d8cced` und alle Matchups bleiben unverändert.
- **Lokale Validierung:** Routing-Assertions grün; 322 Tests in 34,93 s; Fast und Token-Diagnose grün; Benchmarks, 100 Hände, Planfähigkeit 77 %, Produktions-/Finishdichten und Deck-Hash bitstabil; keine Regression.
- **KGB-Entscheidung vor Push:** keine neue KGB. Die Änderung verbessert Prozesssicherheit, nicht belegte Deckstärke; `baseline: none` bleibt bestehen.

## Mana-Strain-Zyklus – lokale Evidenz vor CI

- **Ursache:** D-015 machte `{C}`-Karten korrekt spielbar, Candidate Scoring
  bewertete aber nur Kartenqualität, Rollen und Synergien. Der Opportunitätspreis
  dauerhaft gebundener echter Farblosquellen fehlte; dadurch verdrängten zwei
  marginale `Warping Wail` stärkere farbige Go-Wide-Kandidaten.
- **Hypothese:** Ein allgemeiner, erklärbarer Abzug von 2 Punkten pro striktem
  `{C}`-Symbol bildet die Quellenspannung ab, ohne hochwertige `{C}`-Karten
  pauschal zu verbieten. Hybridkosten bleiben unberührt.
- **Änderungen:** zentraler Zähler für strikte Manasymbole; `{C}`-Pips in der
  normalisierten Kartenbeitragsstruktur; `mana_strain` im Candidate Scoring;
  gezielte Regressionstests und Workflow `Token Go Wide – Mana Strain`.
- **Lokale Validierung:** 43 gezielte Tests und 325 Gesamttests in 44,76 s
  grün; Fast-Validierung und 100-Hand-Diagnose bestanden; Arena-Import 60/15;
  keine Regression. Benchmarks Burn/Tokens/Artifacts/Control/Mill bleiben
  `83/98/90/85/80`.
- **Vorher/Nachher:** gegenüber dem Castability-Stand Early Play T2/T3
  `93/95 → 94/96`, Goldfish-Schaden `24,84 → 24,94`, Killrate
  `65 → 66 %`, Board `9,02 → 9,10`. Die Liste wechselt von zwei
  `Warping Wail`, einer `Basilica Shepherd` und `22 Plains + 2 Wastes` zurück
  auf zwei `Battle Menu`, drei `Okoye` und `24 Plains`; der Deck-Hash ist wieder
  `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`.
- **Opening Hands und Matchups:** Seed `1701`, 100 Hände, Keepability/Plan
  `77/77 %`, Mana-/Farbfehler `22/0 %`. Burn/Artifacts/Mill bleiben
  `48/98/100 %`; 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems und
  0 Outlets bleiben stabil.
- **Alternative Erklärung/Risiko:** Der Gewinn kann primär aus der konkreten
  Rangfolge von `Battle Menu`/`Okoye` gegen `Warping Wail` stammen. Der
  allgemeine Malus ist deshalb bewusst klein: Er macht `{C}` nicht unzulässig
  und greift nur bei strikten, tatsächlich dedizierte Quellen erzwingenden
  Symbolen. Reale Spiele bleiben ungeprüft.
- **KGB-Entscheidung vor Push:** keine neue KGB. Der frühere stabile Kern wird
  reproduzierbar wiederhergestellt, aber `baseline: none` bleibt bis zur
  ausdrücklichen v2-Qualifikation bestehen.
- **CI-Abschluss:** Commit `8e3aa9a62250a1974a5f1b4f2ac475d93a5cd038`,
  Workflow `Token Go Wide – Mana Strain`, Run `30856406328`, Job
  `91828344196`, 325 Tests in 47,38 s, Gesamtlauf 3:59, Artefakt
  `global-calibration-pr-85` (ID `8872721218`); 447 Logzeilen und 49
  Artefaktdateien geprüft, keine fachliche Regression.

## Plan-Aware-Engines-Zyklus – lokale Evidenz vor CI

- **Ursache:** Engine Density meldete bei jedem Token-Plan 0 % als Mangel,
  obwohl die Spezifikation für Go Wide frühe Maker plus Scaling und keine
  wiederholbare Value-Engine verlangt. Dadurch wirkten 100 % Strategy
  Commitment und 0 % Engine Density fälschlich widersprüchlich.
- **Hypothese:** Eine explizite planabhängige Engine-Pflicht beseitigt die
  irreführende Go-Wide-Warnung, ohne die numerische Messung oder echte
  Warnungen für Value Tokens und Aristocrats zu schwächen.
- **Verworfene Deckvariante:** Eine `Cathar's Call` statt einer
  `Rally the Monastery` erhöhte die angezeigte Engine Density, verschlechterte
  aber über 20 Goldfish-Seeds Schaden `24,838 → 24,815` und Killrate
  `65,50 → 65,35 %`; über zehn Matchup-Seeds sanken modellierte
  Artifact-Siege `68,7 → 62,6 %`. Burn/Mill blieben `0/100 %`. Die
  Deckänderung wurde deshalb verworfen.
- **Änderungen:** `EngineDensityReport` weist `engine_required` aus; die
  Null-Engine-Warnung gilt nur für enginepflichtige Pläne; die Zusammenfassung
  kennzeichnet `required` beziehungsweise `optional`. Workflow:
  `Token Go Wide – Plan-Aware Engines`.
- **Lokale Validierung:** 43 gezielte Tests und 326 Gesamttests in 46,61 s
  grün; Fast und Token-Diagnose bestanden. Alle fachlichen Vergleichsartefakte
  sind semantisch identisch zum Ausgangsstand: Benchmarks `83/98/90/85/80`,
  0 Regressionen, Deck-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`,
  100 Hände mit Seed `1701`, Keepability/Plan `77/77 %`, T2/T3 `94/96 %`.
- **Reflexion:** Die Simulation kann langfristige Resilienz einer Aura-Engine
  unter Interaktion unterschätzen; reale Spiele fehlen. Die Mehrseed-Daten
  widerlegen aber eine automatische Aufnahme der einzigen Pool-Engine. Die
  Änderung ist nicht auf eine Kartenfixture, sondern auf die Planinvariante
  kalibriert. Confidence: hoch für die Diagnose, mittel für die spielerische
  Ablehnung von `Cathar's Call`.
- **KGB-Entscheidung vor Push:** keine neue KGB. Messbarkeit wird verbessert,
  die Deckqualität bleibt gleich und `baseline: none` besteht fort.

## Nächster ausführbarer Schritt

Die 23 marginalen Token-Starthände nach konkreten, häufigsten
Sequenzproblemen clustern und nur eine belegte Builder- oder
Handklassifikationsursache bearbeiten.
