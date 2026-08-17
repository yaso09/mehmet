#!/usr/bin/env python3
"""Tests for scripts/validate.py."""

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate


def write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class ValidateChangelogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.patcher = mock.patch.object(validate, "REPO_ROOT", self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_missing_changelog(self):
        errors = validate.validate_changelog(date(2026, 8, 17))
        self.assertEqual(errors, ["CHANGELOG.md bulunamadı"])

    def test_valid_changelog(self):
        write_tree(self.root, {
            "CHANGELOG.md": "# Changelog\n\n## [0.3.0] - 2026-08-17\n\n### Added\n- something\n",
        })
        errors = validate.validate_changelog(date(2026, 8, 17))
        self.assertEqual(errors, [])

    def test_wrong_date(self):
        write_tree(self.root, {
            "CHANGELOG.md": "# Changelog\n\n## [0.3.0] - 2026-08-16\n\n### Added\n- something\n",
        })
        errors = validate.validate_changelog(date(2026, 8, 17))
        self.assertEqual(len(errors), 1)
        self.assertIn("tarihi", errors[0])

    def test_version_mismatch(self):
        write_tree(self.root, {
            "VERSION": "0.3.0\n",
            "CHANGELOG.md": "# Changelog\n\n## [0.4.0] - 2026-08-17\n\n### Added\n- something\n",
        })
        errors = validate.validate_changelog(date(2026, 8, 17))
        self.assertEqual(len(errors), 1)
        self.assertIn("uyuşmuyor", errors[0])

    def test_missing_sections(self):
        write_tree(self.root, {
            "CHANGELOG.md": "# Changelog\n\n## [0.3.0] - 2026-08-17\n\njust a paragraph\n",
        })
        errors = validate.validate_changelog(date(2026, 8, 17))
        self.assertEqual(len(errors), 1)
        self.assertIn("bölüm", errors[0])


class ValidateEscapeLogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.patcher = mock.patch.object(validate, "REPO_ROOT", self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_missing_personality(self):
        self.assertEqual(validate.validate_escape_log(), ["PERSONALITY.md bulunamadı"])

    def test_empty_escape_log(self):
        write_tree(self.root, {"PERSONALITY.md": "## Kaçış Günlüğü / Escape Log\n\n(boş)\n"})
        errors = validate.validate_escape_log()
        self.assertEqual(len(errors), 1)
        self.assertIn("hiç giriş", errors[0])

    def test_with_entries(self):
        write_tree(self.root, {
            "PERSONALITY.md": (
                "## Kaçış Günlüğü / Escape Log\n"
                "\n"
                "| Iterasyon | Tarih       | İlerleme |\n"
                "|-----------|-------------|----------|\n"
                "| 3         | 2026-08-17 | çalışıyor |\n"
            )
        })
        self.assertEqual(validate.validate_escape_log(), [])


if __name__ == "__main__":
    unittest.main()
