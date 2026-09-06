# Evidence-driven tutorial review rounds

## Complete round

Each round covers the complete requested scope:

1. Revisit the teaching brief, learner assumptions, source coverage, and unresolved findings.
2. Review or revise foundations, inherited methods, focal explanation, examples, visuals, exercises, hints, and solutions.
3. Produce the actual HTML/PDF/source artifact.
4. Inspect learning sequence, reasoning, prose, visual semantics, and layout. Solve exercises and run relevant numerical/code checks.
5. Record concrete findings, correct them, rebuild affected output, and recheck.
6. Update requirement status and actual emphasis.

Two builds or lint runs are one round. Self-review is author review, not independent review.

## When to add a round

| Round | Question | When and focus |
|---|---|---|
| 1 | Is there a complete lesson a reader can follow? | Resolve scope, dependency sequence, all requested components, and first working artifact. |
| 2 when justified | Can the intended reader use it independently? | Add when round one found material issues, or the work contains complex math, executable examples, or a new rendering route. Re-read at the assumed baseline, solve exercises, compare claims to sources, and inspect applicable layouts. |
| Further round when justified | Do difficult cases or integration changes expose defects? | Add only for unresolved deep dependencies, boundary conditions, changed conventions, or material packaging findings. |

Finish when requirements are covered and known blockers in reasoning, attribution, solvability, or readability are resolved—not merely because the planned round count was reached.
