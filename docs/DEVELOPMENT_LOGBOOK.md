# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

Run 63 zeigte, dass der Mono-White-Pool nur drei mögliche Kopien einer automatisch wiederholbaren Tokenquelle besitzt. Deshalb wurde Value Tokens zugunsten des besser versorgten Go-Wide-Plans pausiert.

### Runs 64 bis 67

- Run 64: Commit `03dfbc385f252cdd08b1160dab08a02a3b4cabd4`, Workflow `30819019117`, fehlgeschlagen
- Run 65: Commit `a9dc0ea54a842f2b50547768a185abd49b2062cb`, Workflow `30820717373`, fehlgeschlagen
- Run 66: Commit `50c174413f42d6a185631e6d1ae6fd0d5bf69257`, Workflow `30821482441`, fehlgeschlagen
- Run 67: Commit `b5c6698a5c12af852c1dcc79cd6138686047b3d3`, Workflow `30822534395`, fehlgeschlagen
- in allen Runs: Fast-Validierung und Token-Diagnose erfolgreich; jeweils genau ein Full-Pool-Test rot
- Run-67-Artefakt `global-calibration-pr-67`, ID `8859572866`
- Run 67: 300 Tests bestanden, 1 fehlgeschlagen

### Stabiler Produktionsbefund

- Benchmarks: Burn 83, Tokens 96, Artifacts 90, Control 85, Mill 80
- Go-Wide-Profil: 36 Kreatur-Token-Maker, 25 sofortige Maker, 21 Multi-Maker, 6 Anthems
- 100 Hände: Keepability 77 %, Planfähigkeit 77 %, Early Play T2/T3 94/96 %
- Goldfish: 23,72 Schaden, 63 % Killrate, Board 9,30
- Matchups: Burn 0 %, Artifacts 58 %, Mill 100 %
- keine Rollen-Fehlpositive im Token-Diagnoseartefakt

### Belegte Testursache

Drei Hotfixvarianten prüften weiterhin eine instabile Abstraktion:

1. rohe Rollenobjekte als Dictionary-Schlüssel,
2. `str(role)`,
3. `quality_report.role_quality` in einer wiederholten Testsession.

Die finalen `DeckEntry.roles` und die Fast-Artefakte enthalten nachweislich 21 `token_multi_maker`-Kopien. Der Qualitätsbericht der isolierten Fast-Validierung meldet ebenfalls 21; in der Testsession meldete er dagegen 0. Für das Full-Pool-Integrationsgate ist daher die repräsentationsunabhängige Prüfung der finalen Deckeinträge der direkte stabile Vertrag. Die zustandsabhängige Qualitätsberichtabweichung bleibt als separater Fehler offen.

## Aktueller Hotfix-Zyklus

- **Ursache:** Das Integrationsgate prüft eine instabile Zwischenrepräsentation statt der finalen Deckrollen.
- **Hypothese:** Eine `_has_role`-Prüfung, die String-, Enum- und `CardRole.X`-Darstellungen akzeptiert, bestätigt das reale finale Go-Wide-Paket reproduzierbar.
- **Änderung:** nur Full-Pool-Test sowie Logbook und Roadmap.
- **Erfolg:** 301 Tests, Fast-Validierung und Token-Diagnose grün; Deck-Hash und Referenzmetriken unverändert.
- **Rollback:** finale Deckeinträge besitzen weniger als 6 Multi-Maker oder Referenzbenchmarks verändern sich.
- **KGB-Entscheidung vor Push:** keine neue KGB.

## Reflexion

- Nach zwei gescheiterten Varianten wurde nicht weiter dieselbe Normalisierung variiert, sondern der fachlich direkte Endvertrag gewählt.
- Die Qualitätsberichtabweichung zwischen wiederholter Testsession und isoliertem Fast-Prozess muss separat reproduziert werden.
- Benchmark 96 belegt Rollenerfüllung, aber noch nicht automatisch bessere Club-Performance.
- Das Burn-Matchup bleibt die stärkste offene spielerische Warnung.
- Die Go-Wide-Liste enthält eine farblose Manaanforderung; dieser Castability-Fall folgt erst nach grünem Testgate.

## Nächster ausführbarer Schritt

Den finalen Deckrollen-Hotfix veröffentlichen und CI samt Artefakten vollständig auswerten. Bei grünem Gate die zwei befristeten Fortsetzungsaufgaben einrichten und anschließend die farblose Manaanforderung global absichern.
