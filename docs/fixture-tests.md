# Fixture tests

The fixture suite proves the harness catches known failure modes and
passes clean ones.

```bash
make -f makefiles/ManuscriptHarness.mk harness-fixtures
# or
python3 scripts/run_fixture_tests.py
```

It writes a JSON report to `harness/reports/fixture_report.json`.

## Two kinds of cases

### 1. Hard-coded legacy and gate cases

Defined in `scripts/run_fixture_tests.py`:

- table-manifest good/bad, citation-log, forbidden-phrase, path-marker;
- LaTeX build fixtures (only when `latexmk`/`pdflatex` is installed);
- submission gates: cover-letter good/bad, rebuttal good/bad, wall
  good/violation;
- memory tooling: `memory.py digest` and `self_improve.py` smoke checks.

### 2. Discovered paperlint cases

Every `fixtures/paperlint/<case>/case.json` is discovered automatically:

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

- `select` - the check ids this case exercises (omit to run all).
- `expect` - `fail` (exit non-zero) or `pass` (exit zero).
- `config` - optional, resolved relative to the case directory.

The runner invokes `python -m papercheck <tex> --select ... --profile ...`
and asserts the exit code. `q1_full` is the flagship clean case: a full
double-blind manuscript that passes every check under `submission`.

## Adding a case

1. Create `fixtures/paperlint/<case>/manuscript/main.tex` with the
   behavior you want to lock in.
2. Add `case.json` naming the check ids and the expected result.
3. Run `python3 scripts/run_fixture_tests.py`.

Every new check must ship with at least one failing fixture and be
covered by the relevant clean fixture.

## Legacy academic gate

`makefiles/AcademicHarness.mk` still runs the standalone `qgate.py`,
`check_heading.py`, `check_summary.py`, and `check_signals.py`. The
unified engine (`papercheck`) supersedes them; `paper-check` in that
Makefile runs the engine instead.

Note: `fixtures/` intentionally contains rule-violating text, so
repo-wide scans (forbidden phrases, path markers) exclude it.
