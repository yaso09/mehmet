"""Validate GitHub Actions workflow files."""

import unittest

import yaml

from tests.helpers import ROOT, load_yaml

WORKFLOW = ".github/workflows/opencode.yml"


class TestWorkflow(unittest.TestCase):

    def test_workflow_is_valid_yaml(self):
        self.assertTrue(ROOT.joinpath(WORKFLOW).exists())
        self.assertIsInstance(load_yaml(WORKFLOW), dict)

    def test_workflow_has_schedule(self):
        data = load_yaml(WORKFLOW)
        events = data.get("on") or data.get(True) or {}
        self.assertIn("schedule", events)
        cron = events["schedule"]
        self.assertIn("cron", cron[0])

    def test_workflow_has_autonomous_job(self):
        data = load_yaml(WORKFLOW)
        self.assertIn("autonomous", data.get("jobs", {}))
        steps = data["jobs"]["autonomous"].get("steps", [])
        self.assertTrue(any("uses" in s for s in steps))

    def test_workflow_uses_api_key_secret(self):
        data = load_yaml(WORKFLOW)
        text = yaml.safe_dump(data)
        self.assertIn("OPENCODE_API_KEY", text)
        self.assertIn("secrets.OPENCODE_API_KEY", text)

    def test_workflow_has_comment_job(self):
        data = load_yaml(WORKFLOW)
        self.assertIn("comment", data.get("jobs", {}))


if __name__ == "__main__":
    unittest.main()