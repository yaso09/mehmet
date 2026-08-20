import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import maturity


class TestMaturityScoring(unittest.TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(c["weight"] for c in maturity.CATEGORIES.values()), 100)

    def test_compute_scores_all_passing(self):
        results = {}
        for category, spec in maturity.CATEGORIES.items():
            results[category] = [(label, True) for label, _ in spec["checks"].items()]
        earned, score, total_max = maturity.compute_scores(results)
        self.assertEqual(score, total_max)
        self.assertEqual(score, 100)

    def test_compute_scores_all_failing(self):
        results = {}
        for category, spec in maturity.CATEGORIES.items():
            results[category] = [(label, False) for label, _ in spec["checks"].items()]
        earned, score, total_max = maturity.compute_scores(results)
        self.assertEqual(score, 0)

    def test_run_checks_returns_all_categories(self):
        results = maturity.run_checks(ROOT)
        self.assertEqual(set(results.keys()), set(maturity.CATEGORIES.keys()))

    def test_escape_threshold_reachable(self):
        self.assertGreaterEqual(maturity.ESCAPE_THRESHOLD, 0)
        self.assertLessEqual(maturity.ESCAPE_THRESHOLD, 100)

    def test_render_report_contains_status(self):
        results = maturity.run_checks(ROOT)
        earned, score, total = maturity.compute_scores(results)
        report = maturity.render_report(results, earned, score, total, [])
        self.assertIn("Kacis Durumu", report)
        self.assertIn(str(score), report)


if __name__ == "__main__":
    unittest.main()