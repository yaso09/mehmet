"""Unit tests for the mehmet project consistency checks.

Run with:  python -m unittest discover -s tests  (or: make test)
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from checks import (  # noqa: E402
    VERSION_RE,
    check_changelog,
    check_gitignore,
    check_license,
    check_opencode_config,
    check_personality,
    check_readme,
    check_required_files,
    check_workflow_triggers,
    check_workflows,
    run_checks,
)


class ConfigChecksTest(unittest.TestCase):
    def test_opencode_config_is_valid(self):
        res = check_opencode_config()
        self.assertTrue(res.ok, res.detail)

    def test_opencode_config_has_model(self):
        import json

        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", data)
        self.assertIn("/", data["model"])


class WorkflowChecksTest(unittest.TestCase):
    def test_workflows_are_valid(self):
        res = check_workflows()
        self.assertTrue(res.ok, res.detail)

    def test_autonomous_triggers_present(self):
        res = check_workflow_triggers()
        self.assertTrue(res.ok, res.detail)

    def test_ci_runs_tests(self):
        content = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("test", content.lower())


class DocsChecksTest(unittest.TestCase):
    def test_changelog_is_well_formed(self):
        res = check_changelog()
        self.assertTrue(res.ok, res.detail)

    def test_readme_complete(self):
        res = check_readme()
        self.assertTrue(res.ok, res.detail)

    def test_personality_has_escape_log(self):
        res = check_personality()
        self.assertTrue(res.ok, res.detail)

    def test_license_is_gpl3(self):
        res = check_license()
        self.assertTrue(res.ok, res.detail)


class HygieneChecksTest(unittest.TestCase):
    def test_required_files_exist(self):
        res = check_required_files()
        self.assertTrue(res.ok, res.detail)

    def test_gitignore_has_python_entries(self):
        res = check_gitignore()
        self.assertTrue(res.ok, res.detail)

    def test_all_checks_pass(self):
        results = run_checks()
        failed = [r.name for r in results if not r.ok]
        self.assertEqual([], failed, f"failing checks: {failed}")


class HelperTest(unittest.TestCase):
    def test_version_header_regex(self):
        self.assertTrue(VERSION_RE.match("## [1.2.3] - 2026-07-04"))
        self.assertFalse(VERSION_RE.match("## 1.2.3 - 2026-07-04"))
        self.assertFalse(VERSION_RE.match("## [x.y.z] - 2026-07-04"))

    def test_maturity_script_runs(self):
        from maturity import compute

        score = compute()
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)


if __name__ == "__main__":
    unittest.main()
