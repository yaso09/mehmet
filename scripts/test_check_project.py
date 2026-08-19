#!/usr/bin/env python3
"""Unit tests for scripts/check_project.py.

Run with: python3 -m unittest scripts.test_check_project
or:       python3 -m unittest discover scripts
"""

import json
import tempfile
import unittest
from pathlib import Path

import check_project as cp


class HelperTests(unittest.TestCase):
    def test_valid_json_with_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "opencode.json"
            p.write_text(json.dumps({"model": "opencode/deepseek-v4-flash-free"}))
            ok, detail = cp._valid_opencode_json(p)
            self.assertTrue(ok)
            self.assertEqual(detail, "opencode/deepseek-v4-flash-free")

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "opencode.json"
            p.write_text("{not valid json")
            ok, _ = cp._valid_opencode_json(p)
            self.assertFalse(ok)

    def test_json_missing_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "opencode.json"
            p.write_text("{}")
            ok, _ = cp._valid_opencode_json(p)
            self.assertFalse(ok)

    def test_has_all_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "changelog.md"
            p.write_text("### Added\n### Fixed\n")
            ok, _ = cp._has_all_sections(p, cp.MANDATORY_CHANGELOG_SECTIONS)
            self.assertTrue(ok)

    def test_missing_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "changelog.md"
            p.write_text("### Added\n")
            ok, detail = cp._has_all_sections(p, cp.MANDATORY_CHANGELOG_SECTIONS)
            self.assertFalse(ok)
            self.assertIn("### Fixed", detail)

    def test_non_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "readme.md"
            p.write_text("hello")
            ok, _ = cp._non_empty(p)
            self.assertTrue(ok)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "readme.md"
            p.write_text("")
            ok, _ = cp._non_empty(p)
            self.assertFalse(ok)

    def test_workflow_has_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "wf.yml"
            p.write_text("jobs:\n  autonomous:\n    runs-on: ubuntu-latest\n")
            ok, _ = cp._yaml_has_jobs(p)
            self.assertTrue(ok)

    def test_workflow_missing_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "wf.yml"
            p.write_text("name: nothing\n")
            ok, _ = cp._yaml_has_jobs(p)
            self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()