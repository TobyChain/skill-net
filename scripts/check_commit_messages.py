#!/usr/bin/env python3
"""Reject AI attribution trailers in commit messages or reachable history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

TRAILER = re.compile(
    r"^(?P<key>co-authored-by|generated-by|assisted-by|"
    r"ai-generated-by|ai-assisted-by):\s*(?P<value>.+)$",
    re.IGNORECASE,
)
AI_IDENTITY = re.compile(
    r"(?:trae(?:\s*cli|code)?|codex(?:\s*(?:cli|agent|assistant))?|"
    r"(?:openai\s+)?chatgpt|claude(?:\s+(?:code|ai|assistant))?|"
    r"anthropic\s+claude|(?:github\s+)?copilot|"
    r"(?:google\s+)?gemini(?:\s+(?:cli|ai|assistant|agent))?|"
    r"cursor(?:\s+(?:ai|agent|assistant))?|devin(?:\s+(?:ai|agent|assistant))?|"
    r"ai[ -]?(?:coding\s+)?assistant|large language model|llm(?:\s+assistant)?)",
    re.IGNORECASE,
)


def ai_attribution_trailers(message: str) -> list[str]:
    """Return AI attribution trailer lines from one commit message."""
    findings = []
    for line in message.splitlines():
        match = TRAILER.match(line.strip())
        if not match:
            continue
        display_name = match.group("value").split("<", 1)[0].strip()
        if match.group("key").lower().startswith("ai-") or AI_IDENTITY.fullmatch(display_name):
            findings.append(line.strip())
    return findings


def strip_ai_attribution_trailers(message: str) -> tuple[str, list[str]]:
    """Remove AI attribution trailers while preserving all other text."""
    findings = ai_attribution_trailers(message)
    if not findings:
        return message, []
    forbidden = set(findings)
    kept = [line for line in message.splitlines(keepends=True) if line.strip() not in forbidden]
    return "".join(kept), findings


def history_messages(revision: str) -> list[tuple[str, str]]:
    """Read commit hashes and messages reachable from a revision."""
    result = subprocess.run(
        ["git", "log", "--format=%H%x00%B%x00", revision],
        check=True,
        capture_output=True,
        text=True,
    )
    fields = result.stdout.split("\0")
    entries = []
    for index in range(0, len(fields) - 1, 2):
        commit = fields[index].strip()
        message = fields[index + 1]
        if commit:
            entries.append((commit, message))
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message_files", nargs="*", type=Path)
    parser.add_argument("--history", metavar="REVISION")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="remove forbidden trailers from message files before checking",
    )
    args = parser.parse_args()

    if not args.message_files and not args.history:
        parser.error("provide a commit-message file or --history REVISION")
    if args.fix and args.history:
        parser.error("--fix applies only to commit-message files")

    violations = []
    for path in args.message_files:
        message = path.read_text(encoding="utf-8")
        if args.fix:
            message, removed = strip_ai_attribution_trailers(message)
            if removed:
                path.write_text(message, encoding="utf-8")
                print("Removed AI attribution trailer from commit message.", file=sys.stderr)
        for trailer in ai_attribution_trailers(message):
            violations.append(f"{path}: {trailer}")

    if args.history:
        for commit, message in history_messages(args.history):
            for trailer in ai_attribution_trailers(message):
                violations.append(f"{commit}: {trailer}")

    if violations:
        print("AI attribution trailers are not allowed:", file=sys.stderr)
        for violation in violations:
            print(f"  {violation}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
