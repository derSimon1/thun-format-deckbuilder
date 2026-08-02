from __future__ import annotations

from pathlib import Path

from thun_deckbuilder.calibrated_strategies import _prowess_eligible
from thun_deckbuilder.card_analyzer import analyze_card
from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.card_evaluation import CardEvaluationEngine
from thun_deckbuilder.card_roles import detect_roles
from thun_deckbuilder.card_scoring import score_prowess_card
from thun_deckbuilder.card_synergies import detect_synergies
from thun_deckbuilder.config import load_config
from thun_deckbuilder.knowledge_base import CardKnowledge, KnowledgeBase


CARD_NAME = "Vibrant Outburst"
COLORS = ("U", "R")


def _combined_score(knowledge: CardKnowledge) -> float:
    prowess = score_prowess_card(knowledge.analysis).score
    intrinsic = CardEvaluationEngine().evaluate(knowledge.analysis).total
    return prowess + intrinsic


def main() -> None:
    database_path = Path("data/cards.db")
    with CardDatabase(database_path) as database:
        direct_card = database.get_card_by_name(CARD_NAME)
        print(f"Direct database match: {direct_card is not None}")
        print(f"Legal by name: {database.is_card_legal_by_name(CARD_NAME)}")

        knowledge_base = KnowledgeBase(database, load_config())
        knowledge_base.load()
        matching = next(
            (card for card in knowledge_base.cards if card.analysis.name == CARD_NAME),
            None,
        )

        if matching is None:
            print("Legal-pool match: False")
            raise SystemExit(0)

        analysis = matching.analysis
        prowess = score_prowess_card(analysis)
        intrinsic = CardEvaluationEngine().evaluate(analysis)
        eligible = _prowess_eligible(matching, COLORS)

        print("Legal-pool match: True")
        print(f"Mana cost: {matching.card.get('mana_cost', '')}")
        print(f"Mana value: {analysis.mana_value:g}")
        print(f"Type: {analysis.type_line}")
        print(f"Oracle text: {analysis.oracle_text}")
        print(f"Roles: {', '.join(sorted(str(role) for role in matching.roles))}")
        print(f"Prowess eligible: {eligible}")
        print(f"Prowess score: {prowess.score:.2f}")
        print(f"Prowess reasons: {'; '.join(prowess.reasons)}")
        print(f"Intrinsic score: {intrinsic.total:.2f}")
        print(
            "Intrinsic components: "
            + "; ".join(
                f"{item.category}={item.value:.2f} ({item.reason})"
                for item in intrinsic.components
            )
        )
        print(f"Combined static score: {_combined_score(matching):.2f}")

        eligible_cards = tuple(
            card
            for card in knowledge_base.cards
            if _prowess_eligible(card, COLORS)
        )
        ranked = sorted(
            eligible_cards,
            key=lambda card: (
                _combined_score(card),
                card.analysis.name,
            ),
            reverse=True,
        )
        rank = next(
            index
            for index, card in enumerate(ranked, start=1)
            if card.analysis.name == CARD_NAME
        )
        print(f"Static rank among {len(ranked)} eligible Prowess cards: {rank}")
        print("Top 20 static candidates:")
        for index, card in enumerate(ranked[:20], start=1):
            print(
                f"{index:02d}. {card.analysis.name}: "
                f"{_combined_score(card):.2f} "
                f"roles={','.join(sorted(str(role) for role in card.roles))}"
            )


if __name__ == "__main__":
    main()
