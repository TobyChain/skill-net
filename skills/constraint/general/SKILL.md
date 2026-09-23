---
name: general
description: Scope non-code tasks with a compact Work Contract, then persist, audit, or migrate standing instructions only on explicit request. Use for general task scoping, prompt review, or explicit requests to remember, audit, or migrate AGENTS.md, CLAUDE.md, OMP rules, or personal defaults. Skip simple one-off work.
---

# General

Resolve only ambiguities that can change the outcome, scope, authority, risk,
source of truth, or acceptance of a non-code task. Then execute the authorized
work. Do not turn clarification into a mandatory phase or persist a rule
because it helped once.

## Work Contract

A Work Contract is a decision record, not a separate deliverable unless the
user requests it. Derive it silently when possible and state it only when it
exposes a consequential assumption or decision. Capture only the outcome,
target and source of truth, scope and authority, completion evidence, and any
blocking unknown. Skip the contract for a clear, low-risk request.

Use safe reversible assumptions for non-critical gaps. Ask only when an answer
changes scope, authority, risk, source of truth, or acceptance, and begin the
actual work in the same turn once these points are sufficiently clear.

## Persistent instructions

Persistence requires explicit intent such as "remember this," "always do
this," or "update AGENTS.md." Save only the condition, behavior, boundary, and
necessary verification. Exclude secrets, volatile state, one-off details,
unverified workarounds, inferred preferences, and duplicated rules.

Before creating, auditing, or migrating persistent files, read
[platform-instructions.md](references/platform-instructions.md). Choose the
narrowest scope and keep one normative source for shared guidance. When the
user asks to persist this skill's core behavior itself, merge
[persistent-core.md](references/persistent-core.md) instead of copying this
entire skill.

## Completion

- Finish the requested work before broad verification; run one proportionate
  verification pass after the last relevant change.
- Report the result, assumptions, checks actually run, unavailable checks, and
  unresolved exceptions.
