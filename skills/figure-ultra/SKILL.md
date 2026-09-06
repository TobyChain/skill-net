---
name: figure-ultra
description: Create or modify diagrams and data plots with Draw.io, Excalidraw, or Matplotlib. Use for editable visual sources, whiteboard sketches, charts, or image exports. Use tikz-ultra when TikZ/PGF/.tex is required.
---

# Figure Ultra

Create a correct editable source first, validate the rendered result, and export
only the formats the user requests.

## Choose the workflow

| Required source or result | Route |
| --- | --- |
| `.tex`, `tikzpicture`, TikZ/PGF/PGFPlots, or LaTeX-native compilation | Use `tikz-ultra`, not this skill |
| `.drawio`, a structured diagram, or a generic image deliverable | Draw.io |
| `.excalidraw`, a sketch, or a whiteboard-style visual | Excalidraw |
| A chart from numeric data | Matplotlib |

When the request names a format, honor it. When it only asks for an
architecture diagram, flowchart, or paper figure, default to Draw.io. If both
TikZ source and an image are required, use `tikz-ultra` once and export from
the compiled result.

## Load only the relevant resources

### Draw.io

- Existing `.drawio` or XML details: [xml-basics.md](references/xml-basics.md)
- General flow, architecture, ER, state, or mind-map layouts:
  [diagram-generic.md](references/diagram-generic.md)
- UML sequence diagrams: [diagram-sequence.md](references/diagram-sequence.md)
- ML architecture diagrams: [diagram-ml-architecture.md](references/diagram-ml-architecture.md)
- Academic or product styling: [style-academic.md](references/style-academic.md)
  or [style-product.md](references/style-product.md)
- Style transfer: [style-migration.md](references/style-migration.md)
- Subject diagrams: read only the relevant file under `references/edu/`
- Multi-figure work: [use-cases.md](references/use-cases.md)

### Excalidraw

Read [excalidraw-basics.md](references/excalidraw-basics.md), then
[excalidraw-advanced.md](references/excalidraw-advanced.md) when a template,
icon library, or advanced diagram type is needed. Start from a matching file in
`templates/` when available. Read the schema references only for field-level
work. For icon and arrow tools, read
[icon-tools.md](references/icon-tools.md).

### Matplotlib

Read [plot-catalog.md](references/plot-catalog.md), choose one matching style,
then read only that style file under `references/plot/`. Copy the corresponding
script, replace its data, and pass `--out-dir` when the output should not go to
the current directory.

## Workflow

1. Confirm the requested source format, output formats, content, and size or
   venue constraints. Ask only when missing structure changes the result.
2. Inspect any existing source or reference visual before editing.
3. Load the smallest relevant resource set and create the editable source.
4. Validate syntax and references, then inspect the rendered result at its
   actual use size. Fix clipping, overlap, unreadable labels, and broken links.
5. Export only requested formats. Preserve the editable source when export is
   unavailable or fails.

## Invariants

- Preserve unrelated pages, elements, data, and user edits.
- Draw.io cell IDs must be unique and edge endpoints must exist. Escape XML
  special characters; keep cell values plain text unless the source already
  requires another convention.
- Excalidraw IDs must be unique. Keep text readable and avoid unnecessary
  element count.
- Data plots must use the supplied data, label units and series, and report any
  transformation or invented teaching data.
- Do not report visual inspection unless the rendered artifact was actually
  inspected.
- A failed edit must leave the original source at its original path.

## Output

Return the editable source path, requested exports, checks actually run, and
any consequential assumption or unavailable validation.
