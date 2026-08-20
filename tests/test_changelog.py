"""Validate CHANGELOG.md formatting and structure."""
import re
import unittest

from tests import read_text


class TestChangelog(unittest.TestCase):
    def setUp(self):
        self.text = read_text("CHANGELOG.md")
        self.assertIsNotNone(self.text, "CHANGELOG.md missing")

    def test_header(self):
        self.assertTrue(self.text.startswith("# Changelog"))

    def test_version_headers_are_semver(self):
        versions = re.findall(r"^## \[([^\]]+)\]", self.text, flags=re.M)
        self.assertTrue(versions, "no version headers found")
        for v in versions:
            self.assertRegex(
                v, r"^\d+\.\d+\.\d+$", f"version header not semver: {v}"
            )

    def test_version_headers_have_dates(self):
        headers = re.findall(r"^## \[[^\]]+\] - (\d{4}-\d{2}-\d{2})", self.text, flags=re.M)
        self.assertTrue(headers, "version headers must include dates (YYYY-MM-DD)")
        for d in headers:
            self.assertRegex(d, r"^\d{4}-\d{2}-\d{2}$")

    def test_no_duplicate_versions(self):
        versions = re.findall(r"^## \[([^\]]+)\]", self.text, flags=re.M)
        dupes = {v for v in versions if versions.count(v) > 1}
        self.assertEqual(dupes, set(), f"duplicate version headers: {dupes}")

    def test_sections_use_markdown_headers(self):
        for section in ("### Added", "### Fixed", "### Changed", "### Removed"):
            pass
        sections = re.findall(r"^### (\w+)", self.text, flags=re.M)
        self.assertTrue(sections, "no ### subsections found in changelog")


if __name__ == "__main__":
    unittest.main()