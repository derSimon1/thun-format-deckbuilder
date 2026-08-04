# Decisions

Dauerhafte Architektur- und Prozessentscheidungen. Neue Einträge werden nicht überschrieben, sondern ergänzt oder ausdrücklich ersetzt.

## D-001 – GitHub Actions ist Validator, nicht Entwicklungsagent

**Datum:** 2026-08-03  
**Status:** akzeptiert

GitHub Actions führt Tests und Validierungen aus, entwickelt aber keine Verbesserungen. Produktiver Fortschritt entsteht durch einen konkreten Entwicklungszyklus mit Hypothese, Änderung, Commit und anschließender CI.

## D-002 – Kein Cron als primärer Entwicklungsantrieb

**Datum:** 2026-08-03  
**Status:** akzeptiert

Zeitgesteuerte GitHub-Workflows dürfen ergänzend validieren, gelten aber weder als Entwicklungsfortschritt noch als zuverlässiger Motor einer Kalibrierung.

## D-003 – Versionierte Spezifikation als Single Source of Truth

**Datum:** 2026-08-03  
**Status:** akzeptiert

Kalibrierungsregeln leben im Repository. Chat-Aufträge referenzieren auf Spezifikation und Prompt, statt lange Anweisungen zu kopieren.

## D-004 – Ein zusammenhängendes Änderungspaket pro Zyklus

**Datum:** 2026-08-03  
**Status:** akzeptiert

Pro Zyklus werden höchstens drei eng gekoppelte Änderungen derselben Ursache in genau einem Commit gebündelt.

## D-005 – No-Change-Zyklen müssen produktiv sein

**Datum:** 2026-08-03  
**Status:** akzeptiert

Ein Zyklus ohne Commit muss Stopgrund, geprüfte Hypothese, Erkenntnis und nächsten ausführbaren Schritt festhalten. Nach zwei gleichen No-Change-Zyklen wird die Priorität gewechselt.

## D-006 – Tokens werden über Subarchetypen modelliert

**Datum:** 2026-08-03  
**Status:** akzeptiert

Token-Decks werden nicht nur über Rollenanzahlen bewertet. Vor Kartenauswahl wird ein Hauptplan aus Go Wide, Value Tokens oder Aristocrats bestimmt.

## D-007 – Shrines bleiben vorerst Regressionstest

**Datum:** 2026-08-03  
**Status:** ersetzt durch D-009

Diese frühere Entscheidung führte Shrines noch als wiederkehrenden Regressionstest. Sie ist für Development System v2.0 nicht mehr maßgeblich.

## D-008 – Fast und Full bleiben getrennt

**Datum:** 2026-08-03  
**Status:** akzeptiert

Fast dient kurzen Entwicklungszyklen und soll unter zehn Minuten bleiben. Full wird manuell oder am Ende einer Runde ausgeführt.

## D-009 – Control ersetzt Shrines als allgemeinen Referenzarchetyp

**Datum:** 2026-08-03  
**Status:** akzeptiert

Die fünf allgemeinen Referenzarchetypen sind Burn, Tokens, Artifacts, Control und Mill. Control prüft relevante Interaktion, Stabilisierung und eine belastbare Wincondition. Shrines ist kein Pflicht- oder Referenzarchetyp mehr.

**Ersetzt:** D-007.

## D-010 – Known Good Baseline ist der verbindliche Sicherungspunkt

**Datum:** 2026-08-03  
**Status:** akzeptiert

Jeder Zyklus beginnt mit der letzten dokumentierten Known Good Baseline und endet mit `neue KGB`, `keine neue KGB` oder `Regression`.

Grüne CI allein qualifiziert keinen Commit als KGB. Solange keine v2-KGB existiert, wird ein belegter grüner Stand nur als Bootstrap- oder Legacy-Vergleichsstand geführt.

## D-011 – Mehrstundenbetrieb ohne separate 15-Minuten-Aufgaben

**Datum:** 2026-08-03  
**Status:** akzeptiert

Ein externer Auftrag setzt die Laufzeit `X` in Stunden. Innerhalb desselben Laufs werden so viele vollständige Kalibrierungszyklen wie sinnvoll möglich durchgeführt.

Ein neuer Zyklus wird nur begonnen, wenn er innerhalb der Restzeit vollständig implementiert, getestet, validiert und dokumentiert werden kann.

