"""Validate that the real repository complies with the AGENTS.md simulation rules."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"missing file: {rel}")
    return path.read_text(encoding="utf-8")


class DocsTest(unittest.TestCase):
    def test_changelog_updated(self):
        self.assertIn("## [", read("CHANGELOG.md"))

    def test_readme_present(self):
        content = read("README.md")
        self.assertIn("# mehmet", content)
        self.assertIn("## ", content)

    def test_personality_has_escape_log(self):
        self.assertIn("Kaçış Günlüğü", read("PERSONALITY.md"))

    def test_agents_rules_documented(self):
        content = read("AGENTS.md")
        self.assertIn("CHANGELOG.md", content)
        self.assertIn("PERSONALITY.md", content)


class AutomationTest(unittest.TestCase):
    def test_opencode_workflow_has_secret(self):
        self.assertIn("OPENCODE_API_KEY", read(".github/workflows/opencode.yml"))

    def test_quality_workflow_exists(self):
        self.assertIn("quality", read(".github/workflows/quality.yml").lower())

    def test_config_valid_json(self):
        import json

        json.loads(read("opencode.json"))

    def test_license_matches_readme(self):
        license_text = read("LICENSE")
        self.assertIn("GNU", license_text)
        self.assertIn("GPLv3", read("README.md"))


if __name__ == "__main__":
    unittest.main()