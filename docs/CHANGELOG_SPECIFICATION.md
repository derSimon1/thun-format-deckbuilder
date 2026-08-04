# Specification Changelog

## 2.0 – Zusätzliche Cast-Kosten 2026-08-04

### Geändert

- Zusätzliche Kreaturen-Opferkosten werden als Castability-Anforderung
  behandelt.
- Der Goldfish verlangt das entsprechende Board und verbraucht die geopferten
  Körper vor Anwendung des Effekts.
- Kostenmarker bleiben Simulationsmetadaten und werden nicht als funktionale
  Deckrollen normalisiert.

### Anlass

`Duty Beyond Death` konnte bislang auf leerem Board gewirkt werden und behielt
den geopferten Körper in der Schadens- und Boardrechnung. Dadurch war die
Simulation gegenüber der realen Karte zu optimistisch.

## 2.0 – Kontextgebundene Token- und Anthem-Effekte 2026-08-04

### Geändert

- Oracle-Fähigkeiten behalten Bedingungen über Folgesätze, Reminder-Text und
  modale Aufzählungspunkte hinweg.
- Saga-Kapitel II+ sind ohne Read-ahead verzögert; Read-ahead-Kapitel bleiben
  beim Eintritt wählbar.
- Nur sofort verfügbare globale Power-/Counter-Buffs zählen als Go-Wide-Anthem.
- Temporäre Anthems laufen im Goldfish am Zugende aus.

### Anlass

`Descendant of Storms` galt trotz Angriffs- und `{1}{W}`-Bedingung als
sofortiger Maker. `Love Song of Night and Day`, `Political Triumph`,
`Requisition Raid` und `Charmed Stray` erzeugten falsche globale Anthems;
temporäre `Charge`-Effekte wurden dauerhaft gestapelt. Der frühere Goldfish-
Stand war dadurch erneut überhöht.

## 2.0 – Mengenbewusste Sideboard-Suche 2026-08-04

### Geändert

- Sideboard-Kandidaten werden auch als zusammenhängende Mehrkopienpakete
  geprüft, wenn eine Einzelkopie noch keine messbare Verbesserung erreicht.
- Zielabhängiger Lebensgewinn wird von selbständig nutzbarer Stabilisierung
  getrennt; echte modale Lebensgewinnoptionen bleiben Schutz.
- Ungecachte Kandidatendecks übernehmen Sample-Budget und deterministischen
  Seed aus der Matchup-Simulation.

### Anlass

Der Greedy-Optimierer lehnte drei gemeinsam wirksame `Dawnbringer Cleric` ab,
weil die erste Kopie den auf ganze Prozent gerundeten Burn-Wert nicht anhob.
Nach der Mengenkorrektur versuchte er zunächst zusätzlich zielabhängigen
Lebensgewinn wie `Sanctify` ohne legales gegnerisches Ziel; die präzisere
Klassifikation verhindert dieses Modell-Gaming.

## 2.0 – Kartenflächen-Präzisierung 2026-08-04

### Geändert

- Transform-, Craft-, Daybound- und Battle-gebundene Rückseiteneffekte zählen
  nicht als beim normalen Cast sofort verfügbare Produktion, Engine oder
  Payoff.
- Modal castbare Flächen wie Adventures und Rooms bleiben zugänglich.

### Anlass

Die Vorderseite von `Clay-Fired Bricks // Cosmium Kiln` wurde für zwei Mana
fälschlich als sofortige Zwei-Token-Produktion plus permanentes Anthem
simuliert, obwohl beide Effekte erst nach Craft für `{5}{W}{W}` auf der
Rückseite verfügbar sind.

## Prompt 2.1 – 2026-08-03

Operationalisierung des Development Systems für effizientere Drei-Stunden-Läufe. Die Spezifikation bleibt Version 2.0; der ausführende Prompt wurde auf 2.1 erhöht.

### Hinzugefügt

- einmaliger Session-Snapshot statt vollständigem Neustart vor jedem Zyklus
- Artifact-first-Auswertung mit Evidenztabelle
- verbindliche 30-Minuten-Abschlussreserve bei einem Drei-Stunden-Lauf
- Zyklusvertrag mit Erfolgskriterien, Invarianten, Abbruchkriterien und Zeitschätzung
- Connector-only-Regel: kontrollierte Vorprüfung, vollständige Suite in CI, Commit bis Artefaktauswertung vorläufig
- maschinenlesbare Sideboard-Diagnoseartefakte
- expliziter Schleifenschutz gegen wiederholte Varianten derselben gescheiterten Heuristik
- Mill-Komposition als primäres Ziel des nächsten Drei-Stunden-Laufs

### Geändert

- keine Folge identischer CI-Statusabfragen ohne neue erwartbare Information
- grüne CI wird noch klarer von fachlichem Erfolg getrennt
- konkrete Artefaktinvarianten werden vor manuellen Sichtprüfungen bevorzugt
- Sideboard-Tuning wird nach den abgeschlossenen Root-Cause-Zyklen pausiert; nächster Schwerpunkt ist Mill

### Anlass

Die Runs 47 und 48 waren technisch grün, boardeten aber weiterhin `Tormod's Crypt` gegen Burn und Tokens ein. Die bisherigen Prozesse erzeugten außerdem viele Statusprüfungen und ließen die semantische Artefaktauswertung zu spät erfolgen. Prompt 2.1 verschiebt die Arbeit auf vorab definierte Hypothesen, maschinenlesbare Evidenz und ausreichend Abschlusszeit.

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
