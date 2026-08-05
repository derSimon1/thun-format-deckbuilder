from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from thun_deckbuilder.card_database import CardDatabase
from thun_deckbuilder.config import load_config
from thun_deckbuilder.rdw_transfer_audit import FUNCTION_ORDER, rank_candidates


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = (
    PROJECT_ROOT / "research" / "meta" / "pioneer_rdw_reference_2026-08-05.json"
)
DEFAULT_REVIEW = (
    PROJECT_ROOT / "research" / "meta" / "pioneer_rdw_thun_review_2026-08-05.json"
)


def _aliases(name: str) -> tuple[str, ...]:
    values = [name]
    if " // " in name:
        values.extend(part.strip() for part in name.split(" // "))
    return tuple(dict.fromkeys(value.casefold() for value in values))


def _legal_print_summary(card: dict[str, Any]) -> list[dict[str, str]]:
    unique: dict[tuple[str, str], dict[str, str]] = {}
    for card_print in card.get("legal_prints", []):
        key = (
            str(card_print.get("set_code", card_print.get("set", ""))).lower(),
            str(card_print.get("rarity", "")).lower(),
        )
        unique[key] = {"set": key[0], "rarity": key[1]}
    return [unique[key] for key in sorted(unique)]


def _candidate_payload(assessment: Any, card: dict[str, Any]) -> dict[str, Any]:
    payload = asdict(assessment)
    payload["legal_prints"] = _legal_print_summary(card)
    payload["color_identity"] = card.get("color_identity", [])
    return payload


def _review_card_names(review: dict[str, Any]) -> set[str]:
    names = {str(item["card"]) for item in review["direct_transfers"]}
    names.update(str(name) for name in review["sideboard_direct_transfers"])
    for item in review["functional_replacements"]:
        names.update(str(name) for name in item["candidates"])
    for candidates in review["curated_candidate_core"].values():
        names.update(str(name) for name in candidates)
    return names


def _validate_review(
    review: dict[str, Any],
    legal_by_alias: dict[str, dict[str, Any]],
    original_status: list[dict[str, Any]],
) -> dict[str, Any]:
    missing = sorted(
        name
        for name in _review_card_names(review)
        if name.casefold() not in legal_by_alias
    )
    if missing:
        raise ValueError(
            "Curated review contains cards that are not legal in the current "
            f"Thun pool: {', '.join(missing)}"
        )

    mainboard_names = {
        str(name).casefold()
        for name in review["source_mainboard_cards"]
    }
    sideboard_names = {
        str(name).casefold()
        for name in review["sideboard_direct_transfers"]
    }
    mainboard_status = [
        item
        for item in original_status
        if str(item["requested_name"]).casefold() in mainboard_names
    ]
    sideboard_status = [
        item
        for item in original_status
        if str(item["requested_name"]).casefold() in sideboard_names
    ]
    measured = {
        "mainboard_core_cards_checked": len(mainboard_status),
        "mainboard_core_cards_directly_legal": sum(
            1 for item in mainboard_status if item["thun_legal"]
        ),
        "sideboard_cards_checked": len(sideboard_status),
        "sideboard_cards_directly_legal": sum(
            1 for item in sideboard_status if item["thun_legal"]
        ),
    }
    for key, actual in measured.items():
        expected = int(review["evidence_counts"][key])
        if actual != expected:
            raise ValueError(
                f"Curated review count {key} is stale: expected {expected}, "
                f"current audit found {actual}."
            )

    verified_cards: list[dict[str, Any]] = []
    for name in sorted(_review_card_names(review)):
        card = legal_by_alias[name.casefold()]
        verified_cards.append(
            {
                "requested_name": name,
                "resolved_name": card.get("name"),
                "legal_prints": _legal_print_summary(card),
                "oracle_text": card.get("oracle_text"),
            }
        )
    return {
        "review": review,
        "measured_counts": measured,
        "verified_curated_cards": verified_cards,
    }


