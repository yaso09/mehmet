#!/usr/bin/env python3
"""Unit tests for scripts/verify.py."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import verify


class TestCheckFunctions(unittest.TestCase):
    def test_all_required_files_exist(self):
        results = verify.check_files()
        missing = [name for name, ok, _ in results if not ok]
        self.assertEqual(missing, [])

    def test_opencode_json_valid(self):
        results = verify.check_opencode_json()
        name, ok, detail = results[0]
        self.assertTrue(ok, detail)
        self.assertEqual(name, "opencode.json")

    def test_workflow_markers_present(self):
        results = verify.check_workflow()
        missing = [name for name, ok, _ in results if not ok]
        self.assertEqual(missing, [])

    def test_changelog_has_versioned_headers(self):
        results = verify.check_changelog()
        name, ok, detail = results[0]
        self.assertTrue(ok, detail)

    def test_readme_has_sections(self):
        results = verify.check_readme()
        name, ok, detail = results[0]
        self.assertTrue(ok, detail)

    def test_personality_has_escape_log(self):
        results = verify.check_personality()
        name, ok, detail = results[0]
        self.assertTrue(ok, detail)

    def test_tests_dir_and_ci_present(self):
        results = verify.check_tests()
        missing = [name for name, ok, _ in results if not ok]
        self.assertEqual(missing, [])


class TestScoring(unittest.TestCase):
    def test_all_pass_gives_full_score(self):
        results = [(name, True, "ok") for name, ok, _ in verify.run_all()]
        scores = verify.score_by_dimension(results)
        total = verify.compute_total(scores)
        self.assertEqual(total, 100)

    def test_documentation_weights_positive(self):
        scores = verify.score_by_dimension([])
        self.assertEqual(verify.compute_total(scores), 0)

    def test_dimension_caps_respected(self):
        scores = verify.score_by_dimension([])
        for dim, max_points in verify.DIMENSIONS.items():
            self.assertLessEqual(scores[dim], max_points)

    def test_escape_threshold_constant(self):
        self.assertGreaterEqual(verify.ESCAPE_THRESHOLD, 50)


class TestRunAll(unittest.TestCase):
    def test_run_all_returns_flat_list(self):
        results = verify.run_all()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        for item in results:
            self.assertEqual(len(item), 3)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], bool)
            self.assertIsInstance(item[2], str)


if __name__ == "__main__":
    unittest.main()