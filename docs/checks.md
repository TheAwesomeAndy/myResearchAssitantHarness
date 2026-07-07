# Check reference

Every deterministic check in the `papercheck` engine, grouped by the
harness module it enforces. Severity is `error` (E), `warning` (W), or
`info` (I). Under the `draft` profile only errors fail; under
`submission` and `camera` warnings fail too. Infos never fail.

Run a single family with `--select`:

```bash
python3 -m papercheck manuscript/main.tex --select intro,methods --profile submission
python3 -m papercheck manuscript/main.tex --select title.length
python3 -m papercheck --list-checks
```

## M4A - Title, abstract, keywords

Config keys: `title.min_words`, `title.max_words`, `abstract.max_words`,
`abstract.min_sentences`, `abstract.max_sentences`, `keywords.min`,
`keywords.max`, `keywords.required`.

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `title.present` | E | no `\title` | add a title |
| `title.length` | E | title outside 8-13 words | tighten to the active-word band |
| `title.question` | E | title is a question | state the finding declaratively |
| `title.filler` | W | generic opener ("A study of...") | lead with method or finding |
| `abstract.present` | E | no abstract | add one |
| `abstract.length` | E | over 200 words | cut to the limit |
| `abstract.structure` | W | not four sentences | problem, motivation, achievement, implications |
| `abstract.citations` | W | `\cite` in the abstract | keep it self-contained |
| `keywords.count` | W | not 4-6 keywords | adjust the keyword set |

## M4B - Introduction

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `intro.present` | W | no introduction section | add one |
| `intro.roadmap` | E | "The rest of this paper is organized..." | replace with crunchy contributions |
| `intro.cliche-opening` | W | "In recent years..." opener | open with a concrete instance |
| `intro.gap` | W | fewer than two gap archetypes | combine at least two archetypes |
| `intro.contributions` | W | no contributions list | add an itemized list |
| `intro.forward-refs` | W | contributions lack section references | forward-reference the proving section |

## M4C - Methodology

Config keys: `venue.human_subjects`.

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `methods.present` | W | no methods section | add one |
| `methods.baseline` | E | no baseline language | compare against contemporary baselines |
| `methods.leakage` | W | pooled CV on human subjects | use leave-one-subject-out |
| `methods.reproducibility` | W | no seeds/versions/code | report them |
| `methods.robustness` | W | no ablation or stress test | add perturbation sweeps |
| `methods.future-tense` | W | future tense in methods | report completed work in past tense |

## M4D - Results, discussion, claims

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `results.speculation` | W | speculation in Results | move interpretation to Discussion |
| `discussion.present` | W | no discussion section | add one (or Results and Discussion) |
| `discussion.compare` | W | no citations in Discussion | compare with the literature (RCI) |
| `discussion.hedging` | W | no cautious verbs | hedge interpretation |
| `claims.overclaim` | E | "proves that", "undoubtedly" | soften to evidence language |
| `lang.significant` | W | "significant" without a test | report the test or say "substantial" |

## M4D-VIS - Figures and tables

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `floats.caption` | E | float with no caption | add a self-contained caption |
| `floats.label` | W | float with no label | add a label |
| `floats.referenced` | E | labelled float never referenced | introduce it with `\ref` |
| `floats.ref-before` | W | float appears before its reference | mention it in prose first |
| `floats.color-only` | W | "the red line" style references | add strokes, markers, or labels |

## M3/M4E/M4F - Structure, related work, limitations

Config keys: `related_work.prefer_postponed`.

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `structure.sections` | W | missing skeleton sections | add methods/results/discussion/conclusion |
| `limits.present` | E | no limitations | state 1-3 limitations |
| `limits.pivot` | W | limitation without a follow-up | add a defense or future-work pivot |
| `conclusion.abstract-copy` | E | conclusion copies the abstract | rewrite around takeaways |
| `related.position` | W | related work before methods | postpone the synthesis |
| `related.hostile` | W | hostile take-down of prior work | credit generously |
| `related.laundry-list` | W | citation-led sentence run | synthesize, do not enumerate |

## M5 - Compliance

Config keys: `venue.blinding`, `venue.human_subjects`.

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `blind.unset` | I | `venue.blinding` not set | set the blinding policy |
| `blind.author-block` | E | real name under double-blind | anonymize the author block |
| `blind.acknowledgments` | E | acknowledgments/funding under double-blind | remove until camera-ready |
| `blind.self-reveal` | W | "our previous work" | cite in the third person |
| `blind.links` | E | identifiable repo URL | use an anonymized mirror |
| `blind.metadata` | W | email or ORCID | remove until camera-ready |
| `single.authors-required` | E | no author block under single/none | add authors and affiliations |
| `ethics.statement` | E/W | no ethics statement for human data | add IRB and consent language |
| `data.availability` | E | no data-availability statement | add one |

`ethics.statement` is an error when `venue.human_subjects` is true and a
warning when human-subject terms are auto-detected in the text.

## L1 - Language and hype

Config keys: `language.allow_em_dash`.

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `lang.hype` | E | "groundbreaking", "revolutionary" | remove the marketing language |
| `lang.hype-claims` | W | "cutting-edge", "unprecedented" | back with evidence or remove |
| `lang.cautious` | E | "this proves ..." | use the suggested cautious rewrite |
| `lang.ai-tells` | W | "delve into", "rich tapestry" | rewrite in the paper's own voice |
| `lang.em-dash` | W | em dash character | use commas, colons, or parentheses |
| `lang.contractions` | W | "don't", "it's" | expand contractions |
| `lang.weasel` | I | "very", "extremely" | quantify instead of intensifying |

## BIB - Bibliography

Config keys: `paper.bib`, `bibliography.min_recent`,
`bibliography.recent_window`.

| id | sev | detects | fix |
| --- | --- | --- | --- |
| `bib.files` | I | citations but no `.bib` found | add `\bibliography{...}` or `paper.bib` |
| `bib.missing-entries` | E | cited key with no entry | add the entry or fix the key |
| `bib.duplicate-keys` | E | a key defined twice | keep one definition |
| `bib.missing-fields` | W | missing author/title/year | complete the record |
| `bib.uncited` | I | entries never cited | prune or cite |
| `bib.staleness` | W | too few recent references | cite current work |
