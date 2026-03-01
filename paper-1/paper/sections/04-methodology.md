## Methodology

### Models

This study uses the Pythia model suite (Biderman et al., 2023): 160M, 410M, 1B, 2.8B, and 6.9B parameter models. Pythia models share identical architecture and training data across all sizes, isolating scale as the variable of interest. All models were loaded using TransformerLens (Nanda et al., 2022).

One architectural exception: Pythia 1B uses a different configuration than the other models in the suite — 16 layers, 8 heads, d_model=2048, d_mlp=8192, with parallel attention and MLP. The other models use 12 heads. This difference is relevant when interpreting per-head binding counts in Experiment 4; comparisons across model sizes account for this asymmetry.

### Experiments

#### Experiment 1: Declarative Knowledge

Ten accessibility concept prompts were run against each model using greedy decoding (temperature=0, max_new_tokens=10):

```python
model = HookedTransformer.from_pretrained("pythia-2.8b")
output = model.generate(prompt, max_new_tokens=10, temperature=0)
```

Prompts covered core accessibility terms (screen reader, alt text, skip link), foundational acronyms (WCAG, ARIA), and general accessibility concepts (focus indicator, keyboard navigation, color contrast, semantic HTML, captions). Responses were evaluated against known correct definitions.

#### Experiment 2: Evaluative Knowledge

Five code prompts were run against each model (temperature=0, max_new_tokens=20), asking models to identify accessibility violations in HTML snippets. Prompts covered missing alt attributes, non-semantic interactive elements, empty links, unlabeled inputs, and ambiguous link text. Responses were evaluated against correct accessibility explanations.

#### Experiment 3: Recognition vs. Generation

Perplexity measures how expected a sequence is to the model, defined as:

$$PPL(X) = \exp\left(-\frac{1}{N}\sum_{i=1}^{N} \log P(x_i \mid x_{<i})\right)$$

Lower perplexity indicates the model finds the text more natural. Comparing perplexity for a correct and incorrect definition across model sizes reveals whether recognition precedes generation:
```python
correct = "A screen reader is software that reads text aloud for blind users."
wrong = "A screen reader is a device for viewing screens."

def get_perplexity(model, text):
    tokens = model.to_tokens(text)
    logits = model(tokens)
    log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
    token_log_probs = log_probs[0, :-1, :].gather(1, tokens[0, 1:].unsqueeze(1)).squeeze()
    return torch.exp(-token_log_probs.mean()).item()
```

#### Experiment 4: Attention Pattern Analysis

Attention weights were extracted across all layers and heads for the prompt "A screen reader is" using TransformerLens's activation cache:
```python
logits, cache = model.run_with_cache(prompt)
attention = cache["pattern", layer]  # shape: [heads, seq, seq]
```

Token indices were verified for each model prior to analysis:
```python
tokens = model.to_str_tokens(prompt)
print(list(enumerate(tokens)))
```

Binding strength between tokens $t_i$ ("reader") and $t_j$ ("screen") was measured as the scalar attention weight:

$$b(t_i, t_j) = A^{(l,h)}_{ij}$$

where $A^{(l,h)}$ is the attention weight matrix at layer $l$, head $h$, extracted from the activation cache. Heads were classified into binding tiers based on $b(t_i, t_j)^{(l,h)}$:

$$H_{\text{strong}} = \{(l, h) : b(t_i, t_j)^{(l,h)} \geq 0.5\}$$

$$H_{\text{moderate}} = \{(l, h) : 0.2 \leq b(t_i, t_j)^{(l,h)} < 0.5\}$$

Heads with $b(t_i, t_j)^{(l,h)} < 0.2$ were treated as background noise and excluded from analysis. Results report $|H_{\text{strong}}|$ as the primary binding count.

This experiment was run for Pythia 2.8B and 6.9B. Additional binding pairs (alt text, skip link) were analyzed at 2.8B specifically, as this was the first model to demonstrate consistent declarative knowledge across Experiment 1. Full attention binding data for all model sizes is available in the project repository.

### Reproducibility

All experiments were run with temperature=0 for deterministic outputs on Google Colab with an A100 GPU. Full notebooks are available at https://github.com/trishasalas/mech-interp-research/blob/main/pythia/pythia-a11y-emergence.ipynb.
