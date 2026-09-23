#!/usr/bin/env python3
"""Render a TikZ example directly from its named nodes and draw commands."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
from pathlib import Path


NODE_RE = re.compile(r"\\node\[(?P<style>[^]]*)\](?P<placement>.*?)\((?P<id>[A-Za-z0-9_-]+)\)\s*\{(?P<label>.*?)\};", re.S)
DRAW_RE = re.compile(r"\\draw\[[^]]*\]\s*\((?P<src>[A-Za-z0-9_-]+)(?:\.[^)]+)?\)\s*--\s*\((?P<dst>[A-Za-z0-9_-]+)(?:\.[^)]+)?\)", re.S)


def clean_label(label: str) -> str:
    """Convert TeX line breaks and simple math markers to readable text."""
    label = label.replace("\\\\", "\n")
    return re.sub(r"\$", "", label)


def render(source: Path, svg: Path) -> None:
    """Extract real TikZ node declarations and direct routes."""
    text = source.read_text(encoding="utf-8")
    nodes = []
    for match in NODE_RE.finditer(text):
        label = clean_label(match.group("label"))
        style = match.group("style")
        placement = match.group("placement")
        if not label.strip() or "group" in style or "above=" in placement:
            continue
        nodes.append((match.group("id"), label, style, placement))
    if not nodes:
        raise ValueError("no renderable named TikZ nodes found")

    width, height = 1700, 760
    boxes = {}
    # Keep every source node visible. A two-row fallback is deliberately
    # deterministic because TikZ positioning arithmetic is not evaluated here.
    for index, (node_id, label, style, placement) in enumerate(nodes):
        column = index % 7
        row = index // 7
        boxes[node_id] = (35 + column * 215, 150 + row * 300, 190, 100)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>', '<style>text{font-family:Arial,sans-serif} .edge{fill:none;stroke:#333;stroke-width:2}</style>']
    for match in DRAW_RE.finditer(text):
        source_box, target_box = boxes.get(match.group("src")), boxes.get(match.group("dst"))
        if not source_box or not target_box:
            continue
        sx, sy, sw, sh = source_box
        tx, ty, tw, th = target_box
        x1, y1, x2, y2 = sx + sw, sy + sh / 2, tx, ty + th / 2
        parts.append(f'<path class="edge" d="M{x1:g},{y1:g} H{x2:g}"/>')
        parts.append(f'<path fill="#333" d="M{x2:g},{y2:g} l-10,-6 v12 z"/>')
    for node_id, label, style, _placement in nodes:
        x, y, w, h = boxes[node_id]
        fill = "#EAF4E3" if "green" in style else "#FFF2CC" if "yellow" in style else "#DDEBF7" if "blue" in style else "#F4E8F7" if "violet" in style else "#FCE4D6" if "orange" in style else "#EEEEEE"
        parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="10" fill="{fill}" stroke="#333" stroke-width="2"/>')
        lines = html.escape(label).split("\n")
        for index, line in enumerate(lines):
            parts.append(f'<text x="{x+w/2:g}" y="{y+h/2+(index-(len(lines)-1)/2)*22:g}" text-anchor="middle" dominant-baseline="middle" font-size="15">{line}</text>')
    parts.append(f'<text x="35" y="720" font-size="13" fill="#666">Rendered from TikZ source: {html.escape(source.name)}</text></svg>')
    svg.write_text("".join(parts), encoding="utf-8")


def main() -> int:
    """Render SVG and convert it to PNG with sips."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    svg = args.out_dir / (args.source.stem + ".svg")
    render(args.source, svg)
    subprocess.run(["sips", "-s", "format", "png", str(svg), "--out", str(args.out_dir / (args.source.stem + ".png"))], check=True, stdout=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
