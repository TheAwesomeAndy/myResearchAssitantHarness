# Architecture

The `papercheck` engine is a stdlib-only Python package. No third-party
dependencies; Python 3.11+ (it uses `tomllib`).

## Package layout

```text
papercheck/
  model.py       Finding, Severity, Document, SourceMap, CheckContext
  latex.py       parsing: comment stripping, input expansion, sections
  vocab.py       centralized word and phrase lists
  config.py      TOML config, profiles, per-check overrides
  registry.py    @register decorator and check selection
  runner.py      run checks, collect findings, decide pass/fail
  report.py      text, markdown, and JSON rendering
  cli.py         the command-line interface and --history logging
  checks/        one module per rule family, each self-registering
```

## Document and source mapping

`latex.load_document` reads the main `.tex`, strips comments while
preserving character offsets, and expands `\input`/`\include` recursively.
Each expanded segment records the originating file and offset in a
`SourceMap`, so any position in the expanded text resolves back to a real
`file:line`. Checks work on stable offsets; findings report accurate
locations even across included files.

Comment stripping replaces comment text with spaces of equal length, so a
`%` never shifts offsets and an escaped `\%` is preserved.

## The registry pattern

A check is a function `(CheckContext) -> list[Finding]` decorated with
`@register("family.id", "Short title", "MODULE")`. Importing
`papercheck.checks` imports every module, which registers every check.
`--select`/`--skip` and `checks.disable` filter by exact id or dotted
prefix.

## Config and profiles

`Config.load` overlays `harness/papercheck.toml` on built-in defaults.
Profiles set the failure threshold: `draft` fails on errors; `submission`
and `camera` also fail on warnings. `checks.warn_only` downgrades chosen
errors to warnings; `checks.disable` turns checks off entirely.

## Severity policy

`error` is a hard rule (desk-reject risk or a broken artifact). `warning`
is a strong norm that the submission profile enforces. `info` is advisory
and never fails. Severity lives in the finding, not the control flow, so a
project can retune strictness through config without touching code.

## Robustness

The runner wraps each check in a try/except: a check that raises becomes
an `internal.*` warning rather than crashing the run. A check returns `[]`
whenever its target element is absent, unless the absence is itself the
finding (for example `title.present`).

## Adding a check

1. Create or open `papercheck/checks/<family>.py`.
2. Write the function:

   ```python
   from papercheck import latex, vocab
   from papercheck.model import CheckContext, Finding, Severity
   from papercheck.registry import register

   @register("family.rule", "Short title", "M4X")
   def family_rule(ctx: CheckContext) -> list[Finding]:
       """One-line intent."""
       body, offset = latex.document_body(ctx.doc.text)
       hit = body.lower().find("forbidden")
       if hit < 0:
           return []
       return [ctx.finding("family.rule", Severity.WARNING,
                           "found forbidden phrase", pos=offset + hit,
                           rule="M4X.rule", suggestion="rephrase")]
   ```

3. Import the new module in `papercheck/checks/__init__.py`.
4. Add unit tests in `tests/test_<family>.py` covering the failing and
   passing paths.
5. Add a failing fixture (and update a clean fixture) under
   `fixtures/paperlint/`.
6. Add a row to `docs/checks.md`.

Word lists belong in `papercheck/vocab.py` when shared, or a module-local
constant when specific to one check.

## Fixture discovery

`fixtures/paperlint/<case>/case.json` declares a manuscript and the check
ids it must pass or fail:

```json
{
  "name": "intro_roadmap",
  "tex": "manuscript/main.tex",
  "select": ["intro.roadmap"],
  "profile": "submission",
  "expect": "fail",
  "config": "harness/papercheck.toml"
}
```

`scripts/run_fixture_tests.py` discovers every case, runs
`python -m papercheck` with the declared select/profile/config, and
asserts the exit code matches `expect`. `config` is optional and resolved
relative to the case directory.

## Standalone gates

Three gates live in `scripts/` and import `papercheck` for parsing and
vocab: `phase_gate.py` (Wall order), `check_cover_letter.py`, and
`check_rebuttal.py`. They are ordinary scripts with their own exit codes,
wired into the fixture runner as hard-coded cases.

## Deliberately out of scope

Some rules resist deterministic checking and are left to the agent
playbook and human review: genuine novelty versus originality, the RCI
paragraph order and quality, salami-slicing judgment, and the substantive
correctness of a claim. The harness enforces the mechanical preconditions
(a gap exists, a baseline is named, a limitation is stated) and the agent
enforces the judgment (the gap is real, the baseline is strong, the
limitation is honest).
