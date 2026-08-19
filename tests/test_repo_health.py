#!/usr/bin/env python3
"""mehmet repo_health modülü için unit testler."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import repo_health


class RepoHealthTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = self.tmpdir.name
        self.addCleanup(self.tmpdir.cleanup)

    def write(self, relpath, content=""):
        path = os.path.join(self.root, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return path

    def make_healthy(self):
        self.write("AGENTS.md", "# Simülasyon\n")
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [0.1.0] - 2026-01-01\n\n### Added\n- test\n",
        )
        self.write(
            "PERSONALITY.md",
            "# Personality\n\n## Kaçış Günlüğü\n\n| Iterasyon | Tarih | İlerleme |\n",
        )
        self.write("README.md", "# mehmet\n\nProje açıklaması\n")
        self.write("LICENSE", "GPLv3\n")
        self.write("opencode.json", json.dumps({"model": "opencode/test"}))
        self.write(".github/workflows/opencode.yml", "name: mehmet\n")

    def test_required_files_missing(self):
        self.make_healthy()
        os.remove(os.path.join(self.root, "README.md"))
        with self.assertRaises(repo_health.HealthError) as ctx:
            repo_health.check_required_files(self.root)
        self.assertIn("README.md", str(ctx.exception))

    def test_changelog_ok(self):
        self.make_healthy()
        repo_health.check_changelog(self.root)

    def test_changelog_invalid_version(self):
        self.make_healthy()
        self.write("CHANGELOG.md", "# Changelog\n\n## degisiklikler\n")
        with self.assertRaises(repo_health.HealthError):
            repo_health.check_changelog(self.root)

    def test_opencode_json_ok(self):
        self.make_healthy()
        repo_health.check_opencode_json(self.root)

    def test_opencode_json_missing_model(self):
        self.make_healthy()
        self.write("opencode.json", json.dumps({"foo": "bar"}))
        with self.assertRaises(repo_health.HealthError):
            repo_health.check_opencode_json(self.root)

    def test_opencode_json_unknown_key(self):
        self.make_healthy()
        self.write(
            "opencode.json",
            json.dumps({"model": "opencode/test", "skip": True, "enable": True}),
        )
        with self.assertRaises(repo_health.HealthError) as ctx:
            repo_health.check_opencode_json(self.root)
        self.assertIn("skip", str(ctx.exception))
        self.assertIn("enable", str(ctx.exception))

    def test_opencode_json_invalid(self):
        self.make_healthy()
        self.write("opencode.json", "bu json degil {")
        with self.assertRaises(json.JSONDecodeError):
            repo_health.check_opencode_json(self.root)

    def test_personality_escape_log(self):
        self.make_healthy()
        repo_health.check_personality(self.root)

    def test_personality_no_escape_log(self):
        self.make_healthy()
        self.write("PERSONALITY.md", "# Personality\n")
        with self.assertRaises(repo_health.HealthError):
            repo_health.check_personality(self.root)

    def test_readme_ok(self):
        self.make_healthy()
        repo_health.check_readme(self.root)

    def test_readme_missing_project_name(self):
        self.make_healthy()
        self.write("README.md", "Baska bir proje\n")
        with self.assertRaises(repo_health.HealthError):
            repo_health.check_readme(self.root)

    def test_no_secrets(self):
        self.make_healthy()
        self.write("app.py", "OPENCODE_API_KEY = 'gizli-deger-buraya'")
        with self.assertRaises(repo_health.HealthError) as ctx:
            repo_health.check_no_secrets(self.root)
        self.assertIn("app.py", str(ctx.exception))

    def test_github_actions_secret_placeholder_ok(self):
        self.make_healthy()
        self.write(
            ".github/workflows/opencode.yml",
            "env:\n  OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}\n",
        )
        repo_health.check_no_secrets(self.root)

    def test_main_all_pass(self):
        self.make_healthy()
        exit_code = repo_health.main(["--root", self.root])
        self.assertEqual(exit_code, 0)

    def test_main_failure(self):
        self.make_healthy()
        os.remove(os.path.join(self.root, "LICENSE"))
        exit_code = repo_health.main(["--root", self.root])
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
