#!/usr/bin/env python3
"""validate_project.py için unittest testleri."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_project.py"


class ValidateProjectTests(unittest.TestCase):
    def run_script(self, *extra_args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--json", *extra_args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_exit_zero(self):
        proc = self.run_script()
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_json_output_valid(self):
        proc = self.run_script()
        data = json.loads(proc.stdout)
        self.assertIn("status", data)
        self.assertIn("maturity_score", data)
        self.assertIn("escape_threshold", data)

    def test_core_files_pass(self):
        proc = self.run_script()
        data = json.loads(proc.stdout)
        core = next(c for c in data["checks"] if c["id"] == "core-files")
        self.assertTrue(core["passed"], core["errors"])

    def test_skip_optional_filters(self):
        proc = self.run_script("--skip-optional")
        data = json.loads(proc.stdout)
        for check in data["checks"]:
            self.assertTrue(check["required"])

    def test_escape_threshold_defined(self):
        proc = self.run_script()
        data = json.loads(proc.stdout)
        self.assertGreater(data["escape_threshold"], 0)


if __name__ == "__main__":
    unittest.main()
