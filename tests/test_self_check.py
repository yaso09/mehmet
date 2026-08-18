#!/usr/bin/env python3
"""mehmet için unittest tabanlı testler.

Kullanım:
    python3 -m unittest discover -s tests -v
"""

import contextlib
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import self_check  # noqa: E402


class TestCheckFunctions(unittest.TestCase):
    def setUp(self):
        self_check.PASS = 0
        self_check.FAIL = 0

    def check_silently(self, name, ok):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self_check.check(name, ok)

    def test_check_pass_increments(self):
        self.check_silently("deneme", True)
        self.assertEqual(self_check.PASS, 1)
        self.assertEqual(self_check.FAIL, 0)

    def test_check_fail_increments(self):
        self.check_silently("deneme", False)
        self.assertEqual(self_check.PASS, 0)
        self.assertEqual(self_check.FAIL, 1)

    def test_parse_version(self):
        self.assertEqual(self_check.parse_version("0.2.0"), (0, 2, 0))
        self.assertEqual(self_check.parse_version("1.10.3"), (1, 10, 3))


class TestRepositoryIntegrity(unittest.TestCase):
    def test_required_files_exist(self):
        for f in self_check.REQUIRED_FILES:
            with self.subTest(file=f):
                self.assertTrue((ROOT / f).is_file(), f"eksik dosya: {f}")

    def test_opencode_json_is_valid(self):
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", cfg)
        self.assertIn("$schema", cfg)

    def test_changelog_has_versions(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        versions = self_check.CHANGELOG_VERSION_RE.findall(changelog)
        self.assertGreaterEqual(len(versions), 2)


class TestSelfCheckCli(unittest.TestCase):
    def test_self_check_runs_without_error(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/self_check.py"), "--full"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Olgunluk seviyesi", result.stdout)


if __name__ == "__main__":
    unittest.main()