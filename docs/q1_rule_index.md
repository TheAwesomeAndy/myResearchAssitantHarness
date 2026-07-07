# Q1 rule index

Maps every rule in `docs/master-rule-framework.md` to its enforcement:

- **auto** - a deterministic check or script that runs in CI;
- **agent** - a protocol in the installed `CLAUDE.md`, a command, or a
  skill;
- **human** - a judgment the harness surfaces but a person decides.

## Layer 1 / Module 1 - AI environment

| Rule | Enforcement | Where |
| --- | --- | --- |
| 1.1 Anti-waterfall execution | agent | `CLAUDE.md` L1, `/draft-phase` |
| 1.2 Ghost verifier | agent | `CLAUDE.md` L1, `/revise` |
| 1.3 Knowledge anchoring | agent | `CLAUDE.md` L1 |
| 1.4 Strict pre-tool hooks (never-do list) | agent + auto | `CLAUDE.md` L1; `lang.*`, `claims.*`, `title.*`, `intro.roadmap` |
| Intellectual honesty | human + agent | `CLAUDE.md` L1 |

## Layer 2 / Module 2 - Ideation

| Rule | Enforcement | Where |
| --- | --- | --- |
| 2.1 Single-idea virus test | agent | `/idea-gate`, `idea-gate` skill |
| 2.2 Aunt pitch | agent | `/idea-gate` |
| 2.3 Novelty vs. originality | human | `/idea-gate` |
| 2.4 Anti-salami | human | `/idea-gate` |
| 2.5 Algorithmic journal selection | agent | `journal-selection` skill |
| Writing as a forcing function | agent | `CLAUDE.md` L2 |
| Wardle's law / mole hills | agent | `CLAUDE.md` L2 |

## Layer 3 / Module 3 - The Wall

| Rule | Enforcement | Where |
| --- | --- | --- |
| Draft in build order | auto | `scripts/phase_gate.py`, `harness-wall` |
| No later phase before an earlier one | auto | `phase_gate.py` |
| Declared-phase discipline | auto | `phase_gate.py --status` |
| Structural skeleton present | auto | `structure.sections` |

## Layer 4 / Module 4 - Sections

### A. Title, abstract, keywords

| Rule | Enforcement |
| --- | --- |
| Title 8-13 words | auto `title.length` |
| No question or filler title | auto `title.question`, `title.filler` |
| Abstract under 200 words | auto `abstract.length` |
| Four-sentence abstract | auto `abstract.structure` |
| Self-contained abstract | auto `abstract.citations` |
| 4-6 keywords | auto `keywords.count` |

### B. Introduction

| Rule | Enforcement |
| --- | --- |
| No roadmap paragraph | auto `intro.roadmap` |
| Concrete hook, no cliche | auto `intro.cliche-opening` |
| Compound research gap | auto `intro.gap` |
| Crunchy contributions | auto `intro.contributions` |
| Forward references | auto `intro.forward-refs` |

### C. Methodology

| Rule | Enforcement |
| --- | --- |
| Strict baselines | auto `methods.baseline` |
| No data leakage (LOSO) | auto `methods.leakage` |
| Perturbation stress tests | auto `methods.robustness` |
| Reproducibility details | auto `methods.reproducibility` |
| Past tense | auto `methods.future-tense` |
| Completeness (vendors, controls) | human |

### D. Results and discussion

| Rule | Enforcement |
| --- | --- |
| Results state facts only | auto `results.speculation` |
| RCI: compare with literature | auto `discussion.compare` |
| Cautious semantics | auto `discussion.hedging`, `claims.overclaim`, `lang.significant` |
| Grayscale/colorblind figures | auto `floats.color-only` |
| Floats captioned, labelled, referenced | auto `floats.caption`, `floats.label`, `floats.referenced`, `floats.ref-before` |
| RCI paragraph order | human |

### E. Related work

| Rule | Enforcement |
| --- | --- |
| Postponed synthesis | auto `related.position` |
| Generous credit | auto `related.hostile` |
| Synthesis, not listing | auto `related.laundry-list` |
| Critical comparison matrix | human |

### F. Conclusion and limitations

| Rule | Enforcement |
| --- | --- |
| Own the weaknesses | auto `limits.present` |
| Defensive pivot | auto `limits.pivot` |
| Not a copy of the abstract | auto `conclusion.abstract-copy` |

## Layer 5 / Module 5 - Submission

| Rule | Enforcement |
| --- | --- |
| Blinding scrub (double) | auto `blind.author-block`, `blind.acknowledgments`, `blind.self-reveal`, `blind.links`, `blind.metadata` |
| Author block (single/camera) | auto `single.authors-required` |
| Ethics statement | auto `ethics.statement` |
| Data availability | auto `data.availability` |
| Three-paragraph cover letter | auto `scripts/check_cover_letter.py` |
| Reviewer suggestion hard-blocks | agent (`CLAUDE.md` L5) |
| Bullfighter rebuttal | auto + agent (`scripts/check_rebuttal.py`, `/rebuttal`) |

## Layer 6 / Module 6 - Amplification

| Rule | Enforcement |
| --- | --- |
| Publication date, press release, thread, graphical abstract | agent (`/amplify`, `amplification` skill) |

## Module 7 - Memory and self-improvement

| Rule | Enforcement |
| --- | --- |
| 7.1 Run history | auto `papercheck --history` |
| 7.2 Project memory journal | auto `scripts/memory.py` |
| 7.3 Retrospective loop | agent + auto (`/retro`, `scripts/self_improve.py`) |
| 7.4 Self-improvement analysis | auto `scripts/self_improve.py` |
| 7.5 Close the loop | human + agent (`/retro`, `memory_policy.md`) |
