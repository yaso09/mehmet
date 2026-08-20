"""Validate the GitHub Actions workflow file."""
import unittest

from tests import read_text, try_import_yaml

WORKFLOW = ".github/workflows/opencode.yml"


@unittest.skipUnless(try_import_yaml(), "PyYAML not installed")
class TestWorkflow(unittest.TestCase):
    def setUp(self):
        yaml = try_import_yaml()
        text = read_text(WORKFLOW)
        self.workflow = yaml.safe_load(text)

    def test_workflow_parses(self):
        self.assertIsInstance(self.workflow, dict)
        self.assertEqual(self.workflow.get("name"), "mehmet")

    def test_has_schedule(self):
        # YAML 1.1 parses the bare key `on` as boolean True (PyYAML gotcha).
        on = self.workflow.get("on") or self.workflow.get(True) or {}
        self.assertIn("schedule", on)
        crons = [s.get("cron") for s in on["schedule"]]
        self.assertIn("*/10 * * * *", crons)

    def test_has_both_jobs(self):
        jobs = self.workflow.get("jobs", {})
        self.assertIn("autonomous", jobs)
        self.assertIn("comment", jobs)

    def test_autonomous_job_uses_opencode_action(self):
        steps = self.workflow["jobs"]["autonomous"]["steps"]
        self.assertTrue(
            any("actions/checkout" in s["uses"] for s in steps),
            "workflow must checkout the repo",
        )
        self.assertTrue(
            any("opencode/github" in s["uses"] for s in steps),
            "workflow must use the opencode action",
        )

    def test_concurrency_control(self):
        self.assertIn("concurrency", self.workflow)
        self.assertEqual(self.workflow["concurrency"].get("cancel-in-progress"), True)

    def test_permissions_include_write(self):
        perms = self.workflow["jobs"]["autonomous"].get("permissions", {})
        for scope in ("contents", "pull-requests", "issues"):
            self.assertEqual(perms.get(scope), "write", f"missing write permission: {scope}")


if __name__ == "__main__":
    unittest.main()
