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

## Early-Maker-Path-Zyklus – lokale Evidenz vor CI

- **Ursache:** Die 23 marginalen Token-Hände bestanden aus 22 echten
  Landextremen und einer Zwei-Land-Hand ohne Zug-2-Spiel. Die Gegenprüfung der
  77 als planfähig gezählten Hände fand zusätzlich vier False Positives: Die
  Hände 5, 22, 30 und 73 hatten mehrere einzeln bis Zug 3 castbare Planstücke,
  aber keinen bis Zug 2 castbaren Token-Maker und damit keine ausführbare
  Maker-zu-Scaling-Sequenz.
- **Hypothese:** Go Wide ist nur dann planfähig, wenn mindestens ein Maker bis
  Zug 2 tatsächlich castbar ist und bis Zug 3 ein zweiter Maker oder ein
  Payoff zugänglich ist. Ein beliebiger T2-Spielzug genügt nicht.
- **Änderungen:** Die Go-Wide-Klassifikation verwendet `early_makers` und gibt
  `missing_early_token_maker` als konkrete Ursache aus. Zwei Gegenbeispiele
  schützen langsame Maker sowie den gültigen T2-Maker-Pfad. Workflow:
  `Token Go Wide – Early Maker Path`.
- **Lokale Validierung:** 31 gezielte Tests und 328 Gesamttests in 29,61 s
  grün; Fast bestand mit Benchmarks `83/98/90/85/80`, sechs Matchups und
  0 Regressionen. 100 Hände, Seed `1701`, Arena 60/15 und Deck-Hash
  `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`
  bestätigt. Keepability/T2/T3 bleiben `77/94/96 %`; Planfähigkeit sinkt
  korrekt `77 → 73 %`, marginal steigt `23 → 27 %`. Alle anderen
  Vergleichsartefakte sind semantisch identisch.
- **Fehlerkorrektur im Vorgehen:** Lokales Fast benötigt für den vorhandenen
  Cache `THUN_REUSE_CARD_DATABASE=1`. Ein versehentlicher Neubau traf zusätzlich
  auf einen reproduzierbaren Windows-/OneDrive-`replace`-Lock. Der Temp-Build
  wurde vor exaktem Rename mit `integrity=ok`, 38.542 Karten und 116.487 Prints
  geprüft; erst der anschließende Reuse-Lauf zählt als Evidenz.
- **Reflexion:** Die Änderung verbessert Messwahrheit, nicht Deckstärke. Sie
  modelliert weiterhin keine gezogenen Karten bis Zug 3; als Opening-Seven-
  Diagnose ist die strengere Sequenzbedingung aber direkt durch die
  Spezifikation gedeckt. Confidence: hoch.
- **KGB-Entscheidung vor Push:** keine neue KGB. Der Deckbau bleibt identisch,
  während vier überoptimistische Klassifikationen korrigiert werden;
  `baseline: none` besteht fort.

## Engine-Requirement-Context-Zyklus – lokale Evidenz vor CI

- **Ursache:** Nach D-017 bestimmte `engine_density` die planabhängige Pflicht
  noch über eine private Funktion. Der Opening-Hand-Bericht zeigte zwar
  `missing_engine_pct=28`, ließ aber offen, ob dies für Go Wide ein Mangel oder
  nur ein rohes Zugangsmerkmal ist.
- **Hypothese:** Eine zentrale `TokenPlan.requires_engine`-Invariante verhindert
  Drift und macht required/optional explizit, ohne die beobachtete Engine-
  Zugangsquote zu verstecken oder Klassifikationen zu verändern.
- **Änderungen:** `TokenPlan` besitzt die Invariante; Engine Density konsumiert
  sie; `OpeningHandPlanReport.engine_required` ist für Token-Pläne boolesch und
  für Nicht-Token-Archetypen `null`. Workflow:
  `Token Go Wide – Engine Requirement Context`.
