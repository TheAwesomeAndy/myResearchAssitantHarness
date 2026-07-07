# Memory and self-improvement (Module 7)

The harness learns from its own runs and from external feedback. Memory
is plain, inspectable data in the repository, never hidden state.

## Why plain-text memory

- Inspectable: a person can read and audit every entry.
- Versionable: the journal is committed with the paper's history.
- Durable: it survives an AI context window being truncated or lost.
- Portable: no database, no service, stdlib JSON.

## The run history

`papercheck --history` appends one JSON object per run to
`harness/reports/history.jsonl`:

```json
{"timestamp": "...", "tex": "manuscript/main.tex", "profile": "draft",
 "passed": false, "summary": {"errors": 1, "warnings": 3, "infos": 0},
 "check_ids": ["lang.hype", "methods.baseline"]}
```

History is ignored by git (it is per-run and machine-specific) but drives
the self-improvement analysis. The Makefile targets `harness-paper` and
`harness-submission` pass `--history` automatically.

## The memory journal

`scripts/memory.py` manages `harness/memory/memory.jsonl`. Each entry has
an `id`, a `timestamp`, a `kind`, `text`, `tags`, and a `status`
(`open`/`resolved`).

| kind | records |
| --- | --- |
| `decision` | an architectural or framing choice and its rationale |
| `lesson` | what a gate or a human caught and how it was fixed |
| `reviewer` | external review feedback, recorded verbatim in substance |
| `question` | an open question to resolve before submission |

```bash
python3 scripts/memory.py digest                       # session-start context
python3 scripts/memory.py add lesson "LOSO avoids leakage" --tags methods
python3 scripts/memory.py list --status open
python3 scripts/memory.py search leakage
python3 scripts/memory.py resolve 3 "Added baseline in Section 4.2"
```

The journal is committed to git; the run history and generated reports
are not.

## The retrospective loop

After each drafting phase and each review round, run the analyzer:

```bash
python3 scripts/self_improve.py --last 20 --strict
```

It mines the last N runs and the full journal for:

- **recurring findings** - check ids appearing in at least three runs;
- **trend** - error+warning counts, older half versus newer half;
- **chronic families** - a family present in every run of the window;
- **stale memory** - open entries older than the window, or open
  questions;
- **reviewer echoes** - open reviewer entries whose words match a
  recurring check family.

It writes `harness/reports/improvement_report.md` and, under `--strict`,
exits non-zero when the trend is regressing or a chronic family exists.

## From analysis to upgrade

The report maps each signal to a concrete action, for example:

| Signal | Suggested upgrade |
| --- | --- |
| `lang.*` or `claims.*` recurring | add the phrases to `forbidden_phrases.txt`, tighten the never-do list |
| `intro.*`/`structure.*`/`limits.*` recurring | add the rule to `playbooks/sections.md`, re-run `/draft-phase` |
| `methods.*` recurring | record a decision, update `papercheck.toml` |
| `bib.*` recurring | fix the `.bib` and add a pre-commit `harness-paper` |
| `blind.*`/`ethics.*`/`data.*` recurring | update venue settings, add a scrub step |
| `floats.*` recurring | regenerate figures with grayscale-safe styles |

## Closing the loop (Rule 7.5)

A mistake that reaches a reviewer twice is a harness bug. Encode it as a
deterministic check or a standing rule so it cannot recur silently. The
`reviewer echoes` section flags exactly these cases.

## Privacy

Record the substance of reviewer feedback, not who gave it. Never store
personal reviewer identities, contact details, or restricted data in the
journal. See `harness/policies/memory_policy.md`.
