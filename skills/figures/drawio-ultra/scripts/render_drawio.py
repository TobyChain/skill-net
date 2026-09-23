#!/usr/bin/env python3
"""Render a small, source-specific Draw.io XML diagram to SVG and PNG.

The renderer reads mxCell/mxGeometry values from the .drawio source. It is a
portable fallback for examples and CI when the Draw.io desktop CLI is absent;
it does not consume another format's SVG.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path


def style_value(style: str, key: str, default: str) -> str:
    """Read a Draw.io semicolon-delimited style value."""
    match = re.search(rf"(?:^|;){re.escape(key)}=([^;]+)", style)
    return match.group(1) if match else default

def anchor(box: tuple[float, float, float, float], style: str, prefix: str) -> tuple[float, float]:
    """Calculate an edge endpoint from Draw.io perimeter fractions."""
    x, y, width, height = box
    x_fraction = float(style_value(style, prefix + "X", "0.5"))
    y_fraction = float(style_value(style, prefix + "Y", "0.5"))
    return x + width * x_fraction, y + height * y_fraction


def label_lines(value: str, width: float, font_size: float) -> list[str]:
    """Wrap XML labels to fit the source node width."""
    max_width = max(width - 24, font_size * 4)
    lines: list[str] = []
    for line in value.splitlines():
        if " " in line and len(line) > 18:
            words = line.split()
            current_words: list[str] = []
            current_width = 0.0
            for word in words:
                word_width = sum(font_size * (0.95 if ord(char) >= 0x2E80 else 0.58) for char in word)
                extra = font_size * 0.58 if current_words else 0
                if current_words and current_width + extra + word_width > max_width:
                    lines.append(" ".join(current_words))
                    current_words, current_width = [word], word_width
                else:
                    current_words.append(word)
                    current_width += extra + word_width
            if current_words:
                lines.append(" ".join(current_words))
            continue
        current = ""
        current_width = 0.0
        for char in line:
            char_width = font_size * (0.95 if ord(char) >= 0x2E80 else 0.58)
            if current and current_width + char_width > max_width:
                lines.append(current)
                current, current_width = char, char_width
            else:
                current += char
                current_width += char_width
        lines.append(current)
    return lines or [""]


def arrow_head(points: list[tuple[float, float]], color: str) -> str:
    """Draw an arrowhead oriented along the final route segment."""
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    if abs(x2 - x1) >= abs(y2 - y1):
        path = f"M{x2:g},{y2:g} l{'-10' if x2 >= x1 else '10'},-6 v12 z"
    else:
        path = f"M{x2:g},{y2:g} l-6,{'-10' if y2 >= y1 else '10'} h12 z"
    return f'<path class="arrow" fill="{html.escape(color)}" d="{path}"/>'


def render(source: Path, svg: Path) -> None:
    """Render vertex cells and their edge endpoints from Draw.io XML."""
    root = ET.parse(source).getroot()
    cells = {cell.get("id"): cell for cell in root.iter("mxCell") if cell.get("id")}
    vertices = {}
    edges = []
    max_x = max_y = 0.0
    for cell_id, cell in cells.items():
        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue
        x = float(geometry.get("x", 0))
        y = float(geometry.get("y", 0))
        width = float(geometry.get("width", 0))
        height = float(geometry.get("height", 0))
        max_x, max_y = max(max_x, x + width), max(max_y, y + height)
        if cell.get("vertex") == "1":
            vertices[cell_id] = (x, y, width, height, cell.get("value", ""), cell.get("style", ""))
        elif cell.get("edge") == "1":
            edges.append((cell, geometry))

    width, height = max_x + 40, max_y + 80
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" viewBox="0 0 {width:g} {height:g}">', f'<rect x="0" y="0" width="{width:g}" height="{height:g}" fill="#ffffff"/>']
    parts.append('<style>text{font-family:Arial,sans-serif} .edge{fill:none;stroke:#333;stroke-width:2} .arrow{fill:#333}</style>')
    for edge, geometry in edges:
        source_box = vertices.get(edge.get("source"))
        target_box = vertices.get(edge.get("target"))
        if not source_box or not target_box:
            continue
        sx, sy, sw, sh = source_box[:4]
        tx, ty, tw, th = target_box[:4]
        x1, y1 = anchor((sx, sy, sw, sh), edge.get("style", ""), "exit")
        x2, y2 = anchor((tx, ty, tw, th), edge.get("style", ""), "entry")
        points = [(x1, y1)]
        point_array = geometry.find("Array")
        if point_array is not None:
            points.extend((float(point.get("x", 0)), float(point.get("y", 0))) for point in point_array.findall("mxPoint"))
        points.append((x2, y2))
        path_data = "M" + " ".join(f"{px:g},{py:g}" for px, py in points)
        label = html.escape(edge.get("value", ""))
        parts.append(f'<path class="edge" d="{path_data}"/>')
        parts.append(arrow_head(points, style_value(edge.get("style", ""), "strokeColor", "#333333")))
        if label and abs(x2 - x1) >= 120:
            parts.append(f'<text x="{(x1+x2)/2:g}" y="{y1-8:g}" text-anchor="middle" font-size="14">{label}</text>')
    for x, y, box_width, box_height, value, style in vertices.values():
        fill = style_value(style, "fillColor", "#ffffff")
        stroke = style_value(style, "strokeColor", "#333333")
        font_size = style_value(style, "fontSize", "16")
        is_text = "text" in style.split(";")
        if not is_text:
            parts.append(f'<rect x="{x:g}" y="{y:g}" width="{box_width:g}" height="{box_height:g}" rx="10" fill="{html.escape(fill)}" stroke="{html.escape(stroke)}" stroke-width="2"/>')
        lines = [html.escape(line) for line in label_lines(value, box_width, float(font_size))]
        line_height = float(font_size) * (1.15 if is_text else 1.25)
        first_y = y + (box_height - line_height * len(lines)) / 2 + line_height / 2
        if is_text:
            first_y = y + line_height
        for index, line in enumerate(lines):
            parts.append(f'<text x="{x+box_width/2:g}" y="{first_y + index * line_height:g}" text-anchor="middle" dominant-baseline="middle" font-size="{font_size}">{line}</text>')
    parts.append('<text x="40" y="%g" font-size="13" fill="#666">Rendered from Draw.io XML source</text>' % (height - 20))
    parts.append("</svg>")
    svg.write_text("".join(parts), encoding="utf-8")


def main() -> int:
    """Parse arguments, render SVG, and convert with sips when available."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    svg = args.out_dir / (args.source.stem + ".svg")
    render(args.source, svg)
    png = args.out_dir / (args.source.stem + ".png")
    subprocess.run(["sips", "-s", "format", "png", str(svg), "--out", str(png)], check=True, stdout=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