def build_audit(
    reference_path: Path,
    database_path: Path | None = None,
    review_path: Path | None = DEFAULT_REVIEW,
) -> dict[str, Any]:
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    review = (
        json.loads(review_path.read_text(encoding="utf-8"))
        if review_path is not None
        else None
    )
    config = load_config()

    with CardDatabase(database_path) as database:
        all_cards = database.get_all_cards()
        legal_cards = database.get_all_legal_cards(config)

    all_by_alias: dict[str, dict[str, Any]] = {}
    for card in all_cards:
        for alias in _aliases(str(card.get("name", ""))):
            all_by_alias.setdefault(alias, card)

    legal_by_alias: dict[str, dict[str, Any]] = {}
    legal_by_name: dict[str, dict[str, Any]] = {}
    for card in legal_cards:
        legal_by_name[str(card.get("name", ""))] = card
        for alias in _aliases(str(card.get("name", ""))):
            legal_by_alias.setdefault(alias, card)

    original_status: list[dict[str, Any]] = []
    for requested_name in reference["original_cards_to_verify"]:
        key = str(requested_name).casefold()
        card = all_by_alias.get(key)
        legal_card = legal_by_alias.get(key)
        original_status.append(
            {
                "requested_name": requested_name,
                "resolved_name": card.get("name") if card else None,
                "thun_legal": legal_card is not None,
                "mana_value": card.get("mana_value") if card else None,
                "type_line": card.get("type_line") if card else None,
                "oracle_text": card.get("oracle_text") if card else None,
                "legal_prints": _legal_print_summary(legal_card) if legal_card else [],
            }
        )

    ranked = rank_candidates(legal_cards, limit_per_function=25)
    candidate_buckets: dict[str, list[dict[str, Any]]] = {}
    for function_name in FUNCTION_ORDER:
        candidate_buckets[function_name] = [
            _candidate_payload(assessment, legal_by_name[assessment.name])
            for assessment in ranked[function_name]
        ]

    redundancy = {
        function_name: len(candidate_buckets.get(function_name, []))
        for function_name in reference["minimum_functional_redundancy"]
    }
    minimums = reference["minimum_functional_redundancy"]
    coverage = {
        function_name: redundancy[function_name] >= int(minimums[function_name])
        for function_name in minimums
    }

    direct_legal = [item for item in original_status if item["thun_legal"]]
    direct_illegal = [item for item in original_status if not item["thun_legal"]]
    curated = (
        _validate_review(review, legal_by_alias, original_status)
        if review is not None
        else None
    )

    return {
        "audit_id": "pioneer-rdw-thun-card-pool-audit-2026-08-05-v1",
        "as_of": reference["as_of"],
        "source_reference": reference,
        "format_config": {
            "allowed_rarities": list(config.legality.allowed_rarities),
            "allowed_sets": list(config.sets.allowed_sets),
            "max_copies": config.format.max_copies,
        },
        "pool": {
            "oracle_cards": len(all_cards),
            "thun_legal_oracle_cards": len(legal_cards),
            "mono_red_or_colorless_candidates": sum(
                1
                for card in legal_cards
                if set(
                    str(value).upper()
                    for value in card.get("color_identity", [])
                ).issubset({"R"})
            ),
        },
        "original_card_status": original_status,
        "direct_original_cards_legal": len(direct_legal),
        "direct_original_cards_not_legal": len(direct_illegal),
        "candidate_buckets": candidate_buckets,
        "functional_redundancy": redundancy,
        "minimum_redundancy_met": coverage,
        "curated_review_validation": curated,
        "limitations": [
            "Heuristic candidate ranking is a discovery aid, not a deck-strength prediction.",
            "Attack, death, delayed, conditional and activated effects are explicitly flagged and are not treated as immediate guaranteed output.",
            "Role compression of rare Pioneer cards must be evaluated manually; multiple low-rarity cards may be required to replace one rare card.",
            "No Champion deck or generator profile is changed by this audit.",
        ],
    }


def render_markdown(audit: dict[str, Any]) -> str:
    status = audit["original_card_status"]
    lines = [
        "# Pioneer Red Deck Wins — Thun Card-Pool Audit",
        "",
        f"Snapshot: `{audit['audit_id']}`",
        "",
        "This is a read-only card-pool audit. It is not a Challenger deck and does not replace a Champion.",
        "",
        "## Original Pioneer cards",
        "",
        "| Card | Thun legal | Legal print |",
        "|---|---:|---|",
    ]
    for item in status:
        prints = ", ".join(
            f"{value['set']} ({value['rarity']})" for value in item["legal_prints"]
        ) or "—"
        lines.append(
            f"| {item['requested_name']} | "
            f"{'yes' if item['thun_legal'] else 'no'} | {prints} |"
        )

    curated = audit.get("curated_review_validation")
    if curated:
        conclusion = curated["review"]["conclusion"]
        measured = curated["measured_counts"]
        lines.extend(
            [
                "",
                "## Curated conclusion",
                "",
                f"- Transfer prior: **{conclusion['transfer_score_prior']}/10**",
                f"- Band: `{conclusion['transfer_band']}`",
                f"- Confidence: `{conclusion['confidence']}`",
                f"- {conclusion['summary']}",
                "- Mainboard core directly legal: "
                f"{measured['mainboard_core_cards_directly_legal']}/"
                f"{measured['mainboard_core_cards_checked']}",
                "- Sideboard sample directly legal: "
                f"{measured['sideboard_cards_directly_legal']}/"
                f"{measured['sideboard_cards_checked']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Functional redundancy",
            "",
            "| Function | Candidates | Minimum met |",
            "|---|---:|---:|",
        ]
    )
    for function_name, count in audit["functional_redundancy"].items():
        lines.append(
            f"| {function_name} | {count} | "
            f"{'yes' if audit['minimum_redundancy_met'][function_name] else 'no'} |"
        )

    lines.extend(["", "## Top candidates by function", ""])
    for function_name, candidates in audit["candidate_buckets"].items():
        if not candidates:
            continue
        lines.append(f"### {function_name}")
        lines.append("")
        lines.append("| Card | MV | Score | Timing caveats |")
        lines.append("|---|---:|---:|---|")
        for candidate in candidates[:10]:
            caveats = ", ".join(candidate["timing_caveats"]) or "immediate"
            lines.append(
                f"| {candidate['name']} | {candidate['mana_value']:g} | "
                f"{candidate['score']:g} | {caveats} |"
            )
        lines.append("")

    lines.extend(["## Limitations", ""])
    lines.extend(f"- {item}" for item in audit["limitations"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--database", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()

    audit = build_audit(args.reference, args.database, args.review)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(render_markdown(audit), encoding="utf-8")
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
