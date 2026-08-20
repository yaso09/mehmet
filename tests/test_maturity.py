"""Tests for the maturity scoring system."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestMaturity(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "maturity.py"), *args],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )

    def test_script_runs(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Maturity:", result.stdout)

    def test_json_output_is_valid(self):
        import json

        result = self.run_script("--json")
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertIn("maturity", report)
        self.assertIn("dimensions", report)
        self.assertGreaterEqual(report["score"], 0)
        self.assertLessEqual(report["maturity"], 100)

    def test_documented_dimensions_present(self):
        import json

        report = json.loads(self.run_script("--json").stdout)
        expected = {"docs", "automation", "tests", "quality", "resilience"}
        self.assertTrue(expected.issubset(set(report["dimensions"])))

    def test_gate_passing(self):
        result = self.run_script("--gate", "0")
        self.assertEqual(result.returncode, 0)

    def test_gate_impossible(self):
        result = self.run_script("--gate", "200")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()