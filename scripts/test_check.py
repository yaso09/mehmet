#!/usr/bin/env python3
"""Unit tests for scripts/check.py. Stdlib only.

Usage:
    python3 scripts/test_check.py
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self._orig_root = check.ROOT
        check.ROOT = self.tmp

    def tearDown(self):
        check.ROOT = self._orig_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rel, content):
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def test_missing_required_files(self):
        c = check.Checks()
        check.check_required_files(c)
        self.assertEqual(len(c.errors), len(check.REQUIRED_FILES))

    def test_valid_repo_passes(self):
        for rel in check.REQUIRED_FILES:
            self.write(rel, "")
        self.write("VERSION", "0.3.0\n")
        self.write("opencode.json", '{"$schema":"https://opencode.ai/config.json","model":"opencode/deepseek-v4-flash-free"}')
        self.write("CHANGELOG.md", "# Changelog\n\n## [0.3.0] - 2026-08-19\n\n### Added\n- x\n")
        self.write("PERSONALITY.md", "# Personality\n\n## Kaçış Günlüğü\n")
        self.write(".github/workflows/opencode.yml", "model: opencode/deepseek-v4-flash-free\nOPENCODE_API_KEY\n")
        c = check.Checks()
        check.run_checks(c)
        self.assertEqual(c.errors, [])

    def test_unknown_opencode_key(self):
        self.write("opencode.json", '{"model":"x","skip":true}')
        c = check.Checks()
        check.check_opencode_config(c)
        self.assertTrue(any("unknown top-level key 'skip'" in e for e in c.errors))

    def test_version_mismatch(self):
        self.write("VERSION", "0.3.0\n")
        self.write("CHANGELOG.md", "# Changelog\n\n## [0.2.0] - 2026-07-04\n")
        c = check.Checks()
        check.check_version(c)
        self.assertTrue(any("no entry" in e for e in c.errors))
        self.assertTrue(any("!= VERSION" in e for e in c.errors))

    def test_secret_detection(self):
        self.write(".github/workflows/opencode.yml", "OPENCODE_API_KEY: sk-1234567890abcdef1234567890abcdef\n")
        c = check.Checks()
        check.check_workflow(c)
        self.assertTrue(any("hardcoded secret" in e for e in c.errors))

    def test_bump(self):
        self.write("VERSION", "0.2.0\n")
        self.write("CHANGELOG.md", "# Changelog\n")
        import bump_version

        bump_version.ROOT = self.tmp
        bump_version.VERSION_PATH = self.tmp / "VERSION"
        bump_version.CHANGELOG_PATH = self.tmp / "CHANGELOG.md"
        self.assertEqual(bump_version.bump("minor"), "0.3.0")
        bump_version.add_changelog_entry("0.3.0")
        self.assertEqual((self.tmp / "VERSION").read_text().strip(), "0.2.0")
        self.assertIn("## [0.3.0]", (self.tmp / "CHANGELOG.md").read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)