from thun_deckbuilder.cli import build_parser


def test_bo3_command_parses_archetypes_and_samples():
    args = build_parser().parse_args(["bo3", "burn", "mill", "--samples", "5000"])
    assert args.command == "bo3"
    assert args.archetype_a == "burn"
    assert args.archetype_b == "mill"
    assert args.samples == 5000


def test_meta_bo3_command_accepts_subset():
    args = build_parser().parse_args(["meta-bo3", "burn", "mill", "artifacts"])
    assert args.command == "meta-bo3"
    assert args.archetypes == ["burn", "mill", "artifacts"]
