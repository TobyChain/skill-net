# ultra-skills

Focused Agent Skills for reusable work that benefits from domain guidance,
bundled references, or deterministic tools. Each `SKILL.md` is a small router;
detailed material is loaded only when the selected workflow needs it.

## Skills

| Skill | Use when | Do not use when |
| --- | --- | --- |
| [`prompt-ultra`](skills/prompt-ultra) | A task needs a Work Contract, authority or acceptance boundaries, or explicitly persistent instructions | The request is simple and one-off |
| [`learn-ultra`](skills/learn-ultra) | Sources must become a tutorial, learning path, examples, exercises, or textbook-style HTML | The user wants a brief summary or manuscript edit |
| [`paper-ultra`](skills/paper-ultra) | An academic manuscript needs rewriting, translation, review, rebuttal, or contribution auditing | The goal is to learn the paper as a tutorial |
| [`figure-ultra`](skills/figure-ultra) | The deliverable is Draw.io, Excalidraw, a data plot, or a generic exported visual | TikZ or LaTeX source is required |
| [`tikz-ultra`](skills/tikz-ultra) | The required source is TikZ, PGF, PGFPlots, `.tex`, or `tikzpicture` | Draw.io, Excalidraw, Matplotlib, or only a generic image is required |

## Install

Clone the repository, then copy the required skill folders into the native
skill directory for your agent. For Codex repository scope:

```bash
mkdir -p .agents/skills
cp -R /path/to/ultra-skills/skills/figure-ultra .agents/skills/
```

For Codex user scope, use `~/.agents/skills/`. Codex also follows symlinked
skill folders, which is useful while developing this repository. Other agents
may use different native paths; verify their current documentation before
installing.

Install only the skills you expect to use. Every installed skill contributes
its name and description to the initial skill list.

## Optional dependencies

- Draw.io export: a local `drawio` CLI.
- Data plots: Python 3.9+, Matplotlib, and NumPy.
- TikZ compilation: a LaTeX distribution and the compiler required by the
  target document.
- Learn Ultra HTML: core content remains readable without JavaScript; Mermaid,
  syntax highlighting, and web fonts use CDN assets when available.

## Validate

```bash
./scripts/install-hooks.sh
./scripts/validate.sh
```

The validation checks skill metadata and description budgets, resource links,
positive and negative activation-fixture coverage, Python syntax, Excalidraw JSON,
portable script paths, and deterministic editor rollback behavior. Matplotlib
rendering still requires the optional plotting dependencies. The repository's
`commit-msg` hook removes AI attribution trailers before a commit is written,
and validation rejects any such trailer found in reachable history.

## Authoring principles

- Keep descriptions concise and state both trigger and exclusion boundaries.
- Keep `SKILL.md` focused on routing, decisions, inputs, outputs, and invariants.
- Put detailed policies and examples in `references/`, reusable output material
  in `assets/` or `templates/`, and deterministic processing in `scripts/`.
- Add a script only when instructions and existing tools are insufficient.
- Preserve user files on failure and report validation that was actually run.
- Put durable repository-wide guidance in `AGENTS.md` only when it applies to
  most tasks; use skills or scoped files for conditional workflows.

## Sources

- `figure-ultra` incorporates patterns from Snailclimb/AIGuide,
  github/awesome-copilot, Trae1ounG/paper-plot-skills, and earlier local diagram
  skills.
- `paper-ultra` incorporates the reader-first writing and evidence-boundary
  practices from ysyecust/write-reader-first-papers.
