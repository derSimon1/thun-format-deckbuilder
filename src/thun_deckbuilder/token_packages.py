from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Mapping

from thun_deckbuilder.card_analyzer import (
    CardAnalysis,
    analyze_card,
    cast_accessible_effect_segments,
    cast_immediate_team_buff_segments,
    cast_accessible_oracle_text,
)
from thun_deckbuilder.deck_generator import GeneratedDeck


@dataclass(frozen=True)
class TokenPackageSignals:
    creates_any_token: bool = False
    creates_creature_tokens: bool = False
    creates_noncreature_tokens: bool = False
    creates_multiple_creature_tokens: bool = False
    repeatable_creature_source: bool = False
    sacrifice_text: bool = False
    sacrifice_outlet: bool = False
    one_shot_sacrifice: bool = False
    self_death_value: bool = False
    death_payoff: bool = False
    drain_payoff: bool = False
    token_value_payoff: bool = False
    anthem: bool = False
    evasion_payoff: bool = False


_MULTI_CREATURE_TOKEN = re.compile(
    r"create (?:up to )?(?:two|three|four|five|six|[2-9]|\d{2,}) "
    r"[^.\n]*?creature tokens?"
)


def _creates_creature_token(sentence: str) -> bool:
    if "create" not in sentence or "token" not in sentence:
        return False
    if "creature token" in sentence:
        return True
    return "token that's a copy" in sentence and "creature" in sentence


def _sacrifice_outlet(text: str) -> bool:
    """Recognize reusable creature-sacrifice activated abilities.

    Oracle activated abilities place their cost before a colon. Additional cast
    costs and forced one-shot sacrifices do not, and therefore must not turn a
    card into an Aristocrats outlet.
    """

    for match in re.finditer(r"([^.:\n]{0,180}):", text):
        cost = match.group(1).lower()
        if "sacrifice" not in cost or "creature" not in cost:
            continue
        if "as an additional cost" in cost:
            continue
        return True
    return False


def analyze_token_package(analysis: CardAnalysis) -> TokenPackageSignals:
    """Return plan-level token signals from Oracle text.

    Creature-token material is separated from Food, Clue, Blood, Treasure and
    other noncreature tokens. True reusable sacrifice outlets and other-creature
    death payoffs are separated from one-shot sacrifice text and self-death
    value so those broad words cannot fabricate an Aristocrats package.
    """

    text = cast_accessible_oracle_text(analysis).lower()
    sentences = cast_accessible_effect_segments(analysis)
    token_sentences = tuple(
        sentence
        for sentence in sentences
        if "create" in sentence and "token" in sentence
    )
    creature_token_sentences = tuple(
        sentence for sentence in token_sentences if _creates_creature_token(sentence)
    )
    noncreature_token_sentences = tuple(
        sentence for sentence in token_sentences if not _creates_creature_token(sentence)
    )

    creates_creature_tokens = bool(creature_token_sentences)
    creates_multiple_creature_tokens = any(
        _MULTI_CREATURE_TOKEN.search(sentence)
        or "create x " in sentence
        or "for each" in sentence
        or "that many" in sentence
        for sentence in creature_token_sentences
    )
    repeatable_creature_source = creates_creature_tokens and any(
        phrase in sentence
        for sentence in creature_token_sentences
        for phrase in (
            "at the beginning of",
            "whenever",
            "each upkeep",
            "each end step",
            "{t}: create",
        )
    )

    sacrifice_text = "sacrifice" in text
    sacrifice_outlet = _sacrifice_outlet(text)
    self_death_value = any(
        "dies" in sentence
        and any(marker in sentence for marker in ("when this", "whenever this"))
        for sentence in sentences
    )
    death_trigger_sentences = tuple(
        sentence
        for sentence in sentences
        if "creature" in sentence
        and ("dies" in sentence or " die" in sentence)
        and ("whenever" in sentence or "when" in sentence)
        and "when this" not in sentence
        and "whenever this" not in sentence
    )
    death_payoff = bool(death_trigger_sentences)
    drain_payoff = death_payoff and any(
        phrase in sentence
        for sentence in death_trigger_sentences
        for phrase in (
            "each opponent loses",
            "target opponent loses",
            "opponent loses",
            "you gain 1 life",
            "you gain that much life",
        )
    )
    token_value_payoff = any(
        any(
            trigger in sentence
            for trigger in (
                "whenever a token enters",
                "whenever one or more tokens",
                "when one or more tokens",
                "for each token you control",
            )
        )
        and any(
            reward in sentence
            for reward in (
                "draw a card",
                "investigate",
                "scry",
                "put a +1/+1 counter",
                "gain 1 life",
            )
        )
        for sentence in sentences
    )
    anthem = bool(cast_immediate_team_buff_segments(analysis))
    evasion_payoff = any(
        phrase in text
        for phrase in (
            "creatures you control have flying",
            "creature tokens you control have flying",
            "creatures you control can't be blocked",
            "creature tokens you control can't be blocked",
            "creatures you control have menace",
        )
    )

    return TokenPackageSignals(
        creates_any_token=bool(token_sentences),
        creates_creature_tokens=creates_creature_tokens,
        creates_noncreature_tokens=bool(noncreature_token_sentences),
        creates_multiple_creature_tokens=creates_multiple_creature_tokens,
        repeatable_creature_source=repeatable_creature_source,
        sacrifice_text=sacrifice_text,
        sacrifice_outlet=sacrifice_outlet,
        one_shot_sacrifice=sacrifice_text and not sacrifice_outlet,
        self_death_value=self_death_value,
        death_payoff=death_payoff,
        drain_payoff=drain_payoff,
        token_value_payoff=token_value_payoff,
        anthem=anthem,
        evasion_payoff=evasion_payoff,
    )


