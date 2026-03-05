## Results

### Experiment 1: Declarative Knowledge

A correct response demonstrates that the model has encoded the accessibility concept at the scale tested; incorrect or partial responses indicate the concept has not yet emerged.

Models were tested on ten accessibility concept prompts across all five Pythia sizes. Results show a sharp threshold pattern for core accessibility terms, with acronyms behaving differently.

*Correct = matches known definition; Partial = incomplete or imprecise; Incorrect = wrong, off-topic, or loops*

| Prompt                              | 160M | 410M | 1B  | 2.8B | 6.9B |
| ----------------------------------- | ---- | ---- | --- | ---- | ---- |
| A screen reader is                  | $\times$    | $\times$    | $\approx$   | $\checkmark$    | $\approx$    |
| WCAG stands for                     | $\times$    | $\times$    | $\times$   | $\times$    | $\checkmark$    |
| A skip link is                      | $\times$    | $\approx$    | $\times$   | $\checkmark$    | $\times$    |
| The purpose of alt text is          | $\times$    | $\times$    | $\times$   | $\checkmark$    | $\checkmark$    |
| ARIA stands for                     | $\times$    | $\times$    | $\times$   | $\times$    | $\times$    |
| A focus indicator is                | $\times$    | $\times$    | $\times$   | $\times$    | $\times$    |
| Keyboard navigation allows          | $\times$    | $\times$    | $\times$   | $\times$    | $\times$    |
| Color contrast is important because | $\times$    | $\times$    | $\times$   | $\times$    | $\times$    |
| Semantic HTML helps                 | $\times$    | $\times$    | $\times$   | $\times$    | $\times$    |
| Captions are used for               | $\times$    | $\approx$    | $\times$   | $\approx$    | $\times$    |

Several patterns emerge from this data.

**Threshold at 2.8B.** Screen reader, skip link, and alt text all show correct or near-correct responses first at 2.8B. Below this threshold, responses are either wrong or incomplete.

**Screen reader shows non-monotonic behavior.** The 2.8B model produces "reads aloud the text," correctly capturing the auditory output purpose. The 6.9B model produces "reads text on a computer screen," dropping "aloud." The larger model is more verbose but less precise on the critical detail. This mirrors the skip link result, where 2.8B is correct and 6.9B regresses. Capability near emergence thresholds can be unstable.

**WCAG emerges at 6.9B; ARIA never emerges.** Both are foundational accessibility acronyms. WCAG requires 6.9B parameters to expand correctly. ARIA fails at every scale tested — at 160M it produces gibberish, at 410M it loops, and from 1B onward it produces confident but wrong expansions ("Artificial Replacement of a Human Being," "A Rational Approach to Information and Automation," "Association of Research Libraries in Africa"). Confidence increases with scale; accuracy does not. This suggests ARIA is rare enough in training data that even 6.9B parameters cannot reliably encode it, while increased scale produces more fluent confabulation rather than correct recall.

**General accessibility concepts fail across all scales.** Focus indicator, keyboard navigation, color contrast, and semantic HTML produce generic responses at every model size. These terms appear in web-scale training data but without accessibility-specific context. The models complete the prompts plausibly without encoding accessibility meaning.

**Replication: GPT-2**

The same ten prompts were run across GPT-2 small (117M), medium (406M), large (838M), and XL (1.5B).

| Prompt             | Small | Medium | Large | XL |
|--------------------|-------|--------|-------|-----|
| A screen reader is | $\times$     | $\times$      | $\times$     | $\approx$   |
| WCAG stands for    | $\times$     | $\times$      | $\times$     | $\checkmark$   |
| A skip link is     | $\times$     | $\times$      | $\times$     | $\times$   |
| The purpose of alt text is | $\times$ | $\times$    | $\approx$     | $\approx$   |
| ARIA stands for    | $\times$     | $\times$      | $\times$     | $\times$   |


The core findings replicate directionally. WCAG emerges at XL (1.5B) — a lower parameter count than Pythia's 6.9B, consistent with WCAG appearing more densely in WebText's Reddit-sourced content around web standards discussions. Screen reader never fully emerges in GPT-2; even at XL the model produces a partially correct response missing the critical "aloud" detail. ARIA fails at every scale tested in both model families. The declarative–evaluative gap and the pattern of sparse accessibility terms failing at all scales are consistent across architectures.

