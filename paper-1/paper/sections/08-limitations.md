## Limitations

This paper reports findings from a first investigation into accessibility concept emergence across Pythia model scales. Several limitations should be considered when interpreting the results.

### Prompt Design

All experiments used completion-style prompts ("A screen reader is," "WCAG stands for") rather than instruction or question formats. Prompt framing is known to affect retrieval in language models, and this paper's own findings support that sensitivity. The alt text retrieval experiment demonstrated that the HTML-framed prompt ("In HTML, the alt attribute provides a text description of an") performed worse than the simpler framing despite testing identical knowledge. Results reported here reflect one prompt design choice and may not generalize to other framings.

The declarative prompts were adapted from attention binding experiments rather than designed independently for behavioral testing. Future work should compare multiple prompt formulations to establish which results are robust across framings.

### Evaluative Experiment Prompts

The evaluative experiment used zero-shot code completion prompts. The image missing alt attribute result — where models loop the prompt rather than identify the missing attribute — may reflect document completion behavior rather than a knowledge failure. Models trained on code repositories may interpret `<img src='photo.jpg'>` as the beginning of a code listing and complete accordingly. Instruction-tuned models or explicit question formatting ("What accessibility attribute is missing from this HTML?") may produce different results. This limitation is noted but not resolved here.

### Perplexity Experiment Scope

Recognition versus generation was tested using a single sentence pair for one concept (screen reader). The preference flip between 410M and 1B is a clear finding, but a single pair is insufficient to establish this as a general pattern. A broader set of correct/incorrect pairs across multiple accessibility concepts would strengthen the recognition-precedes-generation claim.

### Attention Binding Methodology

The proximity control experiment was run at 2.8B only. Control testing revealed that adjacent token pairs — including function word pairs and modifier-noun pairs without disambiguation — produce strong binding at L1H12, which was subsequently confirmed as a previous-token head attending systematically to the immediately preceding position regardless of content. This finding limits the interpretation of L1H12's consistent appearance across accessibility compounds. Whether other heads show accessibility-specific binding patterns that do not appear in non-compound controls has not been fully characterized and is noted as a direction for future work. Early-layer binding at 160M (including Layer 11 Head 8 at score 1.0) remains ambiguous. Whether this reflects genuine compound representation or positional attention at small scales cannot be determined from attention weights alone.

The compound generalization finding — that alt text and skip link show comparable binding to screen reader at 2.8B — is based on head counts above threshold across all three compounds.

### Hardware and Reproducibility

All experiments were run on Google Colab with an A100 GPU. All notebooks are available in the project repository for independent verification.

### Scale Coverage

The scale ladder covers 160M through 6.9B parameters. ARIA fails to emerge at any scale tested. Whether ARIA would emerge at larger scales is unknown. The evaluative gap — models that define concepts cannot identify violations — was not tested beyond 6.9B. Both findings may reflect limitations of the scale range rather than fundamental properties of these concepts.
