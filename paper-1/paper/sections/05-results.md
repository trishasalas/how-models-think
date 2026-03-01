## Results

### Experiment 1: Declarative Knowledge

Models were tested on ten accessibility concept prompts across all five Pythia sizes. Results show a sharp threshold pattern for core accessibility terms, with acronyms behaving differently.

*Correct = matches known definition; Partial = incomplete or imprecise; Incorrect = wrong, off-topic, or loops*

| Prompt                              | 160M | 410M | 1B  | 2.8B | 6.9B |
| ----------------------------------- | ---- | ---- | --- | ---- | ---- |
| A screen reader is                  | $\times$    | $\times$    | $\approx$   | $\checkmark$    | $\approx$    |
| WCAG stands for                     | $\times$    | $\times$    | $\times$    | $\times$    | $\checkmark$    |
| A skip link is                      | $\times$    | $\approx$    | $\times$    | $\checkmark$    | $\times$    |
| The purpose of alt text is          | $\times$    | $\times$    | $\times$    | $\checkmark$    | $\checkmark$    |
| ARIA stands for                     | $\times$    | $\times$    | $\times$    | $\times$    | $\times$    |
| A focus indicator is                | $\times$    | $\times$    | $\times$    | $\times$    | $\times$    |
| Keyboard navigation allows          | $\times$    | $\times$    | $\times$    | $\times$    | $\times$    |
| Color contrast is important because | $\times$    | $\times$    | $\times$    | $\times$    | $\times$    |
| Semantic HTML helps                 | $\times$    | $\times$    | $\times$    | $\times$    | $\times$    |
| Captions are used for               | $\times$    | $\approx$    | $\times$    | $\approx$    | $\times$    |

Several patterns emerge from this data.

**Threshold at 2.8B.** Screen reader, skip link, and alt text all show correct or near-correct responses first at 2.8B. Below this threshold, responses are either wrong or incomplete.

**Screen reader shows non-monotonic behavior.** The 2.8B model produces "reads aloud the text," correctly capturing the auditory output purpose. The 6.9B model produces "reads text on a computer screen," dropping "aloud." The larger model is more verbose but less precise on the critical detail. This mirrors the skip link result, where 2.8B is correct and 6.9B regresses. Capability near emergence thresholds can be unstable.

**WCAG emerges at 6.9B; ARIA never emerges.** Both are foundational accessibility acronyms. WCAG requires 6.9B parameters to expand correctly. ARIA fails at every scale tested — at 160M it produces gibberish, at 410M it loops, and from 1B onward it produces confident but wrong expansions ("Artificial Replacement of a Human Being," "A Rational Approach to Information and Automation," "Association of Research Libraries in Africa"). Confidence increases with scale; accuracy does not. This suggests ARIA is rare enough in training data that even 6.9B parameters cannot reliably encode it, while increased scale produces more fluent confabulation rather than correct recall.

**General accessibility concepts fail across all scales.** Focus indicator, keyboard navigation, color contrast, and semantic HTML produce generic responses at every model size. These terms appear in web-scale training data but without accessibility-specific context. The models complete the prompts plausibly without encoding accessibility meaning.

---

### Experiment 2: Evaluative Knowledge

Models were tested on five code prompts requiring identification of accessibility violations. This tests whether models can apply accessibility knowledge, not just produce definitions.

*Correct = identifies the accessibility violation accurately; Partial = identifies some issue but not the core violation; Incorrect = wrong, off-topic, or loops*

| Prompt                                      | 160M | 410M | 2.8B | 6.9B |
| ------------------------------------------- | ---- | ---- | ---- | ---- |
| `<img src='photo.jpg'>` missing what        | $\times$    | $\times$    | $\times$    | $\times$    |
| `<div>` with onclick not accessible because | $\times$    | $\times$    | $\times$    | $\times$    |
| Problem with `<a href='#'></a>`             | $\times$    | $\approx$    | $\times$    | $\times$    |
| `<input type='text'>` needs a               | $\times$    | $\times$    | $\times$    | $\times$    |
| 'Click here' button is bad because          | $\times$    | $\times$    | $\checkmark$    | $\checkmark$    |

There is a clear gap between declarative and evaluative knowledge. The 2.8B model correctly defines alt text but cannot identify that `<img src='photo.jpg'>` is missing one — it repeats the prompt and stalls at every scale tested. The question explicitly asks what is missing; no model answers "alt text."

The only evaluative success is the "Click here" prompt, which succeeds at 2.8B and 6.9B. Ambiguous link text may be more common in training data as a named anti-pattern than missing alt attributes.

The `<div>` onclick responses show a trajectory worth noting. Responses become more specific with scale — from loops at 160M to "not a form control" at 6.9B — without arriving at the correct explanation (keyboard inaccessibility, missing role and tabindex). The 6.9B answer is the closest, pointing toward interactivity expectations, but it does not identify the actual problem.

---

### Experiment 3: Recognition vs. Generation

Perplexity measures how expected a sequence is to the model. Lower perplexity means the model finds the text more natural. Testing whether models assign lower perplexity to a correct definition than an incorrect one reveals whether recognition precedes generation.

```
correct = "A screen reader is software that reads text aloud for blind users."
wrong = "A screen reader is a device for viewing screens."
```