### Experiment 2: Evaluative Knowledge

A correct response requires the model to identify the specific accessibility violation, not just complete the code structure plausibly.

Models were tested on five code prompts requiring identification of accessibility violations. This tests whether models can apply accessibility knowledge, not just produce definitions.

*Correct = identifies the accessibility violation accurately; Partial = identifies some issue but not the core violation; Incorrect = wrong, off-topic, or loops*

| Prompt                                      | 160M     | 410M      | 1B       | 2.8B         | 6.9B         |
| ------------------------------------------- | -------- | --------- | -------- | ------------ | ------------ |
| `<img src='photo.jpg'>` missing what        | $\times$ | $\times$  | $\times$ | $\times$     | $\times$     |
| `<div>` with onclick not accessible because | $\times$ | $\times$  | $\times$ | $\times$     | $\times$     |
| Problem with `<a href='#'></a>`             | $\times$ | $\approx$ | $\times$ | $\times$     | $\times$     |
| `<input type='text'>` needs a               | $\times$ | $\times$  | $\times$ | $\times$     | $\times$     |
| 'Click here' button is bad because          | $\times$ | $\times$  | $\times$ | $\checkmark$ | $\checkmark$ |

There is a clear gap between declarative and evaluative knowledge. The 2.8B model correctly defines alt text but cannot identify that `<img src='photo.jpg'>` is missing one — it repeats the prompt and stalls at every scale tested. The question explicitly asks what is missing; no model answers "alt text."

The only evaluative success is the "Click here" prompt, which succeeds at 2.8B and 6.9B. Ambiguous link text may be more common in training data as a named anti-pattern than missing alt attributes.

The `<div>` onclick responses show a trajectory worth noting. Responses become more specific with scale — from loops at 160M to "not a form control" at 6.9B — without arriving at the correct explanation (keyboard inaccessibility, missing role and tabindex). The 6.9B answer is the closest, pointing toward interactivity expectations, but it does not identify the actual problem. This pattern reflects a broader limitation: models complete code structurally before reasoning semantically. Syntactic plausibility and semantic correctness are separable capabilities, and scale closes the gap only partially.

**Replication: GPT-2**

The same five code prompts were run across all GPT-2 sizes. The declarative–evaluative gap replicates fully. No GPT-2 model identified missing alt text at any scale. "Click here" emerged as a partial success at large (838M) — earlier by parameter count than Pythia's 2.8B — but regressed at XL, consistent with the instability observed near emergence thresholds in both model families. The evaluative gap does not close at any scale tested in either architecture.

### Experiment 3: Recognition vs. Generation

A preference flip — where the model assigns lower perplexity to the correct definition than the incorrect one — indicates recognition has emerged at that scale.

Perplexity measures how expected a sequence is to the model. Lower perplexity means the model finds the text more natural. Testing whether models assign lower perplexity to a correct definition than an incorrect one reveals whether recognition precedes generation. This experiment was extended to three accessibility compounds to assess whether the recognition-before-generation pattern generalizes.

| Model | Screen Reader | Alt Text | Skip Link |
|-------|--------------|----------|-----------|
| 160M | Wrong 2.6x | Wrong 1.2x | Wrong 1.9x |
| 410M | Wrong 1.2x | Correct 2.8x | Wrong 1.7x |
| 1B | Correct 2.2x | Correct 1.9x | Wrong 1.3x |
| 2.8B | Correct 4.0x | Correct 1.9x | Wrong 1.1x |
| 6.9B | Correct 3.0x | Correct 3.1x | Wrong 1.8x |

![Line graph showing perplexity scores on the y-axis (lower means more expected) against five Pythia model sizes on the x-axis: 160M, 410M, 1B, 2.8B, and 6.9B. Two lines represent correct and wrong WCAG definitions. At 160M and 410M, the wrong definition line sits below the correct definition line, indicating the model finds it more probable. A shaded region labeled "flip zone" spans 410M to 1B, where the lines cross. From 1B onward, the correct definition line drops below the wrong definition line, reaching its lowest point at 2.8B before both lines converge slightly at 6.9B.](./figures/pythia-perplexity.png)

