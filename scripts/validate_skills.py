#!/usr/bin/env python3
"""Validate Ultra skill metadata, resources, scripts, and activation fixtures."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CASES = ROOT / "tests" / "activation-cases.json"
MAX_DESCRIPTION_CHARS = 400
MAX_SKILL_LINES = 200


def fail(errors: list[str], message: str) -> None:
    """Append one validation error."""
    errors.append(message)


def frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    """Read the scalar frontmatter fields used by this repository."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, f"{path}: invalid frontmatter boundary")
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        values[key] = value.strip().strip('"').strip("'")
    return values


def validate_skill(skill: Path, errors: list[str]) -> None:
    """Validate initial-context and progressive-disclosure constraints."""
    skill_file = skill / "SKILL.md"
    values = frontmatter(skill_file, errors)
    name = values.get("name", "")
    description = values.get("description", "")
    if name != skill.name:
        fail(errors, f"{skill_file}: name must match folder {skill.name}")
    if not description or len(description) > MAX_DESCRIPTION_CHARS:
        fail(errors, f"{skill_file}: description length {len(description)} exceeds {MAX_DESCRIPTION_CHARS}")
    if "use " not in description.lower():
        fail(errors, f"{skill_file}: description must state when to use the skill")
    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > MAX_SKILL_LINES:
        fail(errors, f"{skill_file}: {line_count} lines exceeds the {MAX_SKILL_LINES}-line router budget")

    for markdown in sorted(skill.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            relative = target.split("#", 1)[0]
            if relative and not (markdown.parent / relative).exists():
                fail(errors, f"{markdown}: missing linked resource {target}")

    metadata = skill / "agents" / "openai.yaml"
    if not metadata.is_file():
        fail(errors, f"{skill}: missing agents/openai.yaml")
        return
    content = metadata.read_text(encoding="utf-8")
    for field in ("interface", "display_name", "short_description", "default_prompt", "policy", "allow_implicit_invocation"):
        pattern = rf"^{'  ' if field not in {'interface', 'policy'} else ''}{field}:"
        if len(re.findall(pattern, content, re.MULTILINE)) != 1:
            fail(errors, f"{metadata}: {field} must appear exactly once")
    short = re.search(r'^\s*short_description:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    prompt = re.search(r'^\s*default_prompt:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    short_text = short.group(1) if short else ""
    if not 25 <= len(short_text) <= 64:
        fail(errors, f"{metadata}: short_description length must be 25-64")
    if not prompt or f"${name}" not in prompt.group(1):
        fail(errors, f"{metadata}: default_prompt must mention ${name}")


def validate_scripts(errors: list[str]) -> None:
    """Parse Python and JSON assets and reject machine-specific script paths."""
    for path in sorted(SKILLS.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            fail(errors, f"{path}: {exc}")
        if re.search(r"/(?:Users|home)/[^/]+/", text):
            fail(errors, f"{path}: contains a developer-specific absolute path")
        if path.parent.name == "plot":
            if "--out-dir" not in text:
                fail(errors, f"{path}: plot scripts must accept --out-dir")
            if "from scipy" in text or "import scipy" in text:
                fail(errors, f"{path}: plot scripts must not depend on undeclared SciPy")
            if re.search(r"['\"]text\\.usetex['\"]\\s*:\\s*True", text):
                fail(errors, f"{path}: plot scripts must not require system LaTeX")

    for path in sorted(SKILLS.rglob("*.excalidraw")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"{path}: invalid JSON: {exc}")


def validate_activation_cases(skill_names: set[str], errors: list[str]) -> None:
    """Require positive and negative examples for every installed skill."""
    try:
        cases = json.loads(CASES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"{CASES}: {exc}")
        return
    if set(cases) != skill_names:
        fail(errors, f"{CASES}: skill set does not match installed skills")
    for name, examples in cases.items():
        for key in ("should_trigger", "should_not_trigger"):
            prompts = examples.get(key, [])
            if len(prompts) < 3 or any(not isinstance(item, str) or not item.strip() for item in prompts):
                fail(errors, f"{CASES}: {name}.{key} needs at least three non-empty prompts")
        overlap = set(examples.get("should_trigger", [])) & set(examples.get("should_not_trigger", []))
        if overlap:
            fail(errors, f"{CASES}: {name} has contradictory activation examples")


def main() -> int:
    """Run all static skill checks."""
    errors: list[str] = []
    skills = sorted(path for path in SKILLS.iterdir() if (path / "SKILL.md").is_file())
    for skill in skills:
        validate_skill(skill, errors)
    validate_scripts(errors)
    validate_activation_cases({skill.name for skill in skills}, errors)
    for path in sorted(SKILLS.rglob("README.md")):
        fail(errors, f"{path}: move agent-facing content to SKILL.md or references")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"PASS skills={len(skills)} activation_fixture_sets={len(skills)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