- **Lokale Validierung:** 36 gezielte Tests und 329 Gesamttests in 45,03 s
  grün; Fast, sechs Matchups und Token-Diagnose bestanden. Benchmarks bleiben
  `83/98/90/85/80`, 0 Regressionen, Arena 60/15, 100 Hände mit Seed `1701`,
  Planfähigkeit `73 %`, `missing_engine_pct=28`, Deck-Hash
  `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`.
  Nach Entfernen des neuen Kontextfelds ist das Opening-Hand-JSON semantisch
  identisch zum Vorlauf; alle übrigen Vergleichsartefakte sind ebenfalls
  identisch.
- **Reflexion:** Das neue Feld verbessert Interpretierbarkeit, nicht die
  Prognosekraft. `28 %` bleibt bewusst sichtbar, weil optionale Resilienz
  beobachtbar sein darf; es darf nur nicht als Pflichtdefizit gelesen werden.
  Confidence: hoch.
- **KGB-Entscheidung vor Push:** keine neue KGB. Keine Deck- oder
  Qualitätsmetrik verbessert sich; `baseline: none` besteht fort.

## Transform-Gated-Faces-Zyklus – lokale Evidenz vor CI

- **Ursache:** Der Anthem-/Combat-Audit zeigte, dass drei
  `Clay-Fired Bricks // Cosmium Kiln` beim Cast für zwei Mana sofort als je
  zwei Tokens plus permanentes Anthem simuliert wurden. Beide Effekte gehören
  zur Rückseite, die erst nach Craft für `{5}{W}{W}` erreichbar ist.
- **Hypothese:** Eine allgemeine cast-zugängliche Oracle-Sicht entfernt
  transformationsgesperrte Rückseiteneffekte aus Produktion, Paket und Scoring,
  ohne modal castbare Adventures oder Rooms abzuschneiden.
- **Änderungen:** `cast_accessible_oracle_text` erkennt Transform-, Craft-,
  Daybound- und Battle-Gates; Token-Paket, Produktion und Scoring konsumieren
  die Funktion; präzise Token-Rollen entfernen verbleibende breite
  Anthem-Labels. Workflow: `Token Go Wide – Transform-Gated Faces`.
- **Lokale Validierung:** 65 gezielte Tests und 335 Gesamttests in 44,85 s
  grün; Fast bestand mit Benchmarks `83/100/90/85/80`, sechs Matchups und
  0 Validator-Regressionen. Arena 60/15 und 100 Hände mit Seed `1701`
  bestanden; Keepability/T2/T3 bleiben `77/94/96 %`, Planfähigkeit
  `73 → 70 %`. Deck-Hash
  `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815 → 50184dc7a3d0f998f7feb4b85c9151bac6385ad8d527ff6fc342b8e5fdc97dfa`.
- **Vorher/Nachher:** Die drei Bricks verlassen die Liste; unter anderem kommen
  drei `Hunted Witness`. Maker/Immediate/Multi/Anthem ändern sich
  `35/30/22/7 → 33/27/18/6`, bleiben aber über den Profilminima. Goldfish
  fällt ehrlich `24,94 → 19,94` Schaden, `66 → 47 %` Killrate und
  `9,10 → 8,46` Board; der alte Wert war durch nicht erreichbare
  Rückseiteneffekte aufgebläht.
- **Regression/Rückkehrpfad:** Burn-BO3 fällt modelliert `48 → 0 %`,
  Artifacts `98 → 60 %`, Mill bleibt `100 %`. Der Stand ist eine notwendige
  Messkorrektur, aber keine spielerisch belastbare Baseline. Als nächster
  abgeschlossener Zyklus werden Ersatzpaket und Sideboard-Cuts unter der
  korrigierten Semantik stabilisiert; die alte False-Positive-Semantik ist kein
  zulässiger Rollback.
- **Reflexion:** Der Token-Benchmark steigt auf 100, obwohl die realistischere
  Goldfish-Leistung sinkt. Das belegt erneut, dass Rollendichte allein keine
  Deckqualität ist. Weitere mehrflächige Modalformen bleiben eine bekannte
  Modellgrenze. Confidence: hoch für den Bricks-Fehler, mittel für die neue
  Deckstärke.
