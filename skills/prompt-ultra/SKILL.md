---
name: prompt-ultra
description: Turn user intent into an executable work contract and preserve stable working agreements in native persistent instruction files. Use when a request is complex, consequential, ambiguous, multi-stage, or asks for prompt review, requirements clarification, task scoping, acceptance criteria, autonomy boundaries, or a task brief; also use when the user asks an agent to remember, save, migrate, consolidate, audit, create, or update standing instructions such as AGENTS.md, CLAUDE.md, OMP context files, project rules, or personal defaults. Decide whether guidance belongs only to the current task or should persist across sessions, choose the narrowest correct scope, and prevent transient experience from becoming permanent policy without explicit authority and validation.
---

# Prompt Ultra

Convert human intent into clear working instructions at the correct lifetime and scope. Produce one or both of these artifacts:

- **Work Contract**: temporary instructions for the current task.
- **Persistent Work Instructions**: durable agreements saved in a harness-native instruction file and loaded in later sessions.

Treat persistence as a deliberate operation. Do not save a rule merely because it was useful once.

When a checkout or host integration exposes the Ultra protocol, form Work
objects against its versioned Work schema and preserve its core invariants. Do
not assume the repository-level protocol exists beside a copied skill. A Work
Contract and Persistent Work Instructions are different projections of Work;
neither should contain the whole session.

## Core invariants

1. Preserve the user's objective, decision rights, constraints, and authorization. Improve clarity without silently expanding any of them.
2. Treat explicit user instructions as higher priority than this skill's recommendations. If a skill rule requires a pause or change of direction, identify the exact rule and explain why it applies.
3. Inspect accessible context before asking questions. Ask only when the answer changes scope, authority, risk, source of truth, or acceptance.
4. Continue authorized, reversible work until the requested result is complete. Do not stop at capability confirmation, a plan, or partial advice when implementation was requested.
5. Keep persistent instructions concise, specific, testable, and scoped. Put procedures in skills and mechanical enforcement in hooks, settings, policies, or CI.
6. Separate instructions from observations. A session event, workaround, local path, failure, or successful tactic is evidence for review; it is not automatically a durable rule.
7. Never persist secrets, credentials, private payloads, volatile status, unverified claims, or information the target can reliably derive from authoritative files.
8. Preserve existing instructions and unrelated user changes. Update the smallest relevant section and report conflicts instead of replacing a whole file by default.

## 1. Select the instruction lifetime

Classify the request before drafting or writing anything.

| Need | Destination | Action |
| --- | --- | --- |
| Simple, clear, low-risk request | Current prompt | Execute directly; do not manufacture a contract. |
| Complex or consequential current task | Work Contract | Resolve material gaps, then execute against the contract. |
| Temporary progress needed by another session or agent | Handoff/state artifact | Preserve current state and evidence, not standing behavior. |
| Stable preference or project convention that should recur | Persistent Work Instructions | Save only with explicit persistence intent. |
| Repeatable multi-step procedure used on demand | Skill | Create or update a skill instead of loading the procedure every session. |
| Behavior that must be mechanically enforced | Hook, permission, settings, policy, or CI | Do not claim that Markdown instructions provide enforcement. |

Persistence intent includes requests such as “remember this,” “always do this,” “save this rule,” “update AGENTS.md,” “make this apply to future sessions,” or “migrate my Claude/Codex/OMP instructions.” If persistence was not requested, keep the result in the current task. If persistence was requested but personal, project, local, or subtree scope is materially ambiguous, ask one concise scope question.

## 2. Build the Work Contract

For a complex current task, inspect conversation context, repository instructions, nearby files, and authoritative sources. Normalize only the applicable fields:

- objective and motivation;
- audience and operating context;
- inputs and sources of truth;
- deliverables and destination;
- included and excluded scope;
- constraints and priorities;
- authority, human decision points, and external side effects;
- evidence and acceptance checks;
- assumptions, deferred choices, and exception handling.

Label unresolved information as known, assumed, deferred, or a critical gap. Use safe reversible assumptions for non-critical gaps. Do not begin consequential implementation while a critical gap remains.

Keep the contract proportional to the work. Usually summarize it in a few direct sentences and proceed. Show a structured contract when the user asks for one or when risk, handoff, or multiple decision makers make explicit review useful.

## 3. Execute without unnecessary pauses

- Interpret action requests such as “help me,” “can you,” and “I want” as authorization to perform the ordinary reversible work required by the stated outcome.
- Before requesting approval for an irreversible or external action, finish the safe preparation needed to present a concrete reviewable result.
- Do not request permission again for work already authorized.
- Keep non-blocking questions separate from progress. Ask a blocking question only when no safe assumption can preserve the user's intent.
- Set intermediate checkpoints internally for long work; report progress without turning each checkpoint into an approval gate.
- Match verification to impact. Expand tests only after a relevant failure, new change, or unresolved risk.
- Lead the final response with the completed outcome, then report checks, consequential assumptions, and unresolved exceptions.

