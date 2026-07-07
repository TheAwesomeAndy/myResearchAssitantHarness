# Claude Code template

`scripts/install_harness.py` copies this template into a target
manuscript repository so Claude Code drives the manuscript through the
Q1 harness.

## What gets installed

| Source | Installed as | Purpose |
| --- | --- | --- |
| `project-instructions.md` | `CLAUDE.md` | The system playbook: the seven layers of the Q1 framework, the never-do list, and the operating loop. |
| `.claude/settings.json` | `.claude/settings.json` | Pre-approves the harness commands and denies destructive ones. |
| `.claude/commands/*.md` | `.claude/commands/*.md` | Slash commands: `/audit-paper`, `/verify`, `/revise`, `/idea-gate`, `/draft-phase`, `/submission-check`, `/cover-letter`, `/rebuttal`, `/amplify`, `/retro`. |
| `.claude/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` | Skills for audit, revision, reviewer response, idea gating, Wall drafting, journal selection, cover letters, amplification, and memory keeping. |

## How the pieces interact

1. `CLAUDE.md` sets standing behavior and points every rule at the check
   family that enforces it.
2. Commands and skills invoke the deterministic tooling
   (`python3 -m papercheck`, `scripts/phase_gate.py`,
   `scripts/check_cover_letter.py`, `scripts/check_rebuttal.py`,
   `scripts/memory.py`, `scripts/self_improve.py`).
3. The harness reports findings; the playbook treats them as acceptance
   criteria and loops Plan -> Edit -> Verify -> Repair -> Report ->
   Remember.

After installing, edit `harness/papercheck.toml` to set the venue and
blinding policy, then run
`make -f makefiles/ManuscriptHarness.mk harness-paper`.