- **KGB-Entscheidung vor Push:** Regression festgestellt, keine neue KGB.
  `baseline: none` besteht fort.

## Threshold-Aware-Sideboarding-Zyklus – lokale Evidenz vor CI

- **Ursache:** Der Optimierer prüfte Sideboardkarten nur einzeln, sperrte den
  Namen danach und beschränkte seine acht Cut-Kandidaten auf expandierte
  Einzelkopien. Ein `Dawnbringer Cleric` blieb gerundet bei 0 %, drei Kopien
  verbesserten den isolierten Postboardwert dagegen bis 40 % und waren für die
  Suche unerreichbar.
- **Hypothese:** Mengenbewusste Tauschtests finden das echte Schutzpaket und
  stabilisieren den korrigierten Burn-/Artifact-Stand. Sechs kontrollierte
  Mainboard-Ersatzpakete wurden zuvor verworfen: Alle blieben gegen Burn bei
  0 % und senkten Schaden/Killrate; nur `Duty Beyond Death → Release the Dogs`
  erhöhte das Board `8,45 → 9,90`, aber senkte Killrate `47,3 → 44,7 %`.
- **Änderungen:** Der Optimierer prüft je Namen Mengen 1..N gegen acht
  unterschiedliche Cut-Namen; zielabhängiger Lifegain ist kein selbständiger
  Schutz, modale Lebensgewinnoptionen bleiben es; ungecachte Kandidaten nutzen
  Matchup-Samples und deterministische Seeds. Workflow:
  `Token Go Wide – Threshold-Aware Sideboarding`.
- **Lokale Validierung:** 22 gezielte Tests und 338 Gesamttests in 19,14 s
  grün. Fast bestand in 201,4 s mit Benchmarks `83/100/90/85/80`, fünf
  Archetypen, sechs Matchups und 0 Regressionen. Die reale Optimierersuche mit
  80 Samples sank durch Budgetweitergabe von 247 auf 29 s.
- **Deck-/Handinvarianten:** Mainboard, Goldfish und Hash bleiben unverändert:
  Schaden `19,94`, Killrate `47 %`, Board `8,46`, Hash
  `50184dc7a3d0f998f7feb4b85c9151bac6385ad8d527ff6fc342b8e5fdc97dfa`.
  Arena 60/15 sowie 100 Hände mit Seed `1701` bestanden; Keepability/Plan
  `77/70 %`, T2/T3 `94/96 %`.
- **Matchups:** Der Fast-Plan findet nun drei `Dawnbringer Cleric` statt des
  leeren Plans. Token-BO3 Burn/Artifacts/Mill bleibt `0/60/100 %`; die
  Hypothese einer direkten Matchup-Stabilisierung ist damit widerlegt. Die
  Suchkorrektheit verbessert sich, die Deckstärke nicht.
- **Reflexion:** Ein isolierter 80-Sample-Lauf kann mit zwei echten
  Schutz-Playsets 100 % erreichen, während der vollständige BO3-Lauf gegen das
  ebenfalls geboardete Burn-Deck bei 0 % bleibt. Beide Extreme zeigen die
  offene Skalierungsgrenze des abstrakten Stabilisierungssignals. Grüne CI ist
  hier kein realer Spielstärkenachweis. Confidence: hoch für Such- und
  Zielabhängigkeitsfehler, niedrig für absolute Matchupwerte.
- **KGB-Entscheidung vor Push:** keine neue KGB. `baseline: none` bleibt; die
  Infrastruktur ist korrekter und schneller, aber eine spielerische
  Stabilisierung ist nicht belegt.

## Context-Gated-Effects-Zyklus – lokale Evidenz vor CI

