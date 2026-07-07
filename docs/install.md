# Install

## Automatic

```bash
python3 scripts/install_harness.py --target /path/to/your-paper-repo
```

The installer copies:

| Source | Installed as |
| --- | --- |
| `templates/claude/.claude` | `.claude` |
| `templates/claude/project-instructions.md` | `CLAUDE.md` |
| `papercheck` | `papercheck` |
| `harness` | `harness` |
| `scripts` | `scripts` |
| `tools` | `tools` |
| `makefiles` | `makefiles` |
| `playbooks` | `playbooks` |

It merges into existing directories and skips `__pycache__`.

## Wire up the Makefile

Add to the target `Makefile`:

```make
include makefiles/ManuscriptHarness.mk
```

## Post-install

1. Edit `harness/papercheck.toml`: set `venue.name`, `venue.blinding`
   (`double`/`single`/`none`), and `venue.human_subjects`.
2. Point `paper.main_tex` at your manuscript if it is not
   `manuscript/main.tex`.
3. Run the engine:

   ```bash
   make -f makefiles/ManuscriptHarness.mk harness-paper
   ```

4. Initialize the memory journal:

   ```bash
   python3 scripts/memory.py add decision "Target venue is X (double-blind)" --tags venue
   python3 scripts/memory.py digest
   ```

## Requirements

Python 3.11 or newer (the engine uses `tomllib`). No third-party
packages. `latexmk` or `pdflatex` is optional and only needed for the
LaTeX build and citation checks.

## Using it with Claude Code

Open the target repo and start Claude from the repo root. The installed
`CLAUDE.md` sets standing behavior; run `/audit-paper` to begin.
