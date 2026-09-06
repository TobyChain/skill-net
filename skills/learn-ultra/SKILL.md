---
name: learn-ultra
description: Turn a GitHub repository, paper, technical article, or a collection of internal/external source documents into a source-grounded Chinese learning artifact. Use when the user asks for in-depth study, a learning path, tutorial, textbook-style HTML, interactive study report, worked examples, exercises, or curriculum restructuring. Produces a reader-first single-file HTML with a prerequisite graph, progressive chapters, derivations, worked examples, graded exercises, answers, source traceability, and automated quality checks.
---

# learn-ultra

Build a learning artifact, not a long summary. Optimize for what a first-time reader can understand, practice, and verify.

## Required workflow

1. **Establish the reader and task.** Read supplied material first. Infer the learning goal, prior knowledge, language, source cutoff, depth, retained material, and deliverable. Ask one or two focused questions only when a missing answer materially changes the lowest explanation level or artifact. Honor a request to proceed without questions and record assumptions.
2. **Create a teaching brief.** Fill [project-brief.md](references/project-brief.md): observable outcomes, prerequisites, sources, planned emphasis, explanation/visual, practice, assessment, and status. Show the user only a concise plan; keep the detailed table as working material.
3. **Prove the output route early.** Smoke-test the requested HTML/PDF/toolchain with the actual language, one equation, one visual, and one local asset where applicable. If a route fails after one evidence-based repair, switch to a capable fallback without reducing teaching depth.
4. **Acquire sources before outlining.** Use the most authoritative readable source. For authenticated Lark/Feishu URLs, prefer lark-cli docs +fetch with an authorized identity; otherwise use an authorized browser/CDP route without printing cookies. Record source version and exact sections read.
5. **Build an evidence ledger.** Separate source facts, derived explanations, teaching examples, assumptions, and recommendations. Never promote an AI summary, search snippet, or inference into a source claim. Read [source-and-evidence.md](references/source-and-evidence.md).
6. **Build a concept inventory and prerequisite graph.** Extract the target capability, concepts, formulas, systems, decisions, misconceptions, and practical tasks. Trace only prerequisites used by a downstream argument or task. Order concepts by dependency, not source order. Read [textbook-design.md](references/textbook-design.md).
7. **Create the curriculum contract.** For every chapter specify prerequisites, measurable outcomes, core explanation, example/application, misconceptions, practice, solutions, and source anchors. Allocate emphasis by prerequisite gap and difficulty, not evenly.
8. **Write progressively.** Use concrete problem → intuition → definition → derivation/mechanism → fully worked example → closely related or partly completed problem → independent variation → synthesis. Introduce notation before use and keep a running model when it reveals connections.
9. **Design valid assessment.** Solve each exercise before accepting its wording. State inputs, assumptions, units, constraints, and evaluation criteria. Keep optional hints separate from complete solutions. Solutions must identify decisive reasoning and plausible failure modes, not only final values.
10. **Assemble the artifact.** Use [template.html](references/template.html) and the semantic components in [textbook-design.md](references/textbook-design.md). Preserve static readability without JavaScript; interactive controls need an informative default and print state.
11. **Run two complete rounds for substantial work.** Follow [tutorial-loop.md](references/tutorial-loop.md) and record each round in [round-record.md](references/round-record.md). Each round revisits requirements and sources, reviews the complete scope, builds/opens the actual artifact, solves or tests exercises, records findings, fixes them, and rechecks. Use a third round only for deep dependencies, extensive mathematics, a new rendering route, or material round-two findings. Two lint/build invocations are not two rounds.
12. **Validate and deliver.** Run scripts/validate_learning_html.py, then apply [quality-gates.md](references/quality-gates.md). Distinguish mathematical reasoning, numerical tests, controlled experiments, and visual inspection in the handoff. Verify the delivered copy opens without temporary files. Report source access limits and unresolved claims. Print DONE: followed by the absolute path on its own line.

## Input routing

- GitHub URL or local repository: inspect README/config, find entry points and core abstractions, trace a representative end-to-end path. For large repositories, use README as an index and prioritize the critical 10% of files.
- Paper/PDF: extract problem, assumptions, method, formulas, experiments, limitations, and prerequisite concepts. Do not force software-specific sections.
- Article/blog: retrieve the full article, verify key claims with authoritative sources when current information matters, then reorganize by conceptual dependency.
- Multi-source corpus: create a source manifest, deduplicate overlapping claims, resolve conflicts by authority/recency, and map each chapter to its sources.
- Existing learning HTML: audit the current learning path, source fidelity, examples, exercises, answers, and coverage before editing. Preserve unrelated user content.

## Output architecture

Do not force every topic into a fixed number of chapters. Use 6–14 chapters based on the prerequisite graph. The artifact must still contain these functional layers, distributed naturally:

- orientation: promise, audience, prerequisites, roadmap;
- foundations: definitions, notation, business/problem setting;
- system/model: architecture, mechanisms, formulas, tradeoffs;
- guided practice: worked examples with intermediate steps;
- independent practice: recall, application, transfer, synthesis;
- verification: answers, source map, limitations, coverage report.

## Non-negotiable rules

- Do not invent inaccessible source content. Mark partial access and evidence gaps.
- Do not arrange chapters in source collection order when conceptual dependency suggests another order.
- Use Mermaid only for real dependency, sequence, hierarchy, or architecture relationships.
- Define formula symbols, units, assumptions, and include an interpretation or example.
- Do not present an exercise without an answer or scoring rubric.
- Do not group unrelated questions and call them a connected exercise. Reuse one model or case and change one meaningful condition at a time.
- Do not claim a visual review from rendering alone; inspect the actual desktop, narrow-screen, and print/static result when applicable.
- Do not claim a theorem from numerical tests or a benchmark result from a teaching example.
- Escape source-provided text before inserting it into HTML. Do not preserve or execute source-provided script, event-handler, iframe, object, or untrusted raw HTML content.
- Do not claim completion when validation fails or source coverage is materially incomplete.
- Keep the main explanation in Chinese except code, commands, formulas, product names, and unavoidable technical terms.

## Resource routing

- Curriculum, chapter contract, example and exercise patterns: [textbook-design.md](references/textbook-design.md)
- Teaching brief and requirement coverage: [project-brief.md](references/project-brief.md)
- Full writing/build/review rounds: [tutorial-loop.md](references/tutorial-loop.md)
- Source acquisition, evidence labels, multi-source conflict handling: [source-and-evidence.md](references/source-and-evidence.md)
- Repository/paper/article inspection recipes: [analysis-recipes.md](references/analysis-recipes.md)
- HTML structure and components: [template.html](references/template.html), [style-guide.md](references/style-guide.md)
- Automated and manual acceptance criteria: [quality-gates.md](references/quality-gates.md)
