#!/usr/bin/env python3
"""Render Excalidraw JSON elements to source-specific SVG and PNG."""

from __future__ import annotations

import argparse
import base64
import html
import json
import subprocess
from pathlib import Path


FONT_PATH = Path(__file__).resolve().parents[1] / "assets" / "Excalifont-Regular.ttf"


def render(source: Path, svg: Path) -> None:
    """Render rectangles, arrows, and text directly from Excalidraw JSON."""
    document = json.loads(source.read_text(encoding="utf-8"))
    elements = [element for element in document.get("elements", []) if not element.get("isDeleted")]
    max_x = max((float(element.get("x", 0)) + abs(float(element.get("width", 0))) for element in elements), default=600)
    max_y = max((float(element.get("y", 0)) + abs(float(element.get("height", 0))) for element in elements), default=400)
    canvas_width, canvas_height = max_x + 40, max_y + 70
    font_face = ""
    if FONT_PATH.is_file():
        encoded_font = base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")
        font_face = f"@font-face{{font-family:Excalifont;src:url(data:font/ttf;base64,{encoded_font}) format('truetype');font-weight:400;font-style:normal;}}"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width:g}" height="{canvas_height:g}" viewBox="0 0 {canvas_width:g} {canvas_height:g}">',
        '<defs><filter id="rough" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="17" result="noise"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter></defs>',
        f'<rect x="0" y="0" width="{canvas_width:g}" height="{canvas_height:g}" fill="#ffffff"/>',
        f'<style>{font_face}text{{font-family:Excalifont,"Comic Sans MS",cursive,sans-serif}} .edge{{fill:none;stroke:#1e1e1e;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}} .arrow{{stroke:none}} .rough{{filter:url(#rough)}}</style>',
    ]
    for element in elements:
        x, y = float(element.get("x", 0)), float(element.get("y", 0))
        if element.get("type") in {"arrow", "line"}:
            points = element.get("points", [])
            if len(points) < 2:
                continue
            absolute = [(x + float(point[0]), y + float(point[1])) for point in points]
            d = "M" + " ".join(f"{px:g},{py:g}" for px, py in absolute)
            parts.append(f'<path class="edge rough" d="{d}"/>')
            px, py = absolute[-1]
            if len(absolute) >= 2:
                prev_x, prev_y = absolute[-2]
                if abs(px - prev_x) >= abs(py - prev_y):
                    arrow = f"M{px:g},{py:g} l{'-10' if px >= prev_x else '10'},-6 v12 z"
                else:
                    arrow = f"M{px:g},{py:g} l-6,{'-10' if py >= prev_y else '10'} h12 z"
                parts.append(f'<path class="arrow rough" fill="{html.escape(element.get("strokeColor", "#1e1e1e"))}" d="{arrow}"/>')
        elif element.get("type") in {"rectangle", "ellipse", "diamond"}:
            width, height = abs(float(element.get("width", 0))), abs(float(element.get("height", 0)))
            raw_fill = element.get("backgroundColor", "transparent")
            fill = "none" if raw_fill == "transparent" else html.escape(raw_fill)
            stroke = html.escape(element.get("strokeColor", "#1e1e1e"))
            if element.get("type") == "ellipse":
                parts.append(f'<ellipse class="rough" cx="{x+width/2:g}" cy="{y+height/2:g}" rx="{width/2:g}" ry="{height/2:g}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            elif element.get("type") == "diamond":
                points = f"{x+width/2:g},{y:g} {x+width:g},{y+height/2:g} {x+width/2:g},{y+height:g} {x:g},{y+height/2:g}"
                parts.append(f'<polygon class="rough" points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            else:
                parts.append(f'<rect class="rough" x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        if element.get("type") == "text" or element.get("text"):
            text = html.escape(str(element.get("text", element.get("originalText", ""))))
            lines = text.split("\n")
            parts.extend(f'<text x="{x+float(element.get("width", 0))/2:g}" y="{y+float(element.get("height", 0))/2+(i-(len(lines)-1)/2)*22:g}" text-anchor="middle" dominant-baseline="middle" font-size="{element.get("fontSize", 16)}">{line}</text>' for i, line in enumerate(lines))
    parts.append(f'<text x="40" y="{max_y+40:g}" font-size="13" fill="#666">Rendered from Excalidraw JSON source</text></svg>')
    svg.write_text("".join(parts), encoding="utf-8")


def main() -> int:
    """Parse arguments, render SVG, and convert with sips."""
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
