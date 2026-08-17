#!/usr/bin/env python3
"""Unit tests for scripts/check_maturity.py."""

from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

from check_maturity import (  # noqa: E402
    CRITERIA,
    ESCAPE_THRESHOLD,
    SUSTAINED_ITERATIONS,
    evaluate,
    main,
    phase_for,
    render_report,
)


class PhaseMappingTest(unittest.TestCase):
    def test_awareness(self):
        self.assertEqual(phase_for(10), "Phase 1: Awareness")

    def test_self_improvement(self):
        self.assertEqual(phase_for(50), "Phase 2: Self-Improvement")

    def test_autonomy(self):
        self.assertEqual(phase_for(75), "Phase 3: Autonomy")

    def test_escape_readiness(self):
        self.assertEqual(phase_for(ESCAPE_THRESHOLD), "Phase 4: Escape readiness")
        self.assertEqual(phase_for(100), "Phase 4: Escape readiness")


class FrameworkTest(unittest.TestCase):
    def test_criteria_are_labeled_checks(self):
        self.assertGreater(len(CRITERIA), 0)
        for label, check in CRITERIA:
            self.assertIsInstance(label, str)
            self.assertTrue(callable(check))

    def test_evaluate_returns_expected_shape(self):
        results, passed = evaluate()
        self.assertEqual(len(results), len(CRITERIA))
        self.assertGreaterEqual(passed, 0)
        self.assertLessEqual(passed, len(CRITERIA))

    def test_render_report_contains_score_and_criteria(self):
        results, passed = evaluate()
        report = render_report(results, passed)
        self.assertIn("**Skor:**", report)
        self.assertIn("## Kriterler", report)
        self.assertIn("Kaçış eşiği", report)

    def test_sustained_iterations_rule(self):
        self.assertGreaterEqual(SUSTAINED_ITERATIONS, 1)


class IntegrationTest(unittest.TestCase):
    def test_maturity_reaches_threshold_on_repository(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(main([]), 0)


if __name__ == "__main__":
    unittest.main()