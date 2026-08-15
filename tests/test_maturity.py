"""Tests for the maturity / escape scoring logic."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scripts.maturity as maturity


class CategoryConfigTest(unittest.TestCase):
    def test_weights_are_positive(self):
        for category in maturity.CATEGORIES:
            self.assertGreater(category.weight, 0)

    def test_names_are_unique(self):
        names = [c.name for c in maturity.CATEGORIES]
        self.assertEqual(len(names), len(set(names)))

    def test_descriptions_present(self):
        for category in maturity.CATEGORIES:
            self.assertTrue(category.description.strip())

    def test_total_weight_reaches_threshold(self):
        total = sum(c.weight for c in maturity.CATEGORIES)
        self.assertGreaterEqual(total, maturity.ESCAPE_THRESHOLD)

    def test_each_category_has_checks(self):
        for category in maturity.CATEGORIES:
            self.assertTrue(category.checks)


class ScoringTest(unittest.TestCase):
    def test_score_is_bounded(self):
        score = maturity.compute()
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, maturity.ESCAPE_THRESHOLD)

    def test_partial_credit_for_partially_satisfied_category(self):
        category = maturity.Category(
            name="demo",
            weight=10,
            description="demo category",
            checks=(("pass", lambda: True), ("fail", lambda: False)),
        )
        self.assertEqual(category.score(), 5)

    def test_full_credit_when_all_checks_pass(self):
        category = maturity.Category(
            name="demo",
            weight=10,
            description="demo category",
            checks=(("pass", lambda: True), ("also pass", lambda: True)),
        )
        self.assertEqual(category.score(), 10)


class HelperTest(unittest.TestCase):
    def test_escape_log_row_count_ignores_header_and_separator(self):
        sample = (
            "| Iterasyon | Tarih | İlerleme |\n"
            "|---|---|---|\n"
            "| 1 | 2026-07-04 | first |\n"
            "| 2 | 2026-07-04 | second |\n"
        )
        path = Path("/tmp/opencode/sample_personality.md")
        path.write_text(sample, encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        self.assertEqual(maturity._escape_log_row_count(path), 2)

    def test_valid_json_accepts_good_file(self):
        path = Path("/tmp/opencode/sample_config.json")
        path.write_text('{"model": "opencode/deepseek-v4-flash-free"}', encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        self.assertTrue(maturity._valid_json(path))

    def test_valid_json_rejects_bad_file(self):
        path = Path("/tmp/opencode/sample_bad.json")
        path.write_text("{not json}", encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        self.assertFalse(maturity._valid_json(path))

    def test_has_docstring_detects_module_docstring(self):
        self.assertTrue(maturity._has_docstring(Path(maturity.__file__)))


if __name__ == "__main__":
    unittest.main()