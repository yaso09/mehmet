#!/usr/bin/env python3
"""mehmet proje bütünlüğü testleri.

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import maturity  # noqa: E402


class TestCoreFiles(unittest.TestCase):
    def test_required_files_exist(self):
        for name in ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md", "LICENSE", ".gitignore", "opencode.json"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).exists(), f"{name} yok")

    def test_workflow_exists(self):
        self.assertTrue((ROOT / ".github" / "workflows" / "opencode.yml").exists())

    def test_docs_exist(self):
        self.assertTrue((ROOT / "docs" / "superpowers" / "specs").exists())
        self.assertTrue((ROOT / "docs" / "superpowers" / "plans").exists())


class TestConfig(unittest.TestCase):
    def test_opencode_json_valid(self):
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", data)

    def test_gitignore_blocks_secrets(self):
        content = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", content)
        self.assertIn("node_modules", content)


class TestDocumentation(unittest.TestCase):
    def test_readme_has_key_sections(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for section in ["Kurulum", "Lisans", "Özellikler"]:
            with self.subTest(section=section):
                self.assertIn(section, text)

    def test_changelog_has_version(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"## \[\d+\.\d+\.\d+\]")

    def test_personality_has_escape_log(self):
        text = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", text)
        self.assertIn("|", text)


class TestMaturityScript(unittest.TestCase):
    def test_dimensions_present(self):
        self.assertGreater(len(maturity.dimension_docs()), 0)
        self.assertGreater(len(maturity.dimension_automation()), 0)
        self.assertGreater(len(maturity.dimension_test()), 0)
        self.assertGreater(len(maturity.dimension_meta()), 0)

    def test_score_bounds(self):
        self.assertTrue(maturity.ESCAPE_THRESHOLD > 0)
        self.assertGreaterEqual(maturity.MIN_STREAK, 1)

    def test_no_env_leak(self):
        self.assertFalse((ROOT / ".env").exists(), ".env commit'lenmemeli")

    def test_streak_resets_on_drop(self):
        self.assertEqual(maturity.current_streak([100, 100, 99], 100), 1)

    def test_streak_counts_consecutive(self):
        self.assertEqual(maturity.current_streak([99, 100, 100], 100), 3)

    def test_streak_empty_history(self):
        self.assertEqual(maturity.current_streak([], 100), 1)
        self.assertEqual(maturity.current_streak([], 90), 0)

    def test_streak_matches_min_streak(self):
        history = [maturity.ESCAPE_THRESHOLD] * (maturity.MIN_STREAK - 1)
        self.assertEqual(maturity.current_streak(history, maturity.ESCAPE_THRESHOLD), maturity.MIN_STREAK)


if __name__ == "__main__":
    unittest.main(verbosity=2)