## D-012 – Artifact-first-Auswertung vor weiterer Optimierung

**Datum:** 2026-08-03  
**Status:** akzeptiert

Nach jedem Workflow werden nicht nur Status und Testzahl geprüft. Das relevante Artefakt wird einmal heruntergeladen und maschinenlesbar ausgewertet. Fachliche Aussagen stützen sich auf Decklisten, Rohhände, Rollen, Sideboard-Pläne, Matchups und BO3, nicht allein auf eine grüne Conclusion.

Wiederholte identische Statusabfragen ohne neue erwartbare Information gelten nicht als produktive Arbeit.

**Begründung:** Mehrere grüne Runs enthielten weiterhin 0 Control-Finisher beziehungsweise falsche `Tormod's Crypt`-Einwechslungen.

## D-013 – Verbindliche Abschlussreserve und Zyklusvertrag

**Datum:** 2026-08-03  
**Status:** akzeptiert

Bei einem Drei-Stunden-Lauf werden mindestens 30 Minuten für letzten Workflow, Artefaktprüfung, Logbook, Roadmap und Abschlussbericht reserviert.

Vor jeder Codeänderung werden Ursache, Hypothese, erwartete Metriken, Invarianten, Erfolgskriterium, Abbruchkriterium und Zeitbedarf festgelegt. Ein Zyklus wird nicht gestartet, wenn Implementierung plus CI-/Artefaktpuffer plus Abschlussreserve nicht mehr in die Restzeit passen.

## D-014 – Spezifische Signale vor breiten Rollen

**Datum:** 2026-08-03  
**Status:** akzeptiert

Bei fachlicher Klassifikation haben spezifische Oracle-Text-Signale Vorrang vor breiten Rollen wie `removal`, `card_draw` oder `finisher`. Breite Rollen dienen als Fallback, wenn keine spezifische Kategorie erkannt wurde.

**Begründung:** `Tormod's Crypt` wurde aufgrund des Wortes `exile` global als Removal erkannt und dadurch zusätzlich fälschlich als Anti-Aggro-Sideboardkarte klassifiziert.

## D-015 – Echte farblose Manaanforderungen bleiben eigenständig

**Datum:** 2026-08-03
**Status:** akzeptiert

`{C}` ist eine eigene Zahlungsanforderung und darf weder durch farbiges Mana noch durch eine generische Wildcard-Quelle erfüllt werden. Mana-Parser, Candidate Eligibility, Basic-Land-Verteilung und Opening-Hand-Castability verwenden dieselbe zentrale Definition.

Eine `{C}`-Karte ist nur zulässig, wenn der konfigurierte Mana-Builder echte farblose Quellen erzeugen kann. Die Basic-Land-Manabasis verwendet dafür `Wastes` und reserviert mindestens so viele passende Quellen, wie ein einzelner Zauber an strikten gleichartigen Symbolen verlangt.

**Begründung:** Das frühere pauschale Verbot verhinderte legale, castbare Kandidaten. Eine bloße Entfernung des Verbots hätte dagegen unspielbare Karten ohne echte farblose Quellen zugelassen.

## D-016 – Strikte `{C}`-Kosten tragen einen Quellenspannungsbeitrag

**Datum:** 2026-08-04
**Status:** akzeptiert

Candidate Scoring zieht pro strikt erforderlichem `{C}`-Symbol 2 Punkte als
erklärbare `mana_strain` ab. Der Beitrag modelliert den Opportunitätspreis
dauerhaft gebundener echter Farblosquellen, ohne die Karte unzulässig zu machen.
Hybridkosten wie `{W/C}` und `{2/C}` lösen den Beitrag nicht aus, weil sie keine
echte farblose Quelle erzwingen.

**Begründung:** Nach D-015 wurde `Warping Wail` korrekt castbar, verdrängte aber
trotz leicht schlechterer Opening-Hand- und Goldfish-Metriken farbige
Go-Wide-Kandidaten. Eligibility beantwortet, ob eine Karte spielbar ist;
Candidate Scoring muss zusätzlich bewerten, ob die dafür gebundene Manabasis den
Nutzen rechtfertigt.

## D-017 – Engine-Pflicht ist planabhängig

**Datum:** 2026-08-04
**Status:** akzeptiert

