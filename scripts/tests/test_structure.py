#!/usr/bin/env python3
"""Self-tests for mehmet's scripts.

Runs the consistency validator and maturity scorer against the live repo and
exercises their pure logic in isolation. Uses only the standard library.

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

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
    "Makefile",
    "docs/maturity.md",
]


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )


class TestRepositoryStructure(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
        self.assertEqual(missing, [])

    def test_no_credentials_in_repo(self):
        needles = ("ghp_", "github_pat_", "OPENCODE_API_KEY=")
        offenders = []
        for path in REQUIRED_FILES:
            if not (ROOT / path).exists():
                continue
            text = (ROOT / path).read_text(encoding="utf-8", errors="ignore")
            for needle in needles:
                if needle in text and "secret" not in text.lower():
                    offenders.append(f"{path}:{needle}")
        self.assertEqual(offenders, [])


class TestCheckScript(unittest.TestCase):
    def test_check_exits_zero(self):
        result = run_script("check.py", "--quiet")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_reports_all_passed(self):
        result = run_script("check.py", "--json")
        data = json.loads(result.stdout)
        self.assertEqual(data["total"], data["passed"])


class TestMaturityDimensionLogic(unittest.TestCase):
    def test_dimension_weighting(self):
        sys.path.insert(0, str(SCRIPTS))
        import importlib

        maturity = importlib.import_module("maturity")

        full = maturity.dimension("d", 25, [("a", True), ("b", True)])
        self.assertEqual(full["score"], 25.0)
        self.assertEqual(full["earned"], 2)

        half = maturity.dimension("d", 20, [("a", True), ("b", True), ("c", False)])
        self.assertAlmostEqual(half["score"], round(20.0 * 2 / 3, 2))

        none = maturity.dimension("d", 30, [("a", False), ("b", False)])
        self.assertEqual(none["score"], 0.0)


if __name__ == "__main__":
    unittest.main()