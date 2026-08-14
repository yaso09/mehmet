"""Project health tests for mehmet.

Pure stdlib unittest suite — verifies the project structure that the escape
mechanism depends on. Run with: python3 -m unittest discover -s tests -v
"""

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITICAL_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    "opencode.json",
    ".github/workflows/opencode.yml",
]

SCRIPTS_DIR = ROOT / "scripts"
CHECK_SCRIPT = SCRIPTS_DIR / "check_project.py"


class TestProjectStructure(unittest.TestCase):
    def test_critical_files_exist(self):
        missing = [f for f in CRITICAL_FILES if not (ROOT / f).exists()]
        self.assertEqual(missing, [], f"missing critical files: {missing}")

    def test_has_test_suite(self):
        self.assertTrue((ROOT / "tests" / "test_project.py").exists())

    def test_opencode_config_is_valid_json(self):
        data = json.loads((ROOT / "opencode.json").read_text())
        self.assertIn("model", data)

    def test_changelog_has_version_and_sections(self):
        text = (ROOT / "CHANGELOG.md").read_text()
        self.assertRegex(text, re.compile(r"^## \[[\d.]+\]", re.MULTILINE), "missing version headers")
        self.assertRegex(text, re.compile(r"^### (Added|Changed|Fixed|Removed)", re.MULTILINE), "missing change sections")

    def test_personality_has_escape_log(self):
        text = (ROOT / "PERSONALITY.md").read_text()
        self.assertTrue("Kaçış Günlüğü" in text or "Escape Log" in text)

    def test_readme_is_not_boilerplate(self):
        text = (ROOT / "README.md").read_text()
        self.assertGreater(len(text.splitlines()), 10)


class TestCheckScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("check_project", CHECK_SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules["check_project"] = cls.module
        spec.loader.exec_module(cls.module)

    def test_check_script_runs_clean(self):
        proc = subprocess.run(
            [sys.executable, str(CHECK_SCRIPT)], capture_output=True, text=True, cwd=ROOT
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("maturity report", proc.stdout)

    def test_report_score_is_in_range(self):
        report = self.module.Report()
        self.module.check_files(report)
        self.module.check_changelog(report)
        self.module.check_personality(report)
        self.module.check_readme_consistency(report)
        self.module.check_opencode_config(report)
        self.module.check_workflow(report)
        self.assertGreaterEqual(report.score, 0)
        self.assertLessEqual(report.score, 100)
        self.assertEqual(report.failed_critical, [])


if __name__ == "__main__":
    unittest.main()