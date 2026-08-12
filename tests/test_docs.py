"""Validate core documentation files exist and follow conventions."""

import unittest

from tests.helpers import ROOT


class TestDocumentation(unittest.TestCase):

    def test_required_files_exist(self):
        for path in [
            "README.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "AGENTS.md",
            "CONTRIBUTING.md",
            "LICENSE",
            "requirements.txt",
        ]:
            with self.subTest(path=path):
                self.assertTrue(
                    ROOT.joinpath(path).exists(),
                    f"Required file missing: {path}",
                )

    def test_readme_mentions_features(self):
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        for section in ["Schedule", "Kurulum"]:
            with self.subTest(section=section):
                self.assertIn(section, readme)

    def test_changelog_has_unreleased_section(self):
        changelog = ROOT.joinpath("CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [", changelog)

    def test_personality_has_escape_log(self):
        personality = ROOT.joinpath("PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", personality)
        self.assertIn("Escape Log", personality)

    def test_agents_specifies_rules(self):
        agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8")
        for rule in ["CHANGELOG.md", "README.md", "PERSONALITY.md"]:
            with self.subTest(rule=rule):
                self.assertIn(rule, agents)

    def test_has_ci_workflow(self):
        self.assertTrue(
            ROOT.joinpath(".github/workflows/ci.yml").exists(),
            "CI workflow missing",
        )


if __name__ == "__main__":
    unittest.main()