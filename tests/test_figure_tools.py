#!/usr/bin/env python3
"""Behavior tests for the deterministic Excalidraw editing tools."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "figures" / "excalidraw-ultra" / "scripts"


def diagram() -> dict:
    """Return a minimal valid Excalidraw document."""
    return {"type": "excalidraw", "version": 2, "source": "test", "elements": [], "appState": {}, "files": {}}


class FigureToolTests(unittest.TestCase):
    """Protect successful edits and rollback on failure."""

    def test_add_arrow_success(self) -> None:
        """A successful edit atomically replaces the original."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "diagram.excalidraw"
            path.write_text(json.dumps(diagram()), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPTS / "add-arrow.py"), str(path), "0", "0", "10", "10", "--label", "test"], check=True, capture_output=True, text=True)
            result = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(len(result["elements"]), 2)
            self.assertFalse(path.with_suffix(".excalidraw.edit").exists())

    def test_add_arrow_failure_preserves_original(self) -> None:
        """Invalid input must leave the original bytes and path untouched."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "diagram.excalidraw"
            original = "{invalid json"
            path.write_text(original, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPTS / "add-arrow.py"), str(path), "0", "0", "10", "10"], check=False, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertFalse(path.with_suffix(".excalidraw.edit").exists())

    def test_add_icon_success_and_failure(self) -> None:
        """Icon insertion succeeds for valid input and rolls back missing icons."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            library = root / "library"
            (library / "icons").mkdir(parents=True)
            icon = {"elements": [{"id": "old", "type": "rectangle", "x": 1, "y": 2, "width": 3, "height": 4, "groupIds": [], "boundElements": []}]}
            (library / "icons" / "box.json").write_text(json.dumps(icon), encoding="utf-8")

            success = root / "success.excalidraw"
            success.write_text(json.dumps(diagram()), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPTS / "add-icon-to-diagram.py"), str(success), "box", "10", "20", "--library-path", str(library), "--label", "Box"], check=True, capture_output=True, text=True)
            self.assertEqual(len(json.loads(success.read_text(encoding="utf-8"))["elements"]), 2)
            self.assertFalse(success.with_suffix(".excalidraw.edit").exists())

            failure = root / "failure.excalidraw"
            original = json.dumps(diagram())
            failure.write_text(original, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPTS / "add-icon-to-diagram.py"), str(failure), "missing", "0", "0", "--library-path", str(library)], check=False, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(failure.read_text(encoding="utf-8"), original)
            self.assertFalse(failure.with_suffix(".excalidraw.edit").exists())

            no_library = root / "no-library.excalidraw"
            no_library.write_text(original, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPTS / "add-icon-to-diagram.py"), str(no_library), "box", "0", "0"], check=False, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--library-path is required", result.stdout)
            self.assertEqual(no_library.read_text(encoding="utf-8"), original)

    def test_plot_scripts_expose_help_without_optional_dependencies(self) -> None:
        """Users can inspect every plot command before installing plotting packages."""
        for script in sorted((SCRIPTS / "plot").glob("*.py")):
            with self.subTest(script=script.name):
                result = subprocess.run([sys.executable, str(script), "--help"], check=False, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0)
                self.assertIn("--out-dir", result.stdout)


if __name__ == "__main__":
    unittest.main()
