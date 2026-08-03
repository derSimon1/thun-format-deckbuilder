# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

### Stabiler Deckstand bis Run 74

- Full-Pool-Test-Leak in Commit `2bd921c1688c72d4b5949bd0f93cb65a9d1d206c` behoben und dreimal grün bestätigt.
- `{C}`-Castability korrigiert; 23-Land-Experiment verworfen.
- Immediate-Maker-Scoring erhöhte den Token-Benchmark auf 98.
- Commit `9b4cdb57e92f3753d434fef8c522ed0885aaacd0` entfernte reine Opfer-Outlets.
- Run 74: 306 Tests grün, Benchmarks 83/98/90/85/80, 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets.
- Opening Hands 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate, Board 9,10.

### Lethal-Race-Modell – Runs 75–76

- Run 75 mit harter Kappung bei 20 Schaden wurde verworfen: 307 Tests bestanden, 1 Rundungstest rot; Tokens–Artifacts kippte 76→0 %, Control–Burn 0→100 %.
- Korrekturcommit `08dbde0f261c9d2d1a780c1805a93753fc268f9c` verwendet linearen Fortschritt bis lethal und logarithmisch abnehmenden Nutzen darüber sowie einen kleinen Killratenbonus.
- Workflow `Token Go Wide – Lethal Race Diminishing Returns`, ID `30833119876`, Run 76, erfolgreich; Artefakt `8863859222`.
- 308 Tests, Fast und Token-Diagnose grün; Deck-Hash unverändert `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`.
- Benchmarks und Deckmetriken unverändert; Matchups Tokens gegen Burn/Artifacts/Mill nun 0/64/100 %, Control gegen Burn/Tokens/Artifacts 0/20/50 %.
- Interpretation: archetypenübergreifende Skala bleibt stabil; Burn bleibt ein realer offener Engpass.
- KGB: keine neue KGB, da `baseline: none` fortbesteht.

## Aktueller Zyklus – Burn Stabilization Sideboard

- **Ursache:** Das Token-Sideboard aus Run 76 enthält ausschließlich fünf Pakete mit Artifact-/Enchantment-Antworten und keine Burn-Stabilisierung.
- **Hypothese:** Präzise Lebensgewinn- und Schadensverhinderungsphrasen innerhalb der bestehenden maschinenlesbaren Schutzkategorie priorisieren legale Mono-White-Burn-Antworten, ohne Mainboard oder andere Archetypen zu verändern.
- **Änderungen:** Token-Schutzregel um Lebensgewinn und Schadensverhinderung ergänzt und höher priorisiert; Regressionstest für die Auswahl; Workflow `Token Go Wide – Burn Stabilization Sideboard`.
- **Erfolg:** vollständige Testsuite, Fast und Diagnose grün; Mainboard-Hash und Benchmarks unverändert; mindestens eine Schutz-/Burn-Stabilisierungsoption im 15-Karten-Sideboard; Artifact-/Enchantment-Antworten bleiben vorhanden.
- **Rollback:** wenn das Sideboard einseitig in Lebensgewinn kippt, keine relevante Karte gefunden wird oder Mainboard-/Benchmarkwerte unerwartet ändern.
- **KGB-Entscheidung vor Push:** keine neue KGB; Sideboardverbesserung bei fortbestehendem `baseline: none`.

## Nächster ausführbarer Schritt

Burn-Stabilisierungsregel veröffentlichen und Sideboardliste, BO3-Pläne, vollständige Tests, Benchmarks und Artefakte auswerten. Erst nach grünem Gate weiterarbeiten.
