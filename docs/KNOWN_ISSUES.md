# Known Issues

## KI-001 – Token-Subarchetypen fehlen

**Status:** offen  
**Priorität:** hoch

Go Wide, Value Tokens und Aristocrats werden noch nicht zuverlässig als unterschiedliche Hauptpläne erkannt. Dadurch kann Rollen-Mischmasch zu positiv bewertet werden.

## KI-002 – Strategy Commitment ist unzureichend

**Status:** offen  
**Priorität:** hoch

Der Builder kann viele passende Rollen zählen, ohne zu prüfen, ob diese Rollen gemeinsam denselben Spielplan unterstützen.

## KI-003 – Engine Density und Finish Density fehlen als explizite Qualitätsmerkmale

**Status:** offen  
**Priorität:** hoch

Es fehlt eine robuste Unterscheidung zwischen Karten, die den Plan wiederholbar antreiben, und Karten, die das Spiel tatsächlich abschließen.

## KI-004 – Vergleichsbaseline kann `none` sein

**Status:** offen  
**Priorität:** mittel

Der Regressionsbericht besitzt nicht immer eine belastbare vorherige Baseline. Dadurch sind Verbesserungen und Rückschritte schwerer einzuordnen.

## KI-005 – Matchups sind teilweise unrealistisch extrem

**Status:** offen  
**Priorität:** mittel

Token-Matchups zeigten unter anderem 0 % gegen Burn und 100 % gegen Mill. Das kann echte Schwächen anzeigen, muss aber gegen Simulationsvereinfachungen und echte Clubtests geprüft werden.

## KI-006 – Zeitgesteuerte GitHub-Runs sind nicht zuverlässig genug

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

Über Nacht liefen nur drei sichtbare Workflows, obwohl deutlich mehr Zeitplantermine möglich waren. Cron darf deshalb nicht als Entwicklungsantrieb verwendet werden.

## KI-007 – Zu defensive Automationsaufträge können Fortschritt blockieren

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

Die Nachtaufgaben wiederholten Sicherheitsprüfungen, ohne Code zu verändern oder die nächste Hypothese verbindlich vorzubereiten.

## KI-008 – Dokumentation kann hinter Code zurückbleiben

**Status:** offen  
**Priorität:** hoch

Vor Version 1.0 lagen zentrale Erkenntnisse nur in Chats, Commits und Workflowlogs. Künftige Zyklen müssen relevante Dokumente verpflichtend aktualisieren.
