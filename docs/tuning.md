# Tuning the harness for your field

The default checks encode one school of thought, calibrated for empirical
machine-learning and signal-processing papers. Most of the value is
universal (hype, overclaiming, dangling references, missing statements),
but several checks are field-specific. This guide shows how to adapt the
harness so it helps rather than nags.

Everything here is done in `harness/papercheck.toml` and the vocabulary
files. No code changes are needed for tuning; adding a brand-new rule is
covered at the end.

## The three tuning levers

1. **Config values** - loosen or tighten a check's parameters
   (`title.max_words`, `abstract.max_sentences`, ...).
2. **`checks.disable`** - turn a check off entirely (exact id or dotted
   prefix, e.g. `"methods"` disables all `methods.*`).
3. **`checks.warn_only`** - keep a check but downgrade its errors to
   warnings, so it never blocks the `submission` profile. This only
   affects error-severity checks; a check that is already a warning is
   unchanged by `warn_only` (use `disable`, or the `draft` profile, to
   stop a warning from blocking submission). See `docs/checks.md` for
   each check's severity.

You can also scope a single run with `--select` / `--skip`:

```bash
python3 -m papercheck manuscript/main.tex --skip methods,floats
python3 -m papercheck manuscript/main.tex --select title,abstract,lang
```

`warn_only` is for an error-severity rule you want to see but not be
blocked by yet. For example, while a data-sharing agreement is pending:

```toml
[checks]
warn_only = ["data.availability"]   # error -> warning; still reported
```

## What is universal vs. field-specific

| Always keep | Often field-specific |
| --- | --- |
| `lang.hype`, `lang.cautious`, `claims.overclaim` | `methods.baseline`, `methods.leakage`, `methods.robustness` |
| `title.question`, `title.filler` | `methods.reproducibility` (theory papers) |
| `intro.roadmap` | `results.speculation` (some venues merge Results/Discussion) |
| `bib.missing-entries`, `bib.duplicate-keys` | `data.availability` (non-data papers) |
| `floats.caption`, `floats.referenced` | `abstract.structure` (structured-abstract venues) |
| `limits.present` | `keywords.count`, `title.length` (venue-dependent) |

## Field profiles

Copy the block that fits and paste it into `harness/papercheck.toml`.

### Theory / mathematics (no experiments)

```toml
[venue]
blinding = "none"

[title]
max_words = 18            # theory titles run longer

[checks]
disable = [
  "methods.baseline", "methods.leakage", "methods.robustness",
  "methods.reproducibility", "results.speculation", "data.availability",
]
```

### Qualitative / HCI / social science

```toml
[abstract]
min_sentences = 1         # structured or narrative abstracts vary
max_sentences = 8

[checks]
# methods.baseline is an error; the rest are warnings that would still
# block the submission profile, so disable the ones that do not apply.
disable = [
  "methods.baseline", "methods.leakage",
  "methods.robustness", "results.speculation",
]
```

### Clinical / medical (human subjects, strict ethics)

```toml
[venue]
blinding = "double"
human_subjects = true     # makes ethics.statement and methods.leakage errors

[bibliography]
recent_window = 3         # medicine expects very recent references
min_recent = 5
```

### Empirical ML at a structured-abstract venue (e.g. IEEE)

```toml
[abstract]
min_sentences = 1         # IEEE abstracts are not four sentences
max_sentences = 10

[keywords]
required = true           # IEEE requires index terms

[checks]
disable = ["abstract.structure"]   # already a warning; disable to stop it blocking
```

### Venue that wants a roadmap paragraph

Some venues explicitly ask for "the rest of this paper is organized as
follows". If yours does:

```toml
[checks]
disable = ["intro.roadmap"]
```

## Adapting the vocabulary

The phrase lists live in `papercheck/vocab.py`. Editing them changes what
several checks match at once, consistently.

- Add a hype word your field overuses: append to `HYPE_ERROR` or
  `HYPE_WARN`.
- Add a field-specific machine-writing tell: append to `AI_TELLS`.
- Add a gap-archetype phrase common in your literature: extend the right
  tuple in `GAP_ARCHETYPES`.
- Add a validation term your field uses for leakage-safe splits: append
  to `SUBJECT_SAFE_VALIDATION` (e.g. a domain-specific protocol name).

For project-specific banned phrases that are not part of the shared
vocabulary (a competitor's trademark, an internal codename, a phrase a
reviewer flagged), add them one per line to
`harness/forbidden_phrases.txt`. That file is scanned by
`scripts/check_forbidden_phrases.py`, separate from the engine.

## Blinding and venue

Always set these first; several checks are inert until you do:

```toml
[venue]
name = "Journal Name"     # cover-letter fit is checked against this
blinding = "double"       # "double" | "single" | "none"
human_subjects = true     # escalates ethics + leakage checks
```

## A 10-minute adaptation recipe

1. Run once with defaults:
   `python3 -m papercheck manuscript/main.tex --profile draft`.
2. For each finding that is wrong *for your field* (not wrong for your
   paper), decide: loosen a value, `warn_only`, or `disable`.
3. Put those decisions in `harness/papercheck.toml` and re-run.
4. Record why in the memory journal so the choice is not silently lost:
   `python3 scripts/memory.py add decision "disabled methods.leakage: theory paper, no data" --tags config`.
5. Commit the config. It travels with the paper.

Do not disable a check just because it is inconvenient for *this* paper.
`warn_only` keeps the signal visible without blocking; `disable` is for
rules that genuinely do not apply to your field.

## Adding a brand-new check

When your field needs a rule the harness does not have (a required
"Reporting checklist" section, a units convention, a preregistration
statement), add a check. The full worked example is in
`docs/architecture.md`; the short version:

1. Write the function in the right `papercheck/checks/<family>.py` with
   `@register("family.id", "title", "MODULE")`.
2. Add unit tests and a `fixtures/paperlint/<case>/` fixture.
3. Add a row to `docs/checks.md`.

Because every check is registered and data-driven, your custom rule gets
the same profiles, `--select`, config disabling, and reporting as the
built-ins for free.
