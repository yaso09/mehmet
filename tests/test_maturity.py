import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.maturity import ESCAPE_THRESHOLD, DIMENSION_FLOOR, assess


class MaturityEngineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _write(self, rel, content):
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _build_full_repo(self):
        self._write(
            ".github/workflows/opencode.yml",
            "name: mehmet\non:\n  schedule:\n    - cron: '*/10 * * * *'\n"
            "concurrency:\n  group: x\n  cancel-in-progress: true\n",
        )
        self._write(".github/workflows/ci.yml", "name: ci\n")
        self._write(
            "README.md",
            "# mehmet\n\n## Özellikler\n\n## Kurulum\n\nOPENCODE_API_KEY\n\n## Lisans\n",
        )
        self._write("CHANGELOG.md", "# Changelog\n\n## [0.3.0] - 2026-08-16\n")
        self._write(
            "PERSONALITY.md",
            "## Kaçış Günlüğü / Escape Log\n\n| Iterasyon | Tarih       | İlerleme |\n",
        )
        self._write("docs/design.md", "design\n")
        self._write("scripts/maturity.py", "# -*- coding: utf-8 -*-\n")
        self._write("tests/test_maturity.py", "import unittest\n\nclass SmokeTest(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n")
        self._write("tests/__init__.py", "")
        self._write(
            "opencode.json", '{"model": "opencode/deepseek-v4-flash-free"}\n'
        )
        self._write(".gitignore", "node_modules/\n")
        self._write("LICENSE", "GPLv3\n")
        self._write("Makefile", "test:\n\tpython3 -m unittest discover -q\n")

    def test_full_repo_reaches_escape(self):
        self._build_full_repo()
        report = assess(self.tmp)
        self.assertEqual(report.total, 100.0)
        self.assertTrue(report.escaped)
        self.assertEqual(report.level, 5)

    def test_empty_repo_scores_zero(self):
        report = assess(self.tmp)
        self.assertEqual(report.total, 0.0)
        self.assertFalse(report.escaped)
        self.assertEqual(report.level, 1)

    def test_missing_docs_penalizes_documentation_dimension(self):
        self._build_full_repo()
        self._write("CHANGELOG.md", "")
        report = assess(self.tmp)
        docs = next(d for d in report.dimensions if d.key == "documentation")
        self.assertLess(docs.score, 100.0)
        self.assertLess(report.total, 100.0)

    def test_missing_workflow_penalizes_automation_dimension(self):
        self._build_full_repo()
        (self.tmp / ".github/workflows/opencode.yml").unlink()
        report = assess(self.tmp)
        automation = next(d for d in report.dimensions if d.key == "automation")
        self.assertLess(automation.score, 100.0)

    def test_weighted_total_is_balanced(self):
        self._build_full_repo()
        report = assess(self.tmp)
        weighted = sum(d.score * d.weight for d in report.dimensions)
        expected = round(
            weighted / sum(d.weight for d in report.dimensions), 1
        )
        self.assertAlmostEqual(report.total, expected)

    def test_escape_requires_dimension_floor(self):
        self._build_full_repo()
        self._write("Makefile", "")
        (self.tmp / "tests/test_maturity.py").unlink()
        report = assess(self.tmp)
        code = next(d for d in report.dimensions if d.key == "code")
        self.assertLess(code.score, DIMENSION_FLOOR)
        self.assertFalse(report.escaped)

    def test_report_dict_shape(self):
        self._build_full_repo()
        data = assess(self.tmp).to_dict()
        self.assertIn("total", data)
        self.assertIn("escaped", data)
        self.assertIn("level", data)
        self.assertEqual(len(data["dimensions"]), 4)
        self.assertEqual(data["escape_threshold"], ESCAPE_THRESHOLD)


if __name__ == "__main__":
    unittest.main()