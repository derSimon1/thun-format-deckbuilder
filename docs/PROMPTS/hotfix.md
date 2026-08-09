# Calibration Hotfix Prompt

Verwende diesen Prompt ausschließlich bei roter CI oder einem eindeutig belegten Infrastrukturfehler.

1. Lies `docs/SPECIFICATION.md` und `docs/DECISIONS.md`.
2. Prüfe Branch-Head, aktive CI, Run-ID, fehlerhaften Job, Logs und Artefakte.
3. Identifiziere genau eine belegte Ursache.
4. Ändere nur das Nötigste zur Behebung dieser Ursache.
5. Ergänze einen Regressionstest, sofern sinnvoll.
6. Führe vollständige Testsuite und Fast-Validierung aus.
7. Prüfe unmittelbar vor Commit den Branch-Head erneut.
8. Erstelle genau einen Hotfix-Commit.
9. Verifiziere die neue Workflow-Run-ID und den grünen Abschluss.
10. Dokumentiere Ursache, Fix und Lesson Learned im Logbuch.

Keine Optimierung parallel zum Hotfix. Keine Dummy-Commits. Keine Grenzwertverschiebung ohne fachliche Begründung.
