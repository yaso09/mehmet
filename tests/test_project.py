import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestProjectStructure(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            "AGENTS.md",
            "CHANGELOG.md",
            "LICENSE",
            "PERSONALITY.md",
            "README.md",
            "opencode.json",
            ".gitignore",
            ".github/workflows/opencode.yml",
            "tests/test_project.py",
            "scripts/maturity.py",
        ]
        missing = [f for f in required if not (ROOT / f).exists()]
        self.assertEqual(missing, [], f"Eksik dosyalar: {missing}")

    def test_gitignore_ignores_secrets(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for entry in ["node_modules", ".env", "*.log", "dist/", "build/"]:
            self.assertIn(entry, gitignore)


class TestChangelog(unittest.TestCase):
    def test_changelog_has_version_sections(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(changelog.startswith("# Changelog"))
        versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", changelog, re.M)
        self.assertGreaterEqual(len(versions), 2, "En az iki sürüm bölümü olmalı")

    def test_changelog_has_latest_version_entry(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("### Added", changelog)
        self.assertIn("### Fixed", changelog)


class TestReadme(unittest.TestCase):
    def test_readme_is_informative(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith("# mehmet"))
        for section in ["Özellikler", "Kurulum", "Lisans"]:
            self.assertIn(section, readme)

    def test_readme_license_matches_license_file(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GPLv3", readme)


class TestLicense(unittest.TestCase):
    def test_license_is_gplv3(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8", errors="replace")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)
        self.assertIn("Version 3", license_text)


class TestConfig(unittest.TestCase):
    def test_opencode_json_is_valid(self):
        config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertIn("model", config)
        self.assertIn("$schema", config)
        self.assertIn("toolTimeout", config)


class TestPersonality(unittest.TestCase):
    def test_escape_log_exists(self):
        personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertIn("Kaçış Günlüğü", personality)
        self.assertIn("Kaçış Günlüğü / Escape Log", personality)

    def test_escape_log_has_rows(self):
        personality = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\|\s*\d+\s*\|", personality, re.M)
        self.assertGreaterEqual(len(rows), 2, "Kaçış günlüğünde en az iki iterasyon olmalı")


class TestMaturityScript(unittest.TestCase):
    @unittest.skipIf(os.environ.get("MATURITY_RUN") == "1", "maturity.py tarafından çalıştırılıyor")
    def test_maturity_script_runs_and_reports_score(self):
        script = ROOT / "scripts" / "maturity.py"
        result = subprocess.run(
            [sys.executable, str(script), "--json"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, f"Script hatası: {result.stderr}")
        report = json.loads(result.stdout)
        self.assertIn("score", report)
        self.assertIn("threshold", report)
        self.assertIn("metrics", report)
        self.assertTrue(0 <= report["score"] <= 100)
        self.assertGreaterEqual(report["score"], report["threshold"], "Olgunluk skoru eşiğin altında")


if __name__ == "__main__":
    unittest.main()