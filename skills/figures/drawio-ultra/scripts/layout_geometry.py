#!/usr/bin/env python3
"""Calculate deterministic node geometry and obstacle-avoiding routes.

The input is a format-neutral layout specification. Coordinates use a top-left
origin and pixels so the result can be adapted to Excalidraw, Draw.io, or a
TikZ coordinate system without re-solving the layout by hand.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class Point:
    """A two-dimensional point in the shared layout coordinate system."""

    x: float
    y: float

    def as_list(self) -> list[float]:
        """Return a JSON-compatible point."""
        return [round(self.x, 3), round(self.y, 3)]


@dataclass(frozen=True)
class Rect:
    """An axis-aligned rectangle with an optional semantic identifier."""

    id: str
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        """Return the right edge."""
        return self.x + self.width

    @property
    def bottom(self) -> float:
        """Return the bottom edge."""
        return self.y + self.height

    @property
    def center(self) -> Point:
        """Return the rectangle center."""
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def inflate(self, amount: float) -> "Rect":
        """Return a rectangle expanded on every side by amount."""
        return Rect(self.id, self.x - amount, self.y - amount, self.width + 2 * amount, self.height + 2 * amount)

    def contains_strict(self, point: Point) -> bool:
        """Return whether a point is strictly inside the rectangle."""
        return self.x < point.x < self.right and self.y < point.y < self.bottom

    def as_dict(self) -> dict[str, Any]:
        """Return the rectangle as a node geometry mapping."""
        return {"id": self.id, "x": round(self.x, 3), "y": round(self.y, 3), "width": round(self.width, 3), "height": round(self.height, 3)}


def snap(value: float, grid: float) -> float:
    """Snap a coordinate or size to a positive grid."""
    return round(value / grid) * grid if grid > 0 else value


def text_size(text: str, font_size: float = 16, line_height: float = 1.25) -> tuple[float, float]:
    """Estimate a readable text box, including CJK and multiline labels."""
    lines = text.splitlines() or [""]
    max_width = 0.0
    for line in lines:
        max_width = max(max_width, sum(font_size * (0.95 if ord(char) >= 0x2E80 else 0.62) for char in line))
    return max_width, font_size * line_height * len(lines)


def node_size(node: dict[str, Any], grid: float) -> tuple[float, float]:
    """Calculate a node size that contains its label and declared minimum."""
    font_size = float(node.get("fontSize", 16))
    padding_x = float(node.get("paddingX", 32))
    padding_y = float(node.get("paddingY", 24))
    measured_width, measured_height = text_size(str(node.get("label", "")), font_size)
    width = max(float(node.get("width", 0)), measured_width + padding_x * 2, 80)
    height = max(float(node.get("height", 0)), measured_height + padding_y * 2, 48)
    return snap(width, grid), snap(height, grid)


def dependency_layers(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, int]:
    """Assign nodes to deterministic dependency layers, tolerating cycles."""
    identifiers = [str(node["id"]) for node in nodes]
    incoming = {identifier: 0 for identifier in identifiers}
    outgoing: dict[str, list[str]] = {identifier: [] for identifier in identifiers}
    for edge in edges:
        source, target = str(edge.get("source", "")), str(edge.get("target", ""))
        if source in outgoing and target in incoming:
            outgoing[source].append(target)
            incoming[target] += 1
    queue = sorted(identifier for identifier in identifiers if incoming[identifier] == 0)
    layers = {identifier: 0 for identifier in identifiers}
    visited: set[str] = set()
    while queue:
        source = queue.pop(0)
        visited.add(source)
        for target in sorted(outgoing[source]):
            layers[target] = max(layers[target], layers[source] + 1)
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
        queue.sort()
    for identifier in identifiers:
        if identifier not in visited:
            layers[identifier] = 0
    return layers


def calculate_nodes(raw_nodes: list[dict[str, Any]], edges: list[dict[str, Any]], *, grid: float = 20, margin: float = 40, horizontal_gap: float = 100, vertical_gap: float = 60) -> list[Rect]:
    """Calculate node rectangles, preserving complete user-supplied positions."""
    prepared = [(node, *node_size(node, grid)) for node in raw_nodes]
    if all("x" in node and "y" in node for node, _, _ in prepared):
        return [Rect(str(node["id"]), snap(float(node["x"]), grid), snap(float(node["y"]), grid), width, height) for node, width, height in prepared]

    layers = dependency_layers(raw_nodes, edges)
    grouped: dict[int, list[tuple[dict[str, Any], float, float]]] = {}
    for item in prepared:
        grouped.setdefault(layers[str(item[0]["id"])], []).append(item)
    layer_widths = {layer: max(width for _, width, _ in items) for layer, items in grouped.items()}
    x_by_layer: dict[int, float] = {}
    cursor = margin
    for layer in sorted(grouped):
        x_by_layer[layer] = cursor
        cursor += layer_widths[layer] + horizontal_gap

    result: list[Rect] = []
    for layer in sorted(grouped):
        cursor_y = margin
        for node, width, height in sorted(grouped[layer], key=lambda item: str(item[0]["id"])):
            result.append(Rect(str(node["id"]), snap(x_by_layer[layer], grid), snap(cursor_y, grid), width, height))
            cursor_y += height + vertical_gap
    return result


def segment_hits_rect(start: Point, end: Point, rect: Rect) -> bool:
    """Return whether an orthogonal segment enters a rectangle interior."""
    if start.x == end.x:
        if not rect.x < start.x < rect.right:
            return False
        low, high = sorted((start.y, end.y))
        return low < rect.bottom and high > rect.y
    if start.y == end.y:
        if not rect.y < start.y < rect.bottom:
            return False
        low, high = sorted((start.x, end.x))
        return low < rect.right and high > rect.x
    raise ValueError("routes must use orthogonal segments")


def segment_clear(start: Point, end: Point, obstacles: Iterable[Rect]) -> bool:
    """Return whether an orthogonal segment avoids all obstacle interiors."""
    return not any(segment_hits_rect(start, end, obstacle) for obstacle in obstacles)


def anchor(rect: Rect, toward: Point) -> Point:
    """Choose the side anchor facing a target point."""
    delta_x, delta_y = toward.x - rect.center.x, toward.y - rect.center.y
    if abs(delta_x) * rect.height >= abs(delta_y) * rect.width:
        return Point(rect.right if delta_x >= 0 else rect.x, rect.center.y)
    return Point(rect.center.x, rect.bottom if delta_y >= 0 else rect.y)


def simplify(points: list[Point]) -> list[Point]:
    """Remove duplicate and collinear route points."""
    compact: list[Point] = []
    for point in points:
        if compact and point == compact[-1]:
            continue
        if len(compact) >= 2:
            previous, current = compact[-2], compact[-1]
            if (previous.x == current.x == point.x) or (previous.y == current.y == point.y):
                compact[-1] = point
                continue
        compact.append(point)
    return compact


def route_orthogonal(source: Rect, target: Rect, obstacles: Iterable[Rect] = (), *, gap: float = 24) -> list[Point]:
    """Route an edge between node boundaries with a visibility-grid search."""
    if source.id == target.id:
        raise ValueError("an edge cannot connect a node to itself")
    source_anchor, target_anchor = anchor(source, target.center), anchor(target, source.center)
    all_rects = [source, target, *obstacles]
    blocked = [rect.inflate(gap) if rect.id not in {source.id, target.id} else rect for rect in all_rects]
    x_values = {source_anchor.x, target_anchor.x}
    y_values = {source_anchor.y, target_anchor.y}
    for rect in all_rects:
        x_values.update((rect.x - gap, rect.x, rect.right, rect.right + gap))
        y_values.update((rect.y - gap, rect.y, rect.bottom, rect.bottom + gap))
    start, end = source_anchor, target_anchor
    candidates = {Point(x, y) for x in x_values for y in y_values}
    candidates.update((start, end))
    points = [point for point in candidates if point in {start, end} or not any(rect.contains_strict(point) for rect in blocked)]
    point_index = {point: index for index, point in enumerate(points)}
    adjacency: dict[int, list[tuple[int, float, str]]] = {index: [] for index in range(len(points))}
    by_x: dict[float, list[Point]] = {}
    by_y: dict[float, list[Point]] = {}
    for point in points:
        by_x.setdefault(point.x, []).append(point)
        by_y.setdefault(point.y, []).append(point)
    for direction, groups in (("v", by_x), ("h", by_y)):
        for group in groups.values():
            group.sort(key=lambda point: point.y if direction == "v" else point.x)
            for left, right in zip(group, group[1:]):
                if segment_clear(left, right, blocked):
                    distance = abs(left.x - right.x) + abs(left.y - right.y)
                    a, b = point_index[left], point_index[right]
                    adjacency[a].append((b, distance, direction))
                    adjacency[b].append((a, distance, direction))

    start_index, end_index = point_index[start], point_index[end]
    queue: list[tuple[float, int, str, tuple[int, ...]]] = [(0.0, start_index, "", (start_index,))]
    best: dict[tuple[int, str], float] = {(start_index, ""): 0.0}
    answer: tuple[int, ...] | None = None
    while queue:
        cost, current, previous_direction, path = heapq.heappop(queue)
        if current == end_index:
            answer = path
            break
        if cost > best.get((current, previous_direction), math.inf):
            continue
        for neighbor, distance, direction in adjacency[current]:
            next_cost = cost + distance + (8 if previous_direction and previous_direction != direction else 0)
            state = (neighbor, direction)
            if next_cost < best.get(state, math.inf):
                best[state] = next_cost
                heapq.heappush(queue, (next_cost, neighbor, direction, (*path, neighbor)))

    if answer is None:
        fallback = [start, Point(start.x, end.y), end]
        if not segment_clear(fallback[0], fallback[1], blocked) or not segment_clear(fallback[1], fallback[2], blocked):
            fallback = [start, Point(end.x, start.y), end]
        return simplify(fallback)
    return simplify([points[index] for index in answer])


def label_rect(
    points: list[Point],
    text: str,
    *,
    font_size: float = 14,
    gap: float = 10,
    obstacles: Iterable[Rect] = (),
    occupied: Iterable[Rect] = (),
) -> Rect:
    """Place an edge label beside its longest segment and outside obstacles."""
    if len(points) < 2:
        raise ValueError("a label needs an edge with at least two points")
    width, height = text_size(text, font_size)
    width, height = max(40, width + 12), max(20, height + 6)
    start, end = max(zip(points, points[1:]), key=lambda pair: math.dist(pair[0].as_list(), pair[1].as_list()))
    midpoint = Point((start.x + end.x) / 2, (start.y + end.y) / 2)
    if start.y == end.y:
        candidates = (
            Rect("label", midpoint.x - width / 2, midpoint.y - height - gap, width, height),
            Rect("label", midpoint.x - width / 2, midpoint.y + gap, width, height),
        )
    else:
        candidates = (
            Rect("label", midpoint.x + gap, midpoint.y - height / 2, width, height),
            Rect("label", midpoint.x - width - gap, midpoint.y - height / 2, width, height),
        )
    blocked = (*obstacles, *occupied)
    for candidate in candidates:
        if not any(rectangles_overlap(candidate, obstacle) for obstacle in blocked):
            return candidate
    return candidates[0]


def calculate_layout(spec: dict[str, Any]) -> dict[str, Any]:
    """Calculate nodes, routes, labels, and geometry validation issues."""
    options = spec.get("options", {})
    grid, gap = float(options.get("grid", 20)), float(options.get("gap", 24))
    nodes = calculate_nodes(spec.get("nodes", []), spec.get("edges", []), grid=grid, margin=float(options.get("margin", 40)), horizontal_gap=float(options.get("horizontalGap", 100)), vertical_gap=float(options.get("verticalGap", 60)))
    node_by_id = {node.id: node for node in nodes}
    output_edges: list[dict[str, Any]] = []
    occupied_labels: list[Rect] = []
    for raw_edge in spec.get("edges", []):
        source_id, target_id = str(raw_edge.get("source", "")), str(raw_edge.get("target", ""))
        if source_id not in node_by_id or target_id not in node_by_id:
            output_edges.append({**raw_edge, "points": [], "error": "source or target node is missing"})
            continue
        source, target = node_by_id[source_id], node_by_id[target_id]
        points = route_orthogonal(source, target, [node for node in nodes if node.id not in {source_id, target_id}], gap=gap)
        result: dict[str, Any] = {**raw_edge, "points": [point.as_list() for point in points], "sourceAnchor": points[0].as_list(), "targetAnchor": points[-1].as_list()}
        if raw_edge.get("label"):
            label = label_rect(
                points,
                str(raw_edge["label"]),
                font_size=float(raw_edge.get("fontSize", 14)),
                obstacles=nodes,
                occupied=occupied_labels,
            )
            occupied_labels.append(label)
            result["labelRect"] = label.as_dict()
        output_edges.append(result)
    issues = validate_layout(nodes, output_edges, gap=gap)
    output_nodes: list[dict[str, Any]] = []
    raw_nodes_by_id = {str(node["id"]): node for node in spec.get("nodes", [])}
    for node in nodes:
        geometry = node.as_dict()
        text_element_id = raw_nodes_by_id[node.id].get("textElementId")
        if text_element_id:
            geometry["textElementId"] = str(text_element_id)
        output_nodes.append(geometry)
    return {"coordinateSystem": {"origin": "top-left", "unit": "px", "grid": grid}, "nodes": output_nodes, "edges": output_edges, "issues": issues}


def rectangles_overlap(left: Rect, right: Rect) -> bool:
    """Return whether two rectangles have a positive-area overlap."""
    return left.x < right.right and right.x < left.right and left.y < right.bottom and right.y < left.bottom


def validate_layout(nodes: list[Rect], edges: list[dict[str, Any]], *, gap: float = 0) -> list[str]:
    """Find overlapping nodes, missing endpoints, and routes crossing nodes."""
    issues: list[str] = []
    node_by_id = {node.id: node for node in nodes}
    for index, left in enumerate(nodes):
        for right in nodes[index + 1 :]:
            if rectangles_overlap(left.inflate(gap / 2), right.inflate(gap / 2)):
                issues.append(f"nodes overlap: {left.id} and {right.id}")
    labels: list[tuple[str, Rect]] = []
    for edge in edges:
        source_id, target_id = str(edge.get("source", "")), str(edge.get("target", ""))
        if source_id not in node_by_id or target_id not in node_by_id:
            issues.append(f"edge {edge.get('id', '<unnamed>')} has a missing endpoint")
            continue
        points = [Point(float(point[0]), float(point[1])) for point in edge.get("points", [])]
        if edge.get("labelRect"):
            label = Rect(**edge["labelRect"])
            labels.append((str(edge.get("id", "<unnamed>")), label))
            for node in nodes:
                if rectangles_overlap(label, node):
                    issues.append(f"label {edge.get('id', '<unnamed>')} overlaps node {node.id}")
        for node in nodes:
            if node.id in {source_id, target_id}:
                continue
            if any(segment_hits_rect(start, end, node) for start, end in zip(points, points[1:])):
                issues.append(f"edge {edge.get('id', '<unnamed>')} crosses node {node.id}")
    for index, (left_id, left) in enumerate(labels):
        for right_id, right in labels[index + 1 :]:
            if rectangles_overlap(left, right):
                issues.append(f"labels overlap: {left_id} and {right_id}")
    return issues


def main(argv: list[str] | None = None) -> int:
    """Load a layout specification, calculate geometry, and emit JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="format-neutral layout JSON")
    parser.add_argument("--output", type=Path, help="write calculated geometry to this JSON path")
    parser.add_argument("--strict", action="store_true", help="return non-zero when geometry issues are found")
    args = parser.parse_args(argv or sys.argv[1:])
    result = calculate_layout(json.loads(args.input.read_text(encoding="utf-8")))
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 1 if args.strict and result["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