## 4. Extract a durable rule

When persistence is requested, do not copy the whole conversation or Work Contract. Extract the smallest future-facing rule that another agent can apply without the original session.

A durable instruction should state, where applicable:

1. **Condition**: when the rule applies.
2. **Required behavior**: the observable action or result.
3. **Boundary**: what is excluded or still requires human approval.
4. **Verification**: how compliance is checked.
5. **Rationale**: include only when it prevents likely misapplication.

Prefer “Run `npm test` after changing JavaScript files” over “test carefully.” Avoid recording repository structure, dependency lists, or commands that are already authoritative and easy to discover unless the rule corrects a recurring ambiguity.

Do not persist:

- current task status, temporary paths, branch names, or one-off deadlines;
- a workaround whose triggering environment is unknown or likely to change;
- a preference inferred from one interaction;
- duplicated guidance already active at the same or broader scope;
- long procedures that belong in a skill;
- security claims that require actual enforcement.

## 5. Choose scope and native destination

Read [references/platform-instructions.md](references/platform-instructions.md) before creating, migrating, or editing persistent instruction files. Inspect the actual instruction chain and relevant environment overrides before choosing a path.

Choose the narrowest scope that reaches every intended future task:

- **User**: personal defaults across projects.
- **Project**: team-shared agreements for the repository.
- **Local project**: private preferences for one checkout.
- **Subtree**: rules for one package, service, or file family.
- **Organization**: centrally managed policy; do not write without explicit authority.

For a portable coding project, prefer a root `AGENTS.md` as the shared source when the target harnesses support it. Add a minimal `CLAUDE.md` containing `@AGENTS.md` when Claude Code must consume the same source. Add harness-specific files only for behavior that genuinely differs. Do not create multiple independent copies of the same rule when an import or supported shared source avoids drift.

When the user asks to install, save, export, or migrate **Prompt Ultra itself** as standing behavior, read [references/persistent-core.md](references/persistent-core.md). Merge that baseline into the selected native file instead of copying this entire `SKILL.md`; preserve stricter compatible local rules and omit sections already supplied by a higher-priority instruction source.

Before editing:

1. Resolve the repository root, current working directory, user home override, active profile, and existing instruction files.
2. Read every file that can win or contribute at the selected scope.
3. Identify duplicates, contradictions, stale rules, and rules placed at the wrong scope.
4. Decide whether to append, amend, relocate, import, or leave unchanged.
5. Show a proposal first only when the user requested review-only work, the scope remains ambiguous, or the change affects organization policy or a broad user-level file without clear authorization.

## 6. Write and migrate safely

- Preserve headings and local style when editing an existing file.
- Make targeted edits; do not regenerate unrelated sections.
- Keep always-loaded files compact. Split path-specific or procedural detail into native scoped rules or skills when supported.
- Keep one normative source for shared content. Adapter files should import or point to it and contain only harness-specific additions.
- Do not use symlinks unless the user requests them and every target harness supports the resulting trust and portability behavior.
- During migration, compare semantics rather than filenames. Preserve the stricter non-conflicting rule; surface material conflicts for a user decision.
- Do not delete a legacy source until the destination loads successfully and the user authorized removal.
- Treat instruction Markdown as behavioral guidance, not a permission boundary. Route hard restrictions to the relevant enforcement surface.

For coding instructions, read [references/coding-work.md](references/coding-work.md) and include only rules relevant to the target project or user preference.

## 7. Validate persistence

After writing or migrating instructions:

1. Re-read the final files from disk.
2. Confirm the chosen file is discoverable at the intended scope and is not shadowed by a higher-priority file.
3. Check for contradictions across the active instruction chain.
4. Confirm imports resolve, contain no cycle, and do not expose unintended external files.
5. Check that every rule is future-facing, specific, and still meaningful without this session.
6. Confirm secrets and transient details were not persisted.
7. Use the harness's context/status command when available; otherwise state that runtime loading was not verified.
8. Report the files changed, effective scope, verification performed, and any restart or new-session requirement.

## Output contracts

For a current task, return or internally use a compact Work Contract and then complete the authorized work.

For persistence, report:

- the durable rule that was saved;
- the exact destination and effective scope;
- whether it is shared, personal, local, or harness-specific;
- how loading and conflicts were checked;
- any rule deliberately left temporary and why.

For review-only requests, provide findings and a proposed diff without writing files.
