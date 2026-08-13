"""Tests for scripts/validate.py"""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate


class TestCheckerFunctions(unittest.TestCase):
    def setUp(self):
        self.result = validate.Result()

    def test_check_agents_md_passes(self):
        validate.check_agents_md(self.result)
        self.assertFalse(self.result.errors)

    def test_check_changelog_passes(self):
        validate.check_changelog(self.result)
        self.assertFalse(self.result.errors)

    def test_check_opencode_json_valid(self):
        validate.check_opencode_json(self.result)
        self.assertFalse(self.result.errors)

    def test_check_opencode_json_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opencode.json").write_text("{ nope", encoding="utf-8")
            with patch.object(validate, "ROOT", root):
                self.result = validate.Result()
                validate.check_opencode_json(self.result)
        self.assertTrue(any("opencode.json" in e for e in self.result.errors))

    def test_check_workflow_present(self):
        validate.check_workflow(self.result)
        self.assertFalse(self.result.errors)

    def test_check_readme_license_consistent(self):
        validate.check_readme_license(self.result)
        self.assertFalse(self.result.errors)

    def test_result_report_failure(self):
        self.result.fail("x", "broken")
        with redirect_stdout(io.StringIO()):
            code = self.result.report()
        self.assertEqual(code, 1)

    def test_result_report_success(self):
        self.result.ok("y")
        with redirect_stdout(io.StringIO()):
            code = self.result.report()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
