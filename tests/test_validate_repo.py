#!/usr/bin/env python3
"""Unit tests for scripts/validate_repo.py."""

from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

from validate_repo import (  # noqa: E402
    CHANGELOG_VERSION_RE,
    SECRET_PATTERNS,
    check_changelog,
    check_json,
    main,
)


class ChangelogRegexTest(unittest.TestCase):
    def test_matches_versioned_entry(self):
        self.assertTrue(CHANGELOG_VERSION_RE.match("## [0.3.0]"))
        self.assertTrue(CHANGELOG_VERSION_RE.match("## [1.2.3] - 2026-07-04"))

    def test_rejects_unversioned_header(self):
        self.assertFalse(CHANGELOG_VERSION_RE.match("## Unreleased"))
        self.assertFalse(CHANGELOG_VERSION_RE.match("# Changelog"))


class SecretPatternTest(unittest.TestCase):
    def test_detects_openai_style_key(self):
        self.assertTrue(SECRET_PATTERNS[0].search("key = sk-abcdefghijklmnopqrstuvwxyz123"))
        self.assertTrue(SECRET_PATTERNS[0].search("sk-" + "A" * 30))

    def test_detects_github_tokens(self):
        self.assertTrue(SECRET_PATTERNS[1].search("token=ghp_" + "B" * 30))
        self.assertTrue(SECRET_PATTERNS[2].search("token=gho_" + "C" * 30))

    def test_detects_api_key_assignment(self):
        self.assertTrue(SECRET_PATTERNS[3].search("OPENCODE_API_KEY=abc123"))
        self.assertTrue(
            SECRET_PATTERNS[4].search('FOO_API_KEY = "supersecretvalue123"')
        )

    def test_ignores_github_secret_references(self):
        # ${{ secrets.X }} references are safe and must not be flagged.
        self.assertFalse(SECRET_PATTERNS[4].search("OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}"))


class CheckHelpersTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._tmp_dir = pathlib.Path(self._tmp.name)

    def _temp_file(self, content: str) -> pathlib.Path:
        path = self._tmp_dir / "sample.txt"
        path.write_text(content, encoding="utf-8")
        return path

    def test_check_json_accepts_valid(self):
        path = self._temp_file('{"model": "opencode/deepseek-v4-flash-free"}')
        errors: list[str] = []
        check_json(path, errors)
        self.assertEqual(errors, [])

    def test_check_json_rejects_invalid(self):
        path = self._temp_file("{not valid json}")
        errors: list[str] = []
        check_json(path, errors)
        self.assertEqual(len(errors), 1)

    def test_check_changelog_accepts_version(self):
        path = self._temp_file("## [0.3.0]\n\n### Added\n- thing")
        errors: list[str] = []
        check_changelog(path, errors)
        self.assertEqual(errors, [])

    def test_check_changelog_rejects_missing_version(self):
        path = self._temp_file("# Changelog\nNo versions here.")
        errors: list[str] = []
        check_changelog(path, errors)
        self.assertEqual(len(errors), 1)


class IntegrationTest(unittest.TestCase):
    def test_validation_passes_on_repository(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()