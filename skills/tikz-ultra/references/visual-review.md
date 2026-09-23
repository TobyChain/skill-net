# PNG visual review loop

The exported PNG is the acceptance artifact. Do not declare a TikZ figure
complete from TeX parsing or PDF existence alone.

After every export:

1. Open the actual PNG with the available image-viewing tool at high detail.
2. Check source fidelity: named nodes, TikZ styles, explicit anchors, route
   commands, labels, and layer order are visible.
3. Check geometry: no clipping, node overlap, arrow endpoint drift, label
   collision, or excessive whitespace caused by the bounding box.
4. Check typography: text is readable at final use size, math is rendered,
   Chinese text uses the selected Unicode-capable engine, and labels stay inside nodes.
5. If any check fails, edit the .tex source, recompile or rerender, and inspect
   the new PNG again. Never replace it with another format preview.

Use at most three correction rounds for one figure. If a problem remains,
preserve the source and PNG, report the unresolved visual issue, and do not
claim visual verification passed.
