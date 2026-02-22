# Paper 2: Does Accessibility Knowledge Exist Before It Emerges?
# Linear Probing Across Pythia and GPT-2

**Status:** In progress  

## Research Question

Paper 1 found that accessibility concepts become behaviorally accessible at
2.8B parameters. But behavioral probes are blunt — the model either completes
the sentence correctly or it doesn't.

This paper asks: is accessibility knowledge *geometrically present* in smaller
models before the behavioral threshold? Can a linear probe detect it in the
residual stream even when generation fails?

## Approach

Train logistic regression classifiers (linear probes) on residual stream
activations at each layer, using contrastive prompt pairs:

- **Target:** Prompts about accessibility concepts (screen reader, alt text, WCAG)
- **Control:** Structurally similar prompts about non-accessibility topics

Probe accuracy per layer reveals whether the concept exists as a separable
direction in the model's representation space — independent of whether it
can be decoded into output.

## Models

- Pythia: 160M, 410M, 1B, 2.8B (bridges Paper 1 behavioral findings)
- GPT-2: Medium, Large, XL (bridges Paper 3 mechanistic findings)

## Expected contribution

A spectrum from "not encoded" → "encoded but inaccessible" → "encoded and
retrievable" that explains *why* the behavioral threshold falls where it does,
and connects the Pythia emergence work to the GPT-2 mechanistic work.
