# DECISIONS.md
Research and figure decisions with rationale.

---

## Figure Decisions

### 2026-03-04 — PDF/UA-2 Figure Tagging & Caption Styling Session

#### Problem
Figures completely absent from PDF tag tree. Acrobat accessibility panel skipped images entirely. No `<Figure>` elements despite `\DocumentMetadata{tagging=on}`.

#### Root Cause
Two issues:
1. Figures were in `paper/figures/` but path was unresolvable from the build context — CC discovered this by actually running the build with shell access and reading logs
2. LaTeX float machinery (`htbp` placement + `\begin{figure}` wrapping) is fundamentally incompatible with PDF/UA-2 tag tree ordering

#### Fix
1. Figures moved to `paper/sections/figures/` so paths resolve correctly
2. Added `--from markdown-implicit_figures` to build script — disables Pandoc's automatic float wrapping, images become inline `\includegraphics` only
3. Removed `\usepackage{float}` from template
4. Pandoc 3.9 automatically wires `alt=` from bracketed markdown text `![alt](path)` — no Lua filter needed for alt text

#### Caption Styling
- Captions written as plain paragraphs in markdown using `::: {.caption}` divs
- `caption-style.lua` filter converts divs to styled LaTeX
- Font: `\figurecaptionfont` (`\newfontfamily`) — named to avoid collision with `caption` package's reserved `\captionfont`
- Style: footnotesize, Atkinson Hyperlegible Mono, #767676 gray, italic
- Line height fixed by adding `\\par` inside the Lua filter block — `\linespread` and `\setlength{\baselineskip}` don't apply without a paragraph terminator

#### What We Tried That Didn't Work
- Lua filter with `\tagpdfsetup{alttext=}` — wrong key
- `alt=` on `\includegraphics` directly — graphicx not loaded when filter ran
- `\tagstructbegin/\tagstructend` wrapping — built successfully but images still untagged
- Raw LaTeX figure blocks — correct positioning but broke tagging entirely
- MacTeX update — not the issue
- `\linespread` and `\setlength{\baselineskip}` for line height — no effect without `\par`

#### Agents / Tools
- Created `lualatex-pandoc-debugger` agent in CC (Opus, all tools, project memory) — found the path issue and float fix by reading actual build logs
- Gemini assisted with the `\par` line height fix
- Key lesson: shell access + logs found in 20 minutes what we couldn't see in hours of template archaeology

#### Files Modified
- `build-paper.sh` — added `--from markdown-implicit_figures`, `--lua-filter=paper/filters/caption-style.lua`
- `paper/template.tex` — removed float package, added `\figurecaptionfont`
- `paper/filters/caption-style.lua` — created
- All five section markdown files — figures use plain `![alt](path)` syntax, captions in `::: {.caption}` divs

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
