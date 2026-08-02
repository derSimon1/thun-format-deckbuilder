from __future__ import annotations

import random
from dataclasses import dataclass

from thun_deckbuilder.deck_generator import DeckEntry, GeneratedDeck


@dataclass(frozen=True)
class GoldfishReport:
    archetype: str
    samples: int
    turns: int
    mulligan_rate_pct: int
    average_unused_mana: float
    average_spells_cast: float
    average_damage: float = 0.0
    kill_by_final_turn_pct: int = 0
    average_cards_milled: float = 0.0
    mill_out_by_final_turn_pct: int = 0
    average_artifacts_in_play: float = 0.0
    average_shrines_in_play: float = 0.0


def _signals(entry: DeckEntry) -> frozenset[str]:
    text = " ".join((entry.name, entry.type_line, *entry.roles, *entry.reasons)).lower()
    found: set[str] = set()
    if "burn" in text or "damage" in text:
        found.add("burn")
    if "mill" in text or "library into" in text:
        found.add("mill")
    if "artifact" in entry.type_line.lower():
        found.add("artifact")
    if "shrine" in entry.type_line.lower() or "shrine" in text:
        found.add("shrine")
    if "creature" in entry.type_line.lower():
        found.add("creature")
    roles = {role.lower() for role in entry.roles}
    if "token_maker" in roles:
        found.add("token_maker")
    if "anthem" in roles:
        found.add("anthem")
    if roles.intersection({"token_payoff", "evasion", "aristocrats_payoff"}):
        found.add("token_payoff")
    return frozenset(found)


def _is_keepable(cards: list[tuple[str, DeckEntry | None]]) -> bool:
    lands = sum(1 for kind, _ in cards if kind == "land")
    early = any(kind == "spell" and entry is not None and entry.mana_value <= 2 for kind, entry in cards)
    return 2 <= lands <= 4 and early


def _bottom_for_six(cards: list[tuple[str, DeckEntry | None]]) -> list[tuple[str, DeckEntry | None]]:
    lands = sum(1 for kind, _ in cards if kind == "land")
    if lands >= 5:
        index = next(i for i, (kind, _) in enumerate(cards) if kind == "land")
    elif lands <= 1:
        index = max(
            (i for i, (kind, _) in enumerate(cards) if kind == "spell"),
            key=lambda i: cards[i][1].mana_value if cards[i][1] is not None else 0,
        )
    else:
        index = max(
            range(len(cards)),
            key=lambda i: -1 if cards[i][0] == "land" else (cards[i][1].mana_value if cards[i][1] else 0),
        )
    return cards[:index] + cards[index + 1 :]


def _spell_value(entry: DeckEntry, archetype: str) -> tuple[int, float, str]:
    signals = _signals(entry)
    mana = max(1, int(entry.mana_value))
    if archetype == "burn":
        value = 3.0 if "burn" in signals else (1.5 if "creature" in signals else 0.5)
        return mana, value, "damage"
    if archetype == "mill":
        value = 5.0 if "mill" in signals else 0.5
        return mana, value, "mill"
    if archetype == "artifacts":
        value = 1.0 if "artifact" in signals else 0.0
        return mana, value, "artifact"
    if archetype == "shrines":
        value = 1.0 if "shrine" in signals else 0.0
        return mana, value, "shrine"
    if archetype == "tokens":
        if "token_maker" in signals:
            return mana, 2.0, "token"
        if "creature" in signals:
            return mana, 1.0, "creature"
        if "anthem" in signals:
            return mana, 1.5, "anthem"
        if "token_payoff" in signals:
            return mana, 1.25, "token_payoff"
    return mana, 0.0, "none"


