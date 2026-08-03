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

## Token-Meilensteine vor Go Wide

- Kreatur-Token sind von Food, Clue, Blood und Treasure getrennt.
- Wiederholbare Outlets sind von einmaligen Sacrifice-Kosten getrennt.
- Immediate-, Conditional-, Death-, Activated- und automatische Repeatable-Produktion sind getrennt.
- Run 63 belegt nur eine automatische Mono-White-Enginekarte mit maximal drei Kopien; die Value-Hypothese mit sechs automatischen Enginekopien ist damit widerlegt.
- Der Mono-White-Pool besitzt dagegen 88 sofortige Tokenquellen und ausreichend frühe Multi-Maker sowie Team-Payoffs.

## Sechs-Stunden-Lauf – Token Go Wide

### Session-Snapshot

- Start-Head: `a610843c19a57034428f80f5c99eb497a16b3ebf`
- aktueller übernommener Head: `03dfbc385f252cdd08b1160dab08a02a3b4cabd4`
- PR #14: offen, Draft, mergeable
- letzter grüner Run vor Go Wide: `30817765040`
- Fokus: Token Go Wide
- Primärziel: Go Wide auf garantierte sofortige Produktion, Multi-Maker und Team-Payoffs ausrichten
- Fallback: Mess-/No-Change-Zyklus, falls Pflichtrollen im realen Pool nicht erfüllbar sind
- Stopbedingungen: bewegter Head, aktive unklare CI, rote Integrationsgates oder zu wenig Restzeit für Workflow und Artefakte

## Recovery-Zyklus – Activated versus Repeatable

- Commit `b2bf2f5320894d21ab3bcc82f57e760c7a495ea6`, Run `30817033194`, rot wegen ungefilterter Diagnosemetadatenrolle.
- Hotfix `4d5bad74c84d4f8b03d22ffe55367184ec430996`, Run `30817765040`, grün.
- 297 Tests; Fast/Diagnose ungefähr 4:14 Minuten.
- Benchmarks 83/91/90/85/80.
- Automatisch wiederholbare Poolkapazität: eine Karte, maximal drei Kopien.
- KGB-Entscheidung: keine neue KGB; grüner Messsicherungspunkt.

## Go-Wide-Zyklus – garantierte Produktion und Team-Payoffs

### Zyklusvertrag

- **Ausgangs-Head:** `4d5bad74c84d4f8b03d22ffe55367184ec430996`
- **Ursache:** Value Tokens wurde trotz unerreichbarer automatischer Engine-Mindestdichte gewählt.
- **Hypothese:** Präzise Rollen für sofortige und garantierte Multi-Maker sowie ein Kapazitätsgate lassen den Builder den besser versorgten Go-Wide-Plan wählen.
- **Pflichtdichten:** mindestens 15 Kreatur-Token-Maker, 9 sofortige Maker, 6 garantierte Multi-Maker und 3 Anthems.
- **Invarianten:** Legalität 60/15, Seed 1701, Fast unter zehn Minuten; Burn 83, Artifacts 90, Control 85 und Mill 80.

### Commit und Run 64

- Commit `03dfbc385f252cdd08b1160dab08a02a3b4cabd4`
- Workflow `30819019117`, rot
- 300 Tests bestanden, 1 fehlgeschlagen in 51,53 Sekunden
- Fast-Validierung selbst erfolgreich
- Artefakt `global-calibration-pr-64`, ID `8858133949`, 47 Dateien
- Benchmarks: Burn 83, Tokens 96, Artifacts 90, Control 85, Mill 80
- fünf Archetypen, sechs Matchups, 0 gemeldete Regressionen
- finales Tokenpaket: 36 Kreatur-Token-Maker, 25 sofortige Maker, 21 garantierte Multi-Maker, 6 Anthems
- Produktionsmodi: 25 sofortige, 3 aktivierte, 2 bedingte und 6 Death-Maker-Kopien
- Matchups: 0 % gegen Burn, 58 % gegen Artifacts, 100 % gegen Mill; BO3 0/92/100 %

### Belegte Fehlerursache

Der einzige rote Test zählte rohe Rollenobjekte als Dictionary-Schlüssel und suchte anschließend mit einem String. Der Validator normalisiert dieselben Rollen bereits mit `str(role)`. Die Rolle `token_multi_maker` ist im realen Deck mit 21 Kopien vorhanden; der Fehler ist ausschließlich eine Enum-/String-Normalisierungsinkonsistenz im Test.

### Hotfix-Zyklusvertrag

- **Änderung:** Rollen im Full-Pool-Test vor dem Zählen mit `str(role)` normalisieren.
- **Erfolg:** vollständige Testsuite und Fast grün; Deck-Hash und fachliche Run-64-Artefakte unverändert.
- **Rollback:** Builderdeck oder Referenzmetriken verändern sich.

### KGB-Entscheidung vor Push

Keine neue KGB. Run 64 ist rot, obwohl die Go-Wide-Produktionsvalidierung fachlich erfolgreich ist.

### Kritische Reflexion

- Der Benchmarkanstieg 91→96 belegt bessere Rollenerfüllung, aber noch nicht automatisch bessere Club-Performance.
- 0 % gegen Burn bleibt ein starkes Warnsignal; das Matchupmodell kann sowohl echte Geschwindigkeitsprobleme als auch Simulationsvereinfachungen abbilden.
- 21 Multi-Maker-Kopien sind deutlich über dem Mindestziel und können Interaktion oder Schutz verdrängen.
- Ein Anthem ist ohne Board potenziell tot; die 100 Hände müssen nach grünem Gate auf Maker-plus-Payoff-Sequenzen geprüft werden.

### Priorisierter nächster ausführbarer Schritt

Den Rollen-Normalisierungshotfix veröffentlichen und den neuen Workflow vollständig auswerten. Bei grünem Gate Go-Wide-Deckliste, 100 Hände, Goldfish, Matchups und Arena-Import gegen Run 63 vergleichen; danach genau eine belegte Go-Wide-Schwäche priorisieren.