Eine wiederholbare Engine ist für Value Tokens und Aristocrats eine
Funktionsvoraussetzung. Beim aggressiven Go-Wide-Plan ist sie dagegen eine
optionale Resilienzschicht; dessen Pflichtkern besteht aus frühen,
zuverlässigen Makern und realistischem Team-Scaling.

Die Engine Density wird für alle Pläne weiterhin numerisch ausgewiesen. Eine
fehlende Engine erzeugt aber nur dann eine Mangelwarnung, wenn der gewählte Plan
sie benötigt. `TokenPlan.requires_engine` ist die zentrale Definition; auch der
Opening-Hand-Bericht weist denselben Kontext explizit aus, während er den rohen
Engine-Zugang weiterhin misst.

**Begründung:** Die frühere universelle Warnung stellte 0 % Engine Density bei
100 % Go-Wide-Commitment als Widerspruch dar. Ein kontrollierter Einbau der
einzigen verfügbaren automatischen Mono-White-Engine verschlechterte die
Mehrseed-Metriken und bestätigte, dass die Warnung statt der Deckliste falsch
kalibriert war.

## D-018 – Go Wide benötigt einen frühen Maker-Pfad

**Datum:** 2026-08-04
**Status:** akzeptiert

Eine Go-Wide-Opening-Hand ist nur planfähig, wenn mindestens ein Token-Maker
bis Zug 2 tatsächlich castbar ist und bis Zug 3 ein zweiter Maker oder ein
Payoff zugänglich ist. Mehrere Drei-Mana-Planstücke, die einzeln bis Zug 3
castbar wären, bilden gemeinsam noch keine ausführbare Sequenz. Ein generischer
Zug-2-Spielzug ersetzt den frühen Maker nicht.

**Begründung:** Die frühere mengenbasierte Prüfung klassifizierte vier der 100
Referenzhände als planfähig, obwohl bis Zug 3 höchstens ein Token-Planstück
ausgespielt werden konnte. Die Spezifikation verlangt frühe Spielbarkeit und
einen realistischen Zug-1-bis-Zug-3-Pfad gemeinsam.

## D-019 – Transformationsgesperrte Rückseiten sind nicht sofort verfügbar

**Datum:** 2026-08-04
**Status:** akzeptiert

Oracle-Text einer Rückseite, die erst durch Transformieren, Craft, Daybound
oder das Besiegen einer Battle erreichbar wird, zählt nicht als Effekt des
normalen Vorderseiten-Casts. Die gemeinsame Kartenanalyse stellt dafür
`cast_accessible_oracle_text` bereit; Token-Paket, Produktionsmodus und
Candidate Scoring verwenden dieselbe Sicht. Modal castbare Rückseiten bleiben
zugänglich.

**Begründung:** Drei `Clay-Fired Bricks // Cosmium Kiln` wurden beim
Zwei-Mana-Cast als sechs sofortige Tokens und drei permanente Anthem-Effekte
modelliert. Tatsächlich sucht die Vorderseite nur ein Plains und gibt 2 Leben;
Tokens und Anthem liegen hinter Craft für `{5}{W}{W}`.

## D-020 – Sideboard-Pakete werden mengen- und zielbewusst bewertet

**Datum:** 2026-08-04
**Status:** akzeptiert

Der Sideboard-Optimierer prüft pro Kartenname zusammenhängende Mengen von eins
bis zur verfügbaren Kopienzahl und zum verbleibenden Swap-Budget. Dadurch kann
er Pakete erkennen, deren erste Einzelkopie wegen Rundung oder einer echten
Wirkungsschwelle noch keinen positiven Messwert erzeugt. Kandidaten werden
gegen unterschiedliche Cut-Namen statt mehrfach gegen dieselben expandierten
Kopien verglichen.

Lebensgewinn, der zwingend an „destroy/exile target“ gekoppelt ist, gilt nicht
als eigenständige Burn-Stabilisierung. Modale Karten mit einer ohne Ziel
wählbaren Lebensgewinnoption bleiben Schutz. Ungecachte Kandidatendecks nutzen
das Sample- und Seed-Budget des Matchup-Laufs.

