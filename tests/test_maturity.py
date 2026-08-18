"""Unit tests for the maturity scoring system (docs/ESCAPE.md)."""

import tempfile
import unittest
from pathlib import Path

from scripts.maturity import Check, compute, has_content


class HasContentTests(unittest.TestCase):
    def test_empty_file_is_not_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "empty.txt"
            p.write_text("", encoding="utf-8")
            self.assertFalse(has_content(p))

    def test_nonempty_file_is_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.txt"
            p.write_text("hi", encoding="utf-8")
            self.assertTrue(has_content(p))

    def test_missing_file_is_not_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(has_content(Path(tmp) / "nope.txt"))


class CheckTests(unittest.TestCase):
    def test_check_fields(self):
        c = Check("label", True, 5, 5)
        self.assertEqual(c.label, "label")
        self.assertTrue(c.passed)
        self.assertEqual(c.points, 5)
        self.assertEqual(c.earned, 5)


class ComputeTests(unittest.TestCase):
    def _make_healthy_project(self, tmp: Path) -> Path:
        for name in ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "LICENSE"]:
            (tmp / name).write_text(f"# {name}\ncontent\n", encoding="utf-8")
        (tmp / "opencode.json").write_text('{"model": "opencode/deepseek-v4-flash-free"}', encoding="utf-8")
        (tmp / ".gitignore").write_text("node_modules/\n.env\n", encoding="utf-8")
        (tmp / ".editorconfig").write_text("root = true\n", encoding="utf-8")
        (tmp / "README.md").write_text(
            "# mehmet\n\nKurulum\n\nLisans\n\nTest: python3 -m unittest discover tests\n", encoding="utf-8"
        )
        (tmp / "docs").mkdir()
        (tmp / "docs" / "ESCAPE.md").write_text("# Escape\n", encoding="utf-8")
        (tmp / "docs" / "x.md").write_text("x\n", encoding="utf-8")
        (tmp / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
        (tmp / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
        (tmp / "scripts").mkdir()
        (tmp / "scripts" / "maturity.py").write_text("def main(): pass\n", encoding="utf-8")
        (tmp / "tests").mkdir()
        (tmp / "tests" / "test_maturity.py").write_text("import unittest\n", encoding="utf-8")
        wf = (tmp / ".github" / "workflows")
        wf.mkdir(parents=True)
        (wf / "opencode.yml").write_text(
            "name: mehmet\non:\n  schedule:\n    - cron: '*/10 * * * *'\n  workflow_dispatch:\n"
            "concurrency:\n  group: x\npermissions:\n  id-token: write\n"
            "jobs:\n  comment:\n    if: contains(github.event.comment.body, '/oc')\n",
            encoding="utf-8",
        )
        (wf / "validate.yml").write_text("name: validate\non: [push]\n", encoding="utf-8")
        (tmp / ".git").mkdir()
        return tmp

    def test_healthy_project_escapes(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = compute(self._make_healthy_project(Path(tmp)))
            self.assertGreaterEqual(result["score"], result["threshold"])
            self.assertTrue(result["escaped"])
            self.assertEqual(result["max"], 100)

    def test_empty_project_does_not_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = compute(Path(tmp))
            self.assertLess(result["score"], result["threshold"])
            self.assertFalse(result["escaped"])
            self.assertGreater(len(result["failed_checks"]), 0)

    def test_breakdown_sums_to_total(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = compute(self._make_healthy_project(Path(tmp)))
            self.assertEqual(sum(b["earned"] for b in result["breakdown"]), result["score"])


if __name__ == "__main__":
    unittest.main()