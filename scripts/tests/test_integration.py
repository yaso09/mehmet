#!/usr/bin/env python3
"""Integration tests for mehmet's maturity orchestration.

These tests execute the maturity scorer end-to-end. They are kept separate
from test_structure.py so that the scorer's internal self-test check (which
only runs the fast structure suite) never recurses into this file.

Usage:
    python3 -m unittest discover -s scripts/tests
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"


class TestMaturityIntegration(unittest.TestCase):
    def test_maturity_reaches_threshold(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "maturity.py"), "--json"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreaterEqual(data["score"], data["threshold"])
        self.assertTrue(data["escaped"])

    def test_maturity_json_shape(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "maturity.py"), "--json"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        data = json.loads(result.stdout)
        self.assertEqual({"score", "threshold", "escaped", "dimensions"} <= set(data), True)
        self.assertEqual(sum(d["score"] for d in data["dimensions"]), data["score"])


if __name__ == "__main__":
    unittest.main()