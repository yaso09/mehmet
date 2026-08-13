#!/usr/bin/env python3
"""Unit tests for scripts/project_health.py."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import project_health as ph  # noqa: E402


def _write(root: Path, rel: str, content: str = "") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _make_project(root: Path) -> None:
    _write(root, "AGENTS.md", "# Simülasyon")
    _write(root, "README.md", "# mehmet\n\nKendi kendini geliştiren ajan.")
    _write(
        root,
        "PERSONALITY.md",
        "# Personality\n\n## Kaçış Günlüğü\n\n| İterasyon | Tarih | İlerleme |",
    )
    _write(
        root,
        "CHANGELOG.md",
        "## [0.1.0] - " + date.today().isoformat(),
    )
    _write(root, "opencode.json", json.dumps({"model": "test"}))
    _write(root, ".gitignore", "node_modules/\n")
    _write(root, "LICENSE", "GPLv3")
    _write(root, "Makefile", "health:\n\tpython3 scripts/project_health.py\n")
    _write(
        root,
        ".github/workflows/ci.yml",
        "name: ci\non: [push]\njobs:\n  health:\n    run: make health\n",
    )
    _write(root, "scripts/project_health.py", "pass")
    _write(root, "scripts/test_project_health.py", "pass")
    _write(root, "docs/design.md", "# Design doc")


class TestProjectHealth(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_full_project_scores_high(self) -> None:
        _make_project(self.root)
        report = ph.build_report(self.root)
        self.assertGreaterEqual(report["maturity_score"], ph.ESCAPE_THRESHOLD)

    def test_empty_project_scores_low(self) -> None:
        report = ph.build_report(self.root)
        self.assertLess(report["maturity_score"], ph.ESCAPE_THRESHOLD)
        self.assertFalse(report["escape_ready"])

    def test_recent_changelog_required(self) -> None:
        _make_project(self.root)
        _write(self.root, "CHANGELOG.md", "## [0.1.0] - 2000-01-01")
        results = ph._run_checks(self.root)
        self.assertFalse(results["core_docs"][4])

    def test_valid_json_config(self) -> None:
        _make_project(self.root)
        self.assertTrue(ph._valid_json_config(self.root))

        _write(self.root, "opencode.json", "{ not json")
        self.assertFalse(ph._valid_json_config(self.root))

    def test_escape_log_detection(self) -> None:
        _make_project(self.root)
        self.assertTrue(ph._has_escape_log(self.root))

        _write(self.root, "PERSONALITY.md", "# No log here")
        self.assertFalse(ph._has_escape_log(self.root))

    def test_workflow_health_check_detection(self) -> None:
        _make_project(self.root)
        self.assertTrue(ph._workflow_has_health_check(self.root))

        _write(
            self.root,
            ".github/workflows/ci.yml",
            "name: ci\non: [push]\njobs:\n  build:\n    run: true\n",
        )
        self.assertFalse(ph._workflow_has_health_check(self.root))

    def test_stale_todos_detected(self) -> None:
        _make_project(self.root)
        _write(self.root, "README.md", "# mehmet\n\nTODO: finish docs")
        self.assertTrue(ph._has_stale_todos(self.root))

    def test_main_json_output(self) -> None:
        import contextlib
        import io

        _make_project(self.root)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exit_code = ph.main(["--root", str(self.root), "--json"])
        report = json.loads(buf.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertIn("maturity_score", report)
        self.assertIn("categories", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)