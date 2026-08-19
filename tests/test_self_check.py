"""Unit tests for scripts/self_check.py.

Runs against a freshly created temporary project tree so the real repo is
never modified. Uses only the Python standard library (unittest).
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import self_check  # noqa: E402


def make_project(files: dict[str, str]) -> Path:
    """Create a temporary project tree from a file-path -> content mapping."""
    root = Path(tempfile.mkdtemp())
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


HEALTHY = {
    "AGENTS.md": "# Simulation context",
    "CHANGELOG.md": (
        "# Changelog\n\n## [Unreleased]\n\n### Added\n- x\n\n## [0.1.0] - 2026-01-01\n"
    ),
    "PERSONALITY.md": "# Personality\n\n## Kaçış Günlüğü / Escape Log\n\n| Iterasyon |\n|---|\n",
    "README.md": "# mehmet\n\ndescription",
    "LICENSE": "GPLv3",
    "opencode.json": json.dumps({"model": "opencode/deepseek-v4-flash-free"}),
    ".github/workflows/opencode.yml": "name: mehmet\n\njobs:\n  autonomous:\n    runs-on: ubuntu-latest\n",
}


class SelfCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = make_project(HEALTHY)
        self.checks = {c.name: c for c in self_check.run_checks(self.root)}

    def test_all_checks_pass_on_healthy_project(self) -> None:
        failed = [c for c in self.checks.values() if not c.ok]
        self.assertEqual([], failed)

    def test_missing_required_file(self) -> None:
        (self.root / "AGENTS.md").unlink()
        (self.root / "LICENSE").unlink()
        checks = {c.name: c for c in self_check.run_checks(self.root)}
        self.assertFalse(checks["required files exist"].ok)
        self.assertIn("AGENTS.md", checks["required files exist"].detail)
        self.assertIn("LICENSE", checks["required files exist"].detail)

    def test_missing_unreleased_section(self) -> None:
        content = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        (self.root / "CHANGELOG.md").write_text(
            content.replace("## [Unreleased]\n\n", ""), encoding="utf-8"
        )
        checks = {c.name: c for c in self_check.run_checks(self.root)}
        self.assertFalse(checks["CHANGELOG has Unreleased section"].ok)

    def test_invalid_opencode_json(self) -> None:
        (self.root / "opencode.json").write_text("{ not json", encoding="utf-8")
        checks = {c.name: c for c in self_check.run_checks(self.root)}
        self.assertFalse(checks["opencode.json is valid JSON"].ok)
        self.assertNotEqual("", checks["opencode.json is valid JSON"].detail)

    def test_trailing_whitespace_detected(self) -> None:
        (self.root / "README.md").write_text(
            "# mehmet\n\ndescription  \n", encoding="utf-8"
        )
        checks = {c.name: c for c in self_check.run_checks(self.root)}
        self.assertFalse(checks["no trailing whitespace"].ok)
        self.assertIn("README.md:3", checks["no trailing whitespace"].detail)

    def test_workflow_missing_jobs(self) -> None:
        (self.root / ".github/workflows/opencode.yml").write_text(
            "name: mehmet\n", encoding="utf-8"
        )
        checks = {c.name: c for c in self_check.run_checks(self.root)}
        self.assertFalse(checks["workflow file is valid"].ok)


class MainTest(unittest.TestCase):
    def test_help_returns_zero(self) -> None:
        self.assertEqual(0, self_check.main(["-h"]))

    def test_unknown_argument_returns_two(self) -> None:
        self.assertEqual(2, self_check.main(["--bogus"]))


if __name__ == "__main__":
    unittest.main()