- **Ursache:** Satzweises Oracle-Matching trennte den Reminder-Satz von
  `Descendant of Storms` von „whenever attacks / pay {1}{W}` und machte ihn
  sofort. Begrenzte Countertexte von `Love Song`, `Political Triumph`,
  `Requisition Raid` und `Charmed Stray` galten als globale Anthems;
  temporäre `Charge`-Buffs wurden im Goldfish dauerhaft gestapelt.
- **Hypothese:** Fähigkeitskontext über Folgesätze/Bullets, korrekte
  Read-ahead-Ausnahmen und zugbegrenzte Anthem-Dauer entfernen die falschen
  Soforteffekte ohne echte ETB-Maker oder globale Buffs zu verlieren.
- **Änderungen:** zentrale cast-zugängliche Effektsegmente; Saga-/ETB-/Trigger-
  Kontext in Produktion, Paket, Rollen und Scoring; globale Power-/Counter-
  Anthem-Invariante; temporärer Anthem-Bonus endet je Zug. Workflow:
  `Token Go Wide – Context-Gated Effects`.
- **Gegenbeispiele:** `Love Song` behält seinen Kapitel-II-Token, weil
  Read-ahead ihn beim Eintritt wählen kann, verliert aber den auf zwei Ziele
  begrenzten falschen Anthem. `Battle Menu`, `Okoye` und andere echte
  Cast-/Self-ETB-Maker bleiben sofort. Landfall, Leave-, Attack-/Payment- und
  Saga-II-ohne-Read-ahead-Fälle sind bedingt.
- **Lokale Validierung:** 77 gezielte Tests und 349 Gesamttests in 23,19 s
  grün. Fast bestand in 200,4 s mit Benchmarks `83/93/90/85/80`, fünf
  Archetypen, sechs Matchups und 0 gemeldeten Regressionen bei
  `baseline: none`. Arena 60/15, Manaqualität 97 und 100 Hände mit Seed 1701
  bestanden.
- **Vorher/Nachher:** Maker/Immediate/Conditional/Death
  `33/27/1/5 → 30/23/2/5`, Anthem bleibt am Profilminimum 6. Planfähigkeit
  steigt `70 → 73 %`, Keepability/T2/T3 bleiben `77/94/96 %`. Goldfish fällt
  ehrlich `19,94 → 13,87`, Killrate `47 → 8 %`, Board `8,46 → 7,57`; Hash
  wechselt `50184dc7a3d0f998f7feb4b85c9151bac6385ad8d527ff6fc342b8e5fdc97dfa`
  → `57b806f68f433a63f14c52d1a82acf8236cd279b68cf226cb8ef989c7a042d9c`.
- **Matchups:** Token Burn/Artifacts/Mill `0/60/100 → 0/0/100 %`; Control
  gegen Tokens `65 → 100 %`. Burn, Artifacts, Control und Mill behalten ihre
  eigenen Benchmarks `83/90/85/80`. Die relativen Werte bestätigen eine
  Token-Regression, nicht die absoluten extremen Prozentzahlen.
- **Reflexion:** Der Token-Benchmark fällt nur 7 Punkte, während Killrate und
  Artifact-Matchup massiv fallen; Rollendichte bleibt somit kein ausreichender
  Qualitätsindikator. Die Änderung ist dennoch nicht rückrollbar, weil jeder
  entfernte Effekt durch konkreten Oracle-Kontext widerlegt ist. Zusätzliche
  Opferkosten (`Duty Beyond Death`) bleiben noch unmodelliert und können den
  neuen Stand weiter überschätzen. Confidence: hoch für Effektkontext und
  Dauer, niedrig für absolute Matchupwerte.
- **KGB-Entscheidung vor Push:** Regression festgestellt, keine neue KGB.
  `baseline: none` bleibt; der Stand verbessert Messwahrheit, nicht belegte
  Spielstärke.

## Nächster ausführbarer Schritt

Zusätzliche Opferkosten wie bei `Duty Beyond Death` zentral erkennen und im
Token-Goldfish nur bei vorhandenem, tatsächlich verbrauchtem Board bezahlen.
