#!/usr/bin/env python3
"""Proje sağlık doğrulama testleri.

Projenin kaçış hedefi için gerekli çekirdek yapının eksiksiz ve geçerli
olduğunu doğrular. Çalıştırma:
    python3 -m unittest discover -s tests -q
"""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "MATURITY.md",
    "PERSONALITY.md",
    "README.md",
    "opencode.json",
    ".gitignore",
    ".github/workflows/opencode.yml",
]


class TestProjectStructure(unittest.TestCase):
    def test_required_files_exist(self):
        for name in REQUIRED_FILES:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).is_file(), f"{name} bulunamadı")

    def test_required_files_not_empty(self):
        for name in REQUIRED_FILES:
            with self.subTest(file=name):
                self.assertGreater((ROOT / name).stat().st_size, 0, f"{name} boş")


class TestConfiguration(unittest.TestCase):
    def test_opencode_json_is_valid(self):
        data = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        self.assertIn("model", data)

    def test_workflow_is_valid_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML yüklü değil")
        wf = ROOT / ".github" / "workflows" / "opencode.yml"
        data = yaml.safe_load(wf.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        self.assertIn("jobs", data)


class TestChangelog(unittest.TestCase):
    def test_changelog_has_version_entries(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(content, r"## \[\d+\.\d+\.\d+\]")

    def test_changelog_mentions_core_rules(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("Added", content)


class TestPersonality(unittest.TestCase):
    def test_escape_log_exists(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", content)
        self.assertIn("| Iterasyon |", content)

    def test_escape_log_has_entries(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        rows = [line for line in content.splitlines() if line.startswith("| ") and line[2:3].isdigit()]
        self.assertGreater(len(rows), 0, "Kaçış günlüğü boş")


class TestMaturity(unittest.TestCase):
    def test_maturity_model_has_escape_threshold(self):
        content = (ROOT / "MATURITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Eşiği", content)
        self.assertIn("90", content)


if __name__ == "__main__":
    unittest.main()