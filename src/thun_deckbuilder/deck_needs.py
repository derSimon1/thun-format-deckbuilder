from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.deck_profile import DeckProfile
from thun_deckbuilder.deck_state import DeckState


@dataclass(frozen=True)
class Need:
    key: str
    current: float
    minimum: int
    target: int
    urgency: float
    required: bool

    @property
    def missing_minimum(self) -> float:
        return max(0.0, self.minimum - self.current)

    @property
    def missing_target(self) -> float:
        return max(0.0, self.target - self.current)


@dataclass(frozen=True)
class DeckNeeds:
    role_needs: tuple[Need, ...]
    curve_needs: tuple[Need, ...]
    remaining_spell_slots: int
    remaining_land_slots: int

    def role_urgency(self, role: str) -> float:
        return next((need.urgency for need in self.role_needs if need.key == role), 0.0)

    def curve_urgency(self, curve_key: str) -> float:
        return next((need.urgency for need in self.curve_needs if need.key == curve_key), 0.0)

    def unmet_required_needs(self) -> tuple[Need, ...]:
        return tuple(need for need in self.role_needs if need.required and need.missing_minimum > 0)


class DeckNeedsAnalyzer:
    """Derive dynamic role and curve needs from profile and deck state."""

    def analyze(self, state: DeckState, profile: DeckProfile, *, deck_size: int) -> DeckNeeds:
        remaining_spells = state.remaining_spell_slots(profile, deck_size)
        remaining_lands = max(0, profile.lands - state.land_count)

        role_needs = tuple(
            self._need(
                key=target.role,
                current=state.role_count(target.role),
                minimum=target.minimum,
                target=target.target,
                remaining_slots=remaining_spells,
            )
            for target in profile.role_targets
        )

        curve_needs: list[Need] = []
        previous_maximum = -1.0
        for target in profile.curve_targets:
            key = f"mv_{previous_maximum:g}_{target.maximum_mana_value:g}"
            current = state.curve_count(target.maximum_mana_value, previous_maximum)
            curve_needs.append(
                self._need(
                    key=key,
                    current=current,
                    minimum=0,
                    target=target.target,
                    remaining_slots=remaining_spells,
                )
            )
            previous_maximum = target.maximum_mana_value

        return DeckNeeds(
            role_needs=role_needs,
            curve_needs=tuple(curve_needs),
            remaining_spell_slots=remaining_spells,
            remaining_land_slots=remaining_lands,
        )

    @staticmethod
    def _need(
        *,
        key: str,
        current: float,
        minimum: int,
        target: int,
        remaining_slots: int,
    ) -> Need:
        missing_minimum = max(0.0, minimum - current)
        missing_target = max(0.0, target - current)
        if missing_target == 0:
            urgency = 0.0
        else:
            capacity = max(remaining_slots, 1)
            urgency = min(1.0, missing_target / capacity)
            if missing_minimum > 0:
                urgency = min(1.0, urgency + 0.5)
        return Need(
            key=key,
            current=current,
            minimum=minimum,
            target=target,
            urgency=urgency,
            required=minimum > 0,
        )
