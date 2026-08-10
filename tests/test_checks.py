"""validate modülü için birim testler."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate


class RequiredFileTests(unittest.TestCase):
    def test_agents_md_exists(self):
        ok, _ = validate.required_file("AGENTS.md", 10)
        self.assertTrue(ok)

    def test_readme_exists(self):
        ok, _ = validate.required_file("README.md", 10)
        self.assertTrue(ok)

    def test_missing_file_fails(self):
        ok, _ = validate.required_file("does-not-exist.md", 1)
        self.assertFalse(ok)


class ValidJsonTests(unittest.TestCase):
    def test_opencode_json_valid(self):
        ok, _ = validate.valid_json("opencode.json")
        self.assertTrue(ok)


class ChangelogTests(unittest.TestCase):
    def test_version_headers_present(self):
        ok, _ = validate.regex_in("CHANGELOG.md", r"^## \[\d+\.\d+\.\d+\]")
        self.assertTrue(ok)

    def test_changelog_recent(self):
        ok, _ = validate.changelog_recent("CHANGELOG.md")
        self.assertTrue(ok, "CHANGELOG son sürüm yakın tarihli olmalı")


class PersonalityTests(unittest.TestCase):
    def test_escape_log_has_dates(self):
        ok, _ = validate.contains("PERSONALITY.md", "Kaçış Günlüğü")
        self.assertTrue(ok)

    def test_escape_log_recent(self):
        ok, _ = validate.escape_log_recent("PERSONALITY.md")
        self.assertTrue(ok)


class ParseIsoTests(unittest.TestCase):
    def test_valid_date(self):
        self.assertIsNotNone(validate.parse_iso("2026-08-10"))

    def test_invalid_date(self):
        self.assertIsNone(validate.parse_iso("not-a-date"))


class MaturityReportTests(unittest.TestCase):
    def test_report_recent(self):
        ok, _ = validate.maturity_report_recent("MATURITY.md")
        self.assertTrue(ok, "olgunluk raporu güncel olmalı")


class ScanFreeOfTests(unittest.TestCase):
    def test_secrets_scanner_clean(self):
        ok, _ = validate.scan_free_of(validate.SECRET_PATTERNS, "sır")
        self.assertTrue(ok)


class AllGatesTests(unittest.TestCase):
    def test_all_gates_green(self):
        failed = [label for label, (ok, _) in validate.run() if not ok]
        self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()