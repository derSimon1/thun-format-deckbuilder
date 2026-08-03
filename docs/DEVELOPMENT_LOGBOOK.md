# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort; externe Club-/Meta-Evidenz fehlt.

Aktuelle grüne Sicherungspunkte:

- Sideboard: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- Mill-Messung: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- Token-Builder: `1a4618ed3eaed910632eba526b550d8abf9ed905`, Run `30810553137`
- Token-Produktion: `e246e8d86b0872aec05232d43b9ea87c57f77ae6`, Run `30812706366`
- Token-Produktionskapazität: `4d5bad74c84d4f8b03d22ffe55367184ec430996`, Run `30817765040`

## Token-Meilensteine vor dem Go-Wide-Lauf

### Präzise Paketrollen

- Ausgangsplan Aristocrats wurde durch 43 breite Rollen-Fehlpositive begünstigt.
- Kreatur-Token wurden von Food, Clue, Blood und Treasure getrennt.
- Wiederholbare Outlets wurden von einmaligen Sacrifice-Kosten getrennt.
- Andere-Kreatur-Death-Payoffs wurden von Self-Death-Value getrennt.
- Der grüne Builderstand Run 58 wechselte zu Value Tokens, Benchmark 91 und Keepability/Planfähigkeit 77/76 %.

### Produktionsmessung

Run 60 ersetzte die pauschale Annahme „jeder Maker erzeugt zwei sofortige Tokens“ durch Immediate-, Conditional-, Death- und Repeatable-Modi.

- korrigierter Goldfish: 14,66 Schaden
- Killrate bis Zug 5: 27 %
- durchschnittliches Tokenboard: 5,30
- aktuelles Value-Deck: 4 sofortige, 21 bedingte und 8 Death-Maker-Kopien; keine automatische Engine

### Poolkapazität Run 61

Die alte Repeatable-Kategorie enthielt `Cathar's Call` und die aktivierte Vier-Mana-Fähigkeit von `Whirlermaker`. Deshalb durfte die automatische Value-Engine-Kapazität noch nicht als sechs Kopien behandelt werden.

## Sechs-Stunden-Lauf – Token Go Wide

### Session-Snapshot

- Start-Head: `a610843c19a57034428f80f5c99eb497a16b3ebf`
- PR #14: offen, Draft, mergeable
- letzter grüner Run: `30813247233`
- Fokus: Token Go Wide
- Recovery-Befund: ein vollständiger, aber noch nicht veröffentlichter Messcommit lag exakt einen Commit vor dem Head
- Primärziel: automatische und aktivierte Produktion trennen, danach Go Wide auf garantierte Produktion ausrichten
- Fallback: keine Builderänderung, falls mindestens sechs automatische Enginekopien belegt werden
- Stopbedingungen: bewegter Head, aktive unklare CI, rote Integrationsgates oder zu wenig Restzeit für Workflow und Artefakte

## Recovery-Zyklus – Activated versus Repeatable

### Commit und Run 62

- Commit `b2bf2f5320894d21ab3bcc82f57e760c7a495ea6`
- Workflow `30817033194`, fehlgeschlagen
- 297 Tests bestanden in 52,72 Sekunden
- Burn 83, Artifacts 90, Control 85 und Mill 80 blieben grün
- Token-Validierung brach wegen der unbekannten Diagnosemetadatenrolle `token_activation_mana_3` ab
- Artefakt `global-calibration-pr-62`, ID `8857298524`, 37 Dateien

Die Parser- und Kapazitätstests waren grün. Die Ursache lag ausschließlich im unvollständigen Metadatenfilter.

### Hotfix und Run 63

- Commit `4d5bad74c84d4f8b03d22ffe55367184ec430996`
- Workflow `30817765040`, erfolgreich
- 297 Tests bestanden in 50,10 Sekunden
- Test-/Fast-/Diagnoseschritt ungefähr 4 Minuten 14 Sekunden
- Artefakt `global-calibration-pr-63`, ID `8857605128`, 47 Dateien, 66.409 Byte
- Benchmarks: Burn 83, Tokens 91, Artifacts 90, Control 85, Mill 80
- fünf Archetypen, sechs Matchups, 0 gemeldete Regressionen

