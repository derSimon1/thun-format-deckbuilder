# Token Go Wide – autonomer Optimierungsbericht

**Repository:** `derSimon1/thun-format-deckbuilder`

**Branch:** `codex/global-deckbuilder-calibration`

**PR:** #14; PR #13 blieb unangetastet

**Arbeitsfenster:** 2026-08-03 23:21–23:58 CEST
**Abschlussgrund:** Alle belegten, eng abgegrenzten Zyklen waren abgeschlossen;
für einen weiteren Codezyklus lag noch keine belastbare Hypothese vor. Das
Sieben-Stunden-Limit wurde daher bewusst nicht ausgeschöpft.

## Ergebnis

Der begonnene Castability-Zyklus wurde korrekt abgeschlossen, die fehlende
Repository-Einstiegsanweisung ergänzt und der kleine spielerische Verlust der
neu zulässigen `{C}`-Kandidaten behoben. Drei zusammenhängende Commits wurden
einzeln lokal und durch GitHub Actions validiert:

1. `d278a3d7fb1b729f0f6455908f234465e83d739a` – zentrale echte
   Farblos-Castability, Wastes-Unterstützung und Regressionstests.
2. `67165782587ff3e121d8e03b59917e38142602ec` – Root-`AGENTS.md` mit
   verbindlicher Dokument-, Test-, PR- und GitHub-CLI-Routinganweisung.
3. `8e3aa9a62250a1974a5f1b4f2ac475d93a5cd038` – erklärbarer
   Quellenspannungsbeitrag für strikte `{C}`-Kosten.

## Castability

`{C}` ist jetzt eine eigenständige Zahlungsanforderung. Farbige Quellen und
Wildcard-Mana erfüllen sie nicht. Candidate Eligibility, Basic-Land-Verteilung
und Opening-Hand-Castability verwenden dieselbe zentrale Definition. Wenn der
Builder echte farblose Quellen bereitstellen kann, erzeugt er ausreichend
`Wastes`; ohne solche Unterstützung bleibt die Karte unzulässig.

Der ursprünglich fehlschlagende Test bildete das alte pauschale Verbot jeder
`{C}`-Karte ab. Nach der bewusst eingeführten Wastes-Zusicherung war diese
Erwartung falsch. Sie wurde durch positive Wastes-Fälle und Gegenbeispiele für
fehlende, farbige und Wildcard-Quellen ersetzt, nicht bloß gelockert.

## Mana-Strain und Vorher/Nachher

Die korrekte Zulassung machte zwei `Warping Wail` spielbar, Candidate Scoring
berücksichtigte aber die zwei dafür dauerhaft gebundenen `Wastes` nicht. Ein
allgemeiner Abzug von 2 Punkten je striktem `{C}`-Symbol bildet diesen
Opportunitätspreis ab, ohne `{C}`-Karten zu verbieten; `{W/C}` und `{2/C}` sind
ausgenommen.

| Metrik | Castability | Abschluss | Delta |
|---|---:|---:|---:|
| Early Play T2 | 93 % | 94 % | +1 pp |
| Early Play T3 | 95 % | 96 % | +1 pp |
| Goldfish-Schaden | 24,84 | 24,94 | +0,10 |
| Killrate bis Zug 5 | 65 % | 66 % | +1 pp |
| Token-Board | 9,02 | 9,10 | +0,08 |
| Manabasis | 22 Plains + 2 Wastes | 24 Plains | stärkerer Kern |

Die Abschlussliste enthält wieder zwei `Battle Menu`, drei `Okoye` und keine
nur marginal lohnende `{C}`-Karte. Deck-Hash:
`133e45be5a4ca94dc6bb8dddeb6c811db9e2889ced915f54c018898441668815`.

## Validierung

- Gezielte Mana-/Castability-Regressionen: 43 bestanden.
- Lokale Gesamtsuite: 325 bestanden in 44,76 s.
- Fast-Validierung: PASS; 5 Archetypen, 6 Matchups, 0 Regressionen.
- Benchmarks Burn/Tokens/Artifacts/Control/Mill: `83/98/90/85/80`.
- Token Opening Hands: Seed `1701`, 100 Hände, Keepability/Plan `77/77 %`,
  T2/T3 `94/96 %`, Mana-/Farbfehler `22/0 %`.
- Arena: 60 Mainboard, 15 Sideboard; Import erfolgreich.
- BO3 Token gegen Burn/Artifacts/Mill: `48/98/100 %`; Game One
  `0/70/100 %`, Postboard `62/75/100 %`.
- Token-Paket: 35 Maker, 30 sofortige Maker, 22 Multi-Maker, 7 Anthems,
  0 Outlets; keine False Positives.

## GitHub Actions

| Zyklus | Run-ID | Workflowtitel | Tests | Laufzeit | Artefakt |
|---|---:|---|---:|---:|---|
| Castability | 30853849259 | Token Go Wide – Castability | 322 | 4:12 | global-calibration-pr-83 |
| Agent Instructions | 30854816334 | Token Go Wide – Agent Instructions | 322 | 5:30 | global-calibration-pr-84 |
| Mana Strain | 30856406328 | Token Go Wide – Mana Strain | 325 | 3:59 | global-calibration-pr-85 |

Beim letzten Lauf wurden alle 447 Logzeilen sowie alle 49 Artefaktdateien
geprüft. Die fachlichen JSON-Dateien sind semantisch identisch zum lokalen
Ergebnis. Einzige Infrastrukturwarnung ist die bekannte Erzwingung von Node 24
für Actions, die noch Node 20 deklarieren.

## KGB-Entscheidung und Risiken

**Keine neue KGB.** Der frühere stabile Token-Kern wurde reproduzierbar
wiederhergestellt und die Castability fachlich korrigiert, aber die verbindliche
v2-Baseline bleibt gemäß Repository-Entscheidung `baseline: none`.

Alternative Erklärung: Der messbare Gewinn kann primär aus der konkreten
Rangfolge von `Battle Menu`/`Okoye` gegen `Warping Wail` stammen. Der allgemeine
Malus bleibt deshalb klein und lässt hochwertige `{C}`-Karten weiterhin zu.
Reale Spiele wurden nicht durchgeführt. Die Diagnose meldet außerdem 100 %
Strategy Commitment, aber 0 % wiederholbare Engine; das ist noch keine belegte
Regression und wurde nicht spekulativ geändert.

## Genau ein nächster Schritt

Die Diskrepanz zwischen 100 % Strategy Commitment und 0 % wiederholbarer
Go-Wide-Engine als isolierte Diagnose untersuchen und erst bei belegter Ursache
einen neuen Codezyklus starten.
