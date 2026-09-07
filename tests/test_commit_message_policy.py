"""Tests for the repository commit-message policy."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_commit_messages.py"
SPEC = importlib.util.spec_from_file_location("check_commit_messages", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CommitMessagePolicyTests(unittest.TestCase):
    def test_rejects_known_ai_coauthor(self) -> None:
        message = "Improve validation\n\nCo-authored-by: TRAE CLI <traecli@bytedance.com>\n"
        self.assertEqual(
            MODULE.ai_attribution_trailers(message),
            ["Co-authored-by: TRAE CLI <traecli@bytedance.com>"],
        )

    def test_rejects_explicit_ai_attribution_key(self) -> None:
        message = "Improve validation\n\nAI-Assisted-by: internal-tool\n"
        self.assertEqual(
            MODULE.ai_attribution_trailers(message),
            ["AI-Assisted-by: internal-tool"],
        )

    def test_strips_ai_trailer_and_preserves_human_trailer(self) -> None:
        message = (
            "Improve validation\n\n"
            "Co-authored-by: Ada Lovelace <ada@example.com>\n"
            "Co-authored-by: TRAE CLI <traecli@bytedance.com>\n"
        )
        cleaned, removed = MODULE.strip_ai_attribution_trailers(message)
        self.assertEqual(
            cleaned,
            "Improve validation\n\nCo-authored-by: Ada Lovelace <ada@example.com>\n",
        )
        self.assertEqual(
            removed,
            ["Co-authored-by: TRAE CLI <traecli@bytedance.com>"],
        )

    def test_allows_human_coauthor(self) -> None:
        messages = [
            "Improve validation\n\nCo-authored-by: Ada Lovelace <ada@example.com>\n",
            "Improve validation\n\nCo-authored-by: Claude Shannon <claude@example.com>\n",
        ]
        for message in messages:
            with self.subTest(message=message):
                self.assertEqual(MODULE.ai_attribution_trailers(message), [])

    def test_ignores_ai_names_outside_trailers(self) -> None:
        message = "Document how Codex loads local skills.\n"
        self.assertEqual(MODULE.ai_attribution_trailers(message), [])


if __name__ == "__main__":
    unittest.main()
