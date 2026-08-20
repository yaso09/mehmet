#!/usr/bin/env python3
"""healthcheck.py icin birim testler (stdlib unittest, bagimsizlik yok)."""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import healthcheck  # noqa: E402


class HealthcheckTests(unittest.TestCase):
    def test_opencode_json_parse(self):
        content = (ROOT / "opencode.json").read_text(encoding="utf-8")
        cfg = json.loads(content)
        self.assertIn("model", cfg)
        self.assertIn("deepseek", cfg["model"])

    def test_required_files_exist(self):
        for rel in ["AGENTS.md", "CHANGELOG.md", "PERSONALITY.md", "README.md", "LICENSE"]:
            self.assertTrue((ROOT / rel).exists(), f"eksik dosya: {rel}")

    def test_docs_sections(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for section in ["## Kurulum", "## Lisans", "## Özellikler", "## Proje Yapısı"]:
            self.assertIn(section, readme)

    def test_workflow_exists(self):
        self.assertTrue((ROOT / ".github/workflows/opencode.yml").exists())
        self.assertTrue((ROOT / ".github/workflows/validate.yml").exists())

    def test_changelog_semver(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(re.search(r"^## \[\d+\.\d+\.\d+\]", changelog, re.MULTILINE))

    def test_healthcheck_import(self):
        self.assertTrue(hasattr(healthcheck, "main"))
        self.assertTrue(callable(healthcheck.main))

    def test_threshold_defined(self):
        self.assertEqual(healthcheck.THRESHOLD, 80)


if __name__ == "__main__":
    unittest.main(verbosity=2)