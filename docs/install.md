# Install

Copy the template files into a target repository:

```text
templates/claude/.claude -> .claude
templates/claude/project-instructions.md -> CLAUDE.md
harness -> harness
scripts -> scripts
tools -> tools
makefiles -> makefiles
```

Add this line to the target `Makefile`:

```make
include makefiles/ManuscriptHarness.mk
```

Alternatively, you can run the installer script to copy everything automatically:

```bash
python scripts/install_harness.py --target /path/to/your/project
```

This will copy the `.claude` directory, policy files, scripts, tools and makefiles into the specified project directory.
