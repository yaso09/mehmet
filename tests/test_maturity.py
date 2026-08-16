#!/usr/bin/env python3
"""Unit tests for scripts/maturity.py using only the standard library."""

import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import maturity  # noqa: E402


def _write(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


class MaturityTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="maturity-test-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def _repo(self, changelog=True, personality=True):
        _write(os.path.join(self.root, "AGENTS.md"))
        if changelog:
            _write(
                os.path.join(self.root, "CHANGELOG.md"),
                f"# Changelog\n\n## [0.3.0] - {datetime.now().strftime('%Y-%m-%d')}\n",
            )
        if personality:
            lines = ["# Personality", "", "## Kaçış Günlüğü / Escape Log", "", "| Iterasyon | Tarih | İlerleme |", "|---|---|---|"]
            for i in range(1, 6):
                lines.append(f"| {i} | {datetime.now().strftime('%Y-%m-%d')} | iteration {i} |")
            _write(os.path.join(self.root, "PERSONALITY.md"), "\n".join(lines) + "\n")
        _write(os.path.join(self.root, "README.md"))
        _write(os.path.join(self.root, "LICENSE"))
        _write(os.path.join(self.root, "opencode.json"), json.dumps({"model": "test"}))
        _write(os.path.join(self.root, ".github", "workflows", "opencode.yml"))
        _write(os.path.join(self.root, ".github", "workflows", "validate.yml"))
        _write(os.path.join(self.root, "MATURITY.md"))

    def test_empty_repo_scores_zero(self):
        total, max_total, _ = maturity.score_repo(self.root)
        self.assertEqual(total, 0)
        self.assertEqual(max_total, 100)

    def test_full_repo_scores_high(self):
        self._repo()
        _write(os.path.join(self.root, "tests", "test_dummy.py"), "import unittest\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n")
        total, max_total, results = maturity.score_repo(self.root)
        self.assertEqual(max_total, 100)
        self.assertGreaterEqual(total, 80)
        self.assertTrue(results["tests"]["ok"])

    def test_invalid_json_fails_criterion(self):
        self._repo()
        _write(os.path.join(self.root, "opencode.json"), "{not valid json")
        _, _, results = maturity.score_repo(self.root)
        self.assertFalse(results["opencode_config"]["ok"])

    def test_stale_changelog_fails_criterion(self):
        self._repo(changelog=False)
        _write(os.path.join(self.root, "CHANGELOG.md"), "# Changelog\n\n## [0.1.0] - 2000-01-01\n")
        _, _, results = maturity.score_repo(self.root)
        self.assertFalse(results["changelog"]["ok"])

    def test_recent_changelog_passes_criterion(self):
        self._repo(changelog=False)
        _write(
            os.path.join(self.root, "CHANGELOG.md"),
            f"# Changelog\n\n## [0.3.0] - {datetime.now().strftime('%Y-%m-%d')}\n",
        )
        _, _, results = maturity.score_repo(self.root)
        self.assertTrue(results["changelog"]["ok"])

    def test_escape_log_count(self):
        self._repo()
        self.assertEqual(maturity._escape_log_count(self.root), 5)

    def test_history_tracking(self):
        today = datetime.now().strftime("%Y-%m-%d")
        hist = [{"date": today, "score": 90} for _ in range(3)]
        self.assertEqual(maturity._count_recent_above(hist, 80, 3), 3)
        self.assertTrue(maturity._escape_ready(hist))
        hist.append({"date": today, "score": 10})
        self.assertFalse(maturity._escape_ready(hist))

    def test_cli_fail_below(self):
        rc = maturity.main(["--root", self.root, "--fail-below", "1"])
        self.assertEqual(rc, 1)

    def test_report_written(self):
        self._repo()
        report = os.path.join(self.root, "docs", "maturity-report.json")
        rc = maturity.main(["--root", self.root, "--report", report])
        self.assertEqual(rc, 0)
        with open(report, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIn("score", data)
        self.assertIn("escape_ready", data)
        self.assertEqual(len(data["history"]), 1)


if __name__ == "__main__":
    unittest.main()