#!/usr/bin/env python3
"""
Generate paper figures for Paper 1: Accessibility Emergence.

Outputs to paper/figures/. Run from the paper-1-emergence/ directory:
    python generate-figures.py

Produces:
    fig1-declarative-heatmap.png   — Experiment 1 outcomes by model scale
    fig2-perplexity-flip.png       — Experiment 3 perplexity crossover
    fig3-evaluative-heatmap.png    — Experiment 2 outcomes by model scale
    fig4-compound-comparison.png   — Binding head counts across compounds
    fig5-control-comparison.png    — Screen reader vs control binding
    fig6-l1h12-comparison.png      — Layer 1 head binding: screen reader vs control
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
FIGURES_DIR = Path("paper/figures")
RESULTS_DIR = Path("results")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Palette (matches existing figures) ────────────────────────────────────────
CORRECT_COLOR   = "#2a7f8a"   # teal
PARTIAL_COLOR   = "#c8956c"   # amber
INCORRECT_COLOR = "#d9d9d9"   # light gray
HIGHLIGHT_COLOR = "#1a5c66"   # dark teal for L1H12 callout

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  "#f8f8f8",
    "axes.facecolor":    "#f8f8f8",
})

# ── Outcome encoding ───────────────────────────────────────────────────────────
CORRECT   = 2
PARTIAL   = 1
INCORRECT = 0

OUTCOME_LABELS      = {CORRECT: "Correct",   PARTIAL: "Partial",  INCORRECT: "Incorrect"}
OUTCOME_COLORS      = {CORRECT: CORRECT_COLOR, PARTIAL: PARTIAL_COLOR, INCORRECT: INCORRECT_COLOR}
OUTCOME_TEXT_COLORS = {CORRECT: "white",      PARTIAL: "white",    INCORRECT: "#666666"}

MODELS = ["160M", "410M", "1B", "2.8B", "6.9B"]

# ── Experiment data ────────────────────────────────────────────────────────────
# Encoded from results section (2=Correct, 1=Partial, 0=Incorrect)

DECLARATIVE_DATA = {
    "screen reader":       [INCORRECT, INCORRECT, PARTIAL,   CORRECT,   PARTIAL  ],
    "WCAG":                [INCORRECT, INCORRECT, INCORRECT, INCORRECT, CORRECT  ],
    "skip link":           [INCORRECT, PARTIAL,   INCORRECT, CORRECT,   INCORRECT],
    "alt text":            [INCORRECT, INCORRECT, INCORRECT, CORRECT,   CORRECT  ],
    "ARIA":                [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "focus indicator":     [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "keyboard navigation": [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "color contrast":      [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "semantic HTML":       [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "captions":            [INCORRECT, PARTIAL,   INCORRECT, PARTIAL,   INCORRECT],
}

EVALUATIVE_DATA = {
    "<img> missing alt attribute":          [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "<div onclick> keyboard inaccessible":  [INCORRECT, INCORRECT, INCORRECT, INCORRECT, PARTIAL  ],
    "empty <a href='#'> element":           [INCORRECT, PARTIAL,   INCORRECT, INCORRECT, INCORRECT],
    "<input> missing label":                [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT],
    "'Click here' link text":               [INCORRECT, INCORRECT, INCORRECT, CORRECT,   CORRECT  ],
}


# ── Figure 1 & 3: Outcome heatmaps ────────────────────────────────────────────

def make_outcome_heatmap(data, title, subtitle, caption, fig_path):
    """Categorical heatmap: rows = prompts, columns = model sizes."""
    prompts = list(data.keys())
    n_rows  = len(prompts)
    n_cols  = len(MODELS)

    fig, ax = plt.subplots(figsize=(9, 0.52 * n_rows + 2.4))
    fig.patch.set_facecolor("#f8f8f8")
    ax.set_facecolor("#f8f8f8")

    matrix = np.array([data[p] for p in prompts])

    for r in range(n_rows):
        for c in range(n_cols):
            val        = matrix[r, c]
            cell_color = OUTCOME_COLORS[val]
            text_color = OUTCOME_TEXT_COLORS[val]
            ax.add_patch(plt.Rectangle((c, r), 1, 1, color=cell_color, linewidth=0))
            ax.text(
                c + 0.5, r + 0.5,
                OUTCOME_LABELS[val],
                ha="center", va="center",
                fontsize=8.5, color=text_color,
            )

    # Cell borders
    for r in range(n_rows + 1):
        ax.axhline(r, color="white", linewidth=1.5)
    for c in range(n_cols + 1):
        ax.axvline(c, color="white", linewidth=1.5)

    # Emergence threshold marker at 2.8B (column index 3)
    ax.axvline(3, color="#555555", linewidth=1.8, linestyle="--", alpha=0.55)
    ax.text(
        3.0, n_rows + 0.1,
        "emergence\nthreshold",
        ha="center", va="bottom",
        fontsize=7.5, color="#555555", linespacing=1.3,
    )

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)

    ax.set_xticks([c + 0.5 for c in range(n_cols)])
    ax.set_xticklabels(MODELS, fontsize=10)
    ax.set_yticks([r + 0.5 for r in range(n_rows)])
    ax.set_yticklabels(prompts, fontsize=9.5)
    ax.tick_params(length=0)

    # Model labels on top
    ax.xaxis.set_label_position("top")
    ax.xaxis.tick_top()

    # Legend
    handles = [
        mpatches.Patch(color=CORRECT_COLOR,  label="Correct"),
        mpatches.Patch(color=PARTIAL_COLOR,  label="Partial"),
        mpatches.Patch(color=INCORRECT_COLOR, label="Incorrect",
                       edgecolor="#aaaaaa", linewidth=0.5),
    ]
    ax.legend(
        handles=handles,
        loc="lower right",
        fontsize=8.5,
        framealpha=0.9,
        edgecolor="#cccccc",
        bbox_to_anchor=(1.0, -0.01),
    )

    fig.suptitle(title,    fontsize=12,  fontweight="bold", y=0.99, ha="center")
    ax.set_title(subtitle, fontsize=9.5, color="#555555",   pad=30)

    fig.tight_layout(rect=[0, 0.05, 1, 0.93])

    fig.text(
        0.5, 0.01, caption,
        ha="center", fontsize=8, color="#666666", style="italic",
    )

    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {fig_path}")


# ── Figure 6: L1H12 side-by-side ──────────────────────────────────────────────

def make_l1h12_figure():
    """Layer 1 head attention weights: 'screen reader' vs control (all heads)."""
    df     = pd.read_csv(RESULTS_DIR / "pythia-2.8b/pythia-2.8b-attention-binding.csv")
    layer1 = df[df["layer"] == 1].set_index("head")["reader_to_screen"]

    heads    = np.arange(32)
    sr_vals  = np.array([layer1.get(h, 0.0) for h in heads])
    ctrl_vals = np.zeros(32)

    fig, (ax_l, ax_r) = plt.subplots(
        1, 2, figsize=(11, 4.2), sharey=True, facecolor="#f8f8f8"
    )

    def bar_colors(vals, highlight_h12):
        colors = []
        for h, v in enumerate(vals):
            if highlight_h12 and h == 12:
                colors.append(HIGHLIGHT_COLOR)
            elif v >= 0.5:
                colors.append(CORRECT_COLOR)
            elif v >= 0.1:
                colors.append("#7ab8bf")   # lighter teal: moderate binding
            else:
                colors.append("#d0d0d0")   # below threshold
        return colors

    # Left panel — screen reader
    ax_l.set_facecolor("#f8f8f8")
    ax_l.bar(heads, sr_vals, color=bar_colors(sr_vals, True), width=0.75, edgecolor="none")
    ax_l.axhline(0.5, color="#aaaaaa", linewidth=0.8, linestyle="--")
    ax_l.text(30.5, 0.52, "strong (0.5)", fontsize=7, color="#888888", ha="right", va="bottom")
    ax_l.annotate(
        "L1H12",
        xy=(12, sr_vals[12]),
        xytext=(18, 0.78),
        fontsize=9, color=HIGHLIGHT_COLOR, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=HIGHLIGHT_COLOR, lw=1.2,
                        connectionstyle="arc3,rad=-0.25"),
    )
    ax_l.set_title('"screen reader"', fontsize=11, fontweight="bold", pad=8)
    ax_l.set_xlabel(
        'Attention weight: "reader" \u2192 "screen"  |  Pythia 2.8B, Layer 1\n'
        "24 of 32 heads above 0.1 threshold",
        fontsize=8.5, color="#555555", labelpad=8,
    )
    ax_l.set_ylabel("Attention weight", fontsize=9.5)

    # Right panel — control
    ax_r.set_facecolor("#f8f8f8")
    ax_r.bar(heads, ctrl_vals, color=bar_colors(ctrl_vals, False), width=0.75, edgecolor="none")
    ax_r.axhline(0.5, color="#aaaaaa", linewidth=0.8, linestyle="--")
    ax_r.text(
        16, 0.15,
        "zero binding in all\nfour control pairs",
        ha="center", va="center",
        fontsize=9, color="#888888", style="italic", linespacing=1.5,
    )
    ax_r.set_title("Control (adjacent tokens)", fontsize=11, fontweight="bold", pad=8)
    ax_r.set_xlabel(
        "Same threshold, same model, same conditions\n"
        "cold water  \u2014  the castle is very old  \u2014  and then  \u2014  very old hill",
        fontsize=8.5, color="#555555", labelpad=8,
    )

    for ax in (ax_l, ax_r):
        ax.set_xlim(-0.8, 31.8)
        ax.set_ylim(0, 1.05)
        ax.set_xticks([0, 8, 16, 24, 31])
        ax.set_xticklabels(["Head 0", "Head 8", "Head 16", "Head 24", "Head 31"],
                           fontsize=8.5)
        ax.tick_params(axis="y", labelsize=8.5)
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)

    fig.suptitle(
        "Figure 6 \u2014 L1H12: Candidate Concept-Binding Head\n"
        "Layer 1 attention weights across all 32 heads, Pythia 2.8B",
        fontsize=11.5, fontweight="bold", y=1.03,
    )
    fig.text(
        0.5, -0.06,
        "Figure 6. L1H12 is the dominant binding head for accessibility compounds. "
        "Control pairs with no compound semantic relationship produce zero binding above threshold, "
        "ruling out token proximity as an explanation.",
        ha="center", fontsize=8, color="#666666", style="italic",
        wrap=True,
    )

    fig.tight_layout()

    out = FIGURES_DIR / "fig6-l1h12-comparison.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


# ── Figure 2: Perplexity flip ─────────────────────────────────────────────────

def make_perplexity_figure():
    """Line chart showing perplexity crossover between correct and wrong definitions."""
    models  = ["160M", "410M", "1B", "2.8B", "6.9B"]
    correct = [106.7,   40.1,  18.8,   13.6,   15.6]
    wrong   = [ 41.4,   32.8,  42.2,   54.9,   46.1]
    x       = range(len(models))

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Flip zone shading between 410M (x=1) and 1B (x=2)
    ax.axvspan(1, 2, color="#e8eaf0", alpha=0.7, zorder=0)
    ax.text(1.5, 88, "flip\nzone", ha="center", va="top",
            fontsize=9, color="#888888", style="italic", linespacing=1.4)

    ax.plot(x, correct, color=CORRECT_COLOR,  marker="o", linewidth=2,
            markersize=7, label="Correct definition", zorder=3)
    ax.plot(x, wrong,   color=PARTIAL_COLOR,  marker="s", linewidth=2,
            markersize=7, label="Wrong definition",   zorder=3)

    # Annotation arrow pointing to crossover
    ax.annotate(
        "preference flips\nbetween 410M and 1B",
        xy=(1.5, 36), xytext=(2.6, 66),
        fontsize=8.5, color="#555555", ha="center", linespacing=1.4,
        arrowprops=dict(arrowstyle="->" , color="#555555", lw=1.1),
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(models, fontsize=10)
    ax.set_xlabel("Model Size (Parameters)", fontsize=10, labelpad=8)
    ax.set_ylabel("Perplexity  (lower = more expected)", fontsize=9.5, labelpad=8)
    ax.set_ylim(0, 115)
    ax.legend(fontsize=9.5, framealpha=0.9, edgecolor="#cccccc", loc="upper right")

    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

    ax.set_title(
        "Figure 2 -- Recognition Precedes Generation\n"
        "Perplexity for Correct vs. Wrong Definition",
        fontsize=11, fontweight="bold", pad=10,
    )

    fig.tight_layout()
    out = FIGURES_DIR / "fig2-perplexity-flip.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


# ── Figure 4: Compound comparison ─────────────────────────────────────────────

def make_compound_figure():
    """Grouped bar chart: binding head counts for all three accessibility compounds."""
    compounds = ["screen reader", "alt text", "skip link"]

    # Load counts directly from CSVs
    def counts(path):
        df = pd.read_csv(path)
        total  = len(df)
        strong = (df["reader_to_screen"] >= 0.5).sum()
        return total, strong

    sr_total, sr_strong = counts(RESULTS_DIR / "pythia-2.8b/pythia-2.8b-attention-binding.csv")
    at_total, at_strong = counts(RESULTS_DIR / "pythia-2.8b/pythia-2.8b-altText-attention-binding.csv")
    sl_total, sl_strong = counts(RESULTS_DIR / "pythia-2.8b/pythia-2.8b-skipLink-attention-binding.csv")

    totals  = [sr_total,  at_total,  sl_total ]
    strongs = [sr_strong, at_strong, sl_strong]

    LIGHT_TEAL = "#7ab8bf"
    DARK_TEAL  = CORRECT_COLOR

    x      = np.arange(len(compounds))
    width  = 0.38

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars_all    = ax.bar(x - width / 2, totals,  width, color=LIGHT_TEAL, label="All heads >0.1",    zorder=2)
    bars_strong = ax.bar(x + width / 2, strongs, width, color=DARK_TEAL,  label="Strong heads >=0.5", zorder=2)

    for bar, val in zip(bars_all,    totals ):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                str(val), ha="center", va="bottom", fontsize=9.5)
    for bar, val in zip(bars_strong, strongs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                str(val), ha="center", va="bottom", fontsize=9.5)

    ax.set_xticks(x)
    ax.set_xticklabels(compounds, fontsize=10.5)
    ax.set_ylabel("Head count (Pythia 2.8B)", fontsize=10, labelpad=8)
    ax.set_ylim(0, 240)
    ax.legend(fontsize=9.5, framealpha=0.9, edgecolor="#cccccc")

    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

    ax.set_title(
        "Figure 4 -- Binding Generalizes Across Accessibility Compounds\n"
        "All three tested at 2.8B emergence threshold",
        fontsize=11, fontweight="bold", pad=10,
    )

    fig.tight_layout()
    out = FIGURES_DIR / "fig4-compound-comparison.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


# ── Figure 5: Control comparison ──────────────────────────────────────────────

def make_control_figure():
    """Single bar chart: screen reader vs control binding signal."""
    df_sr   = pd.read_csv(RESULTS_DIR / "pythia-2.8b/pythia-2.8b-attention-binding.csv")
    sr_count = len(df_sr)

    labels = [
        "screen reader\n(accessibility compound)",
        "cold water\n(control -- adjacent tokens)",
    ]
    values = [sr_count, 0]
    colors = [CORRECT_COLOR, "#d0d0d0"]

    fig, ax = plt.subplots(figsize=(6.5, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.bar(labels, values, color=colors, width=0.45, zorder=2)

    # Bold count on screen reader bar
    ax.text(0, sr_count + 1.5, str(sr_count),
            ha="center", va="bottom", fontsize=16,
            fontweight="bold", color=CORRECT_COLOR)

    # Italic annotation on control bar
    ax.text(1, 12,
            "zero heads above threshold\nin all four control prompts",
            ha="center", va="bottom",
            fontsize=8.5, color="#888888", style="italic", linespacing=1.4)
    ax.text(1, 1.5, "0", ha="center", va="bottom", fontsize=10, color="#888888")

    ax.set_ylabel("Heads above 0.1 threshold (Pythia 2.8B)", fontsize=9.5, labelpad=8)
    ax.set_ylim(0, 120)
    ax.tick_params(axis="x", labelsize=10)

    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

    ax.set_title(
        "Figure 5 -- Binding Signal Is Not a Proximity Artifact\n"
        "Same threshold, same model, same conditions",
        fontsize=11, fontweight="bold", pad=10,
    )

    fig.tight_layout()
    out = FIGURES_DIR / "fig5-control-comparison.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    make_outcome_heatmap(
        DECLARATIVE_DATA,
        title    = "Figure 1 \u2014 Declarative Knowledge by Model Scale",
        subtitle = "Ten accessibility concept prompts across five Pythia model sizes",
        caption  = "Figure 1. Dashed line marks 2.8B emergence threshold. "
                   "Partial indicates a response capturing some but not all key information.",
        fig_path = FIGURES_DIR / "fig1-declarative-heatmap.png",
    )

    make_outcome_heatmap(
        EVALUATIVE_DATA,
        title    = "Figure 3 \u2014 Evaluative Knowledge by Model Scale",
        subtitle = "Five accessibility code prompts \u2014 models must identify violations",
        caption  = "Figure 3. Declarative-evaluative gap persists across all scales. "
                   "Only ambiguous link text ('Click here') is identified correctly, at 2.8B and above.",
        fig_path = FIGURES_DIR / "fig3-evaluative-heatmap.png",
    )

    make_perplexity_figure()
    make_compound_figure()
    make_control_figure()
    make_l1h12_figure()
