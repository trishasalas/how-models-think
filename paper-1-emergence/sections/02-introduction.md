
## Introduction

Digital accessibility guidelines represent a narrow, specialized domain in web-scale training data. Terms like WCAG, ARIA, and alt text appear far less frequently than general web vocabulary, and their correct usage requires understanding both syntax and intent. This makes accessibility an unusual test case for studying emergence: the concepts are concrete enough to evaluate, rare enough to show scale sensitivity, and have clear right and wrong answers.

Most emergence research uses broad capability benchmarks — arithmetic, chain-of-thought reasoning, multilingual translation. These are useful but noisy. Accessibility concepts offer something different: a small, well-defined vocabulary with unambiguous ground truth and direct relevance to real-world tooling decisions.

This paper uses the Pythia model suite (160M–6.9B parameters) and TransformerLens to examine accessibility knowledge across four dimensions: whether models can define accessibility concepts, whether they can identify violations in code, whether recognition precedes generation, and how the 2.8B model internally represents a compound accessibility term. Pythia's controlled architecture — identical training data across all sizes — isolates scale as the variable of interest.

The findings are specific: accessibility knowledge emerges at 2.8B parameters for core concepts, later or not at all for acronyms, and evaluative capability lags behind declarative knowledge even at maximum scale tested. Attention pattern analysis shows mechanistic encoding of compound terms before full behavioral competence appears.