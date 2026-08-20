"""Validate README.md structure and relative links."""
import re
import unittest

from tests import read_text, repo_path


class TestReadme(unittest.TestCase):
    def setUp(self):
        self.text = read_text("README.md")
        self.assertIsNotNone(self.text, "README.md missing")

    def test_title(self):
        self.assertTrue(self.text.startswith("# mehmet"))

    def test_relative_links_resolve(self):
        rel_links = re.findall(r"\]\(((?:\./|\.\./|#)[^)]+)\)", self.text)
        broken = []
        for link in rel_links:
            if link.startswith("#"):
                anchor = link.lstrip("#").lower()
                if f" {anchor}" not in self.text.lower():
                    broken.append(link)
                continue
            path = repo_path(link.lstrip("./"))
            if not path.exists():
                broken.append(link)
        self.assertEqual(broken, [], f"broken links in README: {broken}")

    def test_has_license_section(self):
        self.assertIn("## Lisans", self.text)

    def test_mentions_github_actions(self):
        self.assertIn("GitHub Actions", self.text)


if __name__ == "__main__":
    unittest.main()