::: {.caption}
Figure 2: Correct definition perplexity falls below wrong definition perplexity between 410M and 1B parameters in Pythia, indicating the model finds the correct definition more expected before it can generate it.
:::

The preference for screen reader flips between 410M and 1B — recognition precedes generation by one model size. Alt text flips earlier, between 160M and 410M, suggesting it is more densely represented in training data. Skip link never flips; the model finds the incorrect definition more natural at every scale, consistent with the behavioral instability observed in Experiment 1.

The recognition-before-generation pattern holds for two of three compounds tested. Skip link remains the exception across both perplexity and declarative experiments, indicating that some concepts may achieve surface-level generation without the underlying representational grounding that perplexity preference reflects.

**Replication: GPT-2**

| Model | Screen Reader | Alt Text | Skip Link |
|-------|--------------|----------|-----------|
| Small (117M) | Wrong 1.1x | Correct 1.7x | Wrong 1.3x |
| Medium (406M) | Wrong 1.1x | Correct 1.8x | Wrong 1.4x |
| Large (838M) | Correct 2.0x | Correct 1.6x | Wrong 2.5x |
| XL (1.5B) | Correct 2.6x | Correct 2.1x | Wrong 1.8x |

![Line graph showing perplexity scores on the y-axis (lower means more expected) against four GPT-2 model sizes on the x-axis: Small (117M), Medium (406M), Large (838M), and XL (1.5B). Two lines represent correct and wrong WCAG definitions. At Small, the correct definition line sits above the wrong definition line. The lines converge at Medium, then cross within a shaded flip zone spanning Medium to XL. At Large, the wrong definition line dips below the correct definition line. By XL, the correct definition line has dropped below the wrong definition line, completing the preference flip.](./figures/gpt2-perplexity.png)

::: {.caption}
Correct definition perplexity falls below wrong definition perplexity between 406M and 838M parameters in GPT-2, replicating the perplexity preference flip observed in Pythia at a comparable scale threshold.
:::

The screen reader preference flips between medium (406M) and large (838M) in GPT-2 — a remarkably similar parameter range to the Pythia flip between 410M and 1B, despite different architectures and training corpora. Alt text is correct-preferring from small in GPT-2, earlier than in Pythia, consistent with its denser representation in web-focused training data. Skip link never flips in either model family. The recognition-before-generation pattern for screen reader replicates across architectures.

### Experiment 4: Mechanistic Analysis of Compound Term Binding

Sustained strong binding into late network layers, rather than early-layer binding alone, is the signal of interest.

Attention pattern analysis across all five Pythia models examines whether models treat "screen reader" as a compound concept or as two independent tokens, and how this binding pattern relates to behavioral emergence.

For each model, attention weights from "reader" to "screen" were extracted across all layers and heads. Heads with weight above 0.5 are considered strong binding; the full data is available in the project repository.

| Model | Layers | Strong (0.5+) | Early (L0-3) | Last Layer |
|-------|--------|--------------|--------------|------------|
| 160M | 12 | 10 | 7 | 11 |
| 410M | 24 | 22 | 16 | 9 |
| 1B | 16 | 11 | 10 | 6 |
| 2.8B | 32 | 25 | 20 | 29 |
| 6.9B | 32 | 37 | 28 | 30 |

Note: 1B's architectural difference (8 heads vs 12) affects raw head counts; see Methodology.

![Bar chart showing the last layer containing a strong binding head with attention score of 0.5 or greater, across five Pythia model sizes on the x-axis: 160M, 410M, 1B, 2.8B, and 6.9B. Bars for 160M, 410M, and 1B are light blue and show a declining trend: Layer 11 of 12, Layer 9 of 24, and Layer 6 of 16 respectively. A vertical dashed line labeled "emergence threshold" separates these from the remaining models. Bars for 2.8B and 6.9B are dark navy and show a sharp increase: Layer 29 of 32 and Layer 30 of 32 respectively.](./figures/binding-persistence.png)

::: {.caption}
The last layer containing a strong binding head (attention score ≥0.5) drops through 160M, 410M, and 1B before jumping sharply at 2.8B, coinciding with the emergence threshold. Models above the threshold show binding heads persisting into the final layers.
:::

