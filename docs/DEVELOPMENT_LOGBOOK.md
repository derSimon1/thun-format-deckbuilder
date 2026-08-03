# Development Logbook

Detaillierte frühere Fassungen bleiben über die Git-Historie erhalten. Jeder Zyklus dokumentiert Ausgangs-Head, Hypothese, Änderung, CI/Artefakte, KGB-Entscheidung, Reflexion und genau einen nächsten ausführbaren Schritt.

## KGB-Status

Eine vollständig qualifizierte v2-KGB existiert noch nicht. `baseline: none` besteht fort; externe Club-/Meta-Evidenz fehlt.

Aktuelle Sicherungspunkte:

- Sideboard: `937f10f699814e271dd7f8b11b874b0a8f64270c`, Run `30801497068`
- Mill-Messung: `397d989bb19b2c78e4d2f17dcef00b6b572b5aa4`, Run `30803643342`
- Token-Diagnose: `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`, Run `30808101416`

## Vier-Stunden-Lauf – Token-Fokus

### Ausgangsstand Run 54

- Plan Aristocrats
- Benchmark 90
- Keepability/Planfähigkeit 73/73 %
- Commitment 100 %, Engine Density 64 %
- Goldfish 18,69 Schaden, 66 % Killrate bis Zug 5
- Matchups: 0 % Burn, 2 % Artifacts, 100 % Mill

## Token-Zyklus 1 – Paketdiagnose

- Commit `6aa952f2e4d34a39fb32cb1910d3a13d2bcce5f1`
- Run `30808101416`, erfolgreich
- 274 Tests; ungefähr 3:58 Minuten
- Artefakt `global-calibration-pr-55`, ID `8853712704`
- echte Kopien: Material 14, Outlets 9, Death-/Drain-Payoffs 3
- breite Fehlpositive: 19 Nichtkreatur-Token-Maker, 23 One-Shot-Sacrifices und 1 unspezifischer Payoff; gesamt 43
- Poolkapazität ausreichend: 169 Kreatur-Token-Karten, 20 wiederholbare Maker, 34 Outlets und 13 Death-Payoffs
- Hypothese bestätigt; keine neue KGB

## Token-Zyklus 2 – Präzise Planrollen und Komposition

### Commit und Run 56

- Commit `676da07f56abc55651c2d1e1cb25b423ba1a6088`
- Run `30809079933`, rot
- 274 Tests bestanden, 5 fehlgeschlagen
- Fast-Validierung selbst PASS
- Artefakt `global-calibration-pr-56`, ID `8854099893`

### Full-Pool-Ergebnis

| Metrik | Run 55 | Run 56 | Delta |
|---|---:|---:|---:|
| Plan | Aristocrats | Value Tokens | geändert |
| Benchmark | 90 | 91 | +1 |
| echtes Material | 14 | 33 | +19 |
| wiederholbare Maker | 0 | 12 | +12 |
| Rollen-Fehlpositive | 43 | 0 | -43 |
| Keepability | 73 % | 77 % | +4 pp |
| Planfähigkeit | 73 % | 76 % | +3 pp |
| Schaden | 18,69 | 18,97 | +0,28 |
| Killrate | 66 % | 66 % | 0 |
| vs Artifacts | 2 % | 7 % | +5 pp |

Burn blieb bei 0 %, Mill bei 100 %. Der direkte `token_value_payoff` blieb 0/4. Die Rollenbereinigung ist fachlich bestätigt; das rote Gate entstand nur in kleinen Testdatenbanken, denen drei zulässige Kopien fehlten.

### KGB-Entscheidung

Regression festgestellt, weil die vollständige Testsuite rot war. Der Produktionsbefund durfte noch nicht als Sicherungspunkt gelten.

## Token-Hotfix 1 – Poolabhängige Mindestwerte

### Commit und Run 57

- Commit `dfa5bf4cccf21d2eee782191097b8ed894f6f36a`
- Run `30809737220`, rot
- 280 Tests bestanden, 1 Test fehlgeschlagen
- Fast-Validierung selbst PASS
- Artefakt `global-calibration-pr-57`, ID `8854353437`
- Sparse-Pool-Generierung wieder funktionsfähig

### Widerlegte Teilannahme

Neutrale Füller wurden auch im vollständigen Pool zugelassen. Dadurch kamen sechs Clue-/Nichtkreatur-Token-Kopien ins Deck:

| Metrik | Run 56 | Run 57 | Delta |
|---|---:|---:|---:|
| Benchmark | 91 | 87 | -4 |
| Material | 33 | 27 | -6 |
| Nichtkreatur-Token | 0 | 6 | +6 |
| Schaden | 18,97 | 16,80 | -2,17 |
| Killrate | 66 % | 28 % | -38 pp |
| vs Artifacts | 7 % | 0 % | -7 pp |

Der einzelne rote Test erwartete fälschlich keinerlei Warnung, obwohl im Fixture nur die harten Planrollen, nicht aber die weichen Removal-/Draw-Ziele verfügbar waren.

### KGB-Entscheidung

Regression festgestellt. Die Sparse-Pool-Ursache ist gelöst, aber der Hotfix verschlechterte den vollständigen Produktionspool.

## Token-Hotfix 2 – Füller nur bei echter Kopienlücke

### Zyklusvertrag

- **Ursache:** neutrale Füller wurden ohne Prüfung der planrelevanten Gesamtkapazität in jeden Pool aufgenommen.
- **Hypothese:** Füller werden nur ergänzt, wenn unterschiedliche Plan-Karten bei maximaler Kopienzahl weniger als die benötigten Spellslots abdecken.
- **Änderungen:** explizite Kopienkapazität; bedingter Composition-Pool; Regressionstests für Full- und Sparse-Pool.
- **Erfolg:** alle Tests grün; Full-Pool kehrt mindestens zu Benchmark 91, 33 Material, 12 wiederholbaren Makern, 66 % Killrate und 0 Fehlpositiven zurück; Sparse-Pool bleibt generierbar.
- **Invarianten:** Produktionsminimums werden nicht gesenkt; Burn, Artifacts, Control und Mill unverändert.
- **Rollback:** Full-Pool bleibt unter Run 56 oder Sparse-Pool-Tests werden erneut rot.

### KGB-Entscheidung vor Push

Keine neue KGB. Der Commit bleibt bis CI- und Artefaktauswertung vorläufig.

### Priorisierter nächster ausführbarer Schritt

Den Hotfix-Workflow vollständig auswerten. Bei Grün den fehlenden Value-Payoff gegen die ungenaue Token-Goldfish-Simulation nach Qualitätsgewinn, Evidenz, Aufwand und Risiko priorisieren.