def _categories(signals: TokenPackageSignals) -> tuple[str, ...]:
    flags = {
        "creature_material": signals.creates_creature_tokens,
        "noncreature_token_source": signals.creates_noncreature_tokens,
        "multi_creature_maker": signals.creates_multiple_creature_tokens,
        "repeatable_creature_maker": signals.repeatable_creature_source,
        "sacrifice_outlet": signals.sacrifice_outlet,
        "one_shot_sacrifice": signals.one_shot_sacrifice,
        "self_death_value": signals.self_death_value,
        "death_payoff": signals.death_payoff,
        "drain_payoff": signals.drain_payoff,
        "token_value_payoff": signals.token_value_payoff,
        "anthem": signals.anthem,
        "evasion_payoff": signals.evasion_payoff,
    }
    return tuple(name for name, present in flags.items() if present)


def _package_counts(cards: list[dict[str, object]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for card in cards:
        quantity = int(card["quantity"])
        for category in card["categories"]:
            counts[str(category)] += quantity
    return dict(sorted(counts.items()))


def build_token_package_diagnostics(
    deck: GeneratedDeck,
    legal_cards: Mapping[str, Mapping[str, object]],
) -> dict[str, object]:
    """Explain current and available Token subarchetype packages.

    Broad legacy roles are retained in the output so false-positive pressure can
    be measured directly. No composition threshold is imposed by this report.
    """

    deck_cards: list[dict[str, object]] = []
    broad_false_positives: Counter[str] = Counter()
    for entry in deck.mainboard:
        raw = legal_cards.get(entry.name.casefold())
        if raw is None:
            continue
        signals = analyze_token_package(analyze_card(dict(raw)))
        categories = _categories(signals)
        roles = {str(role) for role in entry.roles}
        if "token_maker" in roles and not signals.creates_creature_tokens:
            broad_false_positives["token_maker_without_creature_material"] += entry.quantity
        if "sacrifice" in roles and not signals.sacrifice_outlet:
            broad_false_positives["sacrifice_without_outlet"] += entry.quantity
        if "token_payoff" in roles and not any(
            (
                signals.death_payoff,
                signals.drain_payoff,
                signals.token_value_payoff,
                signals.anthem,
                signals.evasion_payoff,
            )
        ):
            broad_false_positives["token_payoff_without_plan_payoff"] += entry.quantity
        deck_cards.append(
            {
                "name": entry.name,
                "quantity": entry.quantity,
                "mana_value": entry.mana_value,
                "categories": list(categories),
                "roles": sorted(roles),
                "reasons": list(entry.reasons),
            }
        )

    pool_cards: list[dict[str, object]] = []
    seen_names: set[str] = set()
    for raw in legal_cards.values():
        analysis = analyze_card(dict(raw))
        if analysis.name.casefold() in seen_names:
            continue
        seen_names.add(analysis.name.casefold())
        if analysis.is_land or analysis.mana_value > 6:
            continue
        if not set(analysis.color_identity).issubset({"W"}):
            continue
        categories = _categories(analyze_token_package(analysis))
        if not categories:
            continue
        pool_cards.append(
            {
                "name": analysis.name,
                "mana_value": analysis.mana_value,
                "categories": list(categories),
            }
        )

    pool_cards.sort(key=lambda item: (float(item["mana_value"]), str(item["name"])))
    deck_cards.sort(key=lambda item: (float(item["mana_value"]), str(item["name"])))
    deck_counts = _package_counts(deck_cards)
    pool_distinct: Counter[str] = Counter()
    for card in pool_cards:
        pool_distinct.update(str(category) for category in card["categories"])

    aristocrats = {
        "material_copies": deck_counts.get("creature_material", 0),
        "outlet_copies": deck_counts.get("sacrifice_outlet", 0),
        "death_payoff_copies": deck_counts.get("death_payoff", 0),
        "drain_payoff_copies": deck_counts.get("drain_payoff", 0),
    }
    aristocrats["component_presence"] = all(
        int(aristocrats[key]) > 0
        for key in ("material_copies", "outlet_copies", "death_payoff_copies")
    )
    go_wide = {
        "material_copies": deck_counts.get("creature_material", 0),
        "multi_maker_copies": deck_counts.get("multi_creature_maker", 0),
        "anthem_copies": deck_counts.get("anthem", 0),
        "evasion_payoff_copies": deck_counts.get("evasion_payoff", 0),
    }
    value = {
        "material_copies": deck_counts.get("creature_material", 0),
        "repeatable_maker_copies": deck_counts.get("repeatable_creature_maker", 0),
        "token_value_payoff_copies": deck_counts.get("token_value_payoff", 0),
    }

    return {
        "profile_name": deck.profile_name,
        "spell_copies": sum(entry.quantity for entry in deck.mainboard),
        "package_counts": deck_counts,
        "broad_role_false_positive_copies": dict(sorted(broad_false_positives.items())),
        "aristocrats": aristocrats,
        "go_wide": go_wide,
        "value_tokens": value,
        "pool_capacity": {
            "distinct_cards": len(pool_cards),
            "distinct_by_category": dict(sorted(pool_distinct.items())),
            "maximum_copies_at_three_by_category": {
                category: count * 3
                for category, count in sorted(pool_distinct.items())
            },
            "cards": pool_cards,
        },
        "cards": deck_cards,
    }
