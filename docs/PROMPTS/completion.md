# Calibration Completion Prompt

Nutze diesen Prompt am Ende einer zeitlich begrenzten Kalibrierungsrunde.

1. Beende keine laufende CI gewaltsam.
2. Starte keine neue Codeänderung mehr.
3. Prüfe Branch-Head, PR, letzte Commits, Workflow-Run-IDs, Jobs, Logs und Artefakte.
4. Führe vollständige Tests und nach Möglichkeit die Full-Validierung aus.
5. Aktualisiere Logbuch, Roadmap, Entscheidungen, bekannte Probleme und Meta-Wissen.
6. Dokumentiere bestätigte und widerlegte Hypothesen sowie die Confidence.
7. Prüfe, ob die Spezifikation aufgrund belegter Erkenntnisse geändert werden muss. Falls ja, aktualisiere auch das Spezifikations-Changelog.
8. Entferne temporäre Zeitplan-Trigger. `workflow_dispatch` bleibt erhalten.
9. Erstelle einen Abschlussbericht mit:
   - Commits und Run-IDs
   - Qualitätsentwicklung je Archetyp
   - Regressionen und Risiken
   - produktiven und No-Change-Zyklen
   - nächster Priorität
   - kurzem Folgeauftrag für die nächste Runde

Erfinde keine Ergebnisse. Ein Lauf mit vielen Checks, aber ohne Entwicklungsfortschritt ist ausdrücklich als nicht produktiv zu bewerten.
