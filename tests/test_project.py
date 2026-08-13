#!/usr/bin/env python3
"""Proje yapısı bütünlük testleri."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CORE_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "LICENSE",
    "opencode.json",
    "Makefile",
]

WORKFLOWS = [
    ".github/workflows/opencode.yml",
    ".github/workflows/validate.yml",
]


class TestProjectStructure(unittest.TestCase):
    def test_core_files_exist(self):
        missing = [f for f in CORE_FILES if not (ROOT / f).is_file()]
        self.assertEqual(missing, [], f"Eksik temel dosyalar: {missing}")

    def test_workflows_exist(self):
        missing = [f for f in WORKFLOWS if not (ROOT / f).is_file()]
        self.assertEqual(missing, [], f"Eksik workflow dosyaları: {missing}")

    def test_opencode_json_is_valid(self):
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", data)
        self.assertTrue(data["model"].startswith("opencode/"))

    def test_changelog_has_versions(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(content, r"## \[\d+\.\d+\.\d+\]")

    def test_readme_has_sections(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Özellikler", content)
        self.assertIn("## Kurulum", content)

    def test_personality_has_escape_log(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", content)
        self.assertRegex(content, r"\|\s*\d+\s*\|")

    def test_scripts_executable(self):
        script = ROOT / "scripts" / "maturity.py"
        self.assertTrue(script.is_file())
        self.assertTrue(script.stat().st_mode & 0o111, "maturity.py executable olmalı")

    def test_workflows_are_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML kurulu değil")
        for path in WORKFLOWS:
            with self.subTest(path=path):
                yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))

    def test_workflow_has_schedule(self):
        import yaml

        class GitHubLoader(yaml.SafeLoader):
            pass

        GitHubLoader.add_constructor(
            "tag:yaml.org,2002:bool",
            lambda loader, node: loader.construct_scalar(node),
        )

        with open(ROOT / WORKFLOWS[0], encoding="utf-8") as fh:
            data = yaml.load(fh, Loader=GitHubLoader)
        self.assertIn("schedule", data["on"])


if __name__ == "__main__":
    unittest.main()
