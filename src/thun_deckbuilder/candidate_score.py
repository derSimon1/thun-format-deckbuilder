from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreComponent:
    category: str
    value: float
    reason: str

    def __post_init__(self) -> None:
        if not self.category:
            raise ValueError("Score category cannot be empty.")
        if not self.reason:
            raise ValueError("Score reason cannot be empty.")


@dataclass(frozen=True)
class CandidateScore:
    card_name: str
    components: tuple[ScoreComponent, ...] = ()
    rejected: bool = False
    rejection_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.card_name:
            raise ValueError("Card name cannot be empty.")
        if self.rejected and not self.rejection_reason:
            raise ValueError("Rejected candidates require a rejection reason.")

    @property
    def total(self) -> float:
        return sum(component.value for component in self.components)

    def values_for(self, category: str) -> tuple[ScoreComponent, ...]:
        return tuple(component for component in self.components if component.category == category)
