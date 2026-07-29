import pytest

from thun_deckbuilder.candidate_score import CandidateScore, ScoreComponent


def test_candidate_score_sums_explainable_components() -> None:
    score = CandidateScore(
        card_name="Example",
        components=(
            ScoreComponent("base", 10, "Base quality"),
            ScoreComponent("need", 4.5, "Fills a missing role"),
            ScoreComponent("curve", -1, "Crowded mana slot"),
        ),
    )

    assert score.total == 13.5
    assert len(score.values_for("need")) == 1


def test_rejected_candidate_requires_reason() -> None:
    with pytest.raises(ValueError):
        CandidateScore(card_name="Example", rejected=True)
