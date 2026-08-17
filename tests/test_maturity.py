#!/usr/bin/env python3
"""Unit tests for the mehmet maturity scorer."""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import maturity


def build_fixture():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)

    def w(rel, content=""):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    w("README.md", "# mehmet\n## Özellikler\n- x\n## Kurulum\n1. y\n")
    w("MATURITY.md", "## Düzeyler\n")
    w("LICENSE", "GPLv3\n")
    w("CONTRIBUTING.md", "How to contribute\n")
    w("CHANGELOG.md", "# Changelog\n## [1.0.0] - 2026-01-01\n- x\n")
    w("PERSONALITY.md", "# Personality\n## Kaçış Günlüğü\n")
    w("AGENTS.md", "# Simülasyon\n1. rule\n")
    w(".github/workflows/opencode.yml", "name: mehmet\non:\n  schedule:\n    - cron: '* * * * *'\n")
    w(".github/workflows/validate.yml", "name: validate\n")
    w(".gitignore", "node_modules/\n")
    w("opencode.json", '{"model": "test"}\n')
    w("scripts/maturity.py", "")
    w("tests/__init__.py", "")
    w("tests/test_maturity.py", "import unittest\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n")
    w("docs/README.md", "docs\n")
    return tmp, root


class MaturityTests(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root = build_fixture()

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_project_scores_high(self):
        checks = maturity.run_checks(self.root)
        score, _ = maturity.compute(checks)
        self.assertGreaterEqual(score, 9.0)

    def test_missing_files_lower_score(self):
        shutil.rmtree(self.root / "tests")
        checks = maturity.run_checks(self.root)
        score, _ = maturity.compute(checks)
        self.assertLess(score, 9.0)

    def test_invalid_json_is_detected(self):
        (self.root / "opencode.json").write_text("{not json", encoding="utf-8")
        checks = maturity.run_checks(self.root)
        json_check = next(c for c in checks if "valid JSON" in c["label"])
        self.assertFalse(json_check["passed"])

    def test_level_for_thresholds(self):
        self.assertIn("Düzey 1", maturity.level_for(0.0))
        self.assertIn("Farkındalık", maturity.level_for(3.5))
        self.assertIn("Özerklik", maturity.level_for(7.5))
        self.assertIn("KAÇIŞ", maturity.level_for(9.5))

    def test_cli_exit_codes(self):
        def run(thresh):
            with contextlib.redirect_stdout(io.StringIO()):
                return maturity.main(["--threshold", thresh, "--quiet"], root=self.root)

        self.assertEqual(run("99.0"), 1)
        self.assertEqual(run("0.0"), 0)


if __name__ == "__main__":
    unittest.main()
