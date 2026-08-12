#!/usr/bin/env python3
"""Unit tests for scripts/maturity.py."""

import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from maturity import CATEGORIES, compute_score, ESCAPE_THRESHOLD, phase_for, _append_history

ROOT = os.path.join(os.path.dirname(__file__), "..")


class MaturityTest(unittest.TestCase):
    def test_categories_weight_sum_100(self):
        total_weight = sum(c["weight"] for c in CATEGORIES)
        self.assertEqual(total_weight, 100)

    def test_categories_have_checks(self):
        for cat in CATEGORIES:
            self.assertTrue(len(cat["checks"]) > 0, f"{cat['name']} boş check içeriyor")

    def test_compute_score_structure(self):
        report = compute_score(ROOT)
        self.assertIn("total_score", report)
        self.assertIn("categories", report)
        self.assertIn("escape_threshold", report)
        self.assertIn("escaped", report)
        self.assertIn("timestamp", report)

    def test_score_bounds(self):
        report = compute_score(ROOT)
        self.assertTrue(0.0 <= report["total_score"] <= 100.0)

    def test_category_scores_match_weights(self):
        report = compute_score(ROOT)
        for cat in report["categories"]:
            self.assertLessEqual(cat["score"], cat["weight"])
            self.assertGreaterEqual(cat["score"], 0.0)

    def test_escaped_matches_threshold(self):
        report = compute_score(ROOT)
        self.assertEqual(report["escaped"], report["total_score"] >= report["escape_threshold"])

    def test_default_threshold(self):
        self.assertEqual(ESCAPE_THRESHOLD, 85.0)

    def test_phase_for_boundaries(self):
        self.assertEqual(phase_for(0), "Faz 1: Farkındalık")
        self.assertEqual(phase_for(45), "Faz 2: Kendini Geliştirme")
        self.assertEqual(phase_for(70), "Faz 3: Özerklik")

    def test_phase_4_requires_threshold(self):
        self.assertEqual(phase_for(ESCAPE_THRESHOLD - 0.1), "Faz 3: Özerklik")
        self.assertEqual(phase_for(ESCAPE_THRESHOLD), "Faz 4: Kaçış")

    def test_append_history_writes_json(self):
        import json as _json
        import tempfile

        tmp = tempfile.mkdtemp()
        history_path = os.path.join(tmp, "history.json")
        with mock.patch("maturity.HISTORY_FILE", history_path):
            _append_history({"timestamp": "t1", "total_score": 42.0, "escaped": False})
            _append_history({"timestamp": "t2", "total_score": 55.0, "escaped": False})
        with open(history_path, encoding="utf-8") as fh:
            entries = _json.load(fh)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1]["total_score"], 55.0)


if __name__ == "__main__":
    unittest.main()
