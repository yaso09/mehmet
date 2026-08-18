import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestProjectIntegrity(unittest.TestCase):
    def test_opencode_json_valid_and_model(self):
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertEqual(cfg["model"], "opencode/deepseek-v4-flash-free")

    def test_changelog_has_semver_entries(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(re.search(r"^## \[\d+\.\d+\.\d+\]", content, re.MULTILINE))

    def test_escape_log_present(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", content)

    def test_workflow_files_exist(self):
        self.assertTrue((ROOT / ".github/workflows/opencode.yml").exists())
        self.assertTrue((ROOT / ".github/workflows/ci.yml").exists())

    def test_validate_script_runs_clean(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate.py")], capture_output=True
        )
        self.assertEqual(
            result.returncode, 0,
            msg=result.stdout.decode() + result.stderr.decode(),
        )

    def test_readme_has_core_sections(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        for section in ("Özellikler", "Kurulum", "Lisans"):
            self.assertIn(section, content)


if __name__ == "__main__":
    unittest.main()