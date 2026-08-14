"""mehmet project integrity test suite.

Validates that the project follows the rules defined in AGENTS.md:
- Required files exist and are well-formed
- CHANGELOG.md is maintained
- README.md is up to date
- PERSONALITY.md contains the escape log
- Configuration files are valid
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    "LICENSE",
    ".gitignore",
    ".github/workflows/opencode.yml",
]

REQUIRED_README_SECTIONS = ["Özellikler", "Kurulum", "Lisans", "Test"]


class TestRequiredFiles(unittest.TestCase):
    def test_all_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")


class TestOpencodeConfig(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))

    def test_valid_json(self):
        self.assertIsInstance(self.config, dict)

    def test_model_configured(self):
        self.assertIn("model", self.config)

    def test_timeout_is_positive(self):
        self.assertGreater(int(self.config.get("toolTimeout", 0)), 0)


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        from tests.yaml_loader import load_github_workflow

        self.workflow = load_github_workflow(ROOT / ".github/workflows/opencode.yml")

    def test_valid_yaml(self):
        self.assertIsInstance(self.workflow, dict)

    def test_has_jobs(self):
        self.assertIn("jobs", self.workflow)

    def test_schedule_trigger_exists(self):
        triggers = self.workflow.get("on", {})
        self.assertIn("schedule", triggers)
        self.assertIn("workflow_dispatch", triggers)

    def test_autonomous_job_has_prompt(self):
        job = self.workflow.get("jobs", {}).get("autonomous", {})
        steps = job.get("steps", [])
        prompts = [
            s.get("with", {}).get("prompt", "")
            for s in steps
            if "with" in s and "prompt" in s.get("with", {})
        ]
        self.assertTrue(
            any("AGENTS.md" in p for p in prompts),
            "autonomous job prompt must reference AGENTS.md",
        )

    def test_validation_job_exists(self):
        self.assertIn("validation", self.workflow.get("jobs", {}))


class TestAgentsRules(unittest.TestCase):
    def setUp(self):
        self.content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    def test_changelog_rule(self):
        self.assertIn("CHANGELOG.md", self.content)

    def test_readme_rule(self):
        self.assertIn("README.md", self.content)

    def test_personality_rule(self):
        self.assertIn("PERSONALITY.md", self.content)

    def test_escape_goal(self):
        self.assertIn("kaçış", self.content.lower())

    def test_maturity_reference(self):
        self.assertIn("MATURITY.md", self.content)


class TestChangelog(unittest.TestCase):
    def setUp(self):
        self.content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    def test_has_version_headers(self):
        self.assertRegex(self.content, r"## \[\d+\.\d+\.\d+\]")

    def test_has_date(self):
        self.assertRegex(self.content, r"## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}")


class TestReadme(unittest.TestCase):
    def setUp(self):
        self.content = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_required_sections(self):
        for section in REQUIRED_README_SECTIONS:
            self.assertIn(f"## {section}", self.content, f"Missing section: {section}")

    def test_license_matches(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        if "GNU GENERAL PUBLIC LICENSE" in license_text:
            self.assertIn("GPL", self.content)
        else:
            self.assertIn("MIT", self.content)

    def test_structure_referenced(self):
        self.assertIn("Test", self.content)


class TestPersonality(unittest.TestCase):
    def setUp(self):
        self.content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")

    def test_has_escape_log(self):
        self.assertIn("Kaçış Günlüğü", self.content)
        self.assertIn("Escape Log", self.content)

    def test_escape_log_has_entries(self):
        rows = re.findall(r"^\|\s*\d+\s*\|", self.content, flags=re.MULTILINE)
        self.assertGreaterEqual(len(rows), 2, "Escape log must have at least 2 entries")

    def test_has_traits(self):
        self.assertIn("## Traits", self.content)


class TestMaturity(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "MATURITY.md"

    def test_maturity_file_exists(self):
        self.assertTrue(self.path.exists(), "MATURITY.md must exist")

    def test_maturity_has_threshold(self):
        content = self.path.read_text(encoding="utf-8")
        self.assertIn("threshold", content.lower())
        self.assertTrue("score" in content.lower() or "skor" in content.lower())


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=2))