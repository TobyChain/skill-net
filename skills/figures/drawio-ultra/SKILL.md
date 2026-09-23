---
name: drawio-ultra
description: Create and modify precise, editable Draw.io diagrams with deterministic geometry, orthogonal routes, boundary anchors, and requested exports. Use when .drawio is required or a structured architecture, flow, sequence, ER, or academic diagram needs maintainable XML. Prefer Excalidraw for whiteboard sketches, Matplotlib for numeric plots, and TikZ for LaTeX-native figures.
---

# Draw.io Ultra

Create the editable Draw.io source from a semantic node/edge model, then export
only the formats requested by the user. Prefer Draw.io when the source must stay
structured, precise, and maintainable rather than intentionally sketch-like.

## Workflow

1. Confirm diagram type, content, source/output formats, final size, and whether
   the user needs a new figure or an edit that preserves existing structure.
2. Read the relevant diagram and style references. Build a semantic model of
   nodes, edges, labels, and containers before writing XML; use meaningful,
   domain-specific IDs and preserve existing IDs during edits.
3. Run scripts/layout_geometry.py for connected diagrams. Treat nodes and
   labels as rectangles; attach edges to boundaries, route orthogonally around
   obstacles, and reject overlap or route-through-node issues.
4. Write the new .drawio source, or update an existing source with
   scripts/apply_layout.py. Add a title, legend, caption, or source citation
   only when the context or requested figure type benefits from it.
5. Render at the actual use size and run the PNG review loop. Export only the
   requested SVG, PNG, or PDF files. Preserve the editable source if export or
   validation is unavailable.

## Multimodal PNG review

After every PNG export, open the actual PNG with the available image-viewing
tool at high detail and follow references/visual-review.md. If text, geometry,
arrow endpoints, labels, or clipping are wrong, edit the source XML or layout
input, re-export, and inspect again. Text touching a node boundary, a broken or
discontinuous connector, and an arrowhead detached from its route are failures.
Do not report visual verification from XML or SVG checks alone. Stop after the
reference's correction limit and report any remaining issue instead of claiming
the review passed.

For the bundled examples, the source-specific fallback renderer reads the
.drawio XML, including explicit mxPoint waypoints, when the Draw.io CLI is
unavailable. It never consumes an Excalidraw or TikZ preview.

## Resources

- Geometry and adapters: references/geometry-and-routing.md
- XML constraints: references/xml-basics.md
- General layouts: references/diagram-generic.md
- Sequence diagrams: references/diagram-sequence.md
- ML architecture: references/diagram-ml-architecture.md
- Styles: references/style-academic.md or references/style-product.md
- Export commands: references/export-and-files.md

## Invariants

- Cell IDs are unique and meaningful, edge endpoints exist, XML is escaped,
  and values stay plain text unless rich text is explicitly required.
- Use calculated entryX, entryY, exitX, exitY, and mxPoint waypoints; do not aim
  arrows at node centers by eye.
- Keep labels outside paths and occupied rectangles. Keep repeated elements
  aligned and styled consistently; preserve unrelated pages and user edits.
  When figures belong to one deliverable, reuse semantic color roles where the
  formats allow it.
- Content must remain traceable to user input or cited source material. Do not
  invent uncertain architecture details to make a diagram look complete.
- A failed edit leaves the original source at its original path.

## Example source

The bundled Qwen3.8-Flash-Next innovation overview demonstrates a structured
academic figure with consistent visual roles, routed edges, and source
attribution based on Qiu et al., arXiv:2608.30320. Treat it as a construction
reference, not automatic proof of visual quality: inspect text fit and connector
continuity in the exported PNG before reusing its layout.

## Output

Return the editable .drawio path, requested exports, checks actually run, and
any unavailable visual or CLI validation.
