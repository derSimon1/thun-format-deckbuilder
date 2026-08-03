# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide – stabiler Kern

- Run 74: Benchmark 98, 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems, 0 Outlets.
- Opening Hands 77/77 %, Goldfish 24,94 Schaden, 66 % Killrate, Board 9,10.
- Deck-Hash `133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`.

## Lethal-Race-Modell – Runs 75–76

- Harte Kappung in Run 75 verworfen; sie verzerrte archetypenübergreifende Matchups.
- Commit `08dbde0f261c9d2d1a780c1805a93753fc268f9c`, Workflow `Token Go Wide – Lethal Race Diminishing Returns`, Run 76, ID `30833119876`, Artefakt `8863859222`.
- 308 Tests, Fast und Diagnose grün; Benchmarks 83/98/90/85/80; Tokens gegen Burn/Artifacts/Mill 0/64/100 %.
- KGB: keine neue KGB.

## Burn-Stabilisierung im Sideboard – Run 77

- Commit `cbd8c4a2c45c27ed4bda87f3f040351c793bfedf`.
- Workflow `Token Go Wide – Burn Stabilization Sideboard`, ID `30833943550`, erfolgreich; Artefakt `8864180091`.
- 309 Tests, Fast und Diagnose grün; Mainboard-Hash und Benchmarks unverändert.
- Sideboard: je 3 `Dawnbringer Cleric`, `Light of Hope`, `Lucky Offering`, `Sanctify`, `Decommission`.
- Alle fünf Optionen verbinden Lebensgewinn mit Artifact-/Enchantment-Interaktion; `Dawnbringer Cleric` deckt zusätzlich Graveyards ab.
- BO3 boardet drei `Dawnbringer Cleric` gegen Burn ein, das Modell bewertet den Lebensgewinn jedoch noch nicht und bleibt bei 0 %.
- KGB: keine neue KGB.

## Aktueller Zyklus – Postboard Burn Stabilization

- **Ursache:** Das BO3-Modell erkennt `sideboard_protection` als relevante Karte, rechnet den Lebensgewinn aber nicht in den Matchup-Score ein.
- **Hypothese:** Drei explizite Schutzkarten entsprechen ungefähr sechs zusätzlichem Leben beziehungsweise 30 % Startlebenspunkten. Ein nur gegen Burn wirksamer Bonus von `3 × Schutzkartendichte` bildet diese Stabilisierung konservativ ab.
- **Änderungen:** maschinenlesbare Schutzdichte im Matchup-Simulator; Bonus ausschließlich gegen Burn; Regressionstest, dass Burn verbessert und Artifacts unverändert bleibt; Workflow `Token Go Wide – Postboard Burn Stabilization`.
- **Erfolg:** vollständige Testsuite, Fast und Diagnose grün; Game-One und Mainboard unverändert; Postboard-Burn-Winrate steigt sichtbar; andere Matchups und Benchmarks bleiben stabil.
- **Rollback:** wenn Game One beeinflusst wird, Nicht-Burn-Matchups ändern oder der Bonus das Matchup unrealistisch auf 100 % kippt.
- **KGB-Entscheidung vor Push:** keine neue KGB, da `baseline: none` fortbesteht.

## Nächster ausführbarer Schritt

Postboard-Stabilisierungsmodell veröffentlichen und vollständige CI-, BO3- und Artefaktauswertung durchführen. Erst danach weiterarbeiten.
