#!/usr/bin/env python3
"""Apply format-neutral geometry to an Excalidraw or Draw.io source file."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def prepare_edit_path(source: Path) -> Path:
    """Copy a source file to a same-directory temporary edit path."""
    work_path = source.with_suffix(source.suffix + ".edit")
    if work_path.exists():
        raise FileExistsError(f"edit file already exists: {work_path}")
    shutil.copy2(source, work_path)
    return work_path


def point_list(edge: dict[str, Any]) -> list[tuple[float, float]]:
    """Read calculated absolute route points."""
    return [(float(point[0]), float(point[1])) for point in edge.get("points", [])]


def binding_focus(rect: dict[str, Any], point: tuple[float, float]) -> float:
    """Return the Excalidraw focus value for a boundary anchor."""
    x, y = point
    left, top = float(rect["x"]), float(rect["y"])
    right, bottom = left + float(rect["width"]), top + float(rect["height"])
    if abs(x - left) <= 1 or abs(x - right) <= 1:
        return max(-1.0, min(1.0, (y - (top + bottom) / 2) / (bottom - top) * 2))
    return max(-1.0, min(1.0, (x - (left + right) / 2) / (right - left) * 2))


def center_text_element(text_element: dict[str, Any], rect: dict[str, Any]) -> None:
    """Center an independent text element inside its owning node rectangle."""
    text_width = float(text_element.get("width", 0))
    text_height = float(text_element.get("height", 0))
    text_element["x"] = float(rect["x"]) + (float(rect["width"]) - text_width) / 2
    text_element["y"] = float(rect["y"]) + (float(rect["height"]) - text_height) / 2


def apply_excalidraw(source: Path, output: Path, layout: dict[str, Any]) -> None:
    """Apply nodes, routes, bindings, and labels to an Excalidraw file."""
    document = json.loads(source.read_text(encoding="utf-8"))
    elements = document.get("elements", [])
    by_id = {str(element.get("id")): element for element in elements}
    nodes = {str(node["id"]): node for node in layout.get("nodes", [])}

    for node_id, geometry in nodes.items():
        if node_id not in by_id:
            raise ValueError(f"layout node is missing from Excalidraw: {node_id}")
        element = by_id[node_id]
        element.update({key: geometry[key] for key in ("x", "y", "width", "height")})
        text_element_id = geometry.get("textElementId")
        if text_element_id:
            if str(text_element_id) not in by_id:
                raise ValueError(f"layout text element is missing from Excalidraw: {text_element_id}")
            center_text_element(by_id[str(text_element_id)], geometry)

    for edge in layout.get("edges", []):
        edge_id = str(edge.get("id", ""))
        if edge_id not in by_id:
            raise ValueError(f"layout edge is missing from Excalidraw: {edge_id}")
        element = by_id[edge_id]
        points = point_list(edge)
        if len(points) < 2:
            raise ValueError(f"layout edge has no route: {edge_id}")
        origin_x = min(point[0] for point in points)
        origin_y = min(point[1] for point in points)
        element["x"], element["y"] = origin_x, origin_y
        element["width"] = max(point[0] for point in points) - origin_x
        element["height"] = max(point[1] for point in points) - origin_y
        element["points"] = [[x - origin_x, y - origin_y] for x, y in points]
        source_id, target_id = str(edge["source"]), str(edge["target"])
        source_rect, target_rect = nodes[source_id], nodes[target_id]
        element["startBinding"] = {"elementId": source_id, "focus": binding_focus(source_rect, points[0]), "gap": 0}
        element["endBinding"] = {"elementId": target_id, "focus": binding_focus(target_rect, points[-1]), "gap": 0}
        for node_id in (source_id, target_id):
            bound = by_id[node_id].setdefault("boundElements", []) or []
            if not any(item.get("id") == edge_id for item in bound):
                bound.append({"id": edge_id, "type": "arrow"})
            by_id[node_id]["boundElements"] = bound
        label_id = edge.get("labelElementId")
        if label_id and edge.get("labelRect"):
            if str(label_id) not in by_id:
                raise ValueError(f"layout label is missing from Excalidraw: {label_id}")
            by_id[str(label_id)].update({key: edge["labelRect"][key] for key in ("x", "y", "width", "height")})

    output.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def style_map(style: str) -> dict[str, str]:
    """Parse a Draw.io semicolon-delimited style string."""
    return {part.split("=", 1)[0]: part.split("=", 1)[1] for part in style.split(";") if "=" in part}


def style_text(values: dict[str, str]) -> str:
    """Serialize a Draw.io style mapping deterministically."""
    return ";".join(f"{key}={value}" for key, value in values.items()) + ";"


def anchor_style(rect: dict[str, Any], point: tuple[float, float], prefix: str) -> dict[str, str]:
    """Return Draw.io entry or exit anchor style values."""
    x, y = point
    left, top = float(rect["x"]), float(rect["y"])
    right, bottom = left + float(rect["width"]), top + float(rect["height"])
    if abs(x - left) <= 1:
        return {f"{prefix}X": "0", f"{prefix}Y": str(round((y - top) / (bottom - top), 3))}
    if abs(x - right) <= 1:
        return {f"{prefix}X": "1", f"{prefix}Y": str(round((y - top) / (bottom - top), 3))}
    if abs(y - top) <= 1:
        return {f"{prefix}X": str(round((x - left) / (right - left), 3)), f"{prefix}Y": "0"}
    return {f"{prefix}X": str(round((x - left) / (right - left), 3)), f"{prefix}Y": "1"}


def apply_drawio(source: Path, output: Path, layout: dict[str, Any]) -> None:
    """Apply node geometry and absolute orthogonal waypoints to Draw.io XML."""
    tree = ET.parse(source)
    root = tree.getroot()
    cells = {cell.get("id"): cell for cell in root.iter("mxCell") if cell.get("id")}
    nodes = {str(node["id"]): node for node in layout.get("nodes", [])}
    for node_id, geometry in nodes.items():
        if node_id not in cells:
            raise ValueError(f"layout node is missing from Draw.io: {node_id}")
        geometry_element = cells[node_id].find("mxGeometry")
        if geometry_element is None:
            geometry_element = ET.SubElement(cells[node_id], "mxGeometry", {"as": "geometry"})
        for key in ("x", "y", "width", "height"):
            geometry_element.set(key, str(geometry[key]))
        text_element_id = geometry.get("textElementId")
        if text_element_id:
            if str(text_element_id) not in cells:
                raise ValueError(f"layout text element is missing from Draw.io: {text_element_id}")
            text_geometry = cells[str(text_element_id)].find("mxGeometry")
            if text_geometry is None:
                text_geometry = ET.SubElement(cells[str(text_element_id)], "mxGeometry", {"as": "geometry"})
            text_width = float(text_geometry.get("width", geometry["width"]))
            text_height = float(text_geometry.get("height", geometry["height"]))
            text_geometry.set("x", str(float(geometry["x"]) + (float(geometry["width"]) - text_width) / 2))
            text_geometry.set("y", str(float(geometry["y"]) + (float(geometry["height"]) - text_height) / 2))

    for edge in layout.get("edges", []):
        edge_id = str(edge.get("id", ""))
        if edge_id not in cells:
            raise ValueError(f"layout edge is missing from Draw.io: {edge_id}")
        cell = cells[edge_id]
        source_id, target_id = str(edge["source"]), str(edge["target"])
        cell.set("source", source_id)
        cell.set("target", target_id)
        points = point_list(edge)
        if len(points) < 2:
            raise ValueError(f"layout edge has no route: {edge_id}")
        values = style_map(cell.get("style", ""))
        values.update(anchor_style(nodes[source_id], points[0], "exit"))
        values.update(anchor_style(nodes[target_id], points[-1], "entry"))
        values["edgeStyle"] = "orthogonalEdgeStyle"
        cell.set("style", style_text(values))
        geometry_element = cell.find("mxGeometry")
        if geometry_element is None:
            geometry_element = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        geometry_element.set("relative", "1")
        for child in list(geometry_element):
            if child.tag in {"mxPoint", "Array"}:
                geometry_element.remove(child)
        if len(points) > 2:
            waypoint_array = ET.SubElement(geometry_element, "Array", {"as": "points"})
            for x, y in points[1:-1]:
                ET.SubElement(waypoint_array, "mxPoint", {"x": str(x), "y": str(y)})
        label_id = edge.get("labelElementId")
        if label_id and edge.get("labelRect"):
            if str(label_id) not in cells:
                raise ValueError(f"layout label is missing from Draw.io: {label_id}")
            label_geometry = cells[str(label_id)].find("mxGeometry")
            if label_geometry is None:
                label_geometry = ET.SubElement(cells[str(label_id)], "mxGeometry", {"as": "geometry"})
            for key in ("x", "y", "width", "height"):
                label_geometry.set(key, str(edge["labelRect"][key]))

    ET.indent(tree, space="  ")
    tree.write(output, encoding="utf-8", xml_declaration=True)


def main(argv: list[str] | None = None) -> int:
    """Apply a calculated layout while preserving the original on failure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help=".excalidraw or .drawio source")
    parser.add_argument("layout", type=Path, help="calculated layout JSON")
    parser.add_argument("--output", type=Path, help="output path; defaults to source")
    args = parser.parse_args(argv or sys.argv[1:])
    output = args.output or args.source
    work_path = prepare_edit_path(args.source)
    try:
        layout = json.loads(args.layout.read_text(encoding="utf-8"))
        if args.source.suffix == ".excalidraw":
            apply_excalidraw(work_path, work_path, layout)
        elif args.source.suffix == ".drawio":
            apply_drawio(work_path, work_path, layout)
        else:
            raise ValueError("source must end in .excalidraw or .drawio")
        work_path.replace(output)
    except (OSError, ET.ParseError, ValueError, KeyError, json.JSONDecodeError):
        if work_path.exists():
            work_path.unlink()
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
