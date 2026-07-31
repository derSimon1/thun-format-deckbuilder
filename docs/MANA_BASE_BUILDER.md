# Mana Base Builder – Paket 6

Der Mana Base Builder ergänzt erzeugte Decks um eine nachvollziehbare, konservative Basisland-Verteilung.

## Verhalten

- Farbige Manasymbole werden direkt aus den Manakosten gezählt.
- Frühe Anforderungen bis Mana Value 2 werden stärker gewichtet.
- Hybrid- und phyrexianische Symbole werden berücksichtigt.
- Ein- und mehrfarbige Decks erhalten eine reproduzierbare Basisland-Verteilung.
- Jede im Deck benötigte Farbe erhält mindestens eine Quelle.
- Die Kurve liefert eine Empfehlung für die Länderzahl; bestehende Profile können weiterhin eine feste Länderzahl vorgeben.

## Ausgabe

`GeneratedDeck` enthält nun:

- `mana_base`: konkrete Basisländer und Mengen
- `mana_quality`: Quellenbedarf, Empfehlung und Score

Der normale Deckbericht zeigt die Länder einzeln sowie einen Mana-Score. Der allgemeine Deck-Quality-Score berücksichtigt die Manabasis mit 15 Prozent.

## Grenzen dieser Version

Diese Version verwendet bewusst nur Basisländer. Dual Lands, Utility Lands, Taplands und archetypspezifische Länder folgen später, sobald die Kartenbewertung und Benchmark-Decks stabil sind.
