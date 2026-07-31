from thun_deckbuilder.candidate_score import CandidateScore, ScoreComponent
from thun_deckbuilder.explanation import format_candidate_score, format_selection_trace
from thun_deckbuilder.selection_trace import SelectionTrace


def test_candidate_score_explanation_contains_components_and_total() -> None:
    score = CandidateScore(
        card_name="Test Spell",
        components=(
            ScoreComponent("base_quality", 10, "Strong card"),
            ScoreComponent("role_need", 5, "Missing removal"),
        ),
    )

    text = "\n".join(format_candidate_score(score))

    assert "Base Quality" in text
    assert "Role Need" in text
    assert "15.0" in text


def test_selection_trace_explanation_names_primary_need() -> None:
    score = CandidateScore(
        card_name="Token Spell",
        components=(ScoreComponent("base_quality", 8, "Useful"),),
    )
    trace = SelectionTrace(1, "Token Spell", 1, score, "token_maker")

    text = "\n".join(format_selection_trace(trace))

    assert "Step 1" in text
    assert "Token Spell" in text
    assert "token_maker" in text
