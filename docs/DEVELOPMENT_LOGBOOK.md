# Development Logbook

Frühere Detailstände bleiben über die Git-Historie erhalten.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort.

## Token Go Wide

### Stabiler Bestätigungsstand

- Commit `2bd921c1688c72d4b5949bd0f93cb65a9d1d206c` beseitigte den Full-Pool-Test-Leak.
- Workflow `30824779542`, Run 69, wurde dreimal vollständig auf demselben Head ausgeführt.
- alle drei Durchgänge grün; jeweils 301 Tests, Fast-Validierung und Token-Diagnose erfolgreich.
- Artefakte: `8860492462`, `8860710216`, `8860887986`.

### Castability-Zyklus – Run 70

- Commit `94c8430835222b63b40a8b8465ef35df17787526`.
- Workflow `30827014882`, erfolgreich.
- Artefakt `global-calibration-pr-70`, ID `8861386466`.
- 302 Tests sowie Fast-Validierung und Token-Diagnose grün.
- `Warping Wail` wurde wegen nicht unterstützter `{C}`-Kosten ausgeschlossen und durch das spielbare `Parting Gust` ersetzt.
- Benchmarks unverändert: Burn 83, Tokens 96, Artifacts 90, Control 85, Mill 80.
- Token-Delta gegen Run 69: Schaden 23,72→23,58; Killrate 63→62 %; Board 9,30→9,20; Keepability/Planfähigkeit unverändert 77/77 %.
- Interpretation: minimale Leistungsreduktion, aber reale Castability verbessert; technische und fachliche Hypothese bestätigt.
- KGB: keine neue KGB.

## Aktueller Landzahl-Zyklus

- **Ursache:** Run 70 empfiehlt 23 Länder, meldet durchschnittlich 3,33 ungenutztes Mana und neun Flood-Hände bei 24 Plains.
- **Hypothese:** 23 Plains plus 37 Spells verbessern Deckdichte, Boardaufbau und Killrate stärker, als sie Mana-Screw erhöhen.
- **Änderungen:** TokenStrategy 23 Länder; Integrationsverträge auf 37/23; Logbook und Roadmap.
- **Erfolg:** höhere Planfähigkeit oder Goldfish-Leistung bei höchstens moderatem Manafehler-Delta; Pflichtrollen und andere Benchmarks stabil.
- **Rollback:** Manafehler steigen deutlich, Keepability sinkt oder Schaden/Killrate verbessern sich nicht.
- **KGB-Entscheidung vor Push:** keine neue KGB.

## Nächster ausführbarer Schritt

23-Land-Variante veröffentlichen und artifact-first gegen Run 70 vergleichen. Nur bei klar positivem Gesamtdelta bleibt sie bestehen; andernfalls sofort auf 24 Länder zurückrollen.
