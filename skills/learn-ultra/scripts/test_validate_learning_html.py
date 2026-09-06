#!/usr/bin/env python3
"""Regression tests for the learn-ultra HTML validator."""

from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_learning_html import main


BASE_HTML = """<!doctype html>
<html lang="zh-CN">
<head><meta name="viewport" content="width=device-width"></head>
<body>
<a href="#one">第一章</a>
<section id="one" data-objective="o1"><h2>学习目标</h2><p>来源</p></section>
<section id="two"><article class="worked-example">例题</article></section>
<section id="three"><p>练习</p><details class="hint"><summary>提示</summary></details></section>
<section id="four"><details class="quiz" data-objective="o1" data-level="recall"><div class="answer">参考答案</div></details></section>
<section id="five"><details class="quiz" data-level="application"><div class="answer">答案</div></details></section>
<section id="six"><details class="quiz" data-level="transfer"><div class="answer">答案</div></details><details class="quiz" data-level="synthesis"><div class="answer">答案</div></details></section>
</body></html>
"""


class ValidatorTests(unittest.TestCase):
    """Check conditional and structural quality gates."""

    def validate(self, source: str, *, formula: bool = False, diagram: bool = False) -> int:
        """Validate one temporary HTML fixture."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.html"
            path.write_text(source, encoding="utf-8")
            return main(str(path), [], formula, diagram)

    def test_base_artifact_does_not_require_formula_or_diagram(self) -> None:
        """Conceptual lessons may omit irrelevant formulas and diagrams."""
        self.assertEqual(self.validate(BASE_HTML), 0)

    def test_optional_formula_and_diagram_gates(self) -> None:
        """Explicit requirements should fail until corresponding content exists."""
        self.assertEqual(self.validate(BASE_HTML, formula=True), 1)
        self.assertEqual(self.validate(BASE_HTML, diagram=True), 1)
        enriched = BASE_HTML.replace("</body>", '<div class="code-pair">公式解释</div><div class="mermaid">flowchart LR</div></body>')
        self.assertEqual(self.validate(enriched, formula=True, diagram=True), 0)

    def test_broken_anchor_and_uncovered_objective_fail(self) -> None:
        """Navigation and objective coverage remain hard failures."""
        broken = BASE_HTML.replace('href="#one"', 'href="#missing"').replace('data-objective="o1" data-level="recall"', 'data-level="recall"')
        self.assertEqual(self.validate(broken), 1)


if __name__ == "__main__":
    unittest.main()
