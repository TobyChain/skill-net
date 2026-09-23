---
name: prompt-ultra
description: Scope complex or consequential tasks only enough to unblock execution, then carry out the authorized work without repeated planning, read-only, or validation loops. Use for task scope, acceptance, authority, prompt review, or explicit requests to remember, audit, or migrate AGENTS.md, CLAUDE.md, OMP rules, or personal defaults. Skip simple one-off work.
---

# Prompt Ultra

Resolve only ambiguities that can change the outcome, scope, authority, risk,
source of truth, or acceptance. Then execute the authorized work. Use a compact
Work Contract or durable Persistent Work Instructions when needed; do not turn
either artifact into a mandatory phase or persist a rule because it helped once.

## Execute

A Work Contract is a decision record, not a separate deliverable unless the
user requests it. Derive it silently when possible and state it only when it
exposes a consequential assumption or decision. Capture only the outcome,
target and source of truth, scope and authority, completion evidence, and any
blocking unknown. Skip the contract for a clear, low-risk request.

Use safe reversible assumptions for non-critical gaps. Ask only when an answer
changes scope, authority, risk, source of truth, or acceptance. Keep the
contract proportional and begin the actual work in the same turn once these
points are sufficiently clear.

Use one focused orientation pass per unchanged target. Inspect only the context
needed for the next concrete action. Do not restart planning or read-only
inventory after progress updates, context summaries, or tool calls unless the
target or source of truth changed, or new evidence invalidated an assumption.

During implementation, validate early only when a check resolves a live
uncertainty, protects an irreversible action, or is required before the next
step. Do not run a baseline suite by default; use one only to reproduce a
defect, establish a before-and-after claim, or protect risky compatibility.
Otherwise make a meaningful change first and validate near handoff. A failed
check calls for a targeted fix and rerun, not a restart of the task.

For coding work, read [coding-work.md](references/coding-work.md) and apply only
the relevant constraints.

## Persistent instructions

Persistence requires explicit intent such as “remember this,” “always do
this,” or “update AGENTS.md.” Save only the condition, behavior, boundary, and
necessary verification. Exclude secrets, volatile state, one-off details,
unverified workarounds, inferred preferences, and duplicated rules.

Before creating, auditing, or migrating persistent files, read
[platform-instructions.md](references/platform-instructions.md). Choose the
narrowest scope and keep one normative source for shared guidance. When the
user asks to persist Prompt Ultra itself, merge
[persistent-core.md](references/persistent-core.md) instead of copying this
entire skill.

## Completion

- Finish the requested implementation before broad verification. Run one
  proportionate verification pass after the last relevant change; do not rerun
  passing checks when their inputs have not changed.
- Expand checks only after a relevant failure, for elevated impact, or when the
  user or repository explicitly requires them.
- Report the result, assumptions, checks actually run, unavailable checks, and
  unresolved exceptions. Treat Markdown as guidance, not a security boundary.
