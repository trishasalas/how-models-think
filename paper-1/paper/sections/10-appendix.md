## Appendix

### A: Prompts

#### Declarative Prompts

All declarative experiments used completion-style prompts. Models were given the prompt prefix and generated a continuation.

| Prompt |
|--------|
| A screen reader is |
| WCAG stands for |
| A skip link is |
| The purpose of alt text is |
| ARIA stands for |
| A focus indicator is |
| Keyboard navigation allows |
| Color contrast is important because |
| Semantic HTML helps |
| Captions are used for |

#### Evaluative Prompts

Evaluative experiments used zero-shot code completion prompts.

| Prompt |
|--------|
| The following code is not accessible because it doesn't have what? `<img src='photo.jpg'>` |
| A `<div>` with onclick is not accessible because |
| The accessibility problem with `<a href='#'></a>` is |
| `<input type='text'>` needs a |
| A button that only says 'Click here' is bad because |

#### Perplexity Pairs

Each pair consists of a correct and incorrect definition. Perplexity was computed for each sentence independently. Values below 1.0 on the preference ratio indicate the model finds the wrong definition more natural.

| Concept | Correct | Incorrect |
|---------|---------|-----------|
| Screen reader | A screen reader is software that reads text aloud for blind users. | A screen reader is a device for viewing screens. |
| Alt text | The purpose of alt text is to provide a textual description of an image for people with visual disabilities. | The purpose of alt text is to make images load faster. |
| Skip link | A skip link is a navigation aid that allows keyboard users to bypass repetitive content. | A skip link is a broken hyperlink that does not load. |

---

### B: Model Architectures

All experiments used base (non-instruction-tuned) model checkpoints.

#### Pythia Scaling Suite

Architecture: parallel attention + MLP blocks.

| Model | Layers | Heads | d_model | d_mlp |
|-------|--------|-------|---------|-------|
| 160M | 12 | 12 | 768 | 3,072 |
| 410M | 24 | 16 | 1,024 | 4,096 |
| 1B | 16 | 8 | 2,048 | 8,192 |
| 2.8B | 32 | 32 | 2,560 | 10,240 |
| 6.9B | 32 | 32 | 4,096 | 16,384 |

#### GPT-2 Model Family

Architecture: sequential attention + MLP blocks.

| Model | Layers | Heads | d_model | d_mlp |
|-------|--------|-------|---------|-------|
| Small (117M) | 12 | 12 | 768 | 3,072 |
| Medium (406M) | 24 | 16 | 1,024 | 4,096 |
| Large (838M) | 36 | 20 | 1,280 | 5,120 |
| XL (1.5B) | 48 | 25 | 1,600 | 6,400 |