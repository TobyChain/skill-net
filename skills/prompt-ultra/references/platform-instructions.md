# Native persistent instruction files

Use this reference when `prompt-ultra` creates, audits, or migrates standing instructions. Verify current local configuration when environment variables or named profiles can relocate a user directory.

## Selection rules

1. Use the target harness's native file for harness-specific behavior.
2. Use the narrowest scope that covers the intended work.
3. Prefer one shared normative source for cross-harness project guidance.
4. Inspect the active chain once for the selected scope before editing; repeat only if the target path changes or evidence of shadowing appears.
5. Use a documented reload or one new session after changing startup-loaded instructions when available. If unavailable, complete the file edit and report the runtime check as skipped.
6. Use a hook, permission, managed policy, or CI when behavior must be enforced rather than requested.

## Codex

### Native locations and discovery

- User scope: `${CODEX_HOME:-~/.codex}/AGENTS.override.md` when non-empty; otherwise `${CODEX_HOME:-~/.codex}/AGENTS.md`. Codex loads only one file at this level.
- Project scope: starting at the project root, Codex walks toward the current working directory. At each directory it checks `AGENTS.override.md`, then `AGENTS.md`, then configured fallback names, and includes at most one file per directory.
- Files closer to the current working directory appear later and therefore take precedence over broader guidance.
- Empty files are ignored. The combined project instruction limit is controlled by `project_doc_max_bytes`, 32 KiB by default.
- Codex rebuilds the chain at the start of each run or TUI session.

### Authoring guidance

- Put personal cross-project preferences in the Codex home file.
- Put shared repository conventions in the root `AGENTS.md`.
- Put package- or service-specific rules in a nested `AGENTS.md` or `AGENTS.override.md`.
- Use an override only when replacement at that level is intentional; do not use it as a casual append file.
- Codex has no documented project-local append file equivalent to `CLAUDE.local.md`. A gitignored `AGENTS.override.md` replaces the same directory's `AGENTS.md`; use it only when replacement is intended and the shared rules are preserved deliberately. Otherwise keep the preference session-local or choose a narrower supported scope.
- Verify with a new Codex run that asks which instruction files are active, or inspect enabled session/TUI logs.

Official source: `https://learn.chatgpt.com/docs/agent-configuration/agents-md.md`, mirrored in the current Codex manual under “Custom instructions with AGENTS.md.”

## Claude Code

### Native locations and discovery

- Managed policy: platform-specific organization path, such as `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS or `/etc/claude-code/CLAUDE.md` on Linux/WSL.
- User scope: `~/.claude/CLAUDE.md`.
- Shared project scope: `./CLAUDE.md` or `./.claude/CLAUDE.md`.
- Private project scope: `./CLAUDE.local.md`; normally add it to `.gitignore`.
- Claude loads `CLAUDE.md` and `CLAUDE.local.md` from the current working directory and ancestors at launch, ordered broadest to closest. A local file follows the shared file at the same level. Nested files load when Claude accesses their subtree.
- `.claude/rules/**/*.md` supports modular rules; `paths` frontmatter limits a rule to matching files.

### Shared source and imports

- Claude Code does not natively read standalone `AGENTS.md`. To share a project source with Codex, create a minimal `CLAUDE.md` containing `@AGENTS.md`, followed only by Claude-specific additions.
- Relative imports resolve from the importing file. Imports recurse through at most four hops. External project imports can require approval.
- Imports organize content but do not reduce startup context because imported content is expanded.
- Prefer imports over symlinks for portability. Symlink behavior is restricted in some Claude desktop/Cowork contexts.

### Authoring guidance

- Target fewer than 200 lines in an always-loaded CLAUDE.md. Use path-scoped rules or skills for detail.
- Store stable instructions in CLAUDE.md. Store observations and learned project facts in auto memory; do not confuse memory with policy.
- Verify loaded memory files with `/context` and edit locations with `/memory`.

Official source: `https://code.claude.com/docs/en/memory`.

## Oh My Pi (OMP)

### Native locations and discovery

- User context: `<active-agent-dir>/AGENTS.md`, normally `~/.omp/agent/AGENTS.md`; named profiles normally use `~/.omp/profiles/<name>/agent/AGENTS.md`. `PI_CODING_AGENT_DIR` can relocate the default active agent directory.
- Do not infer native loading from a file merely existing at `~/.omp/AGENTS.md`. The current native user location is the active agent directory above; verify any legacy or launcher-specific file through the active session context before editing or migrating it.
- Native project context: `<nearest-non-empty-ancestor>/.omp/AGENTS.md`. OMP stops at the nearest non-empty `.omp/` directory; if that directory lacks `AGENTS.md`, it does not continue to a farther `.omp/` directory.
- Sticky hard guidance: `<active-agent-dir>/RULES.md` or the selected project `.omp/RULES.md`. Keep it short; OMP reattaches it near current turns. User and project sticky candidates can shadow by rule name, so inspect the actual active result.
- OMP also discovers standalone project `AGENTS.md` and `CLAUDE.md` while walking ancestors. It reads `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` as lower-priority user sources.
- Only one user context file survives provider deduplication. Native OMP user context has the highest priority and shadows other user instruction files.
- At the same project depth, higher provider priority wins. Across directory depths, multiple context files can survive.
- OMP expands supported `@path` imports relative to the importing file, with cycle protection and a five-hop limit.

### Authoring guidance

- Prefer native `.omp/AGENTS.md` for OMP-specific project behavior.
- Prefer standalone root `AGENTS.md` when the same project rules should serve Codex and OMP. Do not add a native `.omp/AGENTS.md` with duplicate content; it can shadow the portable source.
- For a private OMP project overlay, use a gitignored `.omp/AGENTS.md` that imports `@../AGENTS.md` before local additions when the root source must remain active. Confirm that this `.omp/` directory is the nearest non-empty native directory.
- Use `.omp/RULES.md` only for a few requirements that must remain prominent during long sessions.
- Verify with `/extensions`, `/status`, or the active session context when available.

Official sources: `https://omp.sh/docs/context-files` and the current `packages/coding-agent/src/discovery/builtin.ts`.

## Portable project layout

Use this layout when one repository must work across Codex, Claude Code, and OMP without duplicating shared instructions:

```text
project/
  AGENTS.md          # shared normative source for Codex and OMP
  CLAUDE.md          # contains @AGENTS.md plus Claude-only additions
  .claude/rules/     # optional Claude path-scoped rules
  .omp/              # add only for OMP-specific config or rules
```

Do not add `.omp/AGENTS.md` merely to copy the root `AGENTS.md`. Do not create `.codex/AGENTS.md` inside a project as a Codex project instruction file; Codex project guidance uses standalone files along the project path.

## Migration procedure

1. Inspect the active instruction chain once for the selected scope and identify only rules that overlap, conflict, or can be shadowed.
2. Put shared project policy in root `AGENTS.md`. Make `CLAUDE.md` import `@AGENTS.md` and retain only Claude-specific additions. Keep OMP-specific overrides in `.omp/AGENTS.md` and only a few sticky requirements in `.omp/RULES.md`.
3. Preserve user-level native files separately because harnesses use different roots and precedence. Reconcile shared meaning without assuming identical import or symlink behavior.
4. Verify discovery once when available before removing or deprecating a legacy source. If removal is not requested, an unavailable fresh-session check does not block completing the migration edits.
