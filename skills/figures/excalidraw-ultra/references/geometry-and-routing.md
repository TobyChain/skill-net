# Geometry and routing contract

Use one format-neutral geometry pass before writing Draw.io XML, Excalidraw
JSON, or TikZ coordinates. The solver is the script
scripts/layout_geometry.py. The result uses a top-left
origin, pixel units, and absolute points.

## Layout input

Keep the semantic model small. Nodes need an id and label; edges need an id,
source, and target. If the format stores text separately, add its
textElementId. Supply x, y, width, and height only when a layout decision is
intentional. Otherwise the solver assigns dependency layers and sizes boxes
from the label, font, padding, and grid.

Example input:

    {
      "nodes": [
        {"id": "input", "label": "输入", "x": 40, "y": 100, "width": 120, "height": 60},
        {"id": "service", "label": "服务", "x": 280, "y": 100, "width": 160, "height": 80}
      ],
      "edges": [
        {"id": "input-to-service", "source": "input", "target": "service", "label": "请求"}
      ],
      "options": {"grid": 20, "gap": 24}
    }

Run:

    python scripts/layout_geometry.py layout.json \
      --output layout.result.json --strict

Strict mode reports overlap, missing endpoint, route-through-node, and label
collision issues through a non-zero exit status. Fix the input or routing
decision before writing the final artifact. Do not repair coordinates by eye
after the solver has produced a route.

## Shared geometry rules

- Treat every node and label as an occupied rectangle, not just a center point.
- Treat separately stored node text as part of the node: center it after the
  node rectangle changes, and include its size when a manual size is supplied.
- Snap nodes to one grid. Use the same grid when converting to Draw.io or
  scaling the pixel coordinates into TikZ units.
- Attach an edge to the source and target boundary. Never aim at a node center
  and expect the renderer to find the correct side.
- Use orthogonal routes for flow and architecture diagrams. The solver adds a
  clearance gap around unrelated nodes and minimizes length plus unnecessary
  bends.
- Keep labels beside the longest route segment. Try both sides of the segment
  and reject positions that overlap nodes or another label.
- Treat a route with no endpoint or an unresolved collision as incomplete, not
  as a visual detail to ignore.

## Format adapters

For an existing source, include the source element IDs in the layout spec and
apply the result:

    python scripts/apply_layout.py diagram.excalidraw \
      layout.result.json
    python scripts/apply_layout.py diagram.drawio \
      layout.result.json --output diagram.routed.drawio

The Excalidraw adapter writes relative points, startBinding, endBinding, and
node boundElements. The Draw.io adapter writes entryX/entryY, exitX/exitY,
orthogonal edge style, and intermediate mxPoint waypoints. Both edit through a
same-directory .edit file and leave the original source unchanged when parsing
or application fails.

## TikZ conversion

TikZ does not need a JSON write-back adapter. Use the result as the geometry
source of truth:

1. Convert pixels to one declared unit, for example 1 cm = 40 px.
2. Create named nodes with the calculated rectangle centers and sizes.
3. Map each first and last route point to an explicit node anchor.
4. Emit intermediate route points with -| / |- or explicit coordinates.
5. Place edge labels at the calculated label rectangle, or use a nearby
   position only when it does not cover the path or another label.

Do not use a second hand-written layout algorithm in TikZ. If the figure is
edited, rerun the geometry pass and update the named-node coordinates together.
