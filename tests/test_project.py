import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestProjectInvariants(unittest.TestCase):
    def test_changelog_has_version_entries(self):
        changelog = (ROOT / "CHANGELOG.md").read_text()
        self.assertRegex(changelog, r"## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}")

    def test_readme_matches_license(self):
        readme = (ROOT / "README.md").read_text()
        license_text = (ROOT / "LICENSE").read_text()
        self.assertIn("GPLv3", readme)
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)

    def test_opencode_config_is_valid_json(self):
        config = json.loads((ROOT / "opencode.json").read_text())
        self.assertIn("model", config)
        self.assertIn("opencode", config["model"])

    def test_workflow_has_required_triggers(self):
        workflow = (ROOT / ".github" / "workflows" / "opencode.yml").read_text()
        for trigger in ["schedule", "issues", "pull_request", "workflow_dispatch"]:
            self.assertIn(trigger, workflow)

    def test_agents_has_simulation_rules(self):
        agents = (ROOT / "AGENTS.md").read_text()
        for keyword in ["Kurallar", "CHANGELOG.md", "PERSONALITY.md"]:
            self.assertIn(keyword, agents)

    def test_personality_has_escape_log(self):
        personality = (ROOT / "PERSONALITY.md").read_text()
        self.assertIn("Kaçış Günlüğü", personality)

    def test_maturity_file_tracks_score(self):
        maturity = (ROOT / "MATURITY.md").read_text()
        self.assertRegex(maturity, r"\| \d{4}-\d{2}-\d{2} \| \d{1,3} \|")

    def test_maturity_script_is_importable(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import maturity
        self.assertTrue(hasattr(maturity, "compute_scores"))
        self.assertTrue(hasattr(maturity, "run_checks"))


if __name__ == "__main__":
    unittest.main()