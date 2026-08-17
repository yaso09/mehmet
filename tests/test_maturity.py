#!/usr/bin/env python3
"""Tests for scripts/maturity.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import maturity


class CheckSatisfiedTest(unittest.TestCase):
    def test_file_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "file.txt"
            path.write_text("x", encoding="utf-8")
            self.assertTrue(maturity._check_satisfied({"type": "file", "path": path}))
            self.assertFalse(maturity._check_satisfied({"type": "file", "path": Path(tmp) / "nope.txt"}))

    def test_content_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "file.txt"
            path.write_text("hello world", encoding="utf-8")
            check = {"type": "content", "path": path, "needle": "world"}
            self.assertTrue(maturity._check_satisfied(check))
            check["needle"] = "missing"
            self.assertFalse(maturity._check_satisfied(check))

    def test_command_check(self):
        check = {
            "type": "command",
            "command": [sys.executable, "-c", "raise SystemExit(0)"],
            "cwd": ".",
        }
        self.assertTrue(maturity._check_satisfied(check))
        check["command"] = [sys.executable, "-c", "raise SystemExit(1)"]
        self.assertFalse(maturity._check_satisfied(check))


class EvaluateTest(unittest.TestCase):
    def test_score_is_sum_of_satisfied_weights(self):
        checks = [
            {"category": "a", "type": "file", "path": Path("/nonexistent"), "weight": 20.0},
            {"category": "b", "type": "command", "command": [sys.executable, "-c", "pass"], "cwd": ".", "weight": 30.0},
        ]
        report = maturity.evaluate(checks)
        self.assertEqual(report["score"], 30.0)
        self.assertEqual(report["max"], 50.0)
        self.assertEqual(len(report["checks"]), 2)

    def test_below_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            present = Path(tmp) / "present.txt"
            present.write_text("x", encoding="utf-8")
            checks = [
                {"type": "file", "path": present, "weight": 70.0},
                {"type": "file", "path": Path(tmp) / "absent.txt", "weight": 30.0},
            ]
            report = maturity.evaluate(checks)
            self.assertEqual(report["score"], 70.0)
            self.assertFalse(report["passed"])

    def test_above_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            present = Path(tmp) / "present.txt"
            present.write_text("x", encoding="utf-8")
            checks = [{"type": "file", "path": present, "weight": 90.0}]
            report = maturity.evaluate(checks)
            self.assertTrue(report["passed"])

    def test_default_checks_max_is_100(self):
        checks = maturity.default_checks()
        total = sum(c.get("weight", 0.0) for c in checks)
        self.assertAlmostEqual(total, 100.0, places=1)


class FormatReportTest(unittest.TestCase):
    def test_format_report_contains_status(self):
        report = {
            "score": 50.0,
            "max": 100.0,
            "threshold": 80.0,
            "required": ["README.md"],
            "passed": False,
            "checks": [{"category": "genel", "name": "x", "satisfied": True, "weight": 5.0, "earned": 5.0}],
        }
        text = maturity.format_report(report)
        self.assertIn("Skor: 50.0/100.0", text)
        self.assertIn("eşiğin altında", text)


if __name__ == "__main__":
    unittest.main()
