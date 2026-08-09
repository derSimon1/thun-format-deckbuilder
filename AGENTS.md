# Repository Agent Instructions

These instructions apply to the entire repository.

## Authoritative context

Before calibration or deck-quality work, read these files completely:

1. `docs/SPECIFICATION.md`
2. `docs/PROMPTS/global-calibration.md`
3. `docs/DEVELOPMENT_LOGBOOK.md`
4. `docs/ROADMAP.md`
5. `docs/DECISIONS.md`
6. `docs/KNOWN_ISSUES.md`
7. `docs/META.md`
8. `docs/CHANGELOG_SPECIFICATION.md`

The precedence rules in `docs/SPECIFICATION.md` apply. Repository documents
override stale external instructions. PR #13 and its Izzet-Prowess work remain
separate from PR #14 and must not be modified from the global-calibration
branch.

## Calibration workflow

- Work on one evidence-backed hypothesis at a time. Make at most three tightly
  coupled changes for one root cause and create exactly one coherent commit per
  completed cycle.
- Do not start a change while CI is active or the local, remote, and PR heads
  are unclear. Recheck the remote head immediately before every push.
- Run targeted regression tests, the complete test suite, Fast validation, and
  the required reproducible 100-hand diagnostics before committing.
- Treat green tests and CI as technical gates. Evaluate the downloaded
  artifact, all five reference benchmarks, deck contents, mana, opening hands,
  matchups, sideboard plans, and regressions before judging deck quality.
- Update `docs/DEVELOPMENT_LOGBOOK.md` and `docs/ROADMAP.md` in the same commit.
  Record durable decisions and known issues in their dedicated documents.
- End every cycle with `new KGB`, `no new KGB`, or `regression`, plus exactly
  one executable next step.

## Local validation

Use the repository virtual environment on Windows:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest
$env:THUN_REUSE_CARD_DATABASE='1'
& '.\.venv\Scripts\python.exe' scripts\ci_global_validation_fast.py
& '.\.venv\Scripts\python.exe' scripts\ci_token_diagnostics.py
```

The full-pool tests require the ignored `data/cards.db` built by the workflow's
`scripts/ci_global_validation.py::_prepare_database()` path. Do not weaken or
skip full-pool assertions when the database is absent.

Generated `artifacts/` and `data/cards.db` are local/CI products and must not be
committed. Finish with a clean, synchronized working tree and no unreviewed CI.

## GitHub CLI

On this Windows checkout, invoke GitHub CLI only through:

```text
C:\Program Files\GitHub CLI\gh.exe
```

Do not substitute a bare `gh` command. Use GitHub Actions as a validator, never
as a development agent, and do not create dummy commits merely to trigger CI.
