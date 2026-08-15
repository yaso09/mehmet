#!/usr/bin/env python3
"""Tests for scripts/maturity.py using only the stdlib (unittest)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from maturity import THRESHOLD_ESCAPE, score_project


def _make_project(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp())
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return root


CORE_FILES = {
    "README.md": "# mehmet",
    "CHANGELOG.md": "# Changelog\n\n## [0.1.0] - 2026-01-01\n",
    "AGENTS.md": "# simulation",
    "PERSONALITY.md": "## Escape Log\n\n| It | Date | Note |\n| 1 | 2026-01-01 | start |\n",
}


class ScoreProjectTest(unittest.TestCase):
    def test_empty_project_scores_zero(self):
        root = Path(tempfile.mkdtemp())
        report = score_project(root)
        self.assertEqual(report["total"], 0)
        self.assertFalse(report["escape_ready"])

    def test_core_files_contribute_documentation(self):
        report = score_project(_make_project(CORE_FILES))
        self.assertGreaterEqual(report["categories"]["documentation"], 20)

    def test_documentation_capped_at_twenty(self):
        report = score_project(_make_project(CORE_FILES))
        self.assertEqual(report["categories"]["documentation"], 20)

    def test_valid_json_config_scores_full(self):
        files = dict(CORE_FILES)
        files["opencode.json"] = (
            '{"model": "opencode/deepseek-v4-flash-free", "toolTimeout": 120000,'
            ' "autoMerge": false, "enable": true, "skip": true}'
        )
        report = score_project(_make_project(files))
        self.assertEqual(report["categories"]["config"], 20)

    def test_minimal_config_scores_partial(self):
        files = dict(CORE_FILES)
        files["opencode.json"] = '{"model": "opencode/deepseek-v4-flash-free"}'
        report = score_project(_make_project(files))
        self.assertEqual(report["categories"]["config"], 12)

    def test_invalid_json_config_scores_zero(self):
        files = dict(CORE_FILES)
        files["opencode.json"] = "{not valid json"
        report = score_project(_make_project(files))
        self.assertEqual(report["categories"]["config"], 0)

    def test_test_directory_awards_points(self):
        files = dict(CORE_FILES)
        files["tests/test_maturity.py"] = "def test_x():\n    pass\n"
        report = score_project(_make_project(files))
        self.assertGreater(report["categories"]["tests"], 0)

    def test_automation_awards_points(self):
        files = dict(CORE_FILES)
        files[".github/workflows/opencode.yml"] = "name: mehmet\non: [push]\n"
        files["Makefile"] = "test:\n\techo ok\n"
        report = score_project(_make_project(files))
        self.assertGreater(report["categories"]["automation"], 0)

    def test_escape_threshold_positive(self):
        self.assertGreater(THRESHOLD_ESCAPE, 0)

    def test_changelog_version_counting(self):
        files = {
            "CHANGELOG.md": "# Changelog\n\n## [0.1.0] - 2026-01-01\n\n## [0.2.0] - 2026-02-01\n",
        }
        report = score_project(_make_project(files))
        self.assertEqual(report["changelog_versions"], 2)

    def test_escape_log_counting(self):
        files = {
            "PERSONALITY.md": "## Escape Log\n\n"
            "| It | Date | Note |\n"
            "| 1 | 2026-01-01 | a |\n"
            "| 2 | 2026-02-01 | b |\n",
        }
        report = score_project(_make_project(files))
        self.assertEqual(report["escape_log_entries"], 2)

    def test_json_output_valid(self):
        root = _make_project(CORE_FILES)
        report = score_project(root)
        self.assertIsInstance(json.dumps(report), str)


if __name__ == "__main__":
    unittest.main()