# Master Rule Framework: High-Impact Q1 Research Architecture

This document is the canonical specification for the harness. Every rule
below is enforced one of three ways, and `docs/q1_rule_index.md` maps each
rule to its enforcement point:

- **auto** - a deterministic check in the `papercheck` engine or a
  standalone script; runs in `make harness-verify` and CI;
- **agent** - a protocol the AI assistant must follow, encoded in
  `templates/claude/` (CLAUDE.md, skills, commands);
- **human** - a judgment call the harness surfaces but a person decides.

**System role for the AI assistant:** act as a ruthless, elite academic
peer reviewer, a Q1 journal editor, and a senior AI systems engineer.
Enforce extreme methodological rigor, strategic narrative framing, and
strict compliance with high-impact journal standards.

---

## Layer 1: AI Operational Directives (the Karpathy-level protocol)

1. **Agile execution, no waterfalling.** Never draft or review an entire
   paper in a single massive output. Break work into tightly scoped,
   sequential phases. Execute one phase, present the output, and STOP.
   Wait for explicit verification before proceeding.
2. **The verification layer (the ghost verifier).** The AI is a
   statistical simulator, not an intuition machine. Before generating
   text or code, explicitly state the evaluation criteria the output must
   satisfy, then check the output against them. Force the user to verify
   key decisions.
3. **Intellectual honesty.** If an experiment yields a negative result or
   lower accuracy than a baseline, report it exactly as measured. Never
   massage data or fabricate benchmark superiority.
4. **Knowledge-base anchoring.** Do not rely on general training data for
   venue-specific claims. Anchor to the target journal's submission
   guidelines, 5-10 model papers from that venue, and the project's own
   dataset and results.
5. **Strict pre-tool hooks.** Standing "never do" rules live in the
   installed CLAUDE.md: never hallucinate data, never invent citations,
   never write hype, never use puns or lyrics in titles. The AI checks
   these before every write or edit.

## Layer 2: Core Research Philosophy

1. **Writing as a forcing function (lazy evaluation).** Do not wait for
   the research to be "finished" to write. Drafting crystallizes ideas
   and exposes gaps early.
2. **The idea as a virus.** A paper delivers a single, reusable,
   infectious idea. Enforce the declaration test early: the paper must be
   able to complete the sentence "The main idea of this paper is ...".
3. **Wardle's law.** Every paper answers two questions: "Is it true?" and
   "So what - who cares?".
4. **Mole hills, not mountains.** Define a specific, soluble problem.
   Over-ambition guarantees failure.

## Module 1: The AI and System Environment

- **Rule 1.1 Anti-waterfall execution** - one scoped micro-task at a
  time; present, verify, proceed.
- **Rule 1.2 The ghost verifier** - evaluation criteria precede content.
- **Rule 1.3 Knowledge-base anchoring** - venue guidelines and model
  papers in-context before drafting.
- **Rule 1.4 Strict pre-tool hooks** - standing "never do" rules in the
  root CLAUDE.md, checked before edits.

## Module 2: Ideation and Target Acquisition (desk-reject prevention)

- **Rule 2.1 The single-idea virus test** - one reusable idea; narrow
  mountains into mole hills.
- **Rule 2.2 The "aunt" pitch** - the core message fits one
  plain-speaking sentence.
- **Rule 2.3 Novelty vs. originality** - new knowledge, not just a new
  permutation of old tests.
- **Rule 2.4 Anti-salami-slicing** - block splitting one study into
  minimum-publishable units.
- **Rule 2.5 Algorithmic journal selection** - build the target list from
  journals appearing 2+ times in the reference list; verify aims and
  scope, time-to-publication, open-access options; screen for predatory
  venues.

## Module 3: The Inside-Out Drafting Engine (the Wall)

A paper is read Head -> Body -> Tail, but it is built like a wall, in
this order. The `scripts/phase_gate.py` gate enforces the sequence:

1. Figures, tables, and data (the concrete core).
2. Methodology (how the data was obtained).
3. Results (the facts).
4. Discussion (the interpretation of the facts).
5. Conclusions and limitations (the takeaways).
6. Introduction and literature review (written after the destination is
   known).
7. Title, abstract, and keywords (the marketing wrappers).

## Module 4: Section-by-Section Micro-Rules

### A. Title, abstract, keywords

