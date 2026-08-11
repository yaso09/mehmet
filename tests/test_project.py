# -*- coding: utf-8 -*-
"""Project integrity tests for the mehmet simulation project.

These tests validate that the project keeps its core files, configuration
and documentation consistent and well-formed. They run on every push and
pull request via the ci.yml workflow.
"""

import json
import os
import re
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

CHANGELOG_HEADER = "# Changelog"

AGENTS_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "kaçış günlüğü",
]


class TestRequiredFiles(unittest.TestCase):
    def test_required_files_exist(self):
        for name in REQUIRED_FILES:
            self.assertTrue(
                (ROOT / name).exists(), f"Required file missing: {name}"
            )


class TestOpenCodeConfig(unittest.TestCase):
    def test_config_is_valid_json(self):
        config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", config)

    def test_config_has_model(self):
        config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertTrue(config["model"].startswith("opencode/"))


class TestWorkflow(unittest.TestCase):
    def test_workflow_parses_as_yaml(self):
        if yaml is None:
            self.skipTest("PyYAML not available")
        text = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        self.assertEqual(data["name"], "mehmet")
        self.assertIn("autonomous", data["jobs"])
        self.assertIn("comment", data["jobs"])

    def test_workflow_has_schedule(self):
        text = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
        self.assertIn("schedule", text)
        self.assertIn("cron", text)


class TestChangelog(unittest.TestCase):
    def test_changelog_header(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith(CHANGELOG_HEADER))

    def test_changelog_has_latest_entry(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        entries = re.findall(r"^## \[([^\]]+)\]", text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(entries), 1)
        self.assertEqual(entries[0], "0.3.0")

    def test_changelog_sections(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        for section in ("Added", "Fixed"):
            self.assertIn(section, text)


class TestReadme(unittest.TestCase):
    def test_readme_has_title(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# mehmet", text)

    def test_readme_has_sections(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for section in ("Özellikler", "Kurulum", "Lisans"):
            self.assertIn(section, text)


class TestAgents(unittest.TestCase):
    def test_agents_mentions_rules(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for rule in AGENTS_RULES:
            self.assertIn(rule, text)


class TestPersonality(unittest.TestCase):
    def test_personality_has_escape_log(self):
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", text)
        self.assertIn("Escape Log", text)

    def test_escape_log_has_progress_rows(self):
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| \d+ ", text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(rows), 3)


class TestGitignore(unittest.TestCase):
    def test_gitignore_has_sensitive_patterns(self):
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in ("node_modules/", ".env", "dist/"):
            self.assertIn(pattern, text)


class TestDocs(unittest.TestCase):
    def test_docs_directory_has_design_docs(self):
        specs = ROOT / "docs/superpowers/specs"
        plans = ROOT / "docs/superpowers/plans"
        self.assertTrue(any(specs.glob("*.md")))
        self.assertTrue(any(plans.glob("*.md")))

    def test_maturity_scorecard_exists(self):
        self.assertTrue((ROOT / "docs/MATURITY.md").exists())


if __name__ == "__main__":
    unittest.main()
