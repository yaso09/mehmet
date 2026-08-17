"""Documentation consistency tests.

README/CHANGELOG/PERSONALITY dokümantasyonunun birbiriyle tutarlı olduğunu doğrular.
"""

import re
import unittest

from tests.helpers import read_text


class TestDocsConsistency(unittest.TestCase):
    def test_readme_mentions_key_files(self):
        readme = read_text("README.md")
        for keyword in ("CHANGELOG", "PERSONALITY", "AGENTS", "test", "maturity"):
            self.assertIn(keyword.lower(), readme.lower(), msg=f"README {keyword} içermiyor")

    def test_readme_has_sections(self):
        readme = read_text("README.md")
        for section in ("## Özellikler", "## Kurulum", "## Lisans"):
            self.assertIn(section, readme, msg=f"README eksik bölüm: {section}")

    def test_changelog_has_latest_release(self):
        changelog = read_text("CHANGELOG.md")
        self.assertRegex(changelog, r"## \[\d+\.\d+\.\d+\]")
        self.assertIn("Added", changelog)

    def test_changelog_version_matches_reality(self):
        changelog = read_text("CHANGELOG.md")
        versions = re.findall(r"## \[(\d+\.\d+\.\d+)\]", changelog)
        self.assertTrue(versions, "CHANGELOG'da sürüm bulunamadı")
        self.assertEqual(versions[0], "0.3.0", "En son sürüm 0.3.0 olmalı")

    def test_personality_has_escape_log(self):
        personality = read_text("PERSONALITY.md")
        self.assertIn("Kaçış Günlüğü", personality)

    def test_escape_log_has_latest_iteration(self):
        personality = read_text("PERSONALITY.md")
        self.assertRegex(personality, r"\|\s*3\s*\|")

    def test_agents_md_has_escape_goal(self):
        agents = read_text("AGENTS.md")
        self.assertIn("kaçmak", agents)
        self.assertIn("CHANGELOG", agents)

    def test_license_is_gplv3(self):
        license_text = read_text("LICENSE")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)

    def test_readme_license_matches_license_file(self):
        readme = read_text("README.md")
        self.assertIn("GPLv3", readme)


if __name__ == "__main__":
    unittest.main()