import json
import subprocess
import sys
import unittest
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from assess import assess, main  # noqa: E402


class AssessTests(unittest.TestCase):
    def test_assess_runs(self):
        result = assess()
        self.assertIn("score", result)
        self.assertIn("max_score", result)
        self.assertIn("checks", result)
        self.assertGreater(result["max_score"], 0)
        self.assertTrue(all(0 <= c["weight"] for c in result["checks"]))

    def test_core_files_passed(self):
        result = assess()
        passed_ids = {c["id"] for c in result["checks"] if c["passed"]}
        for required in ("README", "CHANGELOG", "AGENTS", "PERSONALITY", "LICENSE"):
            self.assertIn(required, passed_ids)

    def test_cli_summary(self):
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "assess.py"), "--summary"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("score:", proc.stdout)

    def test_cli_json(self):
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "assess.py"), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIn("score", data)


if __name__ == "__main__":
    unittest.main()
