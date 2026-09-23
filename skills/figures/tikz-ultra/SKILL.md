---
name: tikz-ultra
description: Create, modify, compile, debug, or export TikZ/PGF/PGFPlots diagrams. Use when .tex or tikzpicture is the required source or existing TikZ code must be changed. Use drawio-ultra, excalidraw-ultra, or matlabplot-ultra for their native formats.
---

# TikZ Ultra

Create publication-ready figures as reproducible LaTeX source. Prefer semantic
structure, stable geometry, and successful compilation over decoration.

## Boundary

- Use this skill when TikZ/PGF/PGFPlots, `.tex`, `tikzpicture`, LaTeX-native
  reuse, or compilation of existing TikZ is required.
- Use `drawio-ultra`, `excalidraw-ultra`, or `matlabplot-ultra` for their native
  formats or when no TikZ/LaTeX source is required.
- If both `.tex` and PNG/SVG/PDF are requested, compile once and export from the
  verified PDF. Use both skills only for two independently editable sources.

## Resources

Read [tikz-reference.md](references/tikz-reference.md) when the task needs
syntax, library, layout, plotting, or export guidance not covered below.
Consult [tikz-cheatsheet.pdf](assets/tikz-cheatsheet.pdf) only when the Markdown
reference lacks the required primitive or a visual example is needed.

## Geometry-first workflow

1. Confirm the figure type, source/output format, final dimensions, language,
   document class, and publisher constraints.
2. Build a semantic node/edge model and use the shared geometry and routing
   contract from references/geometry-and-routing.md when the figure has
   multiple connected nodes.
   Convert its pixel rectangles to one declared TikZ unit.
3. Create named nodes from calculated centers and sizes. Connect explicit
   boundary anchors with orthogonal routes or calculated waypoints; keep labels
   outside occupied rectangles.
4. Produce a standalone .tex file unless the user asks for a fragment, then
   compile with the available engine. Fix errors before visual polishing.
5. Inspect the PDF at final use size for clipping, overlaps, label placement,
   arrowheads, line weights, and whitespace; export only from the verified PDF.

## Multimodal PNG review

After every PNG export, open the actual PNG with the available image-viewing tool
at high detail and follow references/visual-review.md. If nodes, math, labels,
routes, clipping, or whitespace are wrong, edit the .tex source, recompile or
rerender, and inspect again. Do not report visual verification from TeX parsing alone.

For the bundled examples, native LaTeX compilation remains preferred. When a TeX engine is unavailable, the source-specific fallback renderer reads named nodes and draw paths from the TikZ source; it never reuses a Draw.io or Excalidraw image.

## Invariants

- End every path with `;` and declare every non-core library.
- Use named styles and semantic nodes for repeated roles.
- Do not assume `scale` changes text or line widths.
- Distinguish coordinates from nodes and verify every edge endpoint.
- Use one geometry source of truth for node rectangles, boundary anchors, and
  route waypoints; do not hand-adjust TikZ coordinates independently from a
  Draw.io or Excalidraw version of the same figure.
- Use an appropriate Unicode-capable engine for Chinese text.
- Treat overlays and bounding-box exclusions as intentional behavior.
- Recompile when references, overlays, or externalization require another pass.

## Output

Deliver editable source, requested exports, compiler/export commands actually
run, visual inspection status, and any unavailable validation.

## Example source

The README uses a Qwen3.8-Flash-Next module diagram based on Qiu et al.,
arXiv:2608.30320, expanding GDN, QSA, Gated Residual, and host-prefetched
n-gram embedding into named modules and explicit routes.
