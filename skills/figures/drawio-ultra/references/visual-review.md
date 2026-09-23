# PNG visual review loop

The exported PNG is the acceptance artifact. Do not declare a Draw.io figure
complete from XML validity or SVG existence alone.

After every export:

1. Open the actual PNG with the available image-viewing tool at high detail.
2. Check source fidelity: node text, XML styling, arrow direction, edge labels,
   and explicit mxPoint waypoints are visible.
3. Check geometry: no clipping, overlap, arrow endpoint drift, line through a
   text box, or label on top of an arrow.
4. Check typography: text is inside its source geometry, visually centered,
   readable at final use size, and not split into unnecessary fragments.
5. If any check fails, edit the .drawio source or geometry input, re-export,
   and inspect the new PNG again. Keep the loop focused on the affected route.

Use at most three correction rounds for one figure. If a problem remains,
preserve the source and PNG, report the unresolved visual issue, and do not
claim visual verification passed.
