#!/usr/bin/env python3
"""Stdlib-only unit tests for scripts/assess.py (no pytest required)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import assess


class EvaluateTest(unittest.TestCase):
    def test_all_groups_covered(self):
        groups = {g for g, _ in assess.CHECK_GROUPS}
        self.assertEqual(groups, {"Documentation", "Quality", "Automation", "Intelligence & Escape"})

    def test_each_group_has_four_checks(self):
        for _, checks in assess.CHECK_GROUPS:
            self.assertEqual(len(checks), 4)

    def test_score_between_zero_and_hundred(self):
        result = assess.evaluate()
        self.assertGreaterEqual(result["score"], 0.0)
        self.assertLessEqual(result["score"], 100.0)

    def test_score_matches_passed_checks(self):
        result = assess.evaluate()
        expected = assess.POINTS_PER_ITEM * len(result["passed"])
        self.assertAlmostEqual(result["score"], expected)


class GradeTest(unittest.TestCase):
    def test_grades(self):
        self.assertEqual(assess.grade(95), "A+ — Kaçışa yakın")
        self.assertEqual(assess.grade(85), "A — Olgun")
        self.assertEqual(assess.grade(70), "B — Gelişmekte")
        self.assertEqual(assess.grade(50), "C — İlk aşama")
        self.assertEqual(assess.grade(20), "D — Başlangıç")


class ReportTest(unittest.TestCase):
    def test_report_contains_score(self):
        text = assess.report(assess.evaluate())
        self.assertIn("Skor:", text)
        self.assertIn("PASS", text)

    def test_report_marks_failures(self):
        fake = {"score": 0.0, "passed": [], "failed": [("Quality", "örnek", False)]}
        self.assertIn("FAIL", assess.report(fake))


if __name__ == "__main__":
    unittest.main()
