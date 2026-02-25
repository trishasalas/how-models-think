| title                                                     | author       | date |
| --------------------------------------------------------- | ------------ | ---- |
| Testing Accessibility Knowledge Across Pythia Model Sizes | Trisha Salas | 2026 |

## Abstract

Digital accessibility guidelines such as WCAG represent a specialized, low-frequency domain in web-scale training data. This paper investigates how language models acquire accessibility knowledge as a function of scale, using the Pythia model suite (160M–6.9B parameters) and TransformerLens to examine both behavioral outputs and internal representations. Accessibility concept emergence follows a sharp threshold pattern: screen reader, skip link, and alt text emerge behaviorally at 2.8B parameters, while WCAG first appears at 6.9B and ARIA fails to emerge at any scale tested. Perplexity analysis reveals that recognition precedes generation — models prefer correct definitions before they can produce them, with the preference flipping between 410M and 1B. Even at 6.9B, models that correctly define accessibility concepts cannot reliably identify violations in code. Attention pattern analysis shows that the 2.8B model binds "screen reader" as a compound concept across multiple layers and heads, suggesting mechanistic encoding precedes full behavioral competence. These findings suggest that accessibility concepts — rare, domain-specific, and concretely evaluable — are well-suited for studying how specialized knowledge emerges with scale.

---

Structure:

§1 Introduction → sections/introduction.md
§2 Related Work → sections/related_work.md
§3 Methods → sections/methododology.md
§4 Results → sections/results.md
§5 Discussion → sections/discussion.md
§6 Conclusion → sections/conclusion.md
