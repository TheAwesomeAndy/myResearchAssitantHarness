# Research AI Harness

An all-in-one, repo-local harness for writing and reviewing academic
manuscripts for top-tier (Q1) venues. It combines a deterministic
checker engine, an AI agent playbook, standing policies, installable
Claude Code templates, and a memory and self-improvement loop.

Built for Claude Code first, but the enforcement is tool-independent:
policies, Python checks, Makefile targets, fixtures, and templates. The
model is not the harness. The harness is the system around the model
that constrains, verifies, and records its work.

## Core principle

AI output is not accepted because it sounds plausible. It is accepted
only when it survives explicit checks. The harness runs this loop:

```text
Plan -> Edit -> Verify -> Repair -> Report -> Remember
```

## What this repo provides

- `papercheck` - a stdlib-only engine of 61 deterministic checks that
  enforce the Q1 rulebook against a LaTeX manuscript.
- Submission gates - cover-letter, rebuttal, and Wall drafting-order
  checks.
- Memory and self-improvement - a durable JSONL journal plus an analyzer
  that turns recurring findings into concrete harness upgrades.
- Claude Code templates - `CLAUDE.md`, slash commands, and skills.
- Policies - claim discipline, rigor, narrative, submission, privacy,
  amplification, and memory.
- Legacy scripts - forbidden-phrase and path-marker scans, LaTeX build
  and citation checks, and table-value manifests.

## Quickstart

Install into a manuscript repo and verify:

```bash
python3 scripts/install_harness.py --target ../your-paper-repo
cd ../your-paper-repo
# edit harness/papercheck.toml (venue, blinding, human_subjects)
make -f makefiles/ManuscriptHarness.mk harness-paper
```

Run the engine directly:

```bash
python3 -m papercheck manuscript/main.tex --profile submission
python3 -m papercheck --list-checks
```

Open Claude Code from the repo root and run `/audit-paper`.

## The seven modules and how each is enforced

| Module | Concern | Enforcement |
| --- | --- | --- |
| 1 AI environment | Anti-waterfall, ghost verifier, honesty, anchoring | agent (`CLAUDE.md`) |
| 2 Ideation | Single idea, novelty, anti-salami, journal fit | agent (`/idea-gate`, `journal-selection`) |
| 3 The Wall | Draft from the concrete core outward | auto (`scripts/phase_gate.py`) + agent |
| 4 Sections | Title, abstract, intro, methods, results, related, conclusion | auto (`papercheck`) |
| 5 Submission | Blinding, ethics, cover letter, rebuttal | auto + agent |
| 6 Amplification | Post-acceptance assets | agent (`/amplify`) |
| 7 Memory | Learn from runs and reviews | auto (`memory.py`, `self_improve.py`) + agent |

The full rule-to-check mapping is in `docs/q1_rule_index.md`; the rulebook
itself is `docs/master-rule-framework.md`.

## Check catalog

| Family | Checks | Enforces | Example ids |
| --- | --- | --- | --- |
| `title.*` `abstract.*` `keywords.*` | 9 | Front matter (M4A) | `title.length`, `abstract.structure` |
| `intro.*` | 6 | Introduction (M4B) | `intro.roadmap`, `intro.gap` |
| `methods.*` | 6 | Methodology rigor (M4C) | `methods.baseline`, `methods.leakage` |
| `results.*` `discussion.*` `claims.*` | 5 | Results and RCI discussion (M4D) | `claims.overclaim`, `discussion.compare` |
| `floats.*` | 5 | Figures and tables (M4D-VIS) | `floats.color-only`, `floats.referenced` |
| `structure.*` `limits.*` `conclusion.*` `related.*` | 7 | Structure and related work (M3/M4E/M4F) | `limits.pivot`, `related.hostile` |
| `blind.*` `single.*` `ethics.*` `data.*` | 9 | Compliance (M5) | `blind.author-block`, `data.availability` |
| `lang.*` | 8 | Language and hype (L1) | `lang.hype`, `lang.significant` |
| `bib.*` | 6 | Bibliography hygiene (BIB) | `bib.missing-entries`, `bib.staleness` |

See `docs/checks.md` for every id, severity, and fix.

## Profiles

| Profile | Fails on | Use |
| --- | --- | --- |
| `draft` | errors | day-to-day drafting |
| `submission` | errors and warnings | pre-submission gate |
| `camera` | errors and warnings | camera-ready |

## Configuration

`harness/papercheck.toml` (TOML, stdlib-parsed) sets the venue name,
blinding policy (`double`, `single`, `none`), whether the study involves
human subjects, the title and abstract bounds, and per-check overrides
(`checks.disable`, `checks.warn_only`). Every key has a documented
default; the shipped file lists them all.

## The Wall workflow

Build the paper from the concrete core outward - figures, methods,
results, discussion, conclusion, introduction, front matter - and let the
gate refuse to run a later phase ahead of an earlier one:

```bash
python3 scripts/phase_gate.py manuscript/main.tex --status harness/wall_status.toml
```

## Cover letter and rebuttal gates

```bash
python3 scripts/check_cover_letter.py submission/cover_letter.md --journal "..."
python3 scripts/check_rebuttal.py submission/rebuttal.md --strict
```

## Memory and self-improvement

```bash
python3 scripts/memory.py digest                 # read at session start
python3 scripts/memory.py add lesson "..." --tags methods
python3 scripts/self_improve.py                  # recurring findings -> upgrades
```

`papercheck --history` appends a one-line summary of each run to
`harness/reports/history.jsonl`; `self_improve.py` mines that history and
the memory journal. See `docs/memory.md`.

## Claude Code integration

Installing copies `CLAUDE.md` (the seven-layer playbook), `.claude/`
settings, ten slash commands, and nine skills. See `templates/claude/`.

## Repository layout

```text
papercheck/        the deterministic check engine
  checks/          one module per rule family
scripts/           gates, memory tooling, legacy checks, installer
tools/             path-marker scan
tests/             unit tests for every check module and script
fixtures/          rule-violating and clean example manuscripts
  paperlint/       case.json-driven engine fixtures
makefiles/         reusable Makefile includes
harness/           policies, task specs, config, memory journal, reports
playbooks/         human-facing SOPs and checklists
templates/claude/  installable Claude Code template
docs/              rulebook, check reference, architecture, guides
```

## CI

`.github/workflows/verify.yml` compiles the package, lists the checks,
runs the unit tests, runs `harness-verify` and the fixture suite, and
writes a JSON report. `.github/workflows/academic.yml` runs the legacy
academic gate and the unified engine on the `q1_full` fixture.

## Extending

Add a check: create `papercheck/checks/<family>.py`, register functions
with `@register("family.id", "title", "MODULE")`, add a `tests/` case and
a `fixtures/paperlint/<case>/` fixture, and a row in `docs/checks.md`. See
`docs/architecture.md`.

## What not to put here

Do not store restricted data, private manuscripts, student submissions,
API keys, secrets, unpublished raw datasets, reviewer identities, or logs
containing sensitive local paths in this repository.

## License

Apache License 2.0. See `LICENSE`.
