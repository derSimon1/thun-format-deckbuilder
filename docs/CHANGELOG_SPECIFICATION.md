# Specification Changelog

## 2.0 – 2026-08-03

Konsolidierung des Deckbuilder Development Systems für mehrstündige autonome Kalibrierung mit belastbaren Sicherheits- und Wiederanlaufregeln.

### Hinzugefügt

- Mehrstundenbetrieb mit mehreren vollständigen Kalibrierungszyklen
- keine separaten 15-Minuten-Aufgaben erforderlich
- fünf allgemeine Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill
- Control als allgemeiner Referenzfall für das Verhindern gegnerischer Pläne
- Shrines aus den Pflicht- und Referenzarchetypen entfernt
- verbindliche Analyse von genau 100 reproduzierbaren Sieben-Karten-Starthänden je verwendeter Deckliste
- getrennte Metriken für Keepability, Early Play und Planfähigkeit
- maschinenlesbare Starthand-Rohdaten und dokumentierter Zufallsseed
- verpflichtende Reflexion nach jedem Zyklus
- Known Good Baseline Policy
- Baseline-Vergleich vor und nach jedem Zyklus
- Git-Tag-Policy für größere stabile Meilensteine
- Rollback-Policy für später als fehlerhaft erkannte Baselines
- Session-Recovery nach Zeitlimit, Verbindungsabbruch oder externem Abbruch
- Hypothesenwechsel nach zwei gleichen No-Change-Zyklen oder zwei unbegründeten Regressionen

### Geändert

- externe Prompts nennen nur noch Repository, Branch/PR und Laufzeit
- GitHub Actions bleibt Validator und ist nicht Entwicklungsagent
- Roadmap priorisiert zunächst eine belastbare KGB und den `OpeningHandPlanReport`
- grüne CI allein genügt nicht mehr als Qualitäts- oder Baseline-Nachweis

### Anlass

Mehrstündige Läufe benötigen einen eindeutigen belastbaren Ausgangsstand, reproduzierbare Qualitätsmessung, Schutz vor kumulierten Regressionen und einen klaren Wiederanlaufpunkt. Gleichzeitig wurde Shrines als zu spezieller globaler Referenzfall erkannt und durch Control ersetzt.

## 1.0 – 2026-08-03

Initiale Version des Deckbuilder Development Systems.

### Hinzugefügt

- Mission und Single Source of Truth
- verbindlicher Kalibrierungszyklus
- Trennung zwischen Entwicklungsagent und CI-Validator
- Produktivitätsregeln für No-Change-Zyklen
- Workflow- und Run-ID-Verifikation
- Fast-/Full-Trennung
- Token-Subarchetypen Go Wide, Value Tokens und Aristocrats
- Strategy Commitment, Engine Density und Finish Density
- Confidence-System für Hypothesen
- Dokumentationspflicht
- Abschlusskriterien

### Anlass

Die Nachtkalibrierung vom 2. auf den 3. August 2026 führte trotz zahlreicher geplanter Aufgaben nur zu drei sichtbaren GitHub-Workflows und zu keinem neuen Entwicklungscommit. Die Aufgaben wiederholten überwiegend Sicherheits- und Statusprüfungen. Daraus wurde abgeleitet, dass GitHub-Cron nicht als Entwicklungsantrieb geeignet ist und dass jeder Zyklus eine konkrete Hypothese, eine Fortschrittsregel und eine persistente Dokumentation benötigt.
