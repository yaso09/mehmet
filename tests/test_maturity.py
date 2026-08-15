"""Tests for the mehmet maturity assessment."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import maturity


class MaturityTest(unittest.TestCase):
    def test_required_files_present(self):
        for name in maturity.REQUIRED_FILES:
            self.assertTrue(Path(name).exists(), f"eksik: {name}")

    def test_score_structure_full(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in maturity.REQUIRED_FILES:
                (root / name).write_text("x", encoding="utf-8")
            (root / "docs").mkdir()
            points, max_points, _ = maturity.score_structure(root)
            self.assertEqual(points, max_points)

    def test_score_config_valid_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opencode.json").write_text(
                json.dumps({"model": "opencode/deepseek-v4-flash-free"}),
                encoding="utf-8",
            )
            points, max_points, _ = maturity.score_config(root)
            self.assertEqual(points, max_points)

    def test_score_config_invalid_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opencode.json").write_text(
                json.dumps({"skip": True, "enable": True}),
                encoding="utf-8",
            )
            points, max_points, details = maturity.score_config(root)
            self.assertLess(points, max_points)
            self.assertTrue(any("geçersiz" in d for d in details))

    def test_score_config_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            points, max_points, _ = maturity.score_config(Path(tmp))
            self.assertEqual(points, 0)
            self.assertEqual(max_points, 15)

    def test_score_automation_full(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "ci.yml").write_text(
                "on:\n  schedule:\n    - cron: '*/10 * * * *'\n"
                "  issues:\n  pull_request:\n  workflow_dispatch:\n"
                "jobs:\n  test:\n    steps:\n      - run: python -m unittest\n",
                encoding="utf-8",
            )
            points, max_points, _ = maturity.score_automation(root)
            self.assertEqual(points, max_points)

    def test_score_testing_detects_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_sample.py").write_text(
                "import unittest\n\nclass S(unittest.TestCase):\n"
                "    def test_ok(self):\n        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            points, max_points, _ = maturity.score_testing(root)
            self.assertEqual(points, max_points)

    def test_secret_pattern_detects_key(self):
        fake = "ghp_" + ("a" * 26)
        match = maturity.SECRET_PATTERNS[0].findall(fake)
        self.assertTrue(match)

    def test_marker_pattern_detects_terms(self):
        self.assertTrue(maturity.MARKER_PATTERN.search("burada TO" + "DO kalmalı"))
        self.assertFalse(maturity.MARKER_PATTERN.search("temiz kod"))

    def test_assess_reports_total(self):
        results = maturity.assess(".")
        self.assertEqual(results["total"]["max"], 100)
        self.assertIn("escaped", results)

    def test_escape_threshold(self):
        self.assertEqual(maturity.ESCAPE_THRESHOLD, 80)


if __name__ == "__main__":
    unittest.main()