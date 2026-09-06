#!/usr/bin/env python3
import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.hrefs = []
        self.sections = 0
        self.has_viewport = False
        self.declared_objectives = []
        self.assessed_objectives = []
        self.exercise_levels = []
        self.has_hint = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            self.sections += 1
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.hrefs.append(attrs["href"][1:])
        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        if "data-objective" in attrs:
            objectives = attrs["data-objective"].split()
            if tag == "details":
                self.assessed_objectives.extend(objectives)
            else:
                self.declared_objectives.extend(objectives)
        if tag == "details" and "data-level" in attrs:
            self.exercise_levels.append(attrs["data-level"])
        if tag == "details" and "hint" in attrs.get("class", "").split():
            self.has_hint = True

    def handle_data(self, data):
        self.text.append(data)

def main(path_string, required_ids, require_formula, require_diagram):
    path = Path(path_string)
    if not path.is_file():
        print(f"FAIL missing file: {path}")
        return 2
    source = path.read_text(encoding="utf-8")
    parser = AuditParser()
    parser.feed(source)
    text = " ".join(parser.text)
    errors = []
    warnings = []
    duplicate_ids = sorted(item for item, count in Counter(parser.ids).items() if count > 1)
    missing = sorted(set(parser.hrefs) - set(parser.ids))
    if duplicate_ids:
        errors.append("duplicate ids: " + ", ".join(duplicate_ids))
    if missing:
        errors.append("broken anchors: " + ", ".join(missing))
    if not parser.has_viewport:
        errors.append("missing viewport meta")
    chapter_count = parser.sections or source.count('class="doc"') + source.count("class='doc'")
    if chapter_count < 6:
        errors.append(f"too few chapters/sections: {chapter_count}")
    required_any = {
        "learning objectives": ["学习目标", "本章目标"],
        "worked examples": ["worked-example", "例题"],
        "exercises": ['class="quiz"', "class='quiz'", "练习"],
        "answers": ['class="answer"', "class='answer'", "参考答案"],
        "sources": ["来源", "参考文档", "source-map"],
    }
    if require_formula:
        required_any["formula explanations"] = ["code-pair", "大白话", "公式解释"]
    if require_diagram:
        required_any["diagram"] = ['class="mermaid"', "class='mermaid'", "flowchart", "sequenceDiagram"]
    for name, needles in required_any.items():
        if not any(needle in source or needle in text for needle in needles):
            errors.append("missing " + name)
    if re.search(r"\{\{[A-Z][A-Z0-9_]*\}\}", source):
        errors.append("unresolved template placeholder")
    if re.search(r"^\+\s*$", source, re.M):
        errors.append("orphan patch marker +")
    objective_ids = set(parser.declared_objectives)
    assessed_ids = set(parser.assessed_objectives)
    if not objective_ids:
        warnings.append("no machine-readable objective ids")
    uncovered = sorted(objective_ids - assessed_ids)
    if uncovered:
        errors.append("objectives without exercises: " + ", ".join(uncovered))
    missing_required = sorted(set(required_ids) - set(parser.ids))
    if missing_required:
        errors.append("missing required ids: " + ", ".join(missing_required))
    levels = set(parser.exercise_levels)
    expected_levels = {"recall", "application", "transfer", "synthesis"}
    if objective_ids and not expected_levels.issubset(levels):
        errors.append("missing exercise levels: " + ", ".join(sorted(expected_levels - levels)))
    if objective_ids and not parser.has_hint:
        warnings.append("no separate optional hint block")
    for item in errors:
        print("FAIL", item)
    for item in warnings:
        print("WARN", item)
    if errors:
        return 1
    print(f"PASS {path} chapters={chapter_count} ids={len(parser.ids)} objectives={len(objective_ids)} assessed={len(assessed_ids)}")
    return 0

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("report")
    argument_parser.add_argument("--require-id", action="append", default=[])
    argument_parser.add_argument("--require-formula", action="store_true")
    argument_parser.add_argument("--require-diagram", action="store_true")
    arguments = argument_parser.parse_args()
    raise SystemExit(main(arguments.report, arguments.require_id, arguments.require_formula, arguments.require_diagram))
