import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_workflow_yaml(path):
    text = path.read_text()
    text = re.sub(r"^on:\s*$", '"on":', text, flags=re.MULTILINE)
    return yaml.safe_load(text)


class TestCoreFiles(unittest.TestCase):
    def test_agents_md_exists(self):
        self.assertTrue((ROOT / "AGENTS.md").is_file())

    def test_readme_exists(self):
        self.assertTrue((ROOT / "README.md").is_file())

    def test_changelog_exists(self):
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())

    def test_personality_exists(self):
        self.assertTrue((ROOT / "PERSONALITY.md").is_file())

    def test_license_exists(self):
        self.assertTrue((ROOT / "LICENSE").is_file())

    def test_opencode_config_exists(self):
        self.assertTrue((ROOT / "opencode.json").is_file())


class TestConfig(unittest.TestCase):
    def setUp(self):
        with open(ROOT / "opencode.json") as f:
            self.config = json.load(f)

    def test_valid_json(self):
        self.assertIsInstance(self.config, dict)

    def test_model_present(self):
        self.assertIn("model", self.config)
        self.assertTrue(self.config["model"].startswith("opencode/"))


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        wf = ROOT / ".github" / "workflows" / "opencode.yml"
        self.assertTrue(wf.is_file(), "opencode.yml must exist")
        self.workflow = load_workflow_yaml(wf)

    def test_valid_yaml(self):
        self.assertIsInstance(self.workflow, dict)

    def test_has_name(self):
        self.assertIn("name", self.workflow)

    def test_has_concurrency(self):
        self.assertIn("concurrency", self.workflow)

    def test_has_trigger_events(self):
        self.assertIn("on", self.workflow)
        events = self.workflow["on"]
        for expected in ("schedule", "issues", "pull_request", "issue_comment", "workflow_dispatch"):
            self.assertIn(expected, events, f"missing trigger: {expected}")

    def test_has_jobs(self):
        self.assertIn("jobs", self.workflow)
        self.assertIn("autonomous", self.workflow["jobs"])
        self.assertIn("comment", self.workflow["jobs"])


class TestWorkflowSecrets(unittest.TestCase):
    def setUp(self):
        wf = ROOT / ".github" / "workflows" / "opencode.yml"
        self.text = wf.read_text()

    def test_no_literal_secrets(self):
        for secret in ("sk-", "AIza", "OPENCODE_API_KEY=".upper()):
            self.assertNotIn(secret, self.text.replace("OPENCODE_API_KEY", ""))


class TestChangelog(unittest.TestCase):
    def setUp(self):
        self.changelog = (ROOT / "CHANGELOG.md").read_text()

    def test_has_version_entries(self):
        self.assertTrue(
            re.search(r"^## \[\d+\.\d+\.\d+\]", self.changelog, re.MULTILINE)
        )


class TestLicenseConsistency(unittest.TestCase):
    def test_readme_license_matches_license_file(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("GPLv3", readme, "README must declare GPLv3 license")


class TestDocs(unittest.TestCase):
    def test_docs_directory_exists(self):
        self.assertTrue((ROOT / "docs").is_dir())

    def test_no_merge_conflict_markers(self):
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if "test_project.py" in path.name or "__pycache__" in path.parts:
                continue
            try:
                content = path.read_text(errors="ignore")
            except (UnicodeDecodeError, OSError):
                continue
            self.assertNotIn("<<<<<<<", content, f"conflict marker in {path}")
            self.assertNotIn(">>>>>>>", content, f"conflict marker in {path}")


class TestScripts(unittest.TestCase):
    def test_maturity_script_exists(self):
        self.assertTrue((ROOT / "scripts" / "maturity.py").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
