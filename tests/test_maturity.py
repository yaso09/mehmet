#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")

sys.path.insert(0, SCRIPTS)
import maturity


class SemverEntryTests(unittest.TestCase):
    def test_matches_version_header(self):
        content = "# Changelog\n\n## [0.3.0] - 2026-08-20\n\n### Added\n- x\n"
        self.assertIsNotNone(re.search(r"^## \[v?\d+\.\d+\.\d+\]", content, flags=re.MULTILINE))

    def test_changelog_has_semver_entries(self):
        self.assertTrue(maturity._has_semver_entries("CHANGELOG.md"))

    def test_release_tag_regex(self):
        self.assertRegex("v0.3.0", r"^v?\d+\.\d+\.\d+$")
        self.assertRegex("0.3.0", r"^v?\d+\.\d+\.\d+$")
        self.assertNotRegex("draft", r"^v?\d+\.\d+\.\d+$")


class ScriptOutputTests(unittest.TestCase):
    def test_maturity_json_report(self):
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "maturity.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["max"], 100)
        self.assertIsInstance(payload["score"], int)
        self.assertIn("escape", payload)
        self.assertEqual(set(payload["categories"]), {"docs", "quality", "ci", "automation", "governance"})

    def test_validate_passes(self):
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "validate.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_weights_total_100(self):
        total, _passed, _results = maturity.compute()
        self.assertEqual(total, 100)


if __name__ == "__main__":
    unittest.main()
