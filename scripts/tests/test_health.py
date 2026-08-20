#!/usr/bin/env python3
"""Unit tests for scripts/mehmet_health.py."""

import json
import os
import sys
import tempfile
import unittest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)

import mehmet_health as health  # noqa: E402


def make_repo(files):
    """Create a temporary repo populated with the given {rel_path: content}."""
    tmp = tempfile.mkdtemp(prefix="mehmet-test-")
    for rel, content in files.items():
        path = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return tmp


BASE_FILES = {
    "AGENTS.md": "# Simülasyon Bağlamı\n\nKurallar ve hedefler.\n",
    "README.md": "# mehmet\n\n## Özellikler\n\n## Kurulum\n\n## Lisans\n",
    "CHANGELOG.md": "# Changelog\n\n## [0.3.0] - 2026-08-20\n\n- change\n",
    "PERSONALITY.md": "# Personality\n\n| Iterasyon | Tarih | İlerleme |\n|---|---|---|\n| 1 | 2026-07-04 | başlangıç |\n",
    "LICENSE": "GNU GENERAL PUBLIC LICENSE\n" * 10,
    "opencode.json": '{"model": "opencode/deepseek-v4-flash-free"}',
    "VERSION": "0.3.0\n",
    ".github/workflows/opencode.yml": "name: mehmet\non: [workflow_dispatch]\n",
    "scripts/mehmet_health.py": "# exists\n",
    "scripts/tests/test_health.py": "# exists\n",
}


class CheckFunctionsTest(unittest.TestCase):
    def test_required_file_missing(self):
        repo = make_repo({})
        result = health.check_file(repo, "AGENTS.md")
        self.assertFalse(result["ok"])
        self.assertEqual(result["detail"], "missing")

    def test_required_file_trivial(self):
        repo = make_repo({"AGENTS.md": "x\n"})
        result = health.check_file(repo, "AGENTS.md")
        self.assertFalse(result["ok"])
        self.assertEqual(result["detail"], "too trivial")

    def test_required_file_ok(self):
        repo = make_repo({"AGENTS.md": "meaningful content here\n"})
        result = health.check_file(repo, "AGENTS.md")
        self.assertTrue(result["ok"])

    def test_changelog_missing_versions(self):
        repo = make_repo({"CHANGELOG.md": "# Changelog\nno versions\n"})
        result = health.check_changelog(repo)
        self.assertFalse(result["ok"])

    def test_changelog_with_version(self):
        repo = make_repo({"CHANGELOG.md": "# Changelog\n## [1.2.3] - 2026-01-01\n- x\n"})
        result = health.check_changelog(repo)
        self.assertTrue(result["ok"])
        self.assertEqual(result["detail"], "1 versioned entries")

    def test_personality_log_empty(self):
        repo = make_repo({"PERSONALITY.md": "# Personality\n"})
        result = health.check_personality_log(repo)
        self.assertFalse(result["ok"])

    def test_personality_log_has_row(self):
        repo = make_repo({"PERSONALITY.md": "# P\n\n| 1 | 2026-01-01 | ilerleme |\n"})
        result = health.check_personality_log(repo)
        self.assertTrue(result["ok"])

    def test_readme_missing_sections(self):
        repo = make_repo({"README.md": "# mehmet\n"})
        result = health.check_readme(repo)
        self.assertFalse(result["ok"])

    def test_readme_complete(self):
        repo = make_repo({"README.md": "# mehmet\n## Özellikler\n## Kurulum\n## Lisans\n"})
        result = health.check_readme(repo)
        self.assertTrue(result["ok"])

    def test_config_invalid_json(self):
        repo = make_repo({"opencode.json": "{not json"})
        result = health.check_config(repo)
        self.assertFalse(result["ok"])

    def test_config_valid(self):
        repo = make_repo({"opencode.json": '{"model": "foo"}'})
        result = health.check_config(repo)
        self.assertTrue(result["ok"])

    def test_workflow_missing(self):
        repo = make_repo({})
        result = health.check_workflow(repo)
        self.assertFalse(result["ok"])

    def test_version_valid_and_invalid(self):
        good = make_repo({"VERSION": "1.2.3\n"})
        self.assertTrue(health.check_versioning(good)["ok"])
        bad = make_repo({"VERSION": "banana\n"})
        self.assertFalse(health.check_versioning(bad)["ok"])


class ScoringTest(unittest.TestCase):
    def test_full_project_scores_high(self):
        repo = make_repo(BASE_FILES)
        results = health.run_checks(repo)
        self.assertEqual(len(results), len(health.CHECKS))
        score, _breakdown = health.compute_score(results)
        self.assertGreaterEqual(score, 80)

    def test_empty_repo_scores_low(self):
        repo = make_repo({})
        results = health.run_checks(repo)
        score, _breakdown = health.compute_score(results)
        self.assertLess(score, 50)

    def test_report_build_and_write(self):
        repo = make_repo(BASE_FILES)
        report = health.build_report(repo)
        self.assertIn("score", report)
        self.assertIn("breakdown", report)
        path = health.write_report(repo, report, "docs/health-report.md")
        self.assertTrue(os.path.isfile(path))
        with open(path, encoding="utf-8") as fh:
            self.assertIn("# mehmet Health Report", fh.read())

    def test_main_json_output(self):
        repo = make_repo(BASE_FILES)
        import io
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = health.main(["--json", "--root", repo])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertIn("score", payload)
        self.assertIn("results", payload)


if __name__ == "__main__":
    unittest.main()
