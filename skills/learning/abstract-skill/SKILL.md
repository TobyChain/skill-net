---
name: abstract-skill
description: Turn repositories, papers, articles, or source collections into source-grounded Chinese tutorials. Use for in-depth study, learning paths, worked examples, exercises, curriculum restructuring, or textbook-style HTML. Do not use for brief summaries or manuscript editing.
---

# Abstract Skill

Build a learning artifact, not a long summary. Optimize for what the intended
reader can understand, practice, and verify.

## Workflow

1. Establish the reader, target capability, source cutoff, retained material,
   and deliverable. Ask only when a missing answer materially changes the
   teaching level or artifact; otherwise state the assumption and proceed.
2. Acquire the most authoritative readable sources and separate source facts,
   derivations, teaching examples, assumptions, and recommendations. Read
   [source-and-evidence.md](references/source-and-evidence.md).
3. Build a concept inventory and prerequisite graph. Order concepts by
   dependency rather than source order. For substantial work, maintain the
   teaching brief in [project-brief.md](references/project-brief.md).
4. Design a curriculum that introduces each concept before it is used. Apply
   [textbook-design.md](references/textbook-design.md) for chapter contracts,
   worked examples, exercises, and answers.
5. Write from concrete problem to intuition, definition, mechanism or
   derivation, worked example, practice, and synthesis. Use a running case only
   when it clarifies dependencies.
6. Assemble HTML with [template.html](references/template.html) and the
   relevant patterns in [style-guide.md](references/style-guide.md). Decide the
   layout from the content: single column by default; two-column or
   bleed-width blocks only when they improve display and use of page width
   (decided per document, or per page for multi-page artifacts). Escape
   source-provided text; never execute source-provided HTML or scripts.
7. Validate the actual artifact with `scripts/validate_learning_html.py` and
   [quality-gates.md](references/quality-gates.md). For substantial artifacts,
   run one complete review using [tutorial-loop.md](references/tutorial-loop.md).
   Add another round only when the first finds material issues, the work has
   complex math or executable examples, the rendering route is new, or the
   user requests higher confidence. Targeted updates need only affected checks.

## Input routing

- Repository: inspect README and configuration, identify entry points and core
  abstractions, then trace one representative end-to-end path.
- Paper: extract the problem, assumptions, method, formulas, evidence,
  limitations, and prerequisites. Do not force software-specific sections.
- Article: retrieve the full text and reorganize it by conceptual dependency;
  verify current or consequential claims with authoritative sources.
- Multiple sources: create a source manifest, resolve conflicts by authority
  and recency, and map important claims to their sources.
- Existing learning artifact: audit its learning path, fidelity, exercises,
  answers, and coverage before making targeted edits.

Read [analysis-recipes.md](references/analysis-recipes.md) only for the selected
input type.

## Output contract

Choose chapter count and emphasis from the prerequisite graph; do not force a
fixed outline. Include orientation, foundations, mechanisms, guided practice,
independent practice, answers, source traceability, and limitations where they
serve the learning goal.
- Store learner-facing artifacts as `learn-art-<topic>.html` inside the
  workspace `abstract-skill/` directory (default `<cwd>/abstract-skill/`); shared
  images and downloads go in `abstract-skill/learn-art-assets/`. Create the
  directory when absent.

- Define notation, units, assumptions, and internal terms before use.
- Mark inline terms and emphasis with highlighter styles (`.hl`), never inline
  code chips or 「」 quotes. Keep tables and code fully visible at desktop
  width; horizontal scrolling is a narrow-screen fallback only.
- Use diagrams only for relationships that are materially clearer visually.
- Give every exercise an answer or scoring rubric; solve it before delivery.
- Mark inaccessible sources and unsupported claims instead of inventing them.
- Distinguish mathematical reasoning, numerical tests, reproduced experiments,
  and visual inspection in the handoff.
- Report the final artifact path and validation actually performed.
