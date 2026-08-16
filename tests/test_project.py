#!/usr/bin/env python3
"""Project structure and integrity tests (stdlib unittest, no external deps)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "README.md",
    "LICENSE",
    ".gitignore",
    "opencode.json",
    ".github/workflows/opencode.yml",
]


class TestRequiredFiles(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")


class TestChangelog(unittest.TestCase):
    def test_has_release_headers(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r"^## \[\d+\.\d+\.\d+\]", text, flags=re.MULTILINE),
            "Expected at least one release header like '## [0.2.0] - YYYY-MM-DD'",
        )

    def test_entries_are_date_ordered_desc(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        dates = re.findall(r"^## \[[^\]]+\] - (\d{4}-\d{2}-\d{2})", text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(dates), 1)
        self.assertEqual(dates, sorted(dates, reverse=True), "Releases must be newest-first")


class TestLicense(unittest.TestCase):
    def test_license_is_gplv3(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", text)
        self.assertIn("Version 3", text)


class TestReadme(unittest.TestCase):
    def test_mentions_gplv3(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GPLv3", text)


class TestOpenCodeConfig(unittest.TestCase):
    def test_valid_json_and_model(self):
        raw = (ROOT / "opencode.json").read_text(encoding="utf-8")
        data = json.loads(raw)
        self.assertIn("model", data)
        self.assertEqual(data["model"], "opencode/deepseek-v4-flash-free")


class TestWorkflow(unittest.TestCase):
    def test_contains_expected_keys(self):
        text = (ROOT / ".github/workflows/opencode.yml").read_text(encoding="utf-8")
        for key in ["on:", "jobs:", "schedule:", "OPENCODE_API_KEY"]:
            self.assertIn(key, text)


class TestMaturityScript(unittest.TestCase):
    def test_runs_and_writes_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/maturity.py"],
                cwd=ROOT,
                env={**dict(__import__("os").environ), "MATURITY_METRICS_OVERRIDE": tmp + "/metrics.json"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("maturity report", proc.stdout)
            self.assertIn("TOTAL", proc.stdout)


class TestPersonalityEscapeLog(unittest.TestCase):
    def test_has_escape_log_table(self):
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü / Escape Log", text)
        self.assertIn("| Iterasyon |", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)