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

## Aktueller Zyklus – Burn Sideboard Cuts

- **Ursache:** Die drei Burn-Cuts sind fachlich plausibel, entstehen aber nur durch den generischen niedrigen Kartenscore. Damit ist nicht garantiert, dass spätere Deckversionen weiterhin langsame bedingte oder Death-Maker vor dem Go-Wide-Kern entfernen.
- **Hypothese:** Eine explizite Burn-Cut-Priorität entfernt zuerst `token_production_conditional` und `token_production_death`, bewahrt danach sofortige/Multi-Maker sowie Anthem, Card Draw und Protection und lässt Nicht-Burn-Matchups unverändert.
- **Änderungen:** matchupabhängiger Cut-Key im Sideboard-Optimierer; Regressionstest für die Rollenreihenfolge; Workflow `Token Go Wide – Burn Sideboard Cuts`.
- **Erfolg:** vollständige Testsuite, Fast und Diagnose grün; Burn-Plan bleibt bei `Descendant of Storms`/`Duty Beyond Death`; Benchmarks, Mainboard-Hash und andere Matchups bleiben stabil.
- **Rollback:** wenn der Burn-Plan sofortige Maker oder Anthems entfernt, Nicht-Burn-Pläne ändern oder Benchmarks regressieren.
- **KGB-Entscheidung vor Push:** keine neue KGB, da `baseline: none` fortbesteht.

## Nächster ausführbarer Schritt

Burn-Cut-Priorität veröffentlichen und CI-/BO3-Artefakt vollständig auswerten. Danach Arena-Import und 100 Hände final prüfen.