### Evidenz aus Run 63

Poolkapazität bei drei Kopien je Karte:

| Produktionsmodus | Karten | maximale Kopien |
|---|---:|---:|
| sofort | 88 | 264 |
| aktiviert | 16 | 48 |
| bedingt | 50 | 150 |
| Death | 14 | 42 |
| automatisch wiederholbar | 1 | 3 |

Die einzige automatische Quelle ist `Cathar's Call`. Das aktuelle Deck enthält weiterhin:

- 3 aktivierte Makerkopien
- 18 bedingte Makerkopien
- 8 Death-Makerkopien
- 4 sofortige Makerkopien
- 0 automatische Repeatable-Kopien

### Hypothesenentscheidung

Die Value-Hypothese ist widerlegt. Das konfigurierte Minimum von sechs automatischen Enginekopien ist im legalen Mono-White-Pool nicht erreichbar. Aktivierte und bedingte Quellen dürfen diese Kapazität nicht ersetzen. Gleichzeitig besitzt der Pool 88 sofortige Quellen und eine bereits belegte große Auswahl früher Multi-Maker und Anthem-Payoffs.

### KGB-Entscheidung

Keine neue KGB. Run 63 ist ein grüner Messsicherungspunkt, aber die automatische Planwahl erzeugt weiterhin ein Value-Deck ohne automatische Engine.

## Go-Wide-Zyklus – garantierte Produktion und Team-Payoffs

### Zyklusvertrag

- **Ausgangs-Head:** `4d5bad74c84d4f8b03d22ffe55367184ec430996`
- **Ursache:** Value Tokens wird trotz nur drei möglicher automatischer Enginekopien gewählt; aktivierte und bedingte Maker werden als Value-Unterstützung überbewertet.
- **Hypothese:** Präzise Rollen für sofortige und garantierte Multi-Maker sowie ein Kapazitätsgate automatischer Engines lassen den Builder den besser versorgten Go-Wide-Plan wählen.
- **Änderungen:** zentrale Produktionsrollen und Planwahl; Go-Wide-Profil/Kompositionsboni; Regressionstests und Diagnose.
- **Erwartung:** Profil Go Wide mit mindestens 15 Material-, 9 sofortigen, 6 garantierten Multi-Maker- und 3 Anthem-Kopien.
- **Invarianten:** Legalität 60/15, Seed 1701, Fast unter zehn Minuten; Burn 83, Artifacts 90, Control 85 und Mill 80.
- **Erfolg:** finale Deckliste erfüllt alle Pflichtrollen; 100 Hände, Goldfish, drei Token-Matchups und BO3 vollständig vergleichbar.
- **Rollback:** rote CI, nicht erfüllbare Rollen oder eine Verschlechterung ohne belegte höhere Go-Wide-Kohärenz.

### KGB-Entscheidung vor Push

Keine neue KGB. Die Builderänderung ist erst nach vollständiger CI- und Artefaktauswertung bewertbar.

### Kritische Reflexion

- Sofortige Produktion beweist noch keine gute Manaeffizienz; Kurve und Output pro Mana müssen mitgeprüft werden.
- Anthems sind ohne Board tote Karten; mindestens drei sind ein Startpunkt, kein Qualitätsbeweis.
- Die bestehenden Matchupwerte sind stark vereinfacht und dürfen keine Kartennamen-Sonderregel auslösen.
- Ein Planwechsel kann Benchmark oder Keepability senken und dennoch kohärenter sein; die Interpretation muss Deckliste und Rohhände einbeziehen.

### Priorisierter nächster ausführbarer Schritt

Den Go-Wide-Workflow vollständig auswerten. Bei grünem Gate Deckliste, Pflichtrollen, 100 Hände, Goldfish und Matchups gegen Run 63 vergleichen. Bei rotem Gate genau eine belegte Kompositions- oder Testursache beheben.
