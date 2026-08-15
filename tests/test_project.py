"""Project integrity tests for the mehmet self-improving agent repo.

These tests validate that the repository maintains a healthy, mature structure:
documentation, configuration, automation, and the escape log are all consistent.
Runs with the Python standard library only (unittest).
"""

import json
import os
import re
import sys
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
    "opencode.json",
    ".github/workflows/opencode.yml",
]

AGENTS_RULES = [
    "CHANGELOG.md",
    "README.md",
    "PERSONALITY.md",
    "Geliştirme fırsatları",
]

CHANGELOG_SECTIONS = ["Added", "Fixed", "Changed", "Removed"]


class TestRepositoryStructure(unittest.TestCase):
    """Core files must exist and be non-empty."""

    def test_required_files_exist(self):
        for name in REQUIRED_FILES:
            with self.subTest(file=name):
                path = ROOT / name
                self.assertTrue(path.is_file(), f"missing required file: {name}")
                self.assertGreater(path.stat().st_size, 0, f"file is empty: {name}")

    def test_license_is_gplv3(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)
        self.assertIn("Version 3", license_text)


class TestAgentsMd(unittest.TestCase):
    """AGENTS.md must define the simulation rules."""

    @classmethod
    def setUpClass(cls):
        cls.content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    def test_simulation_context_present(self):
        self.assertIn("Simülasyon Bağlamı", self.content)

    def test_rules_referenced(self):
        for rule in AGENTS_RULES:
            with self.subTest(rule=rule):
                self.assertIn(rule.lower(), self.content.lower())


class TestChangelog(unittest.TestCase):
    """CHANGELOG.md must follow the Keep a Changelog convention."""

    @classmethod
    def setUpClass(cls):
        cls.content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    def test_has_version_headers(self):
        versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", self.content, re.MULTILINE)
        self.assertGreater(len(versions), 0, "no versioned entries found")
        for v in versions:
            with self.subTest(version=v):
                self.assertTrue(
                    re.fullmatch(r"\d+\.\d+\.\d+", v), f"bad version format: {v}"
                )

    def test_versions_are_ascending(self):
        versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", self.content, re.MULTILINE)

        def key(v):
            return tuple(int(x) for x in v.split("."))

        self.assertEqual(
            versions,
            sorted(versions, key=key, reverse=True),
            "versions are not sorted newest-first",
        )

    def test_has_dated_entries(self):
        dates = re.findall(r"^## \[\d+\.\d+\.\d+\] - (\d{4}-\d{2}-\d{2})", self.content, re.MULTILINE)
        self.assertEqual(len(dates), len(re.findall(r"^## \[\d", self.content, re.MULTILINE)))
        for d in dates:
            with self.subTest(date=d):
                self.assertTrue(re.fullmatch(r"\d{4}-\d{2}-\d{2}", d))

    def test_has_standard_sections(self):
        present = set(re.findall(r"^### (\w+)$", self.content, re.MULTILINE))
        self.assertGreater(len(present & set(CHANGELOG_SECTIONS)), 0)


class TestReadme(unittest.TestCase):
    """README.md must describe the project accurately."""

    @classmethod
    def setUpClass(cls):
        cls.content = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_project_intro(self):
        self.assertIn("# mehmet", self.content)
        self.assertIn("AI", self.content)

    def test_license_matches_changelog_claim(self):
        self.assertIn("GPLv3", self.content)


class TestPersonality(unittest.TestCase):
    """PERSONALITY.md must track personality evolution and the escape log."""

    @classmethod
    def setUpClass(cls):
        cls.content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")

    def test_has_traits(self):
        self.assertIn("## Traits", self.content)

    def test_has_evolution_phases(self):
        self.assertIn("## Evolution", self.content)
        self.assertIn("## Kaçış Günlüğü", self.content)

    def test_escape_log_has_table_header(self):
        self.assertIn("| Iterasyon |", self.content)
        self.assertIn("|-----------|", self.content)

    def test_escape_log_has_entries(self):
        rows = re.findall(r"^\|\s*\d+\s*\|", self.content, re.MULTILINE)
        self.assertGreater(len(rows), 0, "escape log is empty")


class TestOpencodeConfig(unittest.TestCase):
    """opencode.json must be valid and declare a model."""

    @classmethod
    def setUpClass(cls):
        with open(ROOT / "opencode.json", encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_valid_json(self):
        self.assertIsInstance(self.data, dict)

    def test_has_model(self):
        self.assertIn("model", self.data)
        self.assertRegex(self.data["model"], r"^opencode/")

    def test_has_schema(self):
        self.assertIn("$schema", self.data)
        self.assertIn("opencode.ai", self.data["$schema"])


@unittest.skipIf(yaml is None, "PyYAML not available")
class TestWorkflow(unittest.TestCase):
    """GitHub Actions workflows must parse and define jobs."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(
            (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
        )

    def test_has_name(self):
        self.assertIn("name", self.workflow)

    def test_has_trigger(self):
        triggers = self.workflow.get("on") or self.workflow.get(True) or {}
        self.assertTrue(
            any(k in triggers for k in ["schedule", "push", "issues", "pull_request", "workflow_dispatch"]),
            "workflow has no trigger",
        )

    def test_has_jobs(self):
        self.assertGreater(len(self.workflow.get("jobs", {})), 0)

    def test_permissions_write(self):
        for job in self.workflow.get("jobs", {}).values():
            perms = job.get("permissions", {})
            self.assertIn("contents", perms)
            self.assertIn(perms["contents"], ["write", "read"])


if __name__ == "__main__":
    unittest.main(verbosity=2)