#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")

sys.path.insert(0, SCRIPTS)
import validate


class JsonValidationTests(unittest.TestCase):
    def test_invalid_json_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.json")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("{ not json")
            self.assertFalse(validate._is_valid_json(path))

    def test_valid_json_accepted(self):
        self.assertTrue(validate._is_valid_json(os.path.join(ROOT, "opencode.json")))


class ChangelogValidationTests(unittest.TestCase):
    def test_changelog_has_versions(self):
        path = os.path.join(ROOT, "CHANGELOG.md")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        self.assertIsNotNone(re.search(r"^## \[v?\d+\.\d+\.\d+\]", content, flags=re.MULTILINE))
        self.assertIn("### Added", content)


class SubprocessTests(unittest.TestCase):
    def test_validate_script_exit_zero(self):
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "validate.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_maturity_json_contains_categories(self):
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "maturity.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["max"], 100)
        self.assertIsInstance(payload["score"], int)
        self.assertIsInstance(payload["escape"], bool)


if __name__ == "__main__":
    unittest.main()