**Begründung:** Drei `Dawnbringer Cleric` verbessern den isolierten
Postboard-Wert gemeinsam, während eine Kopie beim gerundeten Ausgangswert 0 %
bleibt. Die alte Einzelkartensuche konnte diese Schwelle nie überschreiten.
Eine erste Korrektur boardete zusätzlich `Sanctify` gegen ein Burn-Deck ohne
Artefakte oder Enchantments ein; dessen Lebensgewinn ist ohne legales Ziel
nicht verfügbar.

## D-021 – Effektkontext endet nicht am Satzpunkt

**Datum:** 2026-08-04
**Status:** akzeptiert

Oracle-Newlines und modale Flächentrenner begrenzen Fähigkeiten; Satzpunkte
innerhalb derselben Fähigkeit tun das nicht. Folgesätze und Reminder-Text
erben deshalb Trigger-, Zahlungs- und Zielkontext. Modale Bullet-Effekte erben
den Kontext ihres „choose one“-Headers.

Spätere Saga-Kapitel sind ohne Read-ahead verzögert. Read-ahead darf ein
späteres Kapitel beim Eintritt wählen und bleibt daher sofort zugänglich.
Self-ETB-Token sind Cast-Sofortproduktion; Attack-, Payment-, Landfall-,
Leave- und sonstige bedingte Trigger nicht.

Ein sofortiger Go-Wide-Anthem muss allen relevanten Kreaturen beim Cast echten
Power-Zuwachs oder globale +1/+1-Counter geben. Ziel-, Namens- und
Unterklassenbegrenzungen sowie Aktivierungs-, Spree- und Solved-Gates sind
nicht sofort global. Temporäre Team-Buffs enden im Goldfish mit dem Zug.

**Begründung:** Der Satzsplit isolierte den Reminder-Satz von
`Descendant of Storms` von dessen Angriffs-/Payment-Trigger. Mehrere begrenzte
Countertexte galten als globale Anthems, und temporäre `Charge`-Effekte wurden
über alle Folgezüge akkumuliert. Read-ahead bei `Love Song of Night and Day`
ist dagegen eine echte Ausnahme: Kapitel II kann beim Eintritt gewählt werden.

## D-022 – Zusätzliche Cast-Kosten sind Simulationsmetadaten

**Datum:** 2026-08-04
**Status:** akzeptiert

Zusätzliche Kreaturen-Opferkosten werden einmal aus dem cast-zugänglichen
Oracle-Text abgeleitet und als maschinenlesbarer Marker bis zum finalen
Deckeintrag transportiert. Der Marker ist keine funktionale Deckrolle. Der
Goldfish darf die Karte nur mit genügend vorhandenen Körpern wirken und
verbraucht diese vor Anwendung des Karteneffekts; noch nicht angriffsbereite
Körper werden zuerst geopfert.

SQLite-Gesundheitsprüfungen schließen ihre Verbindung explizit, bevor ein
atomarer Datenbankersatz versucht wird. Ein Transaktions-Kontext allein gilt
nicht als Ressourcenfreigabe.

**Begründung:** `Duty Beyond Death` war auf leerem Board wirkbar und ließ den
eigentlich geopferten Körper weiter angreifen. Beim anschließenden realen
Fast-Lauf blockierte außerdem die Gesundheitsprüfung unter Windows ihren
eigenen Datenbankersatz, weil `sqlite3.Connection.__exit__` nicht schließt.

## D-023 – Token-Präzisionssichten verfeinern Rollen und Synergien gemeinsam

**Datum:** 2026-08-04
**Status:** akzeptiert

Die Token-spezifische Kartenansicht entfernt oder ergänzt präzise
Opferoutlet-Rollen und `sacrifice_outlet`-Synergie-Tags gemeinsam. Als
Kreaturen-Outelt gilt nur eine aktivierte Fähigkeit, deren Kosten ausdrücklich
eine Kreatur opfern; ein Wort „creature“ in einem benachbarten Ausrüstungssatz
genügt nicht.

**Begründung:** `Duty Beyond Death` hatte keine Outlet-Rolle mehr, erhielt im
Auswahltrace aber weiterhin den vollen Fodder-Bonus. Nach Entfernung dieses
Tags wurde `Citizen's Crowbar` durch das zu breite Kostenfenster als Outlet
eingestuft, obwohl es nur sich selbst opfert.

## D-024 – Cast-Bedingungen sind zentrale Simulationsmetadaten

