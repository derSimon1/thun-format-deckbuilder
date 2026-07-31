from __future__ import annotations

from dataclasses import dataclass

from thun_deckbuilder.candidate_score import CandidateScore


@dataclass(frozen=True)
class SelectionTrace:
    step: int
    card_name: str
    quantity_after_selection: int
    score: CandidateScore
    primary_need: str | None
