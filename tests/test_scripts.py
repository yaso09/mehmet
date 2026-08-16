"""Basic tests for the mehmet verification & maturity scripts."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestScripts(unittest.TestCase):
    def test_verify_passes(self):
        result = subprocess.run(
            [sys.executable, "scripts/verify.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASSED", result.stdout)

    def test_maturity_runs(self):
        result = subprocess.run(
            [sys.executable, "scripts/maturity.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("maturity score", result.stdout)

    def test_maturity_json_output(self):
        result = subprocess.run(
            [sys.executable, "scripts/maturity.py", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        import json

        data = json.loads(result.stdout)
        self.assertIn("score", data)
        self.assertIn("dimensions", data)


if __name__ == "__main__":
    unittest.main()