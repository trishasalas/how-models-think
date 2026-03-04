# DECISIONS.md
Research and figure decisions with rationale.

---

## Figure Decisions

### 2026-03-03 — Exclude Pythia 160M from summary figure (fig-01-summary)

**Decision:** Pythia 160M is excluded from the Figure 1 summary line graph. The emergence trajectory figure runs from 410M to 6.9B.

**Rationale:** 160M's binding depth ratio (11/12 = 0.92) is visually misleading in both the normalized and z-scored versions. Layer 11 in a 12-layer model does not represent the same representational depth as layer 29 in a 32-layer model, even though the ratio looks similar. The high starting point dominates the figure and obscures the V-shape + cliff that is the actual finding. 160M is effectively a control condition — it demonstrates that very small models do not achieve emergence — and this is covered clearly in the results text. The emergence story lives in the 410M–6.9B range.

**160M is retained in:** all results tables, Experiment 4 binding persistence bar chart (fig-binding-persistence.png), and all discussion of the full Pythia suite. It is not omitted from the paper, only from this specific summary figure.

---

## Abstract Decisions

### 2026-03-03 — Rewrite abstract to lead with finding

**Decision:** Abstract rewritten to open with the north star finding rather than domain setup.

**Rationale:** Original abstract opened with "WCAG represents a specialized domain..." — context-first framing that buried the thesis. Neel Nanda's BLUF framework informed the revision. New abstract opens with sustained deep-network binding as necessary structural condition, introduces WCAG as the test domain in sentence two with explicit rationale ("we use X because Y"), and names both coined terms ("fluent wrongness", "declarative-evaluative gap") explicitly.

---

## Title Decisions

### 2026-03-03 — Final title

**Decision:** "Sustained Deep-Network Binding Is a Correlate of Accessibility Concept Emergence: Evidence from the Pythia and GPT-2 Model Suites"

**Rationale:** Finding-first structure per BLUF principle. "Is a correlate of" chosen over "predicts" (overclaims causation) and "suggests/hints at" (undersells the finding). "Correlate" is precise, defensible, and already used in the paper body. Model families named for discoverability.