Several patterns emerge from this data.

**Early layers dominate across all models.** Between 70-91% of strong binding occurs in layers 0-3 regardless of model size. Compound term binding is established early in the forward pass at every scale tested.

**Strong head count scales with model size.** 160M has 10 strong binding heads; 6.9B has 37. 1B is the expected outlier given its different architecture.

**Last strong layer tracks behavioral emergence.** Below the 2.8B emergence threshold, strong binding drops off early — layer 11 for 160M, layer 9 for 410M, layer 6 for 1B. At 2.8B and above, strong binding persists deep into the network — layers 29 and 30 for 2.8B and 6.9B respectively. The models that cannot correctly define screen reader do not sustain compound binding through the network. The models that can, do.

**2.8B is the inflection point.** Total heads above threshold jumps from 28 (1B) to 101 (2.8B) — a 3.6x increase that coincides exactly with the behavioral emergence threshold identified in Experiment 1. Early binding is not representational; late binding is. The presence of sustained late-layer binding appears to be a mechanistic bottleneck for concept emergence.

All six models show strong binding in layers 0-3, including 160M which cannot produce a correct definition. Whether early-layer binding at small scales reflects genuine compound representation or proximity effects cannot be determined from attention weights alone and is noted as a limitation.

### Control Experiment: Ruling Out Proximity Effects

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

![Grouped bar chart showing attention head counts in Pythia 2.8B for three accessibility compounds on the x-axis: screen reader, alt text, and skip link. Each compound has two bars: light blue for all heads with attention score greater than 0.1, and dark navy for strong heads with attention score of 0.5 or greater. For screen reader: 101 all heads, 25 strong heads. For alt text: 200 all heads, 40 strong heads. For skip link: 208 all heads, 40 strong heads.](./figures/compound-comparison.png)

::: {.caption}
Attention head counts for three accessibility compounds in Pythia 2.8B, showing all heads (attention score >0.1) and strong heads (≥0.5). Screen reader activates fewer heads overall, while alt text and skip link show comparable strong head counts despite differences in total activation.
:::

This rules out a compound-specific explanation. The binding pattern is not an artifact of how "screen reader" tokenizes or how frequently it appears in training data. It is a general property of accessibility compound terms at the 2.8B emergence threshold. The models that can define these concepts correctly show robust, distributed binding across many heads and many layers. The models that cannot show weak binding that drops off early.

The binding pattern strengthens the case for a general mechanistic threshold at this scale.

**Replication: GPT-2**

Attention binding was measured across all four GPT-2 model sizes for screen reader, with additional compounds (alt text, skip link) analyzed at XL.

| Model | Total >0.1 | Strong (0.5+) | Last Strong Layer | Max Layers |
|-------|-----------|--------------|-------------------|------------|
| Small (117M) | 41 | 6 | 4 | 12 |
| Medium (406M) | 66 | 12 | 10 | 24 |
| Large (838M) | 146 | 34 | 15 | 36 |
| XL (1.5B) | 199 | 37 | 17 | 48 |

The strong head count jump between medium and large (12 to 34) coincides with the perplexity flip observed in Experiment 3, replicating the Pythia pattern in a different architecture. The last strong layer advances from 10 to 15 at the same transition — consistent with deep-network persistence as a correlate of recognition-level emergence.

\newpage

At XL, binding was measured for all three compounds:

| Compound | Total >0.1 | Strong (0.5+) | Last Strong Layer |
|----------|-----------|--------------|-------------------|
| Screen reader | 199 | 37 | 17 |
| Alt text | 244 | 34 | 19 |
| Skip link | 253 | 49 | 43 |

One divergence from Pythia is notable. GPT-2 XL's last strong layer as a proportion of total network depth is substantially shallower than Pythia 2.8B — approximately 35% vs 91%. This may reflect differences in training data composition and architectural differences. Pythia's training corpus (The Pile) includes technical documentation, Stack Exchange, and academic text where accessibility terminology appears in consistent, well-formed contexts. GPT-2's WebText corpus is dominated by general web content where the same terms appear more diffusely. The shallower binding depth in GPT-2 may account for the weaker and less stable behavioral emergence observed in Experiment 1.