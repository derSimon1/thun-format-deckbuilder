# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort; externe Club-/Meta-Evidenz fehlt.

Aktuelle Sicherungspunkte:

- Sideboard: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- Mill-Messung: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- Token-Builder: `1a4618ed3eaed910632eba526b550d8abf9ed905`, Run `30810553137`
- Token-Produktion: `e246e8d86b0872aec05232d43b9ea87c57f77ae6`, Run `30812706366`
- Token-Poolkapazität: `a610843c19a57034428f80f5c99eb497a16b3ebf`, Run `30813247233`

## Vier-Stunden-Lauf – Token-Fokus

### Ausgangsstand Run 54

- Plan Aristocrats
- Benchmark 90
- Keepability/Planfähigkeit 73/73 %
- bisheriger Goldfish 18,69 Schaden und 66 % Killrate
- Matchups: 0 % Burn, 2 % Artifacts, 100 % Mill

## Token-Zyklus 1 – Paketdiagnose

- Commit `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`, Run `30808101416`, erfolgreich
- echtes Material 14, Outlets 9, Death-/Drain-Payoffs 3
- 43 breite Rollen-Fehlpositive
- Mono-White-Pool besitzt genügend Material-, Outlet- und Death-Payoff-Karten
- keine neue KGB

## Token-Zyklus 2 – Präzise Planrollen und Komposition

- Commits `676da07…`, `dfa5bf4…` und `1a4618e…`
- finaler grüner Run 58 `30810553137`, Artefakt `8854683264`
- automatische Planwahl: Aristocrats → Value Tokens
- Benchmark 90→91
- echtes Material 14→33
- breite Fehlpositive 43→0
- Keepability/Planfähigkeit 73/73→77/76 %
- Sparse-Pools bleiben generierbar; neutrale Füller nur bei echter Kopienlücke

## Token-Zyklus 3 – Produktionsmodi und Goldfish

### Run 60

- Commit `e246e8d86b0872aec05232d43b9ea87c57f77ae6`
- Workflow `30812706366`, erfolgreich
- 295 Tests in 49,55 Sekunden
- Test-/Fast-/Diagnoseschritt ungefähr 4:10 Minuten
- Artefakt `8855522460`, 47 Dateien
- Benchmarks unverändert: Burn 83, Tokens 91, Artifacts 90, Control 85, Mill 80
- Builderprofil, Deck-Hash und 100 Hände unverändert

Produktionsmessung des finalen Decks:

| Modus | Kopien |
|---|---:|
| garantiert sofort | 4 |
| unbedingte wiederholbare Trigger | 0 |
| bedingt | 21 |
| Death-Trigger | 8 |

- garantierte Sofortproduktion: 8 Tokens über alle Deckkopien
- Goldfish: 14,66 Schaden, 27 % Killrate, Boardgröße 5,30
- aktive unbedingte Engines: 0,00
- Keepability/Planfähigkeit weiterhin 77/76 %

Die bisherige 66-%-Killrate war durch pauschal zwei sofortige Tokens je Maker aufgebläht. Keine neue KGB.

## Token-Zyklus 4 – Mono-White-Produktionskapazität

### Commit und Run 61

- Commit `a610843c19a57034428f80f5c99eb497a16b3ebf`
- Workflow `30813247233`, erfolgreich
- 296 Tests in 49,31 Sekunden
- Test-/Fast-/Diagnoseschritt ungefähr 4:06 Minuten
- Artefakt `global-calibration-pr-61`, ID `8855717927`, 47 Dateien, 66.069 Byte
- Buildermetriken, Benchmarks, Hände und Goldfish gegenüber Run 60 unverändert

Poolkapazität bei drei Kopien je Karte:

| bisheriger Modus | unterschiedliche Karten | maximale Kopien | Mindestoutput-Kapazität |
|---|---:|---:|---:|
| sofort | 102 | 306 | 426 |
| bedingt | 51 | 153 | 168 |
| Death | 14 | 42 | 45 |
| wiederholbar | 2 | 6 | 6 |

Die zwei als wiederholbar erkannten Karten sind `Cathar's Call` und `Whirlermaker`. Die Value-Mindestdichte von sechs Kopien wäre damit exakt auf zwei Drei-Karten-Pakete konzentriert und ohne Reserve.

### KGB-Entscheidung

Keine neue v2-KGB. Die Kapazitätsmessung ist grün, aber der Modus `repeatable` vermischt noch automatische Trigger mit aktivierten Fähigkeiten und Aktivierungskosten.

### Reflexion

- Reine Kopienkapazität beweist noch keine belastbare Enginequalität.
- Eine aktivierte Tokenquelle ist wiederholbar, aber nicht automatisch und nicht kostenlos.
- `Whirlermaker` darf im Goldfish nicht wie ein kostenloser End-Step-Trigger behandelt werden.
- Vor einer Builderänderung muss diese Unterklasse maschinenlesbar getrennt werden.

## Token-Zyklus 5 – Aktivierte versus automatische Produktion

### Run 62 – rotes Integrationsgate

- Commit `b2bf2f5320894d21ab3bcc82f57e760c7a495ea6`
- Workflow `30817033194`, fehlgeschlagen
- 297 Tests bestanden in 52,72 Sekunden
- Burn 83, Artifacts 90, Control 85 und Mill 80 blieben grün
- Token-Validierung brach vor Deckausgabe ab
- Artefakt `global-calibration-pr-62`, ID `8857298524`, 37 Dateien

### Belegte Ursache

Der neue Diagnosemarker `token_activation_mana_3` wurde nicht vom bestehenden Metadatenfilter in `card_contribution.py` erfasst. Dadurch wurde Simulationsmetadaten fälschlich als kanonische Funktionsrolle normalisiert. Parser und Tests für die Activated-/Repeatable-Trennung selbst waren grün.

### Hotfix-Zyklusvertrag

- **Hypothese:** Das Ergänzen von `token_activation_mana_` zum zentralen Metadatenfilter stellt den unveränderten Builderstand wieder her und erhält die Diagnosemarker auf den finalen DeckEntries.
- **Änderungen:** Metadatenfilter, Regressionstest und Dokumentation.
- **Invarianten:** keine Plan-, Profil-, Scoring- oder Kartenauswahländerung; Benchmarks 83/91/90/85/80; Hände 77/76 %; Goldfish 14,66/27 %.
- **Erfolg:** vollständige Tests und Fast grün; Artifact trennt `activated` und `repeatable`.
- **Rollback:** Builderdeck oder andere Referenzmetriken ändern sich.

### KGB-Entscheidung

Keine neue KGB. Run 62 ist rot und nur als Diagnose des Integrationsfehlers verwendbar.

### Kritische Reflexion

- Die Annahme, alle Produktionsmarker würden automatisch vom bestehenden Präfixfilter erfasst, war falsch.
- Der Fehler ist technisch und liefert noch keine Aussage zur Go-Wide-Deckqualität.
- Ein grüner Hotfix beweist nur Messkonsistenz; die automatische Planwahl muss danach evidenzbasiert neu bewertet werden.

### Priorisierter nächster ausführbarer Schritt

Den Metadatenfilter-Hotfix validieren. Falls die automatische Repeatable-Kapazität unter sechs Kopien liegt, Value Tokens nicht weiter erzwingen und die automatische Planwahl sowie das Go-Wide-Profil auf garantierte Sofort-/Multi-Maker und Anthem-Payoffs ausrichten.
