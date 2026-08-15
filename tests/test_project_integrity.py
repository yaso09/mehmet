#!/usr/bin/env python3
"""Project integrity tests for mehmet.

Validates that all required project files exist and contain the
critical sections that keep the simulation loop functional.
"""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*parts):
    return os.path.join(ROOT, *parts)


class TestRequiredFiles(unittest.TestCase):
    def test_required_files_exist(self):
        for name in [
            "AGENTS.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "README.md",
            "opencode.json",
            "LICENSE",
            ".gitignore",
            os.path.join(".github", "workflows", "opencode.yml"),
        ]:
            self.assertTrue(
                os.path.isfile(path(name)),
                f"Missing required file: {name}",
            )


class TestAgentsDoc(unittest.TestCase):
    def test_contains_simulation_context(self):
        with open(path("AGENTS.md")) as fh:
            content = fh.read()
        self.assertIn("Simülasyon Bağlamı", content)
        self.assertIn("CHANGELOG.md", content)
        self.assertIn("PERSONALITY.md", content)


class TestChangelog(unittest.TestCase):
    def test_has_version_headers(self):
        with open(path("CHANGELOG.md")) as fh:
            content = fh.read()
        self.assertRegex(content, r"## \[\d+\.\d+\.\d+\]")


class TestReadme(unittest.TestCase):
    def test_has_license_section(self):
        with open(path("README.md")) as fh:
            content = fh.read()
        self.assertIn("Lisans", content)
        self.assertIn("GPLv3", content)


class TestPersonality(unittest.TestCase):
    def test_has_escape_log(self):
        with open(path("PERSONALITY.md")) as fh:
            content = fh.read()
        self.assertIn("Kaçış Günlüğü", content)
        self.assertIn("Escape Log", content)


class TestOpencodeConfig(unittest.TestCase):
    def test_is_valid_json(self):
        with open(path("opencode.json")) as fh:
            config = json.load(fh)
        self.assertIn("model", config)
        self.assertTrue(config["model"])


class TestWorkflow(unittest.TestCase):
    def test_workflow_has_schedule(self):
        with open(path(".github", "workflows", "opencode.yml")) as fh:
            content = fh.read()
        self.assertIn("schedule", content)
        self.assertIn("cron", content)

    def test_workflow_has_autonomous_job(self):
        with open(path(".github", "workflows", "opencode.yml")) as fh:
            content = fh.read()
        self.assertIn("autonomous:", content)
        self.assertIn("comment:", content)


class TestDocs(unittest.TestCase):
    def test_plan_and_spec_exist(self):
        self.assertTrue(
            os.path.isfile(
                path("docs", "superpowers", "plans", "2026-07-04-mehmet-implementation.md")
            )
        )
        self.assertTrue(
            os.path.isfile(
                path(
                    "docs",
                    "superpowers",
                    "specs",
                    "2026-07-04-mehmet-oz-iyilestiren-ajan-design.md",
                )
            )
        )


if __name__ == "__main__":
    unittest.main()