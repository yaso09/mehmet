"""Structural tests: required files and directories exist."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
    "scripts/maturity.py",
    "scripts/run_tests.py",
]

REQUIRED_DIRS = ["tests", "docs/superpowers/plans", "docs/superpowers/specs"]


class TestStructure(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
        self.assertEqual([], missing, f"missing files: {missing}")

    def test_required_dirs_exist(self):
        missing = [d for d in REQUIRED_DIRS if not (ROOT / d).is_dir()]
        self.assertEqual([], missing, f"missing dirs: {missing}")

    def test_test_discovery_matches(self):
        tests = list((ROOT / "tests").glob("test_*.py"))
        self.assertGreaterEqual(len(tests), 2)


if __name__ == "__main__":
    unittest.main()