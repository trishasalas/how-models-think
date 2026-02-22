# Paper 3: How Models Think About Accessibility
# A Mechanistic Taxonomy of Domain-Specific Knowledge Storage

**Status:** In progress

## Research Question

How is accessibility knowledge stored mechanistically in GPT-2 models that
succeed at accessibility tasks? And does domain-specific knowledge use
different storage mechanisms than general factual knowledge?

## Key findings so far

See `../notes/OBSERVATIONS.md` for full experimental notes.

**Memory taxonomy (emerging):**
- Proper noun facts (Space Needle, Paris): tight localized MLP signal at
  subject's last token in mid layers — consistent with ROME (Meng et al. 2022)
- Acronym expansion facts (ARIA): distributed signal across expansion tokens,
  anchored to final content word ("Internet"), not the acronym itself
- General HTML concepts (alt text): frame-sensitive retrieval where prompt
  construction determines which prior dominates

**Capacity ambiguity hypothesis:**
Larger models show *more* mid-layer uncertainty for domain-specific terms
because they encode more plausible completions. Resolution is pushed to later
layers where MLP capacity can overpower competing hypotheses.

**MLP dominance increases with scale:**
Medium: attention-led (compensating for weak MLP capacity)
Large: late MLP dominant
XL: attention nearly irrelevant, single late MLP layer carries the load

## Models

GPT-2 Medium, Large, XL — sequential attention+MLP architecture chosen
deliberately over Pythia (see `../notes/DECISIONS.md`)

## Needs

- Causal tracing on WCAG and alt text to extend memory taxonomy
- Paris/Berlin as proper noun controls
- Connection to Paper 2 probing results
