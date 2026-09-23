---
name: excalidraw-ultra
description: Create and modify editable Excalidraw diagrams with hand-drawn styling, calculated bounds, routed arrows, bindings, and requested exports. Use when .excalidraw is required or the goal is a collaborative whiteboard, brainstorm, or hand-drawn architecture, flow, relationship, or sequence diagram. Prefer Draw.io for formal diagrams, Matplotlib for numeric plots, and TikZ for LaTeX-native figures.
---

# Excalidraw Ultra

Create a readable Excalidraw source from a semantic model. Preserve the
whiteboard character while calculating geometry deterministically; hand-drawn
style is not permission for ambiguous structure or broken bindings.

## Workflow

1. Confirm diagram type, content, source/output formats, final size, and whether
   the user needs a new sketch or an edit that preserves existing elements.
2. Read references/excalidraw-basics.md. Reuse a matching template from
   templates/ when it provides the right structure; read the advanced or icon
   reference only when the task needs it.
3. Run scripts/layout_geometry.py from the geometry implementation copied into
   this skill for connected diagrams. Calculate node rectangles, boundary
   anchors, orthogonal routes, and label rectangles before writing JSON.
4. Write the new .excalidraw source, or use scripts/apply_layout.py for an
   existing source. It writes relative arrow points, startBinding, endBinding,
   boundElements, and centered independent text elements. Use semantic colors
   consistently across elements with the same role.
5. Use scripts/add-icon-to-diagram.py for library icons rather than pasting
   large icon payloads into the working context. Add a title, legend, or source
   note only when the content benefits from one.
6. Render at the actual use size and run the PNG review loop. Export only the
   requested SVG or PNG files. Preserve the editable source if export or
   validation is unavailable.

## Multimodal PNG review

After every PNG export, open the actual PNG with the available image-viewing
tool at high detail and follow references/visual-review.md. If hand-drawn style,
Excalifont, text, bindings, or geometry is wrong, edit the source JSON or layout
input, re-export, and inspect again. A visible arrowhead without its connecting
shaft, an ambiguous direction, or a detached binding is a failed render even if
the JSON is valid. Never replace an Excalidraw result with a different format
preview. Stop after the reference's correction limit and report any remaining
issue instead of claiming the review passed.

For the bundled examples, the source-specific fallback renderer reads
Excalidraw JSON elements, points, bindings, and text when CLI export is
unavailable. It never consumes a Draw.io or TikZ preview.

The fallback embeds the official Excalifont-Regular.woff2 asset when present,
uses Excalifont as the primary Latin font, and keeps a CJK system fallback
because Excalifont does not contain Chinese glyphs. The font is distributed
under OFL-1.1 from the official Excalidraw font page.

## Resources

- Basics, palette, and element rules: references/excalidraw-basics.md
- Schema: references/excalidraw-schema.md
- Element details: references/excalidraw-element-types.md
- Templates and diagram types: references/excalidraw-advanced.md
- Icon and free-arrow tools: references/icon-tools.md

## Invariants

- IDs are unique, text is readable, and nodes, labels, and routes do not overlap.
- Arrow endpoints bind to node boundaries; a connected arrow is not specified
  only by guessed center coordinates.
- Keep fontFamily 5 for text unless the source already uses another valid font.
  Use one semantic color mapping consistently rather than coloring each node
  independently. When figures belong to one deliverable, reuse those color
  roles across formats where possible.
- Preserve unrelated elements, groups, bindings, and user edits. A failed edit
  leaves the original source at its original path.

## Example source

The bundled Qwen3.8-Flash-Next innovation overview demonstrates whiteboard
character, consistent fills, compact labels, and source attribution based on
Qiu et al., arXiv:2608.30320. Treat it as a style and construction reference,
not a visual gold image: its exported PNG must still be checked for continuous
connector shafts and unambiguous direction.

## Output

Return the editable .excalidraw path, requested exports, checks actually run,
and any unavailable visual or CLI validation.
