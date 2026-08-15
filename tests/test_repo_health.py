"""Repo sağlığı test paketi (yalnızca stdlib bağımlılıkları).

Kullanım:
    python3 -m unittest discover -s tests
"""
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check-maturity.py"


class TestProjectStructure(unittest.TestCase):
    def test_required_root_files_exist(self):
        for name in ("AGENTS.md", "CHANGELOG.md", "LICENSE", "PERSONALITY.md", "README.md", "opencode.json", ".gitignore"):
            self.assertTrue((ROOT / name).exists(), f"eksik: {name}")

    def test_docs_exist(self):
        for name in ("docs/maturity.md", "docs/roadmap.md"):
            self.assertTrue((ROOT / name).exists(), f"eksik: {name}")

    def test_workflows_exist(self):
        for name in ("opencode.yml", "ci.yml"):
            self.assertTrue((ROOT / ".github" / "workflows" / name).exists(), f"eksik workflow: {name}")


class TestConfigValidity(unittest.TestCase):
    def test_opencode_json_is_valid(self):
        with open(ROOT / "opencode.json", encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIn("model", data)

    def test_gitignore_covers_artifacts(self):
        content = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for needle in ("node_modules", ".env", "dist"):
            self.assertIn(needle, content)


class TestChangelog(unittest.TestCase):
    def test_semver_sections(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        versions = re.findall(r"^## \[\d+\.\d+\.\d+\]", content, re.M)
        self.assertGreaterEqual(len(versions), 2, "en az 2 sürüm gerekli")

    def test_latest_version_logged(self):
        content = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("0.3.0", content)


class TestPersonalityEscapeLog(unittest.TestCase):
    def test_escape_log_present(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        self.assertTrue("Kaçış Günlüğü" in content or "Escape Log" in content)

    def test_escape_log_has_rows(self):
        content = (ROOT / "PERSONALITY.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\|\s*\d+\s*\|", content, re.M)
        self.assertGreaterEqual(len(rows), 3, "en az 3 iterasyon satırı gerekli")


class TestReadme(unittest.TestCase):
    def test_key_sections(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        for section in ("## Özellikler", "## Kurulum", "## Geliştirme", "## Lisans"):
            self.assertIn(section, content)

    def test_license_consistent_with_license_file(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        license = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GPL", readme)
        self.assertIn("GPL", license)

    def test_api_key_secret_documented(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("OPENCODE_API_KEY", content)


class TestMaturityScript(unittest.TestCase):
    def test_script_runs(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode in (0, 1), True, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("overall", data)
        self.assertEqual(len(data["dimensions"]), 5)


class TestAgents(unittest.TestCase):
    def test_escape_goal_defined(self):
        content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("kaçış", content.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)