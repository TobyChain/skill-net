"""Plot reported Qwen3.8-Next architecture and scaling metrics.

Values are transcribed from Tables 1, 2, and the n-gram vocabulary tables of
arXiv:2608.30320. They are not reconstructed or smoothed teaching data.
"""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Render Qwen3.8-Next reported metrics.")
parser.add_argument("--out-dir", type=Path, default=Path.cwd())
args = parser.parse_args()

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as exc:
    parser.error(f"missing optional plotting dependency: {exc.name}; install matplotlib")

args.out_dir.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.unicode_minus": False})

benchmarks = ["MMLU", "MMLU-Pro", "SuperGPQA", "MATH", "GSM8K", "BBH", "MMMLU", "EvalPlus", "MultiPL-E"]
full_attention = [62.65, 37.59, 21.76, 49.40, 75.13, 63.78, 47.74, 51.01, 39.73]
swa_hybrid = [66.30, 40.67, 22.45, 45.48, 74.22, 65.88, 51.33, 52.12, 41.93]
gdn_hybrid = [66.26, 42.82, 23.45, 53.98, 77.07, 68.72, 54.83, 49.71, 47.48]

vocab_scale = ["None", "20×", "50×", "100×", "200×"]
loss = [1.585, 1.553, 1.541, 1.534, 1.526]
mmlu = [62.78, 64.14, 64.71, 64.70, 64.85]
ceval = [66.91, 71.75, 72.12, 73.75, 74.94]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.2))
width = 0.25
x = list(range(len(benchmarks)))
for offset, values, label, color in [(-width, full_attention, "Full attention", "#9ECAE1"), (0, swa_hybrid, "SWA hybrid", "#74C476"), (width, gdn_hybrid, "GDN hybrid", "#756BB1")]:
    ax1.bar([i + offset for i in x], values, width=width, label=label, color=color, edgecolor="#333333", linewidth=0.5)
ax1.axhline(49.87, color="#999999", linestyle="--", linewidth=0.8)
ax1.axhline(51.15, color="#74C476", linestyle=":", linewidth=0.9)
ax1.axhline(53.81, color="#756BB1", linestyle=":", linewidth=0.9)
ax1.set_xticks(x, benchmarks, rotation=35, ha="right")
ax1.set_ylabel("Score (%)")
ax1.set_title("Architecture comparison")
ax1.legend(fontsize=8, frameon=False)
ax1.grid(axis="y", linestyle="--", linewidth=0.5, color="#DDDDDD")
ax1.set_axisbelow(True)

ax2.plot(vocab_scale, loss, marker="o", color="#C44E52", linewidth=2, label="Loss ↓")
ax2.set_ylabel("Loss", color="#C44E52")
ax2.tick_params(axis="y", labelcolor="#C44E52")
ax2.set_xlabel("N-gram vocabulary scale")
ax2.set_title("N-gram vocabulary scaling")
ax2.grid(axis="y", linestyle="--", linewidth=0.5, color="#DDDDDD")
ax2b = ax2.twinx()
ax2b.plot(vocab_scale, mmlu, marker="s", color="#4C72B0", linewidth=2, label="MMLU")
ax2b.plot(vocab_scale, ceval, marker="^", color="#55A868", linewidth=2, label="C-Eval")
ax2b.set_ylabel("Benchmark score (%)")
ax2b.set_ylim(55, 80)
handles, labels = [], []
for axis in (ax2, ax2b):
    h, l = axis.get_legend_handles_labels(); handles.extend(h); labels.extend(l)
ax2b.legend(handles, labels, frameon=False, fontsize=8, loc="lower right")
fig.suptitle("Qwen3.8-Flash-Next reported metrics — arXiv:2608.30320", fontsize=15, y=1.01)
fig.text(0.5, -0.02, "Reported values transcribed from the paper; no interpolation. GDN avg=53.81, full attention avg=49.87, SWA avg=51.15.", ha="center", fontsize=9, color="#666666")
fig.tight_layout()
fig.savefig(args.out_dir / "qwen38-next-metrics.svg", format="svg", bbox_inches="tight")
fig.savefig(args.out_dir / "qwen38-next-metrics.png", dpi=220, facecolor="white", bbox_inches="tight")
plt.close(fig)
