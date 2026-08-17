#!/usr/bin/env python3
"""Unit tests for scripts/maturity.py (stdlib-only, run with unittest)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import maturity  # noqa: E402


class MaturityEngineTest(unittest.TestCase):
    def test_compute_returns_total(self):
        results = maturity.compute()
        self.assertIn("total", results)
        self.assertIsInstance(results["total"], float)

    def test_score_within_bounds(self):
        results = maturity.compute()
        self.assertGreaterEqual(results["total"], 0.0)
        self.assertLessEqual(results["total"], 100.0)

    def test_escape_ready_is_boolean(self):
        results = maturity.compute()
        self.assertIsInstance(results["escape_ready"], bool)

    def test_each_category_bounded_by_weight(self):
        results = maturity.compute()
        for name, weight in maturity.CATEGORIES.items():
            self.assertLessEqual(results[name]["score"], weight)
            self.assertGreaterEqual(results[name]["score"], 0.0)

    def test_render_is_markdown(self):
        results = maturity.compute()
        out = maturity.render(results)
        self.assertIn("# Durum Raporu", out)
        self.assertIn(f"**Skor / Score:** {results['total']}", out)


if __name__ == "__main__":
    unittest.main()