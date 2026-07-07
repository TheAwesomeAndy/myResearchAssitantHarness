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
