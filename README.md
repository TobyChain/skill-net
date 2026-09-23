# skill-net

Focused Agent Skills for reusable work that benefits from domain guidance,
bundled references, or deterministic tools. Each `SKILL.md` is a small router;
detailed material is loaded only when the selected workflow needs it.

Skills are organized by domain under `skills/<domain>/<name>`. Skills with an
`agents/openai.yaml` metadata file are authored in this repository; **Community
picks** are vendored third-party skills that the community repeatedly
recommends, stored complete with their original licenses and documentation.

## Skills

| Domain | Skill | Use when | Do not use when |
| --- | --- | --- | --- |
| constraint | [`coding`](skills/constraint/coding) | A coding task needs a Work Contract: scope, authority, or acceptance settled before implementation, then proportionate validation and a diff self-review | The edit is trivial with an unambiguous target |
| constraint | [`general`](skills/constraint/general) | A non-code task needs a Work Contract, or standing instructions (AGENTS.md, CLAUDE.md, personal defaults) must be created, audited, or migrated on explicit request | The work is a simple one-off request |
| learning | [`abstract-skill`](skills/learning/abstract-skill) | Sources must become a tutorial, learning path, examples, exercises, or textbook-style HTML | The user wants a brief summary or manuscript edit |
| writing | [`paper-writing`](skills/writing/paper-writing) | An academic manuscript needs rewriting, translation, review, rebuttal, or contribution auditing | The goal is to learn the paper as a tutorial |
| writing | [`report-writing`](skills/writing/report-writing) | A status report, analysis or review document, decision memo, or report-based bilingual synchronization needs drafting or restructuring | The deliverable is an academic manuscript or a study guide |
| figures | [`drawio-ultra`](skills/figures/drawio-ultra) | The deliverable is an editable Draw.io XML diagram | A whiteboard sketch, numeric plot, or LaTeX source is required |
| figures | [`excalidraw-ultra`](skills/figures/excalidraw-ultra) | A hand-drawn whiteboard, brainstorm, or relationship sketch is wanted | A formal Draw.io diagram, numeric plot, or LaTeX source is required |
| figures | [`matlabplot-ultra`](skills/figures/matlabplot-ultra) | Publication-ready numeric charts from experimental data | The deliverable is a node-link diagram or LaTeX-native figure |
| figures | [`tikz-ultra`](skills/figures/tikz-ultra) | The required source is TikZ, PGF, PGFPlots, `.tex`, or `tikzpicture` | Draw.io, Excalidraw, or Matplotlib is the required source |

## Community picks

Complete, unmodified copies of community-recommended skills. Install paths
point at each skill's loadable directory; the vendored copy keeps everything
(demos, assets, sub-skills, scripts) for offline use and provenance.

| Domain | Skill | Source | License | Use when |
| --- | --- | --- | --- | --- |
| design | [`huashu-design`](skills/design/huashu-design) | [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design) | MIT | Deliverable HTML-native design: product-launch animations, clickable prototypes, editable slide decks, print-grade infographics |
| design | [`taste-skill`](skills/design/taste-skill/skills) (14 sub-skills: taste, brutalist, minimalist, redesign, brandkit, …) | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT | Frontend work that must avoid generic AI slop and land a distinctive, tasteful visual identity |
| learning | [`university-skill`](skills/learning/university-skill/skills) (university-textbook, university-coursebook) | [walkinglabs/university-skill](https://github.com/walkinglabs/university-skill) | none declared | Turning any topic into a structured university lecture or textbook-style course |

No license was declared by university-skill upstream; it is vendored with full
attribution and can be removed on the author's request.

## Install

Clone the repository, then copy the required skill folders into the native
skill directory for your agent. For Codex repository scope:

```bash
mkdir -p .agents/skills
cp -R /path/to/skill-net/skills/figures/drawio-ultra .agents/skills/
```

For Codex user scope, use `~/.agents/skills/`. Codex also follows symlinked
skill folders, which is useful while developing this repository. Other agents
may use different native paths; verify their current documentation before
installing.

Install only the skills you expect to use. Every installed skill contributes
its name and description to the initial skill list. Community picks that are
collections (`taste-skill`, `university-skill`) install their sub-skills from
the nested `skills/` directory, e.g. `skills/design/taste-skill/skills/taste-skill`.

## Optional dependencies

- Draw.io export: a local `drawio` CLI.
- Data plots: Python 3.9+, Matplotlib, and NumPy.
- TikZ compilation: a LaTeX distribution and the compiler required by the
  target document.
- Abstract-skill HTML: core content remains readable without JavaScript;
  Mermaid, syntax highlighting, and web fonts use CDN assets when available.
- Community picks may declare their own dependencies; see each vendored
  `README.md`.

## Validate

```bash
./scripts/install-hooks.sh
./scripts/validate.sh
```

The validation checks skill metadata and description budgets, resource links,
positive and negative activation-fixture coverage, Python syntax, Excalidraw JSON,
portable script paths, and deterministic editor rollback behavior. Skills with
`agents/openai.yaml` must satisfy every rule; vendored community picks are only
checked for loadability. The repository's `commit-msg` hook removes AI
attribution trailers before a commit is written, and validation rejects any
such trailer found in reachable history.

## Authoring principles

- Keep descriptions concise and state both trigger and exclusion boundaries.
- Keep `SKILL.md` focused on routing, decisions, inputs, outputs, and invariants.
- Put detailed policies and examples in `references/`, reusable output material
  in `assets/` or `templates/`, and deterministic processing in `scripts/`.
- Add a script only when instructions and existing tools are insufficient.
- Preserve user files on failure and report validation that was actually run.
- Put durable repository-wide guidance in `AGENTS.md` only when it applies to
  most tasks; use skills or scoped files for conditional workflows.
- Vendor community skills complete and unmodified; record source and license
  in the Community picks table instead of editing the vendored copy.

## Sources

- `drawio-ultra`, `excalidraw-ultra`, and `matlabplot-ultra` split out of the
  earlier `figure-ultra`, which incorporated patterns from Snailclimb/AIGuide,
  github/awesome-copilot, Trae1ounG/paper-plot-skills, and earlier local
  diagram skills.
- `coding` and `general` split out of the earlier `prompt-ultra`; the
  `prompting` domain was renamed `constraint`.
- `paper-writing` and `report-writing` split out of the earlier `paper-ultra`;
  `paper-writing` incorporates the reader-first writing and evidence-boundary
  practices from ysyecust/write-reader-first-papers.
- `abstract-skill` was renamed from the earlier `learn-ultra`.
- The repository was renamed from `ultra-skills` to `skill-net`.
- Community picks: [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)
  (MIT), [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT),
  [walkinglabs/university-skill](https://github.com/walkinglabs/university-skill)
  (no license declared).
