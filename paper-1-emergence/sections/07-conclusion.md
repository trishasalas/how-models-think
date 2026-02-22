# Conclusion

This paper mapped accessibility concept acquisition across five Pythia model sizes using behavioral, perplexity-based, and mechanistic analysis. The findings establish a clear picture of how and when accessibility knowledge emerges in language models trained on web-scale data.

Core accessibility concepts — screen reader, alt text, skip link — emerge behaviorally at 2.8B parameters. Foundational acronyms require more scale (WCAG at 6.9B) or fail entirely (ARIA at all scales tested). General accessibility vocabulary fails across all model sizes, suggesting training data frequency as the limiting factor rather than model capacity. Evaluative capability — identifying accessibility violations in code — does not emerge within the range tested, even in models that correctly define the relevant concepts.

The perplexity results show that recognition precedes generation: models prefer correct definitions before they can produce them, with the preference flipping between 410M and 1B. The attention binding analysis shows that sustained binding of "screen reader" as a compound concept across the full network is a mechanistic correlate of emergence — present at 2.8B and 6.9B, absent at smaller scales.

For practitioners building accessibility tooling on language models, the central implication is that behavioral success on definition tasks does not predict success on evaluation tasks. The declarative-evaluative gap observed here suggests that reliable accessibility code review requires either substantially larger models or domain-specific training data that goes beyond the web-scale distribution.

For emergence researchers, accessibility concepts offer a useful probe domain: rare enough to show scale sensitivity, concrete enough to evaluate against ground truth, and distinct enough from general knowledge to isolate domain-specific acquisition. The ARIA confabulation pattern — increasingly fluent wrong answers with scale — illustrates a failure mode that definition-based benchmarks would not detect.

The mechanistic findings here are correlational. Whether sustained attention binding causes behavioral emergence or reflects a common underlying factor requires causal analysis beyond the scope of this paper, and is a direction for future work.
