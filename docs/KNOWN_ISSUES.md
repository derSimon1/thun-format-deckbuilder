# Known Issues

## KI-001 – Token-Subarchetypen sind noch nicht spielerisch kalibriert

**Status:** teilweise gelöst  
**Priorität:** hoch

Go Wide, Value Tokens und Aristocrats werden vor der Kartenauswahl unterschieden und planabhängig bewertet. Noch offen ist der belastbare Vergleich realer Builder-Ausgaben anhand planfähiger Starthände, Matchups und Clubdaten.

## KI-002 – Strategy Commitment ist noch tokenspezifisch

**Status:** teilweise gelöst  
**Priorität:** mittel

Ein kopiengewichteter Commitment-Bericht erkennt planprägende, planfremde und neutrale Token-Karten. Die Metrik ist noch nicht archetypenübergreifend in den allgemeinen Qualitätsbericht integriert.

## KI-003 – Engine Density ist teilweise vorhanden; Finish Density fehlt

**Status:** teilweise gelöst  
**Priorität:** hoch

Token-Engines werden von einmaligem Material getrennt. Eine archetypenübergreifende Engine-Abstraktion und eine robuste Finish-/Wincondition-Erkennung fehlen weiterhin.

## KI-004 – Keine vollständig qualifizierte v2-KGB

**Status:** offen  
**Priorität:** hoch

Run `30792560878` auf Commit `31f6c1e053976435481c07ab2098430bc2a45471` ist technisch grün und dient als v2-Bootstrap-Vergleichsstand. Er ist keine v2-KGB, weil der Validator noch Shrines statt Control verwendet, die Regression-Baseline `none` meldet und noch keine 100 planabhängigen Rohhände speichert.

## KI-005 – Matchups sind teilweise unrealistisch extrem

**Status:** offen  
**Priorität:** mittel

Token-Matchups zeigten unter anderem 0 % gegen Burn und 100 % gegen Mill. Das kann echte Schwächen anzeigen, muss aber gegen Simulationsvereinfachungen und echte Clubtests geprüft werden.

## KI-006 – Zeitgesteuerte GitHub-Runs sind nicht zuverlässig genug

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

Cron darf nicht als Entwicklungsantrieb verwendet werden. Mehrstundenläufe arbeiten kontinuierlich; GitHub Actions validiert Commits.

## KI-007 – Zu defensive Automationsaufträge können Fortschritt blockieren

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

No-Change-Zyklen müssen Stopgrund, Erkenntnis und nächsten ausführbaren Schritt dokumentieren. Nach zwei gleichen Ursachen wird die Priorität gewechselt.

## KI-008 – Dokumentation kann hinter Code zurückbleiben

**Status:** bestätigt  
**Priorität:** Prozessregel umgesetzt

Development System v2.0 verlangt Logbook-, Roadmap- und KGB-Entscheidungen pro Zyklus. Der Konsistenz-Check bleibt dennoch Pflicht.

## KI-009 – Pflichtvalidator verwendet noch Shrines statt Control

**Status:** bestätigt  
**Priorität:** hoch

Der Fast-/Full-Validator erzeugt aktuell Burn, Tokens, Artifacts, Shrines und Mill. Damit widerspricht die ausführbare Validierung der v2.0-Referenzgruppe Burn, Tokens, Artifacts, Control und Mill. Bis zur Control-Integration darf kein Lauf als vollständig qualifizierte v2-KGB gelten.

## KI-010 – Planabhängige Starthandrollen beruhen teilweise auf Rollen und Auswahlgründen

**Status:** offen  
**Priorität:** mittel

`DeckEntry` enthält derzeit keinen vollständigen Oracle-Text. Der `OpeningHandPlanReport` muss deshalb Rollen, Typzeile und Auswahlgründe verwenden. Ungewöhnlich formulierte Karten oder falsch erkannte Rollen können dadurch als Enabler, Engine, Payoff, Finisher oder Interaktion übersehen werden.