**Datum:** 2026-08-04
**Status:** akzeptiert

Nur eine aktivierte Fähigkeit mit einem expliziten Opfer im Kostenteil vor dem
Doppelpunkt gilt als wiederverwendbares Opfer-Outlet. Eine zusätzliche
Opfer-Cast-Kostenklausel ist stattdessen eine Castability-Anforderung und
verbraucht das Material. Exakte Ziel-Lebenspunkte werden als enges Cast-Fenster
transportiert; der zugehörige Schaden darf nur in diesem Fenster entstehen.

Die Metadaten werden einmal aus cast-zugänglichem Oracle-Text abgeleitet und
auf den finalen Deckeintrag übertragen. Scoring und Goldfish verwenden dieselbe
Definition. Das Burn-Scoring berechnet geopfertes Material als zusätzlichen
Opportunitätspreis und gibt eng gegatetem Schaden nur reduzierten Auswahlwert.

**Begründung:** `Heartfire` wurde zugleich als Outlet und als ohne Board
wirkbarer Vier-Schaden-Zauber behandelt; `Hidetsugu's Second Rite` erhielt
vollen Zehn-Schaden-Wert ohne das Fenster bei exakt 10 Leben. Beide Annahmen
erzeugten falsche Synergien, illegale Sequenzen und aufgeblähte Goldfish-Werte.

## D-025 – Mill-Engines benötigen wiederholbaren Effektzugang

**Datum:** 2026-08-04
**Status:** akzeptiert

Eine permanente Typzeile macht einen Mill-Effekt nicht wiederholbar. Engine
ist nur ein wiederkehrender Trigger oder eine wiederverwendbare Aktivierung im
gleichen Effektsegment. ETB-, Adventure-, Saga- und andere Einmaleffekte
bleiben Quellen, aber keine Engines. Aktivierungen mit Selbstopfer, endlicher
Energie oder mehreren als Kosten getappten Permanenten liefern keinen
intrinsischen Wiederholdurchsatz; andere Fähigkeiten derselben Karte werden
separat bewertet.

Einmal- und Wiederholkarten werden als maschinenlesbare Durchsatzmarker an den
Deckeintrag gegeben. Mill-Scoring, Profil, Opening-Hand-Plan, Goldfish und
Diagnoseartefakt verwenden dieselben zentralen Signale. Bedingte Engines
beginnen im Goldfish frühestens im Folgezug; pauschales Fünf-Karten-Mill und
prozentuales Anwachsen bereits gemillter Karten entfallen.

**Begründung:** `Merfolk Secretkeeper` wurde wegen seiner Kreatur-Typzeile als
Engine gezählt. Drei `Persistent Petitioners` simulierten je zwölf Karten,
obwohl die betreffende Aktivierung vier Advisors als Kosten verlangt. Beides
verzerrte Auswahl, Planfähigkeit und Goldfish.

## D-026 – Control-Qualität ist eine Sequenz aus Antwort, Vorteil und Abschluss

**Datum:** 2026-08-04
**Status:** akzeptiert

Control verwendet eine strategiegebundene, zentrale Kartensicht. Eine
verlässliche Antwort muss im cast-zugänglichen Effektsegment einen gegnerischen
Plan tatsächlich unterbrechen; eigene Blink-/Friedhofseffekte und enge
Zustandsbedingungen sind keine universellen Antworten. Cycling und
Kartenauswahl sind kein echter Kartenvorteil. Ein Deck benötigt außerdem eine
belastbare Wincondition; Planeswalker werden dabei wie andere Finisher als
Bedrohung erfasst.

Profil, Candidate Scoring, Opening-Hand-Plan, Matchup-Simulation und
Diagnoseartefakt verwenden dieselben Control-Rollen. Die präzise Sicht bleibt
auf die Control-Strategie beschränkt, damit andere Archetypen ihre eigene
Rollensemantik und Auswahl nicht unbeabsichtigt ändern.

**Begründung:** Der frühere Champion meldete 71 % planfähige Hände, erreichte
unter der korrigierten Definition aber nur 33 %. Er zählte unter anderem
Siren's Ruse, Friedhofsexil, bedingte Schadens-Removal und Selection als
vollwertige Stabilisierung. Gleichzeitig ignorierte die Matchup-Heuristik
Planeswalker-Winconditions.
