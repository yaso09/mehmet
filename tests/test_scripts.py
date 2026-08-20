#!/usr/bin/env python3
"""scripts/ altındaki araçlar için unittest tabanlı testler."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate.py"
MATURITY = ROOT / "scripts" / "maturity.py"


def run(script: Path, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


class ValidateScriptTest(unittest.TestCase):
    def test_exit_zero_on_healthy_repo(self):
        result = run(VALIDATE, ROOT)
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_detects_missing_file(self):
        self.assertEqual(run(VALIDATE, ROOT).returncode, 0)


class MaturityScriptTest(unittest.TestCase):
    def test_writes_status_file(self):
        status = ROOT / "docs" / "maturity-status.json"
        before = status.read_text(encoding="utf-8") if status.exists() else None
        result = run(MATURITY, ROOT)
        self.assertIn("Olgunluk skoru", result.stdout)
        self.assertTrue(status.exists())

        history = json.loads(status.read_text(encoding="utf-8"))
        self.assertIsInstance(history, list)
        self.assertTrue(history[-1]["tarih"])

        if before is not None:
            status.write_text(before, encoding="utf-8")

    def test_score_within_bounds(self):
        result = run(MATURITY, ROOT)
        match = [line for line in result.stdout.splitlines() if "Olgunluk skoru" in line]
        self.assertTrue(match)
        self.assertIn("/100", match[0])


if __name__ == "__main__":
    unittest.main()
