"""Verify the core project structure exists and is coherent."""
import unittest

from tests import repo_path


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    "LICENSE",
    ".gitignore",
    ".github/workflows/opencode.yml",
]


class TestProjectStructure(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not repo_path(f).is_file()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")

    def test_gitignore_ignores_secrets_and_builds(self):
        text = repo_path(".gitignore").read_text(encoding="utf-8")
        for entry in (".env", "node_modules/", "*.log", "dist/", "build/"):
            self.assertIn(entry, text, f".gitignore missing entry: {entry}")

    def test_root_has_no_stray_artifacts(self):
        banned = {"__pycache__", ".pytest_cache", ".coverage"}
        found = [p.name for p in repo_path().iterdir() if p.name in banned]
        self.assertEqual(found, [], f"Unexpected artifacts in repo root: {found}")


if __name__ == "__main__":
    unittest.main()
