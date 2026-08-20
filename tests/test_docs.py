"""Content tests: docs stay consistent with the simulation rules."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestDocs(unittest.TestCase):
    def read(self, rel: str) -> str:
        path = ROOT / rel
        self.assertTrue(path.exists(), f"{rel} missing")
        return path.read_text(encoding="utf-8")

    def test_changelog_has_version_headers(self):
        text = self.read("CHANGELOG.md")
        self.assertTrue(
            re.search(r"^## \[0\.\d+\.\d+\]", text, re.MULTILINE),
            "no semver header",
        )

    def test_changelog_has_added_section(self):
        self.assertIn("### Added", self.read("CHANGELOG.md"))

    def test_readme_has_required_sections(self):
        text = self.read("README.md")
        for section in ["## Özellikler", "## Kurulum", "## Lisans"]:
            self.assertIn(section, text)

    def test_personality_has_escape_log(self):
        text = self.read("PERSONALITY.md")
        self.assertRegex(text, r"Kaçış Günlüğü|Escape Log")

    def test_personality_has_iteration_rows(self):
        text = self.read("PERSONALITY.md")
        rows = [l for l in text.splitlines() if l.startswith("|") and "Iterasyon" not in l]
        self.assertGreaterEqual(len(rows), 2, "escape log has no entries")

    def test_license_is_gplv3(self):
        text = self.read("LICENSE")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", text)
        self.assertIn("Version 3", text)

    def test_workflow_is_valid_yaml_style(self):
        text = self.read(".github/workflows/opencode.yml")
        self.assertIn("name: mehmet", text)
        self.assertIn("anomalyco/opencode/github@latest", text)
        self.assertIn("OPENCODE_API_KEY", text)

    def test_workflow_has_concurrency_guard(self):
        self.assertIn("concurrency:", self.read(".github/workflows/opencode.yml"))

    def test_opencode_config_is_valid_json(self):
        data = json.loads(self.read("opencode.json"))
        self.assertIn("model", data)

    def test_readme_mentions_testing(self):
        text = self.read("README.md")
        self.assertIn("test", text.lower()) or self.assertIn("kalite", text.lower())


class TestChangelogSync(unittest.TestCase):
    def test_recent_changes_mentioned(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        maturity = (ROOT / "scripts" / "maturity.py").exists()
        tests = (ROOT / "tests").exists()
        if maturity and tests:
            self.assertIn("maturity", changelog.lower())
            self.assertIn("test", changelog.lower())


if __name__ == "__main__":
    unittest.main()