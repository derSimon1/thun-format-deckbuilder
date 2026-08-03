# Roadmap

## Development System v2.0 / Prompt 2.1

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten ausführbaren Schritt.

## Globale Grundlagen

- [x] Fast-Validierung und Cache
- [x] genau 100 reproduzierbare Starthände je Deck, Seed 1701
- [x] Opening-Hand-, Goldfish-, Benchmark-, Matchup- und BO3-Berichte
- [x] Manafehler-Invariante
- [x] Control als fünfter Referenzarchetyp, Benchmark 85
- [x] Phrase-first-Sideboardklassifikation und Diagnoseartefakte
- [x] zentrale Mill-Quellendefinition und Poolkapazität

## Token-Fokus – Builder und Messung

- [x] Kreatur-Token von Nichtkreatur-Tokens getrennt
- [x] echte Outlets und Death-Payoffs getrennt
- [x] 43 Rollen-Fehlpositive entfernt
- [x] präzise Planrollen und kapazitätsgeprüfte Mindestpakete
- [x] automatische Planwahl auf Value Tokens
- [x] Benchmark 91, Material 33, Fehlpositive 0
- [x] Keepability/Planfähigkeit 77/76 %
- [x] Immediate-, Repeatable-, Conditional- und Death-Produktion
- [x] Goldfish neu kalibriert: 14,66 Schaden, 27 % Killrate, Board 5,30
- [x] Mono-White-Poolkapazität je Produktionsmodus gemessen

## Run-61-Poolkapazität

| Modus | Karten | maximale Kopien |
|---|---:|---:|
| sofort | 102 | 306 |
| bedingt | 51 | 153 |
| Death | 14 | 42 |
| bisher wiederholbar | 2 | 6 |

Die zwei bisherigen Repeatable-Karten sind `Cathar's Call` und `Whirlermaker`. Aktivierte und automatische Produktion müssen vor einer Builderänderung getrennt werden.

## Activated-versus-Repeatable-Zyklus

- [x] aktivierte Tokenfähigkeit über Kosten-vor-Doppelpunkt erkennen
- [x] generische und farbige Aktivierungsmana konservativ zählen
- [x] Modus `activated` und Aktivierungskostenmarker implementieren
- [x] Unit-Tests für Whirlermaker und Kapazitätsgruppen grün
- [x] Run 62 gestartet und vollständig ausgewertet
- [ ] Metadatenfilter-Hotfix vollständig grün bestätigen
- [ ] Artifact-Kapazität für `activated` und `repeatable` auswerten

## Run-62-Befund

- 297 Unit-/Integrationstests bestanden
- Fast brach nur bei Tokens ab
- Ursache: `token_activation_mana_*` wurde als Funktionsrolle normalisiert
- Burn 83, Artifacts 90, Control 85 und Mill 80 unverändert
- keine Builder- oder Go-Wide-Aussage aus diesem roten Run ableiten

## Erfolgskriterien Hotfix

- [ ] vollständige Testsuite grün
- [ ] Fast unter zehn Minuten
- [ ] Tokens Benchmark 91 und Deck-Hash unverändert
- [ ] Hände weiterhin 77/76 %
- [ ] Goldfish weiterhin 14,66 Schaden und 27 % Killrate
- [ ] `Whirlermaker` als aktiviert mit Mana 4 ausgewiesen
- [ ] automatische Repeatable-Kapazität separat dokumentiert
- [ ] andere vier Benchmarks unverändert

## Entscheidung nach grünem Hotfix

### Automatische Repeatable-Kapazität unter sechs Kopien

- [ ] `token_repeatable_maker` nur automatischen Triggern zuweisen
- [ ] Value-Mindestziel nicht künstlich auf bedingte oder aktivierte Karten ausweiten
- [ ] automatische Planwahl anhand garantierter Produktionskapazität neu bewerten
- [ ] Go Wide über garantierte Sofort-/Multi-Maker und Anthem-/Evasion-Payoffs definieren
- [ ] Go-Wide-Deck gegen den Run-61-Value-Stand vergleichen

### Automatische Repeatable-Kapazität mindestens sechs Kopien

- [ ] Value-Profil auf echte automatische Engines verpflichten
- [ ] aktivierte Quellen nur als sekundäre Value-Unterstützung bewerten
- [ ] explizites Go-Wide-Referenzdeck unabhängig erzeugen und vergleichen

## Danach

1. Go Wide, Value Tokens und Aristocrats als separate Referenzdecks erzeugen.
2. Matchupmodell erst auf belastbaren Produktionsdaten weiterentwickeln.
3. Mill-Kompositionsschritt mit 18 Quellen und 6 echten Engines abschließen.
4. relevante Control-Antworten aus konkreten Gegnerdecks ableiten.
5. belastbare Regression-Baseline statt `baseline: none`.
6. erste v2-KGB und Club-/Meta-Benchmark.

## Definition of Done für den aktuellen Go-Wide-Lauf

- Activated-/Repeatable-Messung technisch grün
- automatische Planwahl verwendet dieselbe Produktionsdefinition
- Go Wide besitzt frühe garantierte Maker, Multi-Maker und Anthem-/Evasion-Payoffs
- Full- und Sparse-Pool funktionieren
- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs Matchups
- genau 100 Hände je Deck mit Seed 1701
- andere vier Benchmarks ohne unbegründete Regression
- Arena-Import des besten bestätigten Go-Wide-Decks verfügbar
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
