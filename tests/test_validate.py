"""Tests for scripts/validate.py using only the standard library."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate


class TestValidateScript(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in validate.REQUIRED_FILES if not (validate.ROOT / f).exists()]
        self.assertEqual(missing, [])

    def test_opencode_json_is_valid_and_has_model(self):
        cfg = json.loads(validate.file_text("opencode.json"))
        self.assertIn("model", cfg)

    def test_readme_has_all_sections(self):
        readme = validate.file_text("README.md")
        self.assertTrue(all(s in readme for s in validate.README_SECTIONS))

    def test_changelog_has_version_section(self):
        changelog = validate.file_text("CHANGELOG.md")
        self.assertIsNotNone(validate.CHANGELOG_VERSION_PATTERN.search(changelog))

    def test_personality_has_escape_log(self):
        personality = validate.file_text("PERSONALITY.md")
        self.assertTrue(all(a in personality for a in validate.PERSONALITY_ANCHORS))

    def test_agents_md_has_rules(self):
        agents = validate.file_text("AGENTS.md")
        self.assertIn("Simülasyon", agents)
        self.assertIn("Kurallar", agents)

    def test_workflow_has_both_jobs(self):
        workflow = validate.file_text(".github/workflows/opencode.yml")
        self.assertTrue(all(f"{job}:" in workflow for job in validate.WORKFLOW_JOBS))

    def test_full_validation_passes(self):
        _, ok = validate.run_checks()
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