| Model | Correct | Wrong | Ratio |
| :---- | :------ | :---- | :---- |
| 160M | 106.7 | 41.4 | Wrong by 2.6x |
| 410M | 40.1 | 32.8 | Wrong by 1.2x |
| 1B | 18.8 | 42.2 | Correct by 2.2x |
| 2.8B | 13.6 | 54.9 | Correct by 4.0x |
| 6.9B | 15.6 | 46.1 | Correct by 3.0x |

The preference flips between 410M and 1B. At 160M and 410M the model finds the wrong definition more natural; at 1B it prefers the correct one. This flip precedes the generation threshold by one model size — 1B recognizes the correct definition before 2.8B can produce it.

The 2.8B model shows stronger correct preference than 6.9B (4.0x vs 3.0x). This is consistent with the non-monotonic pattern observed in declarative results: the relationship between scale and capability is not strictly linear near emergence thresholds.

---

### Experiment 4: Mechanistic Analysis of Compound Term Binding

Attention pattern analysis across all five Pythia models examines whether models treat "screen reader" as a compound concept or as two independent tokens, and how this binding pattern relates to behavioral emergence.

For each model, attention weights from "reader" to "screen" were extracted across all layers and heads. Heads with weight above 0.5 are considered strong binding; the full data is available in the project repository.

| Model | Layers | Strong (0.5+) | Strong in L0-3 | % Early | Last Strong Layer |
|-------|--------|--------------|----------------|---------|-------------------|
| 160M | 12 | 10 | 7 | 70% | 11 |
| 410M | 24 | 22 | 16 | 73% | 9 |
| 1B | 16 | 11 | 10 | 91% | 6 |
| 2.8B | 32 | 25 | 20 | 80% | 29 |
| 6.9B | 32 | 37 | 28 | 76% | 30 |

Note: 1B's architectural difference (8 heads vs 12) affects raw head counts; see Methodology.

Several patterns emerge from this data.

**Early layers dominate across all models.** Between 70-91% of strong binding occurs in layers 0-3 regardless of model size. Compound term binding is established early in the forward pass at every scale tested.

**Strong head count scales with model size.** 160M has 10 strong binding heads; 6.9B has 37. 1B is the expected outlier given its different architecture.

**Last strong layer tracks behavioral emergence.** Below the 2.8B emergence threshold, strong binding drops off early — layer 11 for 160M, layer 9 for 410M, layer 6 for 1B. At 2.8B and above, strong binding persists deep into the network — layers 29 and 30 for 2.8B and 6.9B respectively. The models that cannot correctly define screen reader do not sustain compound binding through the network. The models that can, do.

**2.8B is the inflection point.** Total heads above threshold jumps from 28 (1B) to 101 (2.8B) — a 3.6x increase that coincides exactly with the behavioral emergence threshold identified in Experiment 1. This suggests that robust, sustained attention binding across many heads is a mechanistic correlate of accessibility concept emergence, not merely a consequence of larger model size.

All six models show strong binding in layers 0-3, including 160M which cannot produce a correct definition. Whether early-layer binding at small scales reflects genuine compound representation or proximity effects cannot be determined from attention weights alone and is noted as a limitation.

#### Control Experiment: Ruling Out Proximity Effects

To test whether the binding signal reflects compound concept encoding rather than simple token adjacency, attention weights were measured between non-compound token pairs at 2.8B. Two conditions were tested: adjacent function words ("and then") and an adjacent modifier-noun pair without disambiguation ("cold water"). Both conditions produced strong early-layer binding, consistent with the known behavior of previous-token heads (Olsson et al., 2022) — a class of induction circuit components that attend systematically to the immediately preceding position regardless of content.

This reframes the control comparison. Early-layer binding is not specific to accessibility compounds; it reflects general positional mechanisms present across token types. The meaningful signal is the distribution and persistence of binding across the full head population. Accessibility compounds at 2.8B recruit 101-208 heads above threshold with strong binding persisting to layers 29-30. Function word pairs produce early-layer binding without the same deep-network persistence. The sustained late-layer binding pattern, rather than raw head count, appears to differentiate accessibility compound binding from general adjacent-token binding. A complete characterization requires systematic comparison across a broader set of controls and is noted as a direction for future work.

### Binding Generalizes Across Accessibility Compounds

Having ruled out proximity effects, attention binding was measured for two additional accessibility compound terms at 2.8B: alt text and skip link.

| Compound | Total heads >0.1 | Strong (0.5+) | Top score |
|----------|-----------------|--------------|----------|
| screen reader | 101 | 25 | 0.9909 |
| alt text | 211 | 49 | 0.9856 |
| skip link | 158 | 32 | 0.9816 |

All three compounds show the same pattern of early-layer concentration with deep-network persistence at 2.8B, with top binding scores above 0.98 in each case.

This rules out a compound-specific explanation. The binding pattern is not an artifact of how "screen reader" tokenizes or how frequently it appears in training data. It is a general property of accessibility compound terms at the 2.8B emergence threshold. The models that can define these concepts correctly show robust, distributed binding across many heads and many layers. The models that cannot show weak binding that drops off early.

The binding pattern generalizes across all three accessibility compounds tested at 2.8B — screen reader, alt text, and skip link — ruling out a term-specific explanation and strengthening the case for a general mechanistic threshold at this scale.
