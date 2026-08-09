# Meta Analysis Prompt

Ziel: externe und interne Referenzdaten in allgemeine Builder-Regeln übersetzen.

1. Lies `docs/SPECIFICATION.md`, `docs/META.md`, `docs/ROADMAP.md` und `docs/KNOWN_ISSUES.md`.
2. Analysiere nur Quellen, die zum Auftrag passen: erfolgreiche Standard-/Pioneer-Listen, Turnierergebnisse, Primer, Sideboard-Guides, Clubtests und interne Benchmarks.
3. Kopiere keine Deckliste blind. Extrahiere stattdessen:
   - Hauptspielplan
   - Kurve
   - Engine-Dichte
   - Finish-Dichte
   - Interaktion
   - Card Advantage
   - typische Matchup-Stärken und -Schwächen
4. Trenne Formatunterschiede sauber vom allgemeinen strategischen Muster.
5. Dokumentiere jede neue Erkenntnis mit Quelle/Testbasis, abgeleiteter Regel, betroffenen Archetypen und Confidence in `docs/META.md`.
6. Formuliere höchstens drei testbare Builder-Hypothesen für einen späteren Kalibrierungslauf.
7. Ändere in diesem Analyseauftrag keinen Produktionscode.
8. Aktualisiere bei neuen bestätigten Erkenntnissen Logbuch, Roadmap oder bekannte Probleme.

Tokens werden getrennt als Go Wide, Value Tokens und Aristocrats betrachtet. Commander-spezifische Muster dürfen nicht ungeprüft auf das 60-Karten-Thun-Format übertragen werden.
