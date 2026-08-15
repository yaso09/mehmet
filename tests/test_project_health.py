import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CORE_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
]


class TestProjectHealth(unittest.TestCase):
    def test_core_files_exist(self):
        for name in CORE_FILES:
            self.assertTrue((ROOT / name).exists(), f"{name} eksik")

    def test_main_workflow_exists(self):
        self.assertTrue((ROOT / ".github/workflows/opencode.yml").exists())

    def test_healthcheck_workflow_exists(self):
        self.assertTrue((ROOT / ".github/workflows/healthcheck.yml").exists())

    def test_changelog_has_version_entries(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [", content)

    def test_opencode_config_is_valid_json(self):
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", data)

    def test_docs_directory_exists(self):
        self.assertTrue((ROOT / "docs").is_dir())

    def test_maturity_system_present(self):
        self.assertTrue((ROOT / "scripts/maturity.py").exists())
        self.assertTrue((ROOT / "MATURITY.md").exists())

    def test_scripts_compile(self):
        for p in (ROOT / "scripts").glob("*.py"):
            compile(p.read_text(encoding="utf-8"), str(p), "exec")

    def test_readme_has_license(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GPLv3", content)

    def test_personality_has_escape_log(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertTrue("kaçış" in content.lower() or "escape" in content.lower())

    def test_workflow_uses_secret_not_plain_value(self):
        content = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
        self.assertIn("secrets.OPENCODE_API_KEY", content)


if __name__ == "__main__":
    unittest.main()