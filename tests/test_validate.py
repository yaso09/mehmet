#!/usr/bin/env python3
"""Unit tests for scripts/validate.py using only the standard library."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate as v


class ValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for name in v.REQUIRED_FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        (self.root / ".gitignore").write_text(
            "\n".join(v.GITIGNORE_ENTRIES), encoding="utf-8"
        )
        (self.root / "opencode.json").write_text(
            json.dumps({"model": "opencode/deepseek-v4-flash-free", "enable": True,
                        "autoMerge": False, "toolTimeout": 120000}),
            encoding="utf-8",
        )
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [0.3.0] - 2026-08-15\n\n### Added\n- stuff\n",
            encoding="utf-8",
        )
        (self.root / "PERSONALITY.md").write_text(
            "# Personality\n\n## Traits\n- x\n\n## Kaçış Günlüğü / Escape Log\n\n| row |\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text(
            "# mehmet\n\nRuns via GitHub Actions.\n", encoding="utf-8"
        )
        (self.root / v.MATURITY_DOC).write_text(
            "# Maturity\n\nTrack milestones here.\n", encoding="utf-8"
        )
        (self.root / ".github/workflows/opencode.yml").write_text(
            "name: mehmet\non: {}\njobs: {}\nOPENCODE_API_KEY\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_healthy_repo_passes(self) -> None:
        self.assertEqual(v.validate(self.root), [])

    def test_missing_required_file_fails(self) -> None:
        (self.root / "LICENSE").unlink()
        failures = v.validate(self.root)
        self.assertTrue(any("LICENSE" in f for f in failures))

    def test_bad_opencode_json_fails(self) -> None:
        (self.root / "opencode.json").write_text("{not json", encoding="utf-8")
        failures = v.validate(self.root)
        self.assertTrue(any("not valid JSON" in f for f in failures))

    def test_missing_model_fails(self) -> None:
        (self.root / "opencode.json").write_text(
            json.dumps({"enable": True}), encoding="utf-8"
        )
        failures = v.validate(self.root)
        self.assertTrue(any("model" in f for f in failures))

    def test_changelog_unordered_fails(self) -> None:
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [0.1.0] - 2026-07-04\n\n### Added\n- a\n\n## [0.2.0] - 2026-08-01\n\n### Added\n- b\n",
            encoding="utf-8",
        )
        failures = v.validate(self.root)
        self.assertTrue(any("not ordered" in f for f in failures))

    def test_personality_missing_escape_log_fails(self) -> None:
        (self.root / "PERSONALITY.md").write_text(
            "# Personality\n\n## Traits\n- x\n", encoding="utf-8"
        )
        failures = v.validate(self.root)
        self.assertTrue(any("Kaçış Günlüğü" in f for f in failures))

    def test_missing_maturity_doc_fails(self) -> None:
        (self.root / v.MATURITY_DOC).unlink()
        failures = v.validate(self.root)
        self.assertTrue(any("maturity.md" in f for f in failures))

    def test_main_exit_code(self) -> None:
        self.assertEqual(v.main(["--quiet"]), 0)


if __name__ == "__main__":
    unittest.main()