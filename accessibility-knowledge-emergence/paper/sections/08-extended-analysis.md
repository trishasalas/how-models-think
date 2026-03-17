## Extended Analysis: Elicitation Robustness & Additional Observations

### Introduction

The original experiments relied on two prompt types to assess evaluative reasoning. A natural question follows: could the observed gap be an artifact of how we asked rather than a genuine capability boundary? To address this, we expanded to multiple elicitation strategies, varying the prompt structure while holding the underlying concept constant.

Testing was limited to Pythia 1B and 2.8B, the two model scales where the declarative-evaluative gap was originally observed.

## Completion Tasks

We used two different elicitation strategies, few-shot structural and bare completion, making sure that there was no accessibility language in either prompt. *(Appendix C, Table 6)* 2.8B completed every accessibility concept correctly except the bare closed captions prompt. 1B struggled across the board but got close on a couple. The control prompts completed correctly on both models, confirming that the differences are specific to accessibility concepts, not general HTML ability.

This establishes that the declarative knowledge is there — the model knows these patterns. The question is what happens when we ask it to reason about them.

## Hypothesis-Driven Evaluation

To test whether prompt framing influenced the evaluative failure observed in Experiment 2, three elicitation strategies were introduced: direct questioning, error correction, and Socratic prompting. *(Appendix C, Table 7)*

All three strategies produced the same core outcome. The model could recognize the accessibility concept but failed to identify the violation.

The consistent prompt structures tells us that the declarative-evaluative gap is real, it's robust across multiple elicitation strategies, and it's not an artifact of how we asked. The failure appears to reflect a genuine capability boundary rather than a retrieval problem.

## Validation Prompts

A small validation set was introduced to determine whether the observed failures reflected prompt-specific behavior or a broader pattern. *(Appendix C, Table 8)* These prompts produced a range of responses rather than simple pass/fail outcomes. In several cases the model correctly identified the accessibility problem but could not articulate the specific solution.

One response was particularly striking. When asked "What accessibility attribute is missing from this HTML: `<img src='photo.jpg'>`?", the model responded:

> "I have a photo gallery on my website. I want to add an accessibility attribute to the image tag so that the image can be clicked on. I have tried adding the attribute to the img tag, but it doesn't work."

The model appears to recognize the issue while lacking the structured reasoning needed to resolve it — describing its own gap from inside the gap.

## Cross-Model Comparison

To distinguish domain-specific behavior from general capability limits, the same prompt structures were tested on a smaller model (1B).

The 1B model fails broadly across tasks, producing generic or off-topic completions. In contrast, the 2.8B model shows a split profile: strong performance on declarative completion tasks but consistent failure on evaluative reasoning.

This contrast localizes the gap. The issue is not general model weakness but a specific failure to transition from declarative knowledge to evaluative reasoning.

## Entropy Analysis

We computed mean and last-token entropy on the 3 hypothesis-driven prompts for both 2.8B and 1B

2.8B recognizes "screen reader" territory and locks in confidently — but it's confident about PARROTING, not about answering. 1B doesn't even recognize the territory. High entropy corresponds to stalled or echoing completions; intermediate entropy corresponds to fluent but incorrect explanations; low entropy corresponds to confident continuation of the prompt’s rhetorical structure.

The 1B model shows no comparable differentiation. This provides quantitative evidence that different prompt structures push the larger model into distinct predictive states even when the final answer is incorrect.

| Model | Prompt          | Mean Entropy | Last Token Entropy |
| ----- | --------------- | ------------ | ------------------ |
| 1B    | Direct Question | 4.7761       | 5.6073             |
| 1B    | Error Question  | 5.6830       | 4.9935             |
| 1B    | Socratic        | 4.9666       | 5.7079             |
| 2.8B  | Direct Question | 4.4127       | 5.1879             |
| 2.8B  | Error Question  | 5.7185       | 5.5864             |
| 2.8B  | Socratic        | 4.5445       | 4.1660             |


## Extended Binding Analysis

To determine whether the sustained binding pattern continues beyond the original model suite, we extended the attention binding analysis to Pythia 12B. We used the same methodology as the original experiment: threshold ≥0.5 for strong binding, ≥0.1 for inclusion.

### **12B Binding Results**

- 119 total heads above 0.1 threshold
- 36 strong heads above 0.5 threshold
- Last strong binding layer: 34 (out of 35, zero-indexed) = 97% depth
- Top binding head: Layer 1, Head 15 at 0.9905

**The late-layer resurgence finding:** Layer 33 has 7 active binding heads (4 above 0.5), including Head 16 at 0.8766. This is the strongest late-layer cluster of any model tested.

Late-layer binding entries scale with model size:

- 1B: 1 late entry
- 2.8B: 4 late entries
- 6.9B: 6 late entries
- 12B: 11 late entries

**The specialization finding:** % of heads active in binding DECREASES with scale: 31.9% at 160M → 8.3% at 12B. But the absolute count plateaus around 100-120 for models ≥2.8B. The model figures out how many heads it NEEDS and stops adding more. Larger models use proportionally fewer but more specialized heads.

### Cross-model pattern

- Binding is front-loaded in ALL models (65-82% of heads in first 25% of layers) — universal
- Strong heads (>0.9) cluster at 3-10% depth for all models ≥1B — universal
- Late-layer resurgence scales with model size — this is the new finding
- Mean binding scores are stable (~0.36-0.44) regardless of scale — the STRENGTH doesn't change, the DEPTH does

**The key point: **12B extends the published scaling curve. The original paper's bar chart gains a sixth data point. Sustained binding continues to push deeper with scale. The late-layer resurgence is a new observation not in the original paper — a cluster of binding heads re-engaging near the output layers, scaling with model size.

This is consistent with the hypothesis that larger MLP capacity sustains compound representations through deeper network propagation. Direct MLP investigation is future work.

## Additional Discussion

The extended analysis was motivated by a straightforward question: could the declarative-evaluative gap observed in the original experiments be an artifact of prompt design? Across 15 prompts, 3 elicitation strategies, 4 accessibility concepts, and a non-accessibility control, the answer is no. The gap persists regardless of how we ask.

But the failure isn't uniform. Entropy analysis reveals that the model enters measurably different internal states depending on the prompt structure, high entropy when it stalls, intermediate entropy when it confabulates and low entropy when it confidently parrots. The model is processing these prompts differently even when the outcome is the same: failure. The Socratic prompt in particular produces a striking confidence signature at 2.8B that warrants circuit-level investigation in future work.

The 12B binding analysis extends the original scaling curve with a sixth data point and introduces a new observation: late-layer resurgence. A cluster of binding heads re-engages near the output layers, and this cluster scales with model size. Larger models also show increased specialization — fewer heads participating in binding overall, but sustaining it deeper through the network. This is consistent with the hypothesis that wider MLP layers enable sustained propagation of compound representations, though direct investigation of MLP activations is deferred to future work.

Not all concepts benefit equally from scale. Skip link prefers the incorrect definition even at 12B, suggesting that training data representation may impose a floor that scale alone cannot overcome. Similarly, cross-domain confabulation patterns observed for terms like ARIA suggest the phenomenon may not be specific to accessibility, though this paper uses accessibility as its lens. Both directions are left for future investigation.