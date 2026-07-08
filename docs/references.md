# Further reading

The harness distills several established schools of thought. This list
describes the ideas rather than prescribing specific sources; find the
canonical texts in each tradition and add them to your own reading.

## Agile, AI-assisted drafting

The Layer 1 protocol follows the practice of treating a large language
model as a component in a verified loop rather than an oracle: work in
tightly scoped steps, define acceptance criteria before generating,
verify every output, and keep the human in the decision seat. The "ghost
versus animal" framing (a statistical simulator without intrinsic
intuition) motivates the ghost-verifier rule.

## Classic "how to write a paper" advice

The manuscript-construction layers draw on the long tradition of
research-writing guidance:

- the single-idea paper: a paper should deliver one reusable, memorable
  idea, stated early (the declaration test);
- inside-out drafting: build the paper from figures and results outward,
  and write the introduction once the destination is known (the Wall);
- the compound research gap: motivate the work by combining archetypes of
  what is missing;
- crunchy contributions: replace the boilerplate roadmap with refutable,
  forward-referenced claims;
- generous related work: credit prior work warmly and synthesize it
  rather than listing it.

## Evaluation rigor

The methodology checks encode standard defenses against inflated results:
strong contemporary baselines, subject-independent validation to prevent
identity leakage, perturbation stress tests to map failure thresholds,
and full reproducibility reporting.

## Reviewer and rebuttal etiquette

The submission layer follows the collegial-negotiation view of peer
review: a sober cover letter, a cooling-off period before responding, and
an itemized, courteous, precisely located rebuttal that treats each
comment as a point to address rather than an attack to repel.

## The forbidden-phrase and hype lists

The specific phrase lists the harness enforces live in
`papercheck/vocab.py` and `harness/forbidden_phrases.txt`, not here, so
that this document stays free of the language the harness flags.
