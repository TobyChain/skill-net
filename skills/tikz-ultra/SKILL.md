---
name: tikz-ultra
description: Create, modify, compile, debug, or export TikZ/PGF/PGFPlots diagrams. Use when .tex or tikzpicture is the required source or existing TikZ code must be changed. Use figure-ultra for Draw.io, Excalidraw, Matplotlib, or generic image deliverables.
---

# TikZ Ultra

Create publication-ready figures as reproducible LaTeX source. Prefer semantic
structure, stable geometry, and successful compilation over decoration.

## Boundary

- Use this skill when TikZ/PGF/PGFPlots, `.tex`, `tikzpicture`, LaTeX-native
  reuse, or compilation of existing TikZ is required.
- Use `figure-ultra` for Draw.io, Excalidraw, Matplotlib, or a generic image
  deliverable without a LaTeX source requirement.
- If both `.tex` and PNG/SVG/PDF are requested, compile once and export from the
  verified PDF. Use both skills only for two independently editable sources.

## Resources

Read [tikz-reference.md](references/tikz-reference.md) when the task needs
syntax, library, layout, plotting, or export guidance not covered below.
Consult [tikz-cheatsheet.pdf](assets/tikz-cheatsheet.pdf) only when the Markdown
reference lacks the required primitive or a visual example is needed.

## Workflow

1. Confirm the figure type, source/output format, final dimensions, language,
   document class, and publisher constraints that affect implementation.
2. Plan named nodes, coordinates, layers, styles, and connection routing; load
   only required libraries.
3. Produce a standalone `.tex` file unless the user asks for a fragment.
4. Compile with the appropriate available engine. Fix errors before visual
   polishing; do not claim compilation when tools are unavailable.
5. Inspect the PDF at final use size for clipping, overlaps, label placement,
   arrowheads, line weights, and whitespace.
6. Export requested raster or SVG formats only from the verified PDF.

## Invariants

- End every path with `;` and declare every non-core library.
- Use named styles and semantic nodes for repeated roles.
- Do not assume `scale` changes text or line widths.
- Distinguish coordinates from nodes and verify every edge endpoint.
- Use an appropriate Unicode-capable engine for Chinese text.
- Treat overlays and bounding-box exclusions as intentional behavior.
- Recompile when references, overlays, or externalization require another pass.

## Output

Deliver editable source, requested exports, compiler/export commands actually
run, visual inspection status, and any unavailable validation.
