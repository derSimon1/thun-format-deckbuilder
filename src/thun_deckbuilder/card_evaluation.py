from __future__ import annotations

from dataclasses import dataclass
import re

from thun_deckbuilder.card_analyzer import CardAnalysis


@dataclass(frozen=True)
class EvaluationComponent:
    category: str
    value: float
    reason: str


@dataclass(frozen=True)
class CardEvaluation:
    components: tuple[EvaluationComponent, ...]

    @property
    def total(self) -> float:
        return sum(component.value for component in self.components)

    @property
    def reasons(self) -> tuple[str, ...]:
        return tuple(component.reason for component in self.components)


class CardEvaluationEngine:
    """Estimate intrinsic card quality from conservative Oracle-text heuristics.

    This layer intentionally evaluates only qualities that are broadly useful
    across archetypes. Deck needs, curve fit, synergy and archetype fit remain
    dynamic concerns handled by :class:`CandidateEvaluator`.
    """

    _NUMBER_WORDS = {
        "a": 1,
        "an": 1,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    def evaluate(self, analysis: CardAnalysis) -> CardEvaluation:
        if analysis.is_land:
            return CardEvaluation(())

        text = self._normalized_text(analysis.oracle_text)
        mv = max(analysis.mana_value, 0.0)
        components: list[EvaluationComponent] = [self._mana_efficiency(analysis)]

        self._score_speed(analysis, text, components)
        self._score_card_flow(text, mv, components)
        self._score_interaction(analysis, text, mv, components)
        self._score_battlefield_impact(analysis, text, mv, components)
        self._score_keywords(analysis, text, mv, components)
        self._score_creature_rate(analysis, text, mv, components)
        self._score_repeatability(text, mv, components)
        self._score_narrowness(analysis, text, mv, components)
        self._score_expensive_cards(text, mv, components)

        return CardEvaluation(tuple(component for component in components if component.value != 0))

    @staticmethod
    def _normalized_text(text: str) -> str:
        return " ".join(text.lower().replace("\n", " ").split())

    @staticmethod
    def _append(
        components: list[EvaluationComponent],
        category: str,
        value: float,
        reason: str,
    ) -> None:
        if value:
            components.append(EvaluationComponent(category, value, reason))

    @staticmethod
    def _mana_efficiency(analysis: CardAnalysis) -> EvaluationComponent:
        mv = analysis.mana_value
        if mv <= 1:
            return EvaluationComponent("mana_efficiency", 2.0, "Very low mana value.")
        if mv <= 2:
            return EvaluationComponent("mana_efficiency", 1.5, "Efficient mana value.")
        if mv <= 3:
            return EvaluationComponent("mana_efficiency", 0.5, "Moderate mana value.")
        if mv >= 6:
            return EvaluationComponent("mana_efficiency", -1.5, "Very high mana value requires substantial impact.")
        if mv >= 5:
            return EvaluationComponent("mana_efficiency", -0.5, "High mana value.")
        return EvaluationComponent("mana_efficiency", 0.0, "Neutral mana efficiency.")

    def _score_speed(
        self,
        analysis: CardAnalysis,
        text: str,
        components: list[EvaluationComponent],
    ) -> None:
        if analysis.is_instant:
            self._append(components, "flexibility", 1.25, "Instant-speed flexibility.")
        elif re.search(r"\bflash\b", text):
            self._append(components, "flexibility", 0.9, "Flash enables reactive play.")

    def _score_card_flow(
        self,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        draw_count = self._draw_count(text)
        rummage = bool(re.search(r"discard (?:a|one|\d+) cards?.*draw", text))
        loot = bool(re.search(r"draw (?:a|one|\d+) cards?.*discard", text))
        impulse = "exile the top" in text and "you may play" in text
        scry = self._scry_count(text)

        if draw_count >= 3:
            self._append(components, "card_advantage", 4.0, "Generates substantial card advantage.")
        elif draw_count == 2:
            value = 3.0 if mv <= 4 else 2.25
            self._append(components, "card_advantage", value, "Generates true card advantage.")
        elif draw_count == 1:
            if rummage or loot:
                self._append(components, "card_selection", 0.75, "Filters cards without creating full card advantage.")
            else:
                self._append(components, "card_advantage", 1.0, "Replaces itself with a new card.")

        if impulse:
            self._append(components, "card_selection", 1.25, "Provides temporary access to additional cards.")

        if scry >= 2:
            self._append(components, "card_selection", 0.75, "Improves draw quality through meaningful selection.")
        elif scry == 1:
            self._append(components, "card_selection", 0.35, "Provides minor card selection.")

    def _score_interaction(
        self,
        analysis: CardAnalysis,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        unconditional_exile = bool(re.search(r"exile target (?:nonland )?(?:permanent|creature|artifact|enchantment)", text))
        unconditional_destroy = bool(re.search(r"destroy target (?:nonland )?(?:permanent|creature|artifact|enchantment)", text))
        damage = self._damage_amount(text)
        counterspell = "counter target spell" in text
        bounce = bool(re.search(r"return target .* to (?:its|their) owner'?s hand", text))
        taps_creature = any(
            phrase in text
            for phrase in (
                "tap up to one target creature",
                "tap target creature an opponent controls",
            )
        )
        conditional = any(
            marker in text
            for marker in (
                "with mana value",
                "with power",
                "with toughness",
                "attacking creature",
                "blocked creature",
                "if that creature",
                "unless its controller pays",
            )
        )

        speed_bonus = 0.65 if analysis.is_instant else 0.0
        cost_penalty = max(0.0, mv - 3.0) * 0.35

        if unconditional_exile:
            value = 3.25 + speed_bonus - cost_penalty
            if conditional:
                value -= 0.9
            self._append(components, "interaction", value, "Exiles an opposing threat.")
        elif unconditional_destroy:
            value = 2.75 + speed_bonus - cost_penalty
            if conditional:
                value -= 0.9
            self._append(components, "interaction", value, "Destroys an opposing threat.")
        elif counterspell:
            value = 2.6 + (0.4 if mv <= 2 else 0.0) - cost_penalty
            self._append(components, "interaction", value, "Can trade efficiently with an opposing spell.")
        elif bounce:
            value = 1.5 + speed_bonus - max(0.0, mv - 2.0) * 0.3
            self._append(components, "tempo", value, "Provides temporary interaction and tempo.")
        elif damage > 0:
            value = 1.1 + min(damage, 5) * 0.35 + speed_bonus - cost_penalty
            if "any target" in text or "target player" in text:
                value += 0.35
            self._append(components, "interaction", value, "Provides direct damage interaction.")

        if taps_creature:
            value = 0.75 + (0.25 if analysis.is_instant else 0.0)
            value -= max(0.0, mv - 3.0) * 0.2
            self._append(
                components,
                "tempo",
                max(0.25, value),
                "Can tap an opposing creature to open a temporary combat window.",
            )

    def _score_battlefield_impact(
        self,
        analysis: CardAnalysis,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        token_count = self._token_count(text)
        if token_count:
            value = min(3.5, 0.8 + token_count * 0.75)
            if "for each" in text or "at the beginning of" in text:
                value += 0.75
            self._append(components, "board_impact", value, "Adds multiple bodies or material to the battlefield.")

        if self._has_etb_value(text):
            value = 1.0
            if any(term in text for term in ("draw", "destroy target", "exile target", "create")):
                value += 0.5
            self._append(components, "immediate_value", value, "Generates value as it enters the battlefield.")

        if "each opponent loses" in text or "deals damage to each opponent" in text:
            self._append(components, "reach", 1.0, "Can pressure the opponent without combat.")

        if analysis.is_planeswalker and mv <= 4:
            self._append(components, "repeatable_value", 1.5, "Low-cost planeswalker can generate repeated value.")

    def _score_keywords(
        self,
        analysis: CardAnalysis,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        if not analysis.is_creature:
            return

        keyword_values = {
            "haste": 0.9,
            "flying": 0.75,
            "menace": 0.4,
            "trample": 0.35,
            "vigilance": 0.25,
            "lifelink": 0.55,
            "deathtouch": 0.6,
            "first strike": 0.35,
            "double strike": 0.9,
            "hexproof": 1.1,
            "indestructible": 1.0,
        }
        score = sum(value for keyword, value in keyword_values.items() if re.search(rf"\b{re.escape(keyword)}\b", text))

        ward_match = re.search(r"\bward(?:—| | \{)([^.,]+)", text)
        if ward_match:
            score += 0.65

        if score:
            score = min(score, 2.4)
            self._append(components, "creature_keywords", score, "Relevant creature keywords improve combat or resilience.")

        if "defender" in text and not any(term in text for term in ("draw", "create", "when", "whenever")):
            self._append(components, "creature_drawback", -1.0, "Defender limits offensive pressure without clear compensation.")

        if "can\'t block" in text or "can't block" in text:
            self._append(components, "creature_drawback", -0.45, "Cannot block, reducing defensive utility.")

    def _score_creature_rate(
        self,
        analysis: CardAnalysis,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        if not analysis.is_creature or analysis.power is None or analysis.toughness is None or mv <= 0:
            return

        rate = (analysis.power + analysis.toughness) / (2 * mv)
        has_value_text = self._has_meaningful_creature_text(text)

        if rate >= 1.35:
            self._append(components, "creature_rate", 1.5, "Excellent power and toughness for its mana value.")
        elif rate >= 1.05:
            self._append(components, "creature_rate", 0.65, "Solid power and toughness for its mana value.")
        elif rate < 0.6 and not has_value_text:
            self._append(components, "creature_rate", -1.5, "Poor body without meaningful compensation.")
        elif rate < 0.8 and not has_value_text:
            self._append(components, "creature_rate", -0.75, "Below-rate body without clear compensation.")

        if not text.strip() and mv >= 3 and rate < 1.2:
            self._append(components, "vanilla_penalty", -1.0, "Vanilla creature offers little beyond its stats.")

    def _score_repeatability(
        self,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        repeatable_markers = (
            "at the beginning of your upkeep",
            "at the beginning of your end step",
            "whenever you cast",
            "whenever another",
            "once each turn",
        )
        activated_value = bool(re.search(r"\{[^}]+\}[^:]*:.*(?:draw|create|destroy|exile|deals)", text))
        if any(marker in text for marker in repeatable_markers) or activated_value:
            value = 1.25 if mv <= 4 else 0.8
            self._append(components, "repeatable_value", value, "Can generate value repeatedly if it remains in play.")

    def _score_narrowness(
        self,
        analysis: CardAnalysis,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        if analysis.is_instant and self._looks_like_combat_trick(text):
            value = -0.75
            if "draw a card" in text:
                value += 0.5
            self._append(components, "situational", value, "Combat trick is situational and risks card disadvantage.")

        if "only during your turn" in text or "activate only as a sorcery" in text:
            self._append(components, "timing_restriction", -0.35, "Timing restriction reduces flexibility.")

        if "target creature you control" in text and not any(term in text for term in ("draw", "create", "return")) and mv >= 3:
            self._append(components, "narrow_effect", -0.5, "Requires an existing creature and has limited standalone value.")

    def _score_expensive_cards(
        self,
        text: str,
        mv: float,
        components: list[EvaluationComponent],
    ) -> None:
        impact_categories = {
            "card_advantage",
            "board_impact",
            "interaction",
            "immediate_value",
            "repeatable_value",
            "reach",
        }
        has_impact = any(component.category in impact_categories and component.value > 0 for component in components)

        if mv >= 6 and not has_impact:
            self._append(components, "expensive_low_impact", -2.5, "Very high mana value without a clear immediate impact.")
        elif mv >= 5 and not has_impact:
            self._append(components, "expensive_low_impact", -1.5, "High mana value without a clear immediate impact.")
        elif mv >= 5 and has_impact:
            total_impact = sum(component.value for component in components if component.category in impact_categories)
            if total_impact < 2.5:
                self._append(components, "expensive_low_impact", -0.75, "High mana value for only modest immediate impact.")

    @classmethod
    def _draw_count(cls, text: str) -> int:
        matches = re.findall(r"draw (a|an|one|two|three|four|five|\d+) cards?", text)
        if not matches:
            return 0
        return max(cls._parse_count(token) for token in matches)

    @classmethod
    def _scry_count(cls, text: str) -> int:
        match = re.search(r"scry (one|two|three|four|five|\d+)", text)
        return cls._parse_count(match.group(1)) if match else 0

    @classmethod
    def _parse_count(cls, token: str) -> int:
        return cls._NUMBER_WORDS.get(token, int(token) if token.isdigit() else 1)

    @staticmethod
    def _damage_amount(text: str) -> int:
        matches = re.findall(r"deals? (\d+) damage", text)
        return max((int(value) for value in matches), default=0)

    @classmethod
    def _token_count(cls, text: str) -> int:
        matches = re.findall(r"create (a|an|one|two|three|four|five|\d+) [^.]*?tokens?", text)
        if matches:
            return max(cls._parse_count(token) for token in matches)
        return 1 if "create" in text and "token" in text else 0

    @staticmethod
    def _has_etb_value(text: str) -> bool:
        return any(
            marker in text
            for marker in (
                "enters the battlefield",
                "when this creature enters",
                "when this permanent enters",
                "when ~ enters",
            )
        )

    @staticmethod
    def _has_meaningful_creature_text(text: str) -> bool:
        meaningful_terms = (
            "when ",
            "whenever ",
            "at the beginning",
            "draw",
            "create",
            "destroy",
            "exile",
            "deals",
            "flying",
            "haste",
            "lifelink",
            "deathtouch",
            "ward",
            "hexproof",
            "indestructible",
            "double strike",
        )
        return any(term in text for term in meaningful_terms)

    @staticmethod
    def _looks_like_combat_trick(text: str) -> bool:
        pump = bool(re.search(r"target creature (?:you control )?gets? \+[0-9x]+/\+[0-9x]+", text))
        temporary = "until end of turn" in text
        return pump and temporary
