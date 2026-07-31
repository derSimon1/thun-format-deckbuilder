# Benchmark System

Paket 8 ergänzt reproduzierbare Zielprofile für Deckqualität. Benchmarks beschreiben
Rollen-, Kurven- und Länderziele; sie sind bewusst keine exakten Decklisten.

## Enthaltene Profile

- `white_tokens`
- `mono_red_burn`
- `ub_mill`
- `ur_artifacts`
- `five_color_shrines`

Nur Burn und Tokens besitzen derzeit vollständige Generatorstrategien. Die übrigen
Profile sind bereits als Zieldefinitionen verfügbar und werden aktiviert, sobald
die entsprechenden Strategien implementiert sind.

## CLI

```bash
thun-deckbuilder build tokens --colors W --benchmark
thun-deckbuilder benchmark burn
```

Der Score setzt sich aus Rollen (60 %), Manakurve (25 %) und Länderzahl (15 %)
zusammen. Über- und Unterfüllung werden gleichermaßen sichtbar gemacht, damit ein
Deck nicht durch bloßes Überladen einer Rolle einen unrealistisch hohen Wert erhält.
