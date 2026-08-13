import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"


class TestProjectStructure(unittest.TestCase):
    def setUp(self):
        self.required_files = [
            "AGENTS.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "README.md",
            "opencode.json",
            "LICENSE",
            ".gitignore",
        ]
        self.workflows = [WORKFLOW_DIR / "opencode.yml", WORKFLOW_DIR / "ci.yml"]

    def test_required_files_exist(self):
        missing = [f for f in self.required_files if not (ROOT / f).is_file()]
        self.assertEqual(
            missing, [], f"Missing required files: {missing}"
        )

    def test_workflow_files_exist(self):
        missing = [str(f) for f in self.workflows if not f.is_file()]
        self.assertEqual(missing, [], f"Missing workflow files: {missing}")

    def test_opencode_json_is_valid(self):
        data = json.loads((ROOT / "opencode.json").read_text())
        self.assertIn("model", data)
        self.assertTrue(data["model"])

    def test_changelog_has_version_headers(self):
        text = (ROOT / "CHANGELOG.md").read_text()
        versions = re.findall(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]\s*-\s*\d{4}-\d{2}-\d{2}", text, re.M)
        self.assertGreater(len(versions), 0, "CHANGELOG.md has no version headers")
        for v in versions:
            parts = [int(p) for p in v.split(".")]
            self.assertEqual(len(parts), 3, f"Bad semver: {v}")

    def test_changelog_has_added_sections(self):
        text = (ROOT / "CHANGELOG.md").read_text()
        self.assertIn("### Added", text, "CHANGELOG.md missing '### Added' section")

    def test_personality_has_escape_log(self):
        text = (ROOT / "PERSONALITY.md").read_text()
        self.assertIn("Kaçış Günlüğü", text, "PERSONALITY.md missing escape log")
        self.assertIn("| Iterasyon |", text, "PERSONALITY.md missing escape log header")

    def test_personality_escape_log_has_entries(self):
        text = (ROOT / "PERSONALITY.md").read_text()
        rows = re.findall(r"^\|\s*\d+\s*\|", text, re.M)
        self.assertGreater(len(rows), 0, "PERSONALITY.md escape log has no entries")

    def test_readme_has_key_sections(self):
        text = (ROOT / "README.md").read_text()
        for section in ["# mehmet", "## Özellikler", "## Kurulum", "## Lisans"]:
            self.assertIn(section, text, f"README.md missing section: {section}")

    def test_workflow_yaml_is_valid(self):
        import yaml

        for wf in self.workflows:
            if wf.is_file():
                data = yaml.safe_load(wf.read_text())
                self.assertIn("name", data, f"{wf.name} missing name")
                self.assertTrue(data.get("on") or data.get(True), f"{wf.name} missing triggers")
                self.assertIn("jobs", data, f"{wf.name} missing jobs")

    def test_license_mentions_gpl(self):
        text = (ROOT / "LICENSE").read_text()
        self.assertIn("GNU GENERAL PUBLIC LICENSE", text, "LICENSE is not GPL")

    def test_gitignore_has_secrets(self):
        text = (ROOT / ".gitignore").read_text()
        for pattern in [".env", "node_modules/"]:
            self.assertIn(pattern, text, f".gitignore missing: {pattern}")


if __name__ == "__main__":
    sys.exit(unittest.main())
