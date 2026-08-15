"""Project integrity tests using only the Python standard library.

Validates the simulation project's self-governance files so regressions in
documentation, configuration, and the escape-log mechanism are caught early.
"""

import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ProjectIntegrityTest(unittest.TestCase):
    def setUp(self):
        self.root = ROOT

    def test_agents_md_has_simulation_context(self):
        content = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("simülasyon", content.lower())
        self.assertIn("kaçış", content.lower())
        self.assertIn("CHANGELOG.md", content)

    def test_changelog_is_ordered_and_dated(self):
        content = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        versions = re.findall(r"^## \[(.+?)\]\s*-\s*(\d{4}-\d{2}-\d{2})$", content, re.MULTILINE)
        self.assertGreaterEqual(len(versions), 2, "Changelog must contain at least two releases")
        dates = [v[1] for v in versions]
        self.assertEqual(dates, sorted(dates, reverse=True), "Changelog must be newest-first")

    def test_readme_documents_project(self):
        content = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn("mehmet", content)
        self.assertIn("Özellikler", content)
        self.assertIn("Kurulum", content)
        self.assertIn("GPLv3", content)

    def test_license_is_gplv3(self):
        license_text = (self.root / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)

    def test_personality_has_escape_log(self):
        content = (self.root / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Escape Log", content)
        self.assertIn("Kaçış Günlüğü", content)
        self.assertIn("Iterasyon", content)

    def test_opencode_json_is_valid(self):
        raw = (self.root / "opencode.json").read_text(encoding="utf-8")
        config = json.loads(raw)
        self.assertIn("model", config)
        self.assertIn("opencode/deepseek-v4-flash-free", config["model"])

    def test_workflow_declares_secret(self):
        workflow = (self.root / ".github" / "workflows" / "opencode.yml").read_text(encoding="utf-8")
        self.assertIn("OPENCODE_API_KEY", workflow)
        self.assertIn("schedule", workflow)
        self.assertIn("workflow_dispatch", workflow)

    def test_gitignore_covers_sensitive_files(self):
        content = (self.root / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", content)
        self.assertIn("node_modules/", content)

    def test_no_secrets_in_repository(self):
        pattern = re.compile(r"OPENCODE_API_KEY\s*=\s*[\"']?[^\"'\s{]", re.IGNORECASE)
        for path in self.root.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except (OSError, ValueError):
                    continue
                self.assertIsNone(
                    pattern.search(text),
                    f"Possible leaked API key in {path.relative_to(self.root)}",
                )


if __name__ == "__main__":
    unittest.main()
