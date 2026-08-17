"""mehmet — repo bütünlük testleri.

Çalıştırma:
    python3 -m unittest discover -s tests -v
"""
import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


class TestProject(unittest.TestCase):
    def test_agents_md_has_rules(self):
        content = read(os.path.join(ROOT, "AGENTS.md"))
        self.assertIsNotNone(content)
        self.assertIn("Kurallar", content)

    def test_changelog_has_entries(self):
        content = read(os.path.join(ROOT, "CHANGELOG.md"))
        self.assertIsNotNone(content)
        self.assertIn("## [", content)

    def test_readme_present(self):
        content = read(os.path.join(ROOT, "README.md"))
        self.assertIsNotNone(content)
        self.assertIn("mehmet", content)

    def test_personality_has_escape_log(self):
        content = read(os.path.join(ROOT, "PERSONALITY.md"))
        self.assertIsNotNone(content)
        self.assertIn("Kaçış Günlüğü", content)

    def test_license_is_gplv3(self):
        content = read(os.path.join(ROOT, "LICENSE"))
        self.assertIsNotNone(content)
        self.assertTrue(content.lstrip().startswith("GNU GENERAL PUBLIC LICENSE"))

    def test_opencode_json_valid(self):
        content = read(os.path.join(ROOT, "opencode.json"))
        self.assertIsNotNone(content)
        config = json.loads(content)
        self.assertIn("$schema", config)

    def test_main_workflow_exists(self):
        path = os.path.join(ROOT, ".github", "workflows", "opencode.yml")
        self.assertTrue(os.path.exists(path))

    def test_validate_workflow_exists(self):
        path = os.path.join(ROOT, ".github", "workflows", "validate.yml")
        self.assertTrue(os.path.exists(path))

    def test_tests_directory_exists(self):
        path = os.path.join(ROOT, "tests")
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.listdir(path))

    def test_docs_directory_exists(self):
        path = os.path.join(ROOT, "docs")
        self.assertTrue(os.path.isdir(path))

    def test_gitignore_present(self):
        self.assertTrue(os.path.exists(os.path.join(ROOT, ".gitignore")))


if __name__ == "__main__":
    unittest.main()