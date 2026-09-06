---
name: prompt-ultra
description: Build a scoped Work Contract for complex or consequential tasks, or save explicitly persistent agreements in native instruction files. Use for scope, acceptance, authority, prompt review, or requests to remember, audit, or migrate AGENTS.md, CLAUDE.md, OMP rules, or personal defaults. Skip simple one-off work.
---

# Prompt Ultra

Clarify human intent at the correct lifetime and scope. Produce a temporary
Work Contract, durable Persistent Work Instructions, or both when explicitly
requested. Do not persist a rule merely because it helped once.

## Choose the destination

| Need | Destination |
| --- | --- |
| Simple, clear, low-risk request | Execute from the current prompt |
| Complex or consequential current task | Work Contract |
| Temporary progress for another session | Handoff or state artifact |
| Stable agreement the user explicitly wants reused | Persistent Work Instructions |
| Repeatable procedure loaded on demand | Skill |
| Mechanically enforced behavior | Hook, permission, setting, policy, or CI |

## Work Contract

Inspect accessible context first. Normalize only fields that affect the work:

- objective, audience, inputs, and authoritative sources;
- deliverable, included and excluded scope;
- constraints, priorities, and external side effects;
- authority and human decision points;
- evidence, acceptance checks, assumptions, and exception handling.

Use safe reversible assumptions for non-critical gaps. Ask only when an answer
changes scope, authority, risk, source of truth, or acceptance. Keep the
contract proportional, then continue the authorized work without turning the
contract into another approval gate.

For coding work, read [coding-work.md](references/coding-work.md) and apply only
the relevant constraints.

## Persistent instructions

Persistence requires explicit intent such as “remember this,” “always do
this,” or “update AGENTS.md.” Extract the smallest future-facing rule another
agent can apply without this session. Include the condition, required behavior,
boundary, and verification; include rationale only when it prevents misuse.

Do not persist secrets, volatile state, one-off paths or deadlines, unverified
workarounds, inferred preferences, duplicated rules, or procedures better kept
in a skill.

Before creating, auditing, or migrating persistent files, read
[platform-instructions.md](references/platform-instructions.md). Choose the
narrowest scope, inspect the active instruction chain, preserve existing user
rules, and keep one normative source for shared guidance. When the user asks to
persist Prompt Ultra itself, merge [persistent-core.md](references/persistent-core.md)
instead of copying this entire skill.

## Completion

- For current work, complete the requested task and its proportionate checks.
- For persistence, reread the result, verify discovery and precedence in a new
  session when available, and report the exact file and effective scope.
- Treat Markdown as guidance, not a security boundary.
- Report assumptions, checks actually run, and unresolved exceptions.