class GoldfishSimulator:
    """Play deterministic five-turn solitaire games using simple archetype heuristics."""

    def simulate(
        self,
        deck: GeneratedDeck,
        *,
        archetype: str,
        samples: int = 2000,
        turns: int = 5,
        seed: int = 31,
    ) -> GoldfishReport:
        if samples <= 0 or turns <= 0:
            raise ValueError("samples and turns must be positive")
        library: list[tuple[str, DeckEntry | None]] = [("land", None)] * deck.lands
        for entry in deck.mainboard:
            library.extend([("spell", entry)] * entry.quantity)
        if len(library) < 7:
            raise ValueError("deck must contain at least seven cards")

        rng = random.Random(seed)
        mulligans = kills = mill_outs = 0
        total_unused = total_cast = total_damage = total_mill = 0.0
        total_artifacts = total_shrines = 0.0

        for _ in range(samples):
            shuffled = library[:]
            rng.shuffle(shuffled)
            hand = shuffled[:7]
            draw_index = 7
            if not _is_keepable(hand):
                mulligans += 1
                rng.shuffle(shuffled)
                hand = _bottom_for_six(shuffled[:7])
                draw_index = 7

            lands_in_play = 0
            damage = milled = artifacts = shrines = 0.0
            spells_cast = unused = 0
            creatures: list[float] = []
            ready_tokens = pending_tokens = 0.0
            anthem_bonus = payoff_bonus = 0.0

            for turn in range(1, turns + 1):
                if archetype == "tokens":
                    ready_tokens += pending_tokens
                    pending_tokens = 0.0
                if draw_index < len(shuffled):
                    hand.append(shuffled[draw_index])
                    draw_index += 1
                for index, (kind, _) in enumerate(hand):
                    if kind == "land":
                        lands_in_play += 1
                        hand.pop(index)
                        break
                mana = lands_in_play
                while True:
                    candidates = []
                    for index, (kind, entry) in enumerate(hand):
                        if kind != "spell" or entry is None:
                            continue
                        cost, value, metric = _spell_value(entry, archetype)
                        if cost <= mana:
                            candidates.append((value / cost, value, -cost, index, cost, metric, entry))
                    if not candidates:
                        break
                    _, value, _, index, cost, metric, entry = max(candidates)
                    hand.pop(index)
                    mana -= cost
                    spells_cast += 1
                    if metric == "damage":
                        damage += value
                        if "creature" in _signals(entry):
                            creatures.append(max(1.0, value))
                    elif metric == "mill":
                        milled += value
                    elif metric == "artifact":
                        artifacts += value
                    elif metric == "shrine":
                        shrines += value
                    elif metric == "creature":
                        pending_tokens += 1.0
                    elif metric == "token":
                        pending_tokens += 2.0
                    elif metric == "anthem":
                        anthem_bonus += 0.5
                    elif metric == "token_payoff":
                        payoff_bonus += 0.15
                if archetype == "burn":
                    damage += sum(creatures)
                elif archetype == "mill":
                    milled += max(0.0, milled * 0.05)
                elif archetype == "shrines":
                    damage += shrines
                elif archetype == "tokens":
                    damage += ready_tokens * (1.0 + anthem_bonus + payoff_bonus)
                unused += mana

            total_unused += unused
            total_cast += spells_cast
            total_damage += damage
            total_mill += milled
            total_artifacts += artifacts
            total_shrines += shrines
            kills += int(damage >= 20)
            mill_outs += int(milled >= 53)

        pct = lambda value: round(value * 100 / samples)
        return GoldfishReport(
            archetype=archetype,
            samples=samples,
            turns=turns,
            mulligan_rate_pct=pct(mulligans),
            average_unused_mana=round(total_unused / samples, 2),
            average_spells_cast=round(total_cast / samples, 2),
            average_damage=round(total_damage / samples, 2),
            kill_by_final_turn_pct=pct(kills),
            average_cards_milled=round(total_mill / samples, 2),
            mill_out_by_final_turn_pct=pct(mill_outs),
            average_artifacts_in_play=round(total_artifacts / samples, 2),
            average_shrines_in_play=round(total_shrines / samples, 2),
        )
