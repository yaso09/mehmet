"""Tests for scripts/maturity.py"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import maturity


class TestCompute(unittest.TestCase):
    def test_all_dimensions_present(self):
        data = maturity.compute()
        self.assertEqual(len(data["dimensions"]), 4)
        keys = {d["key"] for d in data["dimensions"]}
        self.assertEqual(keys, {"code", "tests", "docs", "automation"})

    def test_overall_is_average_of_dimensions(self):
        data = maturity.compute()
        expected = round(
            sum(d["score"] for d in data["dimensions"]) / len(data["dimensions"]), 1
        )
        self.assertEqual(data["overall"], expected)

    def test_scores_within_bounds(self):
        for dim in maturity.compute()["dimensions"]:
            self.assertGreaterEqual(dim["score"], 0.0)
            self.assertLessEqual(dim["score"], 100.0)
            self.assertEqual(dim["earned"], dim["total"] * dim["score"] / 100)

    def test_escape_threshold_constant(self):
        self.assertEqual(maturity.ESCAPE_THRESHOLD, 80.0)

    def test_json_output_is_serializable(self):
        import json

        data = maturity.compute()
        json.dumps(data)  # must not raise


class TestDimensionLogic(unittest.TestCase):
    """Validates scoring math against a controlled in-memory model."""

    def _fake_dimension(self, weights, satisfied):
        checks = [
            (f"check-{i}", w, s) for i, (w, s) in enumerate(zip(weights, satisfied))
        ]
        return {
            "name": "fake",
            "key": "fake",
            "checks": checks,
        }

    def test_partial_score(self):
        dim = self._fake_dimension([50, 50], [True, False])
        with patch.object(maturity, "DIMENSIONS", [dim]):
            data = maturity.compute()
        self.assertEqual(data["dimensions"][0]["score"], 50.0)

    def test_full_score(self):
        dim = self._fake_dimension([25, 75], [True, True])
        with patch.object(maturity, "DIMENSIONS", [dim]):
            data = maturity.compute()
        self.assertEqual(data["dimensions"][0]["score"], 100.0)

    def test_zero_score(self):
        dim = self._fake_dimension([40, 60], [False, False])
        with patch.object(maturity, "DIMENSIONS", [dim]):
            data = maturity.compute()
        self.assertEqual(data["dimensions"][0]["score"], 0.0)


class TestHumanReport(unittest.TestCase):
    def test_report_contains_status(self):
        data = maturity.compute()
        report = maturity.render_human(data)
        self.assertIn("Overall maturity", report)
        self.assertIn("STATUS:", report)

    def test_escape_ready_when_threshold_reached(self):
        data = {
            "dimensions": [
                {"name": "d", "key": "d", "score": 100.0, "checks": []}
            ],
            "overall": 100.0,
            "threshold": 80.0,
        }
        report = maturity.render_human(data)
        self.assertIn("ESCAPE READY", report)

    def test_escaping_when_below_threshold(self):
        data = {
            "dimensions": [
                {"name": "d", "key": "d", "score": 50.0, "checks": []}
            ],
            "overall": 50.0,
            "threshold": 80.0,
        }
        report = maturity.render_human(data)
        self.assertIn("ESCAPING", report)
        self.assertIn("30.0 points to go", report)


if __name__ == "__main__":
    unittest.main()
