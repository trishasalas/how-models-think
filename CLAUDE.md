# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mechanistic interpretability research studying how language models acquire, represent, and store accessibility knowledge. Three-paper series by Trisha Salas:

1. **Paper 1** (`paper-1-emergence/`): Behavioral emergence across Pythia scales — published Jan 2026, code in separate repo
2. **Paper 2** (`paper-2-probing/`): Linear probing for pre-behavioral knowledge — in progress
3. **Paper 3** (`paper-3-mechanistic/`): Mechanistic taxonomy via logit lens, decomposition, head analysis on GPT-2 — in progress, most active

## Environment Setup

```bash
pip install -r requirements.txt
```

Key dependencies: `torch`, `transformer-lens`, `transformers`, `tuned-lens`, `matplotlib`, `pandas`

Hardware target: MacBook M5 with 24GB RAM. All GPT-2 sizes (Medium/Large/XL) fit in memory but require explicit cleanup between models via `models.unload()`.

## Architecture

Shared analysis library in `src/` with thin Jupyter notebooks as experiment scripts. All analysis functions return pandas DataFrames with `.attrs` metadata (model name, prompt, target token).

### src/ modules

- **models.py** — Model loading via TransformerLens, device auto-detection (CUDA/MPS/CPU), `ModelInfo` dataclass, explicit `unload()` for memory cleanup
- **logit_lens.py** — Layer-by-layer prediction tracing through residual stream → unembed projection
- **decompose.py** — Attention vs MLP contribution decomposition per layer. Handles GPT-2 sequential (MLP sees attention output) vs Pythia parallel (independent) architectures
- **heads.py** — Per-head attention contribution via W_O → W_U projection. Includes `top_heads()` and `layer_summary()`
- **perplexity.py** — Token-level cross-entropy loss for measuring concept familiarity across models
- **probe.py** — Linear probing with cross-validation on residual stream activations. Contrastive target/control prompt pairs, per-layer accuracy with pattern classification (not_encoded/early/middle/late/sustained)
- **viz.py** — Standardized matplotlib plots. Color scheme: attention=#2196F3, MLP=#FF9800, target=#4CAF50, suppression=#F44336. `save_figures()` uses naming convention `{model}-{target}-{analysis}.png`

### Notebooks

Live in `paper-3-mechanistic/notebooks/` organized by model family (`gpt2/`, `pythia/`). Comparison notebooks at the top level. Results (CSVs + PNGs) save to `paper-3-mechanistic/results/`.

## Key Design Decisions

- **GPT-2 over Pythia for mechanistic work**: GPT-2's sequential attention→MLP architecture and consistent 4x MLP ratio across scales make decomposition interpretable. Pythia's parallel architecture and changing dimensions across scales confound analysis.
- **DataFrame-centric API**: Every analysis function returns a DataFrame, enabling chaining, filtering, and CSV export. Metadata stored in `.attrs`.
- **Cross-validation in probing**: Default 3-fold CV because prompt sets are small (<20 per class). Activations are standardized per layer since residual stream scale varies.

## Research Context

Key findings driving current work:
- Knowledge storage varies by concept type: proper nouns (tight MLP mid-layers), acronym expansion like ARIA (distributed), domain concepts like alt text (frame-sensitive retrieval)
- MLP dominance increases with model scale: Medium is attention-led, Large shows late MLP dominance, XL concentrates in single late MLP layer
- Knowledge can exist geometrically (high probe accuracy) without being retrievable behaviorally (failed generation) — "capacity ambiguity"

Decision and observation logs are in `notes/decisions/` and `notes/observations/`, indexed by `notes/DECISIONS.md` and `notes/OBSERVATIONS.md`.
