# How Models Think
## A three-paper series on accessibility knowledge in language models

**Author:** Trisha Salas  
**Series question:** How do language models acquire, represent, and store
domain-specific accessibility knowledge — and what does that tell us about
the limits and possibilities of AI-powered accessibility tooling?

---

## The Papers

### [Paper 1: Testing Accessibility Knowledge Across Pythia Model Sizes](./paper-1-emergence/)
*Published January 2026*

Behavioral emergence study. When do accessibility concepts (screen reader,
alt text, WCAG, ARIA) become accessible to model outputs? Answer: 2.8B
parameters for most concepts, never for ARIA. Recognition precedes generation.
Code: [mech-interp-research](https://github.com/trishasalas/mech-interp-research)

### [Paper 2: Does Accessibility Knowledge Exist Before It Emerges?](./paper-2-probing/)
*In progress*

Linear probing study. Is accessibility knowledge geometrically present in
smaller models before the behavioral threshold? Bridges Paper 1's behavioral
findings to Paper 3's mechanistic findings.

### [Paper 3: How Models Think About Accessibility](./paper-3-mechanistic/)
*In progress*

Mechanistic study. Using causal tracing, logit lens, and MLP/attention
decomposition on GPT-2 Medium/Large/XL to understand *how* accessibility
knowledge is stored — and whether it uses different mechanisms than general
factual knowledge.

---

## Repository Structure

```
how-models-think/
├── src/                    ← shared analysis library
│   ├── models.py           ← model loading, ModelInfo, memory management
│   ├── logit_lens.py       ← logit lens analysis
│   ├── decompose.py        ← MLP vs attention decomposition
│   ├── heads.py            ← attention head analysis
│   ├── viz.py              ← visualization utilities
│   ├── perplexity.py       ← perplexity / recognition probing
│   └── probe.py            ← linear probing (in progress)
├── paper-1-emergence/      ← published, code in mech-interp-research
├── paper-2-probing/        ← in progress
├── paper-3-mechanistic/    ← in progress
└── notes/
    ├── DECISIONS.md        ← architectural decisions with rationale
    └── OBSERVATIONS.md     ← experimental findings and hypotheses
```

---

## Note on repo history

*February 2026: Restructured as three-paper series. Original GPT-2 mechanistic
notebooks and results moved to `paper-3-mechanistic/`. Paper 2 probing work
added. Shared `src/` library extracted from notebook code.*
