# Research AI Harness

A reusable, repo-local harness for controlled AI-assisted research workflows.

This project is designed for Claude Code first, but the core enforcement is tool-independent: policies, scripts, Makefile targets, eval cases, and installation templates. The model is not the harness. The harness is the system around the model that constrains, verifies, and records its work.

## What this repo provides

- Claude Code templates: `CLAUDE.md`, `.claude/settings.json`, slash commands, and skills.
- Manuscript policies: claim discipline, privacy, citation handling, style, and reproducibility.
- Deterministic checks: forbidden phrase scanning, privacy leak scanning, LaTeX log checks, table-value checks, and manifest checks.
- Makefile integration: one-command verification targets.
- Minimal example repo: a small LaTeX paper scaffold showing how to install and use the harness.

## Core principle

AI output is not accepted because it sounds plausible. It is accepted only when it survives explicit checks.

The harness is built around this loop:

```text
Plan -> Edit -> Verify -> Repair -> Report
```

## Repository layout

```text
research-ai-harness/
  templates/claude/          Claude Code installable template
  policies/                  Standing research and manuscript rules
  scripts/                   Deterministic verification scripts
  makefiles/                 Reusable Makefile include files
  evals/                     Regression/evaluation task cases
  examples/minimal-paper-repo Minimal harnessed paper repo
  harness/                   Harness design notes and profiles
```

## Quick install into a target repo

From this repo root:

```bash
bash install.sh --target ../your-paper-repo --profile manuscript
```

Then in the target repo:

```bash
make harness-verify
```

For Claude Code, open the target repo and start Claude from the repo root:

```bash
cd ../your-paper-repo
claude
```

Then run:

```text
/audit-paper
```

## Minimum viable use

A target manuscript repo should contain:

```text
CLAUDE.md
.claude/
harness/policies/
scripts/
makefiles/ManuscriptHarness.mk
Makefile
```

The project-specific repo remains the source of truth for local constraints. This generic harness provides reusable machinery.

## What not to put here

Do not store restricted data, private manuscripts, student submissions, API keys, secrets, unpublished raw datasets, reviewer identities, or logs containing sensitive local paths in this repository.

## License

Apache License 2.0. See `LICENSE` for details.
