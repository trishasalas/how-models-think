# Discussion

This paper examined accessibility concept acquisition across Pythia model scales using four complementary methods: behavioral generation, code evaluation, perplexity-based recognition, and attention pattern analysis. The results converge on a consistent picture with several implications for both accessibility tooling and emergence research.

## The 2.8B Threshold Is Meaningful, Not Arbitrary

The behavioral findings show a sharp threshold at 2.8B parameters for core accessibility concepts. This is not a smooth gradient — 1B partially retrieves "reads text from a screen" while 2.8B produces "reads aloud the text," capturing the critical auditory output purpose. The threshold pattern, combined with the 3.6x jump in sustained attention binding heads at 2.8B, suggests a qualitative shift rather than incremental improvement. Below 2.8B, the model has partial encoding that cannot support reliable generation. At 2.8B, encoding is sufficient to sustain compound binding throughout the network and produce correct behavioral output.

## Encoding and Retrieval Are Dissociable

The perplexity results demonstrate that models prefer correct definitions before they can produce them. At 1B, the model assigns lower perplexity to the correct screen reader definition despite generating "reads text from a screen" — missing the auditory purpose. This dissociation between recognition and generation suggests that accessibility knowledge accumulates in model representations before it becomes accessible through the generation pathway. The capability exists earlier than behavior indicates.

This has practical implications: perplexity-based probes may detect accessibility knowledge at smaller scales than behavioral tests suggest. Models that appear to fail accessibility benchmarks may have partial encoding that structured probing could surface.

## The Declarative-Evaluative Gap Is Not Closed at Any Scale Tested

Even at 6.9B, models that correctly define accessibility concepts cannot reliably identify violations in code. The single evaluative success — identifying ambiguous link text — may reflect training data frequency rather than genuine accessibility reasoning. The image missing alt attribute failure is particularly telling: a model asked explicitly what is missing produces the prompt back rather than "alt text," despite correctly defining alt text in declarative tests. Knowing and applying are different capabilities that do not emerge together.

For accessibility tooling practitioners, this gap is the central finding. A model that passes a definition benchmark is not ready for code review tasks. Evaluative capability requires either substantially larger scale than tested here or domain-specific training.

## Acronym Failure Is Systematic

WCAG and ARIA show qualitatively different failure patterns than conceptual terms. Conceptual terms show emergence — partial at 1B, correct at 2.8B. Acronyms either emerge very late (WCAG at 6.9B) or not at all (ARIA at any scale tested). The ARIA failure is particularly informative: hallucinated expansions become more fluent and confident with scale without becoming accurate. At 160M, ARIA produces gibberish. At 6.9B, it produces a coherent but wrong expansion ("Association of Research Libraries in Africa") with apparent conviction.

This suggests WCAG and ARIA are rare enough in web-scale training data that standard scaling cannot reliably encode them. Specialized training data or fine-tuning is likely required for reliable acronym expansion in the accessibility domain.

## Attention Binding as a Correlate of Emergence

The sustained attention binding pattern at 2.8B and 6.9B — strong binding persisting to layers 29-30 versus dropping off at layers 6-11 in smaller models — provides a mechanistic correlate for behavioral emergence. The models that can define screen reader sustain the compound binding across the full network. The models that cannot drop it early.

This finding is correlational, not causal. Whether sustained binding causes correct generation, or both are consequences of a third factor such as MLP encoding depth, cannot be determined from attention weights alone. The presence of strong early-layer binding in 160M — including one head at perfect score 1.0 — despite behavioral failure suggests early binding is necessary but not sufficient for emergence. Whether this reflects genuine compound representation or proximity effects in the absence of higher-level context remains an open question for future probing work.

Canonical induction head testing confirmed that L1H12 does not exhibit prefix-matching behavior, suggesting it implements a distinct binding mechanism rather than general-purpose token repetition detection. What mechanism L1H12 implements, and whether it is routing to MLP-encoded compound representations, is a question for future causal analysis.

## Relationship to Prior Work

Wei et al. (2022) established emergence as a general phenomenon. This paper treats accessibility concept acquisition as a domain-specific case study with properties that make it a productive probe: concepts are rare enough to show scale sensitivity, evaluable against clear ground truth, and directly relevant to real-world applications. The results confirm that emergence operates in specialized domains but with domain-specific timing — accessibility acronyms require substantially more scale than conceptual terms, and evaluative capability does not emerge within the range tested.

The finding that general accessibility concepts (focus indicator, keyboard navigation, color contrast, semantic HTML) fail across all scales suggests training data frequency is the limiting factor, not model capacity per se. These terms appear in web-scale data but without the accessibility-specific context required for meaningful representation.
