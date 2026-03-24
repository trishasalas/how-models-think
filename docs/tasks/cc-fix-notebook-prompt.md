## Task

Fix the notebook at `notebooks/add-compounds-across-all_Testing_Accessibility_Knowledge_Across_Pythia_Model_Sizes.ipynb`

Only modify cells from the top of the notebook through the "Pythia 410M" markdown heading. Do NOT touch anything from the 410M heading onward.

### Here is exactly what each cell should contain:

**Cell 0 (markdown):**
```
# Testing Accessibility Knowledge Across Pythia Model Sizes
```

**Cell 1 (markdown):**
```
## Setup
```

**Cell 2 (code):**
```python
!pip install transformer_lens -q
!pip install circuitsvis -q
```

**Cell 3 (code):**
```python
from transformer_lens import HookedTransformer
import transformer_lens.utils as utils
import csv
import torch
import gc
import circuitsvis as cv
```

**Cell 4 (markdown):**
```
## Pythia 160M
```

**Cell 5 (markdown):**
```
### Load Model
```

**Cell 6 (code):**
```python
model = HookedTransformer.from_pretrained("pythia-160m")
print(f"Layers: {model.cfg.n_layers}")
print(f"Heads: {model.cfg.n_heads}")
print(f"Hidden size: {model.cfg.d_model}")
print(f"Params: {sum(p.numel() for p in model.parameters())/1e6:.1f}M")
```

**Cell 7 (markdown):**
```
### Attention Pattern Analysis
```

**Cell 8 (markdown):**
```
#### Screen Reader (reader to screen)
```

**Cell 9 (code):**
```python
# DIRECTION: second token attends BACK to first token
# "reader" looks at "screen" = attn[reader_idx, screen_idx]
# "text" looks at "alt" = attn[text_idx, alt_idx]
# "link" looks at "skip" = attn[link_idx, skip_idx]
# Rule: attn[SECOND, FIRST]

prompt = "A screen reader is"
tokens = model.to_str_tokens(prompt)
print(list(enumerate(tokens)))  # verify indices
logits, cache = model.run_with_cache(prompt)

threshold = 0.1
rows = []

for layer in range(model.cfg.n_layers):
    attention = cache["pattern", layer]
    for head in range(model.cfg.n_heads):
        attn = attention[0, head]
        reader_idx = 3
        screen_idx = 2
        score = attn[reader_idx, screen_idx].item()
        if score > threshold:
            rows.append({
                "layer": layer,
                "head": head,
                "binding_score": round(score, 4)
            })

with open("../results/pythia/extended/160m_screenReader_attention_binding.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["layer", "head", "binding_score"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Found {len(rows)} heads above threshold {threshold}")
print("\nTop 10 by binding strength:")
sorted_rows = sorted(rows, key=lambda x: x["binding_score"], reverse=True)
for row in sorted_rows[:10]:
    print(f"Layer {row['layer']:2d}, Head {row['head']:2d}: {row['binding_score']}")
print("Saved to 160m_screenReader_attention_binding.csv")
```

**Cell 10 (markdown):**
```
##### Circuitsvis
*Circuitsvis* is run on the layer that has the head with the top binding strength.
**Layer 11, Head 8 (score: 1.0)**
```

**Cell 11 (code):**
```python
# Layer 11, Head 8 (score: 1.0)
layer = 11
attention = cache["pattern", layer]
cv.attention.attention_patterns(tokens=tokens, attention=attention[0])
```

**Cell 12 (markdown):**
```
#### Alt Text (text to alt)
```

**Cell 13 (code):**
```python
# DIRECTION: "text" looks at "alt" = attn[text_idx, alt_idx]
# Rule: attn[SECOND, FIRST]

prompt = "An image needs alt text to be accessible"
tokens = model.to_str_tokens(prompt)
print(list(enumerate(tokens)))  # verify indices
logits, cache = model.run_with_cache(prompt)

threshold = 0.1
rows = []

for layer in range(model.cfg.n_layers):
    attention = cache["pattern", layer]
    for head in range(model.cfg.n_heads):
        attn = attention[0, head]
        text_idx = 5
        alt_idx = 4
        score = attn[text_idx, alt_idx].item()
        if score > threshold:
            rows.append({
                "layer": layer,
                "head": head,
                "binding_score": round(score, 4)
            })

with open("../results/pythia/extended/160m_altText_attention_binding.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["layer", "head", "binding_score"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Found {len(rows)} heads above threshold {threshold}")
print("\nTop 10 by binding strength:")
sorted_rows = sorted(rows, key=lambda x: x["binding_score"], reverse=True)
for row in sorted_rows[:10]:
    print(f"Layer {row['layer']:2d}, Head {row['head']:2d}: {row['binding_score']}")
print("Saved to 160m_altText_attention_binding.csv")
```

**Cell 14 (markdown):**
```
##### Circuitsvis
**Layer 11, Head 0 (score: 0.9932)**
```

**Cell 15 (code):**
```python
# Layer 11, Head 0 (score: 0.9932)
layer = 11
attention = cache["pattern", layer]
cv.attention.attention_patterns(tokens=tokens, attention=attention[0])
```

**Cell 16 (markdown):**
```
#### Skip Link (link to skip)
```

**Cell 17 (code):**
```python
# DIRECTION: "link" looks at "skip" = attn[link_idx, skip_idx]
# Rule: attn[SECOND, FIRST]

prompt = "Use a skip link to bypass navigation"
tokens = model.to_str_tokens(prompt)
print(list(enumerate(tokens)))  # verify indices
logits, cache = model.run_with_cache(prompt)

threshold = 0.1
rows = []

for layer in range(model.cfg.n_layers):
    attention = cache["pattern", layer]
    for head in range(model.cfg.n_heads):
        attn = attention[0, head]
        link_idx = 4
        skip_idx = 3
        score = attn[link_idx, skip_idx].item()
        if score > threshold:
            rows.append({
                "layer": layer,
                "head": head,
                "binding_score": round(score, 4)
            })

with open("../results/pythia/extended/160m_skipLink_attention_binding.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["layer", "head", "binding_score"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Found {len(rows)} heads above threshold {threshold}")
print("\nTop 10 by binding strength:")
sorted_rows = sorted(rows, key=lambda x: x["binding_score"], reverse=True)
for row in sorted_rows[:10]:
    print(f"Layer {row['layer']:2d}, Head {row['head']:2d}: {row['binding_score']}")
print("Saved to 160m_skipLink_attention_binding.csv")
```

**Cell 18 (markdown):**
```
##### Circuitsvis
**Layer 11, Head 0 & Head 6 (score: 1.0)**
```

**Cell 19 (code):**
```python
# Layer 11, Head 0 & Head 6 (score: 1.0)
layer = 11
attention = cache["pattern", layer]
cv.attention.attention_patterns(tokens=tokens, attention=attention[0])
```

**Cell 20 (markdown):**
```
### Delete Model & Clear Cache
```

**Cell 21 (code):**
```python
# Run this between models
del model
del cache
gc.collect()
torch.cuda.empty_cache()
print("Memory cleared")
```

### Rules
- Replace cells 0 through the cell immediately before the "Pythia 410M" markdown heading with exactly the cells above.
- Do NOT modify, delete, or reorder any cells from the "Pythia 410M" heading onward.
- Clear all cell outputs in the cells you replace.
- Do not add any cells that are not listed above.
