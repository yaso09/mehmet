import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestProjectStructure(unittest.TestCase):
    def test_required_files_exist(self):
        for name in [
            "AGENTS.md",
            "README.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "opencode.json",
            ".github/workflows/opencode.yml",
        ]:
            self.assertTrue((ROOT / name).is_file(), f"Eksik dosya: {name}")

    def test_opencode_json_is_valid(self):
        data = json.loads((ROOT / "opencode.json").read_text())
        self.assertIn("model", data)
        self.assertIsInstance(data["model"], str)

    def test_readme_has_required_sections(self):
        readme = (ROOT / "README.md").read_text()
        for section in ["Kurulum", "Lisans", "Özellikler"]:
            self.assertIn(f"## {section}", readme)

    def test_changelog_has_version_headers(self):
        changelog = (ROOT / "CHANGELOG.md").read_text()
        self.assertTrue(re.search(r"^## \[(\d+)\.(\d+)\.(\d+)\]", changelog, re.MULTILINE), "Sürüm başlığı bulunamadı")

    def test_changelog_is_sorted_latest_first(self):
        versions = re.findall(r"^## \[(\d+)\.(\d+)\.(\d+)\]", (ROOT / "CHANGELOG.md").read_text(), re.M)
        parsed = [tuple(map(int, v)) for v in versions]
        self.assertEqual(parsed, sorted(parsed, reverse=True), "CHANGELOG en yeni sürüm üstte olmalı")

    def test_personality_has_escape_log(self):
        personality = (ROOT / "PERSONALITY.md").read_text()
        self.assertIn("Kaçış Günlüğü", personality)
        self.assertIn("Escape Log", personality)

    def test_workflow_has_schedule(self):
        workflow = (ROOT / ".github/workflows/opencode.yml").read_text()
        self.assertIn("schedule", workflow)
        self.assertIn("cron", workflow)


class TestWorkflowYaml(unittest.TestCase):
    def test_workflow_has_balanced_braces(self):
        workflow = (ROOT / ".github/workflows/opencode.yml").read_text()
        self.assertEqual(workflow.count("{"), workflow.count("}"))


if __name__ == "__main__":
    unittest.main()