# Dynamic Composition Engine – Schritt 2

Dieses Paket ersetzt die bisherige statische Rollenabfüllung durch eine iterative Auswahl.

## Sichtbare Änderung

Nach jeder ausgewählten Kartenkopie wird der Deckzustand neu ausgewertet. Rollen- und Kurvenbedarf verändern dadurch den Score der nächsten Kandidaten.

## Neue Komponenten

- `CandidateEligibility`: harte Ausschlussregeln vor dem Scoring
- `CandidateEvaluator`: kombiniert Basisqualität, Rollenbedarf und Kurve
- `RoleNeedScorer`: belohnt aktuell fehlende Rollen
- `CurveScorer`: belohnt unterbesetzte Manakurvenbereiche
- `SelectionTrace`: dokumentiert jeden Auswahlschritt

## Sicherheitsgrenzen

- Legalität und strategiebezogene Filter bleiben unverändert vorgeschaltet.
- Das Kopienlimit wird hart geprüft.
- Pflichtrollen werden vor Abschluss des Zauberanteils abgesichert.
- Burn- und Token-Prototyp bleiben über dieselben öffentlichen Funktionen nutzbar.

## Noch nicht enthalten

- Synergie-Scoring
- dynamische Länderbasis
- CLI-Schalter `--explain`

Die Auswahlspuren sind bereits im `CompositionResult.selections` verfügbar und bilden die Grundlage für die spätere CLI-Ausgabe.
