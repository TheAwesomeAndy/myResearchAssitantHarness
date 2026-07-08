# CLAUDE.md - harness development

This file is for developing the harness itself. It is NOT the installable
manuscript playbook - that is `templates/claude/project-instructions.md`,
which is copied to `CLAUDE.md` in a target paper repo.

## What this repo is

An all-in-one Q1 publication harness: a deterministic checker engine
(`papercheck`), submission gates, memory and self-improvement tooling, an
agent playbook, policies, and installable Claude Code templates. See
`README.md` and `docs/master-rule-framework.md`.

## Layout

```text
papercheck/        the check engine (model, latex, vocab, config, registry, runner, report, cli)
  checks/          one module per rule family; each self-registers
scripts/           gates (phase_gate, check_cover_letter, check_rebuttal),
                   memory (memory, self_improve), legacy checks, installer
tools/             path-marker scan
tests/             unit tests for every check module and script
fixtures/          example manuscripts; paperlint/ is case.json-driven
makefiles/         reusable Makefile includes
harness/           policies, task_specs, config, memory journal, reports
playbooks/         human-facing SOPs
templates/claude/  installable Claude Code template
docs/              rulebook, check reference, architecture, guides
```

## Dev commands

```bash
python3 -m unittest discover -s tests        # all unit tests
python3 scripts/run_fixture_tests.py         # fixture regression suite
python3 -m papercheck --list-checks          # every registered check
make -f makefiles/ManuscriptHarness.mk harness-verify
```

## Conventions

- Stdlib only. No third-party imports anywhere in `papercheck/` or
  `scripts/`.
- One check module per rule family in `papercheck/checks/`.
- Register every check with `@register("family.id", "title", "MODULE")`.
- Shared word and phrase lists live in `papercheck/vocab.py`;
  check-specific lists are module-local constants.
- SPDX header (`# SPDX-License-Identifier: Apache-2.0`) on every source
  file.
- ASCII only in prose files; no em dashes (the harness forbids them).

## The rule for adding a check

Every new check ships with all three:

1. unit tests in `tests/test_<family>.py` (failing and passing paths);
2. a failing fixture in `fixtures/paperlint/<case>/` with a `case.json`,
   plus coverage in the family's clean fixture;
3. a row in `docs/checks.md`.

See `docs/architecture.md` for a worked example.

## Watch out

`fixtures/` intentionally contains rule-violating text (hype, roadmap
paragraphs, leaked paths). Repo-wide scans
(`check_forbidden_phrases.py`, `check_path_markers.py`) skip `fixtures/`,
`docs/`, `templates/`, `playbooks/`, and generated reports when
self-scanning, so do not rely on those scans to lint the harness's own
instructional content.
