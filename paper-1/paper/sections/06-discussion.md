## Discussion

This paper examined accessibility concept acquisition across Pythia model scales using mechanistic analysis, perplexity-based recognition, and behavioral evaluation. The results converge on a consistent picture with several implications for both accessibility tooling and emergence research.

### The 2.8B Threshold Is Meaningful, Not Arbitrary

The behavioral findings show a sharp threshold at 2.8B parameters for core accessibility concepts. This is not a smooth gradient — 1B partially retrieves "reads text from a screen" while 2.8B produces "reads aloud the text," capturing the critical auditory output purpose. The threshold pattern, combined with the 3.6x jump in sustained attention binding heads at 2.8B, suggests a qualitative shift rather than incremental improvement. Below 2.8B, the model has partial encoding that cannot support reliable generation. At 2.8B, encoding is sufficient to sustain compound binding throughout the network and produce correct behavioral output.

### Encoding and Retrieval Are Dissociable

The perplexity results demonstrate that models prefer correct definitions before they can produce them. At 1B, the model assigns lower perplexity to the correct screen reader definition despite generating "reads text from a screen" — missing the auditory purpose. This dissociation between recognition and generation suggests that accessibility knowledge accumulates in model representations before it becomes accessible through the generation pathway. The capability exists earlier than behavior indicates.

This has practical implications: perplexity-based probes may detect accessibility knowledge at smaller scales than behavioral tests suggest. Models that appear to fail accessibility benchmarks may have partial encoding that structured probing could surface.

### The Declarative-Evaluative Gap Is Not Closed at Any Scale Tested

Even at 6.9B, models that correctly define accessibility concepts cannot reliably identify violations in code. The single evaluative success — identifying ambiguous link text — may reflect training data frequency rather than genuine accessibility reasoning. The image missing alt attribute failure is particularly telling: a model asked explicitly what is missing produces the prompt back rather than "alt text," despite correctly defining alt text in declarative tests. Knowing and applying are different capabilities that do not emerge together.

For accessibility tooling practitioners, this gap is the central finding. A model that passes a definition benchmark is not ready for code review tasks. Evaluative capability requires either substantially larger scale than tested here or domain-specific training.

### Acronym Failure Is Systematic

WCAG and ARIA show qualitatively different failure patterns than conceptual terms. Conceptual terms show emergence — partial at 1B, correct at 2.8B. Acronyms either emerge very late (WCAG at 6.9B) or not at all (ARIA at any scale tested). The ARIA failure is particularly informative: hallucinated expansions become more fluent and confident with scale without becoming accurate. At 160M, ARIA produces gibberish. At 6.9B, it produces a coherent but wrong expansion ("Association of Research Libraries in Africa") with apparent conviction.

This suggests WCAG and ARIA are rare enough in web-scale training data that standard scaling cannot reliably encode them. This pattern is consistent with findings on knowledge frequency effects in parametric memory: model accuracy on factual recall correlates with entity popularity in training data, and rare entities produce confident confabulation rather than correct retrieval (Mallen et al., 2023). Specialized training data or fine-tuning is likely required for reliable acronym expansion in the accessibility domain.

### Attention Binding as a Mechanistic Correlate of Emergence

The sustained attention binding pattern at 2.8B and 6.9B — strong binding persisting to layers 29-30 versus dropping off at layers 6-11 in smaller models — provides a mechanistic correlate for behavioral emergence. The models that can define screen reader sustain the compound binding across the full network. The models that cannot drop it early.

Early binding is not representational; late binding is. The presence of sustained late-layer binding appears to be a mechanistic bottleneck for concept emergence: a necessary structural condition without which behavioral competence does not appear. All models, including those that fail behaviorally, show strong binding in early layers. The differentiating factor is whether that binding persists deep into the network.

This finding is correlational, not causal. Whether sustained binding causes correct generation, or both are consequences of a third factor such as MLP encoding depth, cannot be determined from attention weights alone (Geva et al., 2021). Whether this reflects genuine compound representation or proximity effects in the absence of higher-level context remains an open question for future probing work.

### Cross-Architecture Replication

To assess whether the threshold and binding patterns are specific to Pythia's architecture and training data, all four experiments were replicated on the GPT-2 model suite. The core findings replicate directionally across both model families.

The recognition-before-generation pattern for screen reader holds in GPT-2, with the perplexity preference flipping between medium (406M) and large (838M) — a parameter range closely matching Pythia's 410M–1B transition. The declarative–evaluative gap replicates fully: no GPT-2 model identified missing alt text, and ARIA fails at every scale in both families. The attention binding jump between GPT-2 medium and large (12 to 34 strong heads) coincides with the perplexity flip, consistent with deep-network persistence as a correlate of recognition-level emergence.

One notable divergence: GPT-2's last strong binding layer as a proportion of total network depth is substantially shallower than Pythia 2.8B — approximately 35% vs 91%. Full behavioral emergence is weaker and less stable in GPT-2 across all compounds tested. This may reflect differences in training data composition. Pythia's training corpus (The Pile) includes technical documentation, Stack Exchange, and academic text where accessibility terminology appears in consistent, well-formed contexts. GPT-2's WebText corpus is dominated by general web content where the same terms appear more diffusely. The shallower binding depth in GPT-2 may account for the weaker behavioral emergence: the network encodes the compound relationship but does not reinforce it through enough layers to support reliable generation.

This cross-architecture comparison suggests that deep-network persistence is not merely a property of Pythia's architecture but a general structural correlate of concept emergence, and that training data quality and context consistency may influence the depth to which that persistence develops.

### Relationship to Prior Work

Wei et al. (2022) established emergence as a general phenomenon. This paper treats accessibility concept acquisition as a domain-specific case study with properties that make it a productive probe: concepts are rare enough to show scale sensitivity, evaluable against clear ground truth, and directly relevant to real-world applications. The results confirm that emergence operates in specialized domains but with domain-specific timing — accessibility acronyms require substantially more scale than conceptual terms, and evaluative capability does not emerge within the range tested.

Prior work on accessibility and LLMs has focused primarily on behavioral evaluation — whether models can identify or remediate violations. The present study adds a mechanistic dimension: not only what models know but how that knowledge is structurally encoded, and at what point in the network that encoding becomes sufficient for generation. The cross-architecture replication strengthens the mechanistic claim: deep-network binding persistence as a correlate of emergence is not an artifact of a single model family.

The finding that general accessibility concepts (focus indicator, keyboard navigation, color contrast, semantic HTML) fail across all scales in both model families suggests training data frequency is the limiting factor, not model capacity per se. These terms appear in web-scale data but without the accessibility-specific context required for meaningful representation.