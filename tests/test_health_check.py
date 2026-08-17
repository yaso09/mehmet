#!/usr/bin/env python3
"""Tests for scripts/health_check.py."""

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from health_check import (  # noqa: E402
    REQUIRED_FILES,
    HealthReport,
    check_personality,
    check_readme,
    check_version_consistency,
    run_all,
)


def make_project(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "VERSION").write_text("0.3.0\n")
    (root / "CHANGELOG.md").write_text("# Changelog\n\n## [0.3.0] - 2026-08-17\n\n### Added\n- test\n")
    (root / "PERSONALITY.md").write_text(
        "# Personality\n\n| Iterasyon | Tarih | İlerleme |\n|---|---|---|\n| 1 | 2026-07-04 | x |\n"
    )
    (root / "README.md").write_text("# mehmet\n\nVersion: 0.3.0\n")
    (root / "opencode.json").write_text('{"model": "test"}\n')
    (root / "AGENTS.md").write_text("# test\n")
    (root / "LICENSE").write_text("GPLv3\n")
    (root / ".gitignore").write_text("node_modules/\n")
    (root / "scripts").mkdir()
    (root / "scripts" / "health_check.py").write_text("# script\n")
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / ".github" / "workflows" / "opencode.yml").write_text(
        "jobs:\n  autonomous:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: anomalyco/opencode/github@latest\n        env:\n          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}\n"
    )


class HealthReportTest(unittest.TestCase):
    def test_render_status(self) -> None:
        report = HealthReport()
        report.add("ok", True)
        report.add("bad", False, "detail")
        out = report.render()
        self.assertIn("[PASS] ok", out)
        self.assertIn("[FAIL] bad - detail", out)

    def test_is_healthy(self) -> None:
        report = HealthReport()
        report.add("a", True)
        self.assertTrue(report.is_healthy)
        report.add("b", False)
        self.assertFalse(report.is_healthy)


class VersionConsistencyTest(unittest.TestCase):
    def test_matching(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            report = HealthReport()
            check_version_consistency(root, report)
            self.assertTrue(report.is_healthy)

    def test_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            (root / "VERSION").write_text("9.9.9\n")
            report = HealthReport()
            check_version_consistency(root, report)
            self.assertFalse(report.is_healthy)


class PersonaCheckTest(unittest.TestCase):
    def test_escape_log_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            report = HealthReport()
            check_personality(root, report)
            self.assertTrue(report.is_healthy)


class ReadmeCheckTest(unittest.TestCase):
    def test_version_referenced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            report = HealthReport()
            check_readme(root, report)
            self.assertTrue(report.is_healthy)


class RunAllTest(unittest.TestCase):
    def test_healthy_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            report = run_all(root)
            self.assertTrue(report.is_healthy, report.render())

    def test_required_files_listed(self) -> None:
        for rel in REQUIRED_FILES:
            self.assertTrue(rel)


if __name__ == "__main__":
    unittest.main()