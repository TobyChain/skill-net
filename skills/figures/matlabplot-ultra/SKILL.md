---
name: matlabplot-ultra
description: Create publication-ready numeric charts with Python Matplotlib using reusable templates, truthful transformations, and requested exports. Use for experimental results, training curves, grouped comparisons, uncertainty bands, scatter plots, or radar charts. Prefer Draw.io or Excalidraw for node-link diagrams and TikZ when LaTeX-native source is required.
---

# Matplotlib Ultra

Create a reproducible chart from supplied numeric data. This skill name is
matlabplot-ultra for compatibility with the requested taxonomy; the
implementation uses Python Matplotlib, not MATLAB. Work template-first: adapt a
validated plotting pattern instead of rebuilding publication styling from
scratch.

## Workflow

1. Confirm data source, chart purpose, chart type, units, series, uncertainty,
   final dimensions, and output formats.
2. Read references/plot-catalog.md and select the closest plot pattern from the
   data shape and comparison task. Read only that pattern's reference under
   references/plot/.
3. Copy or adapt the matching script under scripts/plot/. Change the declared
   data and labels first; retain the proven layout and style unless the request
   requires a deliberate variation. Pass --out-dir for generated files outside
   the working directory.
4. Validate that dimensions, labels, units, series, uncertainty, scales, and
   transformations match the source data. Render at final use size with tight
   bounds and publication-quality raster resolution when PNG is requested.
5. Inspect the actual rendered output for clipping, collisions, unreadable or
   missing legends, misleading scales, and incorrect annotations. Every series
   must be identifiable by a legend or direct label, and every quantitative axis
   needs enough name or unit context to interpret it. Minimal styling must not
   remove meaning. Correct and render again when needed; do not infer visual
   success from script execution alone.
6. Export only requested formats and report transformations, derived values, or
   invented teaching data explicitly.

## Plot selection

- Use paired or grouped bars for discrete method comparisons.
- Use training curves or confidence bands for ordered measurements over time,
  steps, or another continuous axis.
- Use scatter patterns for distributions, clusters, or broken-axis comparisons.
- Use radar charts only for a small, comparable set of normalized dimensions.
- Do not use this skill for architecture, flow, sequence, ER, or other
  node-and-edge diagrams.

## Invariants

- Use supplied or traceable data; never invent, smooth, normalize, or omit
  values silently.
- Label units and series, preserve meaningful uncertainty, and avoid decorative
  annotations or axis choices that change interpretation.
- Keep typography, palette, and scale treatment consistent across related
  figures. When a deliverable also contains diagrams, reuse semantic color roles
  where doing so does not distort the data. Use vector output when requested and
  300 dpi for final PNG output.
- Do not require system LaTeX for standard plot scripts.

## Example source

The bundled examples demonstrate two useful patterns: a teaching plot that
labels its values as illustrative rather than benchmark data, and a compact
multi-panel Qwen3.8-Flash-Next figure with values transcribed from Qiu et al.,
arXiv:2608.30320. Treat them as construction references, not blanket publication
gold images; verify legends, series identity, axis meaning, and units before
reusing their minimal styling.

## Output

Return the reusable plotting script or editable data source, requested exports,
checks actually run, and any unavailable rendering or visual validation.
