"""Illustrative next-token probability chart for the README gallery."""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Render the illustrative next-token chart.")
parser.add_argument("--out-dir", type=Path, default=Path.cwd())
args = parser.parse_args()

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as exc:
    parser.error(f"missing optional plotting dependency: {exc.name}; install matplotlib")

args.out_dir.mkdir(parents=True, exist_ok=True)
tokens = ["故宫", "烤鸭", "旅游", "天气"]
probabilities = [0.46, 0.27, 0.18, 0.09]
colors = ["#6C8EBF", "#82B366", "#D6B656", "#B3B3B3"]

fig, ax = plt.subplots(figsize=(7.4, 4.2))
bars = ax.bar(tokens, probabilities, color=colors, edgecolor="#333333", linewidth=0.8)
ax.set_ylim(0, 0.55)
ax.set_ylabel("Illustrative probability")
ax.set_xlabel("Candidate next token")
ax.set_title("GPT-style next-token prediction")
ax.text(0.99, 0.98, "Teaching illustration — not benchmark data", transform=ax.transAxes, ha="right", va="top", fontsize=9, color="#666666")
ax.grid(axis="y", linestyle="--", linewidth=0.6, color="#DDDDDD")
ax.set_axisbelow(True)
for bar, value in zip(bars, probabilities):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 0.015, f"{value:.2f}", ha="center", fontsize=10)
fig.tight_layout()
output = args.out_dir / "next-token-probability.svg"
fig.savefig(output, format="svg", facecolor="white")
plt.close(fig)
print(f"saved: {output.resolve()}")
