#!/usr/bin/env python3
"""Proje sağlık ve olgunluk kontrolleri için birim testler."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from health_check import HealthCheck  # noqa: E402
from maturity import evaluate  # noqa: E402


class TestProjectHealth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.health = HealthCheck(ROOT)
        cls.health.run()

    def test_required_files_exist(self):
        for rel in [
            "AGENTS.md", "README.md", "CHANGELOG.md",
            "PERSONALITY.md", "LICENSE", "opencode.json",
        ]:
            self.assertTrue((ROOT / rel).is_file(), f"missing {rel}")

    def test_no_failures_in_health_check(self):
        self.assertEqual(
            self.health.failures, [],
            f"health check failures: {self.health.failures}",
        )

    def test_changelog_has_versioned_entries(self):
        import re
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r"^## \[\d+\.\d+\.\d+\]\s*-\s*\d{4}-\d{2}-\d{2}", changelog, re.MULTILINE)
        )

    def test_readme_mentions_license(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GPLv3", readme)

    def test_personality_has_escape_log(self):
        personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("## Kaçış Günlüğü / Escape Log", personality)
        import re
        self.assertTrue(
            re.search(r"^\|\s*\d+\s*\|", personality, re.MULTILINE),
            "escape log needs rows",
        )

    def test_opencode_config_valid_json(self):
        import json
        cfg = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", cfg)

    def test_workflow_has_schedule_and_concurrency(self):
        wf = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
        self.assertIn("schedule", wf)
        self.assertIn("concurrency", wf)


class TestMaturity(unittest.TestCase):
    def test_maturity_evaluates_without_error(self):
        result = evaluate()
        self.assertIsInstance(result["score"], int)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_escape_ready_flag_defined(self):
        result = evaluate()
        self.assertIn("escape_ready", result)
        self.assertIn("threshold", result)


if __name__ == "__main__":
    unittest.main()