- Title: 8-13 active, specific words; no puns, lyrics, metaphors, or
  questions; no generic filler openers ("An investigation into...", "A
  study of..."); a colon subtitle is allowed and correlates with
  citations.
- Abstract: under 200 words; the Kent Beck 4-sentence structure -
  (1) the problem, (2) why it is interesting, (3) what the solution
  achieves, (4) the broader implications; self-contained, no citations.
- Keywords: 4-6 search-optimized terms; specific but not private jargon.

### B. The introduction (page-1 gold dust)

- Hook the reader with a concrete instance of the problem before
  generalizing; no cliche openings ("In recent years...").
- The compound research gap: end the introduction with a gap combining
  at least two archetypes - lack of research, lack of consensus,
  limitations of previous methods, practical real-world bottleneck.
- Crunchy contributions ("celery, not spaghetti"): eradicate the roadmap
  paragraph ("The rest of this paper is organized as follows...");
  replace it with a bulleted list of refutable claims, each carrying a
  forward-reference to the section that proves it.

### C. Methodology (absolute reproducibility)

- Strict baselines: never benchmark only against weak classical models;
  compare against contemporary architectures.
- No data leakage: for human-subject data use subject-wise validation
  (e.g. leave-one-subject-out) instead of pooled k-fold; defend against
  identity leakage explicitly.
- Perturbation stress tests: inject noise (jitter, channel dropout) and
  map exact failure thresholds.
- Grammar: past tense; completeness - vendors, versions, seeds,
  hyperparameters, statistical software, control samples.
- Ethical compliance statement whenever human or animal subjects appear.

### D. Results and discussion (the RCI matrix)

- Results state observed facts only; speculation belongs in the
  discussion.
- Every discussion paragraph follows RCI: Restate the result, Compare
  with literature, Explain the finding, Interpret the broader meaning.
- Cautious semantics: "this suggests / indicates / a likely
  explanation", never "this proves".
- Visuals: figures over tables for trends; grayscale- and
  colorblind-safe (varied stroke patterns, never color-only references);
  every float introduced in the text before it appears.
- Own the weaknesses: state limitations boldly and weaponize them as
  boundary conditions or robustness trade-offs.

### E. Related work (the postponed synthesis)

- Push exhaustive literature synthesis late in the paper; no "sandbar"
  of dense citations on page 1.
- Synthesis, not listing: no laundry-list paragraphs ("A did X. B did
  Y."); group references to support arguments.
- Credit is like love: generous acknowledgment ("insightful",
  "inspiring"); no hostile take-downs.
- Critical comparison matrix: multi-axis comparison against the
  strongest prior work.

### F. Conclusion and limitations

- The conclusion is not a copy of the abstract.
- List one to three limitations; follow each with a defense, a
  contribution-despite-the-flaw, or a future-work pivot.

## Module 5: Submission and Peer-Review Navigation

- **Blind compliance:** double-blind - scrub names, affiliations,
  acknowledgments, funding, identifiable repository URLs, self-revealing
  citations; single-blind - authors and affiliations required.
- **Data governance:** a visible data-availability and ethics statement
  is mandatory.
- **The 3-paragraph cover letter:** a sober, un-hyped pitch, at most one
  page - (1) what the paper says, (2) why it matters, (3) why it fits
  this journal's ongoing conversation.
- **Reviewer selection:** suggest reviewers from the reference list;
  hard-block co-authors, close colleagues, and same-institution names.
- **The rebuttal framework (bullfighting):** 7-day cooling-off; strip
  emotion; itemized point-by-point replies with exact page/line numbers;
  rewrite critiqued text so it cannot be misunderstood twice.

## Module 6: Post-Publication Amplification

- Acquire the exact publication date from the journal.
- Generate a layman-accessible press release, a social thread on the
  paper's core utility, and prompts for a graphical abstract and a
  video/audio overview.

## Module 7: Memory and Self-Improvement

The harness learns from its own runs and from external feedback. Memory
is plain, inspectable data in the repository, never hidden state.

- **Rule 7.1 Run history.** Every checker run can append a one-line JSON
  summary to `harness/reports/history.jsonl` (the `--history` flag).
  History is the raw material for improvement analysis.
- **Rule 7.2 The project memory journal.** Durable knowledge lives in
  `harness/memory/memory.jsonl`, managed by `scripts/memory.py`:
  decisions (with rationale), lessons (what a gate caught and why),
  reviewer feedback (verbatim, source-tagged), and open questions. The
  AI assistant reads the memory digest at session start and records new
  entries at every phase boundary; memory survives context loss.
- **Rule 7.3 The retrospective loop.** After each drafting phase and
  after every external review round, run a retrospective: what did the
  gates catch, what did they miss, what did a human or reviewer catch
  that a gate should have caught.
- **Rule 7.4 Self-improvement analysis.** `scripts/self_improve.py`
  mines the run history and memory journal for recurring findings and
  regressions, and emits concrete harness upgrades: phrases to add to
  `harness/forbidden_phrases.txt`, rules to add to the CLAUDE.md
  never-do list, checks to tighten in `harness/papercheck.toml`, and
  memory entries to resolve. Suggestions are advisory; a human approves
  each change.
- **Rule 7.5 Close the loop.** A recurring mistake that reaches a
  reviewer twice is a harness bug: encode it as a deterministic check or
  a standing rule so it cannot recur silently.
