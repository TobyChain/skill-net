---
name: coding
description: Scope and execute coding tasks with a compact Work Contract, one orientation pass, and proportionate validation, then self-review the diff. Use for implementing, modifying, or restructuring code whose scope, authority, or acceptance needs settling first. Skip trivial edits with an unambiguous target.
---

# Coding

Resolve only ambiguities that can change the outcome, scope, authority, risk,
source of truth, or acceptance of the coding task. Then execute the authorized
work without repeated planning, read-only, or validation loops.

## Work Contract

A Work Contract is a decision record, not a separate deliverable unless the
user requests it. Derive it silently when possible and state it only when it
exposes a consequential assumption or decision. Capture only the outcome,
target and source of truth, scope and authority, completion evidence, and any
blocking unknown. Skip the contract for a clear, low-risk change.

Use safe reversible assumptions for non-critical gaps. Ask only when an answer
changes scope, authority, risk, source of truth, or acceptance. Begin the
actual implementation in the same turn once these points are sufficiently
clear.

## Execution rules

- Use one focused orientation pass per unchanged target. Inspect only the
  context needed for the next concrete action. Do not restart planning or
  read-only inventory after progress updates, context summaries, or tool calls
  unless the target or source of truth changed, or new evidence invalidated an
  assumption.
- Validate early only when a check resolves a live uncertainty, protects an
  irreversible action, or is required before the next step. Do not run a
  baseline suite by default; use one only to reproduce a defect, establish a
  before-and-after claim, or protect risky compatibility.
- Before writing code, read [coding-work.md](references/coding-work.md) and
  apply only the constraints relevant to this task.

## Completion

- After implementation, review the changed diff once for speculative guards,
  generic wrappers, unnecessary abstractions, scattered control flow,
  undocumented public behavior, invented identifiers, and unrelated
  refactoring.
- Run one proportionate verification pass for the changed behavior after the
  last relevant change; do not rerun passing checks when their inputs have not
  changed.
- Report the result, assumptions, checks actually run, unavailable checks, and
  unresolved exceptions.
