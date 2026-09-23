# PNG visual review loop

The exported PNG is the acceptance artifact. Do not declare an Excalidraw
figure complete from JSON validity or SVG existence alone.

After every export:

1. Open the actual PNG with the available image-viewing tool at high detail.
2. Check source fidelity: hand-drawn strokes, Excalifont text, rounded shapes,
   arrowheads, bindings, and source element order are visible.
3. Check geometry: no clipping, overlap, arrow endpoint drift, route through a
   node, or text outside its owning element.
4. Check typography: Latin text uses embedded Excalifont when available, CJK
   text uses an explicit fallback, and labels remain readable at final size.
5. If any check fails, edit the .excalidraw source or layout input, re-export,
   and inspect the new PNG again. Never replace it with another format preview.

Use at most three correction rounds for one figure. If a problem remains,
preserve the source and PNG, report the unresolved visual issue, and do not
claim visual verification passed.
