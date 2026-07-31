# Thun Format Deckbuilder

Ein Deckbuilder für das Magic Club Thun Clubformat.

## Unterstützte Archetypen

```bash
thun-deckbuilder build burn --colors R
thun-deckbuilder build tokens --colors W
thun-deckbuilder build artifacts --colors U R
thun-deckbuilder build shrines --colors W U B R G
thun-deckbuilder build mill --colors U B
```

Mit `--benchmark` wird zusätzlich geprüft, ob das generierte Deck nicht nur eine passende Manakurve und Rollenverteilung besitzt, sondern auch genügend archetypische Kernkarten enthält:

```bash
thun-deckbuilder build artifacts --colors U R --benchmark
thun-deckbuilder build shrines --colors W U B R G --benchmark
thun-deckbuilder build mill --colors U B --benchmark
```

Die kalibrierten Strategien priorisieren ihre eigentliche Win Condition. Generischer Kartennachschub und Removal sind optionale Ergänzungen und dürfen die Artefakt-, Schrein- oder Mill-Dichte nicht verdrängen. Shrine und Mill nehmen als Support bevorzugt günstige Karten bis Mana Value 3 auf.
