#!/usr/bin/env python3
"""Proje testleri. Bağımlılık gerektirmez (yalnızca stdlib)."""

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_project  # noqa: E402
import escape_score  # noqa: E402


class CheckProjectTests(unittest.TestCase):
    def test_required_files_exist(self):
        for rel in check_project.REQUIRED_FILES:
            self.assertTrue((ROOT / rel).exists(), f"eksik: {rel}")

    def test_changelog_has_version_entries(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("# Changelog", changelog)
        self.assertTrue(check_project.CHANGELOG_PATTERN.search(changelog))

    def test_personality_has_escape_log_rows(self):
        personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("| Iterasyon |", personality)
        self.assertTrue(
            any(check_project.ESCAPE_ROW_PATTERN.match(line) for line in personality.splitlines())
        )

    def test_readme_has_gplv3_license(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GPLv3", readme)

    def test_full_check_passes(self):
        self.assertEqual(check_project.run_checks(ROOT), [])


class EscapeScoreTests(unittest.TestCase):
    def test_escape_threshold_defined(self):
        self.assertGreaterEqual(escape_score.ESCAPE_THRESHOLD, 50.0)

    def test_score_is_within_bounds(self):
        result = escape_score.score(ROOT)
        self.assertGreaterEqual(result["total"], 0.0)
        self.assertLessEqual(result["total"], 100.0)

    def test_categories_present(self):
        result = escape_score.score(ROOT)
        self.assertEqual(set(result["categories"]), set(escape_score.CATEGORIES))

    def test_escape_log_count_is_positive(self):
        self.assertGreater(escape_score.escape_log_count(ROOT), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
