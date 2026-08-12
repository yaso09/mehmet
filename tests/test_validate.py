#!/usr/bin/env python3
"""Unit tests for scripts/validate.py."""

import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from validate import validate

BASE_FILES = {
    "AGENTS.md": "# Simulation\n",
    "README.md": "# mehmet\n\n## Lisans\n\nGPLv3\n",
    "CHANGELOG.md": "# Changelog\n\n## [0.1.0] - 2026-07-04\n\n### Added\n- init\n",
    "PERSONALITY.md": "# Personality\n",
    "LICENSE": "GNU GENERAL PUBLIC LICENSE Version 3\n",
    ".gitignore": "node_modules/\n",
    "opencode.json": '{"model": "opencode/deepseek-v4-flash-free"}\n',
}


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for name, content in BASE_FILES.items():
            self._write(name, content)
        wf_dir = os.path.join(self.tmp, ".github", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        self._write(os.path.join(".github", "workflows", "opencode.yml"),
                    "name: mehmet\non: {workflow_dispatch: {}}\njobs: {}\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, rel, content):
        path = os.path.join(self.tmp, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    def test_clean_project_no_errors(self):
        errors, _ = validate(self.tmp)
        self.assertEqual(errors, [])

    def test_missing_required_file(self):
        os.remove(os.path.join(self.tmp, "AGENTS.md"))
        errors, _ = validate(self.tmp)
        self.assertTrue(any("AGENTS.md" in e for e in errors))

    def test_invalid_json(self):
        self._write("opencode.json", "{not json")
        errors, _ = validate(self.tmp)
        self.assertTrue(any("opencode.json" in e for e in errors))

    def test_invalid_yaml(self):
        self._write(os.path.join(".github", "workflows", "opencode.yml"), ":\n  - :\n")
        errors, _ = validate(self.tmp)
        self.assertTrue(any("opencode.yml" in e for e in errors))

    def test_secret_detection(self):
        fake_secret = "sk-" + ("a" * 40)
        self._write("secrets.txt", "api_key = '" + fake_secret + "'\n")
        errors, _ = validate(self.tmp)
        self.assertTrue(any("secrets.txt" in e for e in errors))

    def test_missing_workflow(self):
        os.remove(os.path.join(self.tmp, ".github", "workflows", "opencode.yml"))
        errors, _ = validate(self.tmp)
        self.assertTrue(any("opencode.yml" in e for e in errors))

    def test_license_mismatch_warns(self):
        self._write("README.md", "# mehmet\n\n## Lisans\n\nMIT\n")
        _, warnings = validate(self.tmp)
        self.assertTrue(any("README.md" in w for w in warnings))

    def test_bad_changelog_header_warns(self):
        self._write("CHANGELOG.md", "# Changelog\n\n## v1.0.0 bazı değişiklikler\n")
        _, warnings = validate(self.tmp)
        self.assertTrue(any("CHANGELOG.md" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()