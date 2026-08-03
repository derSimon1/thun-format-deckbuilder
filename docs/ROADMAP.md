# Roadmap

## Development System v2.0 / Prompt 2.1

Referenzarchetypen: Burn, Tokens, Artifacts, Control und Mill. Tokens werden zusätzlich als Go Wide, Value Tokens und Aristocrats bewertet. Jeder Zyklus endet mit KGB-Entscheidung, Reflexion und genau einem nächsten ausführbaren Schritt.

## Erledigte globale Grundlagen

- [x] Fast-Validierung, Cache, Opening-Hand-, Goldfish-, Matchup- und BO3-Berichte
- [x] genau 100 reproduzierbare Starthände je Referenzdeck, Seed 1701
- [x] Keepability, Early Play und Planfähigkeit getrennt
- [x] Manafehler-Invariante
- [x] Control als fünfter Referenzarchetyp, Benchmark 85 und sechs Finisher
- [x] fünf Pflichtarchetypen und sechs priorisierte Fast-Matchups
- [x] maschinenlesbare Sideboard-Diagnose und Phrase-first-Klassifikation
- [x] zentrale Mill-Quellendefinition, Poolkapazität und Messkompatibilität

## Aktueller Vier-Stunden-Lauf – Token-Fokus

### Token-Zyklus 1 – Paketdiagnose

- [x] Kreatur-Token von Food/Clue/Blood/Treasure trennen
- [x] wiederholbare Creature-Sacrifice-Outlets von One-Shot-Sacrifice trennen
- [x] Other-Creature-Death-/Drain-Payoffs von Self-Death-Value trennen
- [x] Deck- und Mono-White-Pooldiagnose erzeugen
- [x] Run 55 vollständig auswerten

**Run-55-Befund:** 14 echte Materialkopien, 9 Outletkopien, 3 Death-/Drain-Payoffs und 43 breite Rollen-Fehlpositive. Der Pool besitzt genügend Kapazität für alle drei Pläne.

### Token-Zyklus 2 – Präzise Planrollen und Komposition

- [x] präzise Tokenrollen vorbereiten
- [x] Planerkennung auf echte Kreatur-Token-/Outlet-/Death-Signale umstellen
- [x] Food-only und One-Shot-Sacrifice aus den planprägenden Rollen entfernen
- [x] planabhängige, kapazitätsgeprüfte Mindestpakete definieren
- [x] gezielte Plan-, Profil- und Rollenbereinigungstests vorbereiten
- [ ] vollständige CI und Artefakte auswerten

### Erfolgskriterien für Zyklus 2

- [ ] legal 60/15, Kopienlimit und Mono-White-Manabasis korrekt
- [ ] Fast-Lauf unter zehn Minuten
- [ ] finales Deck erfüllt die echten Mindestrollen seines gewählten Plans
- [ ] `token-packages.json` meldet keine breiten planprägenden Fehlpositive
- [ ] Commitment und 100-Hand-Klassifikation stimmen mit der Paketdiagnose überein
- [ ] Keepability und Manafehler verschlechtern sich nicht unbegründet
- [ ] Goldfish-Schaden beruht auf Kreatur-Tokens statt Food/Blood
- [ ] Matchups gegen Burn, Artifacts und Mill werden gegen Run 55 verglichen
- [ ] Burn, Artifacts, Control und Mill zeigen keine unbegründete Benchmarkregression

### Möglicher Token-Zyklus 3 – nur nach Artefaktevidenz

Falls der neue Builder einen kohärenten Go-Wide- oder Value-Plan erzeugt, aber Matchups weiterhin extrem bleiben:

- [ ] Token-Goldfish zählt tatsächliche Tokenanzahl statt pauschal zwei pro Maker
- [ ] Aristocrats-Schaden wird nur bei Material + Outlet + Death-/Drain-Payoff modelliert
- [ ] Token-Combat unterscheidet Kreatur-Tokens von Nichtkreatur-Tokens
- [ ] Matchupmodell trennt Boardentwicklung, Interaktion und Abschlussdruck

Falls der neue Builder weiterhin ein unvollständiges Paket erzeugt:

- [ ] exakte fehlende Rolle und Optimierungsschritt anhand Auswahltrace isolieren
- [ ] höchstens eine belegte Kompositionsursache korrigieren

## Pausierter Mill-Rückkehrpunkt

- [ ] mindestens 18 Mill-Quellen, Ziel 20
- [ ] mindestens 6 echte wiederholbare Engines, Ziel 8
- [ ] Komposition und Optimierer erhalten diese Dichte
- [ ] Benchmark und Opening-Hand-Analyse bleiben auf der zentralen Definition

## Danach

1. Token-Subarchetypen als separate Referenzdecks statt nur automatische Planwahl benchmarken
2. relevante Control-Antworten aus konkreten Gegnerdecks ableiten
3. Mill-Kompositionsschritt abschließen
4. Strategy Commitment und Engine Density archetypenübergreifend abstrahieren
5. Finish Density allgemein modellieren
6. belastbare Regression-Baseline statt `baseline: none`
7. erste vollständig qualifizierte v2-KGB
8. Meta- und Club-Benchmark

## Definition of Done für den aktuellen Token-Meilenstein

- zentrale Token-Paketdefinition in Diagnose, Planerkennung und Komposition identisch
- vollständige Testsuite und Fast-Validierung grün
- fünf Referenzarchetypen und sechs Matchups
- genau 100 Hände je Deck mit Seed 1701
- Token-Metriken gegen Run 55 verglichen
- keine unbegründete Regression anderer Referenzarchetypen
- KGB-Entscheidung, Reflexion und genau ein nächster Schritt dokumentiert
