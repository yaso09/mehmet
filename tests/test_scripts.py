#!/usr/bin/env python3
"""check_project.py ve escape_score.py için testler."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestProjectChecks(unittest.TestCase):
    def test_check_project_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_project.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_escape_score_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "escape_score.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_escape_score_reports_percentage(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "escape_score.py")],
            capture_output=True,
            text=True,
        )
        self.assertIn("Toplam:", result.stdout)


if __name__ == "__main__":
    unittest.main()
