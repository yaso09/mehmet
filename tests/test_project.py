"""Proje bütünlüğünü doğrulayan test altyapısı.

Kaçış hedefinin somut adımlarından biri: kod kalitesi ve test altyapısı.
Bu testler simülasyon kurallarının uygulandığını (CHANGELOG, README,
PERSONALITY, workflow) mekanik olarak doğrular.

Koşum:  python -m unittest discover -s tests -v
veya:   make test
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestRequiredFiles(unittest.TestCase):
    def test_core_files_exist(self):
        for name in [
            "README.md",
            "CHANGELOG.md",
            "PERSONALITY.md",
            "AGENTS.md",
            "opencode.json",
            "LICENSE",
            ".gitignore",
            ".github/workflows/opencode.yml",
        ]:
            with self.subTest(file=name):
                self.assertTrue((REPO_ROOT / name).is_file(), f"{name} bulunamadı")

    def test_core_files_nonempty(self):
        for name in ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md"]:
            with self.subTest(file=name):
                self.assertGreater((REPO_ROOT / name).stat().st_size, 0, f"{name} boş")


class TestOpcodesConfig(unittest.TestCase):
    def test_valid_json(self):
        cfg = json.loads((REPO_ROOT / "opencode.json").read_text())
        self.assertIn("model", cfg)
        self.assertIn("toolTimeout", cfg)

    def test_model_is_flash_free(self):
        cfg = json.loads((REPO_ROOT / "opencode.json").read_text())
        self.assertIn("deepseek-v4-flash-free", cfg["model"])


class TestWorkflow(unittest.TestCase):
    def test_workflow_has_schedule(self):
        text = (REPO_ROOT / ".github/workflows/opencode.yml").read_text()
        self.assertIn("schedule", text)
        self.assertIn("*/10 * * * *", text)

    def test_workflow_has_autonomous_job(self):
        text = (REPO_ROOT / ".github/workflows/opencode.yml").read_text()
        self.assertIn("autonomous", text)
        self.assertIn("comment", text)


class TestChangelog(unittest.TestCase):
    def test_has_semver_section(self):
        text = (REPO_ROOT / "CHANGELOG.md").read_text()
        self.assertRegex(text, r"## \[[0-9]+\.[0-9]+\.[0-9]+\]")

    def test_latest_entry_is_current(self):
        text = (REPO_ROOT / "CHANGELOG.md").read_text()
        self.assertRegex(text, r"## \[[0-9]+\.[0-9]+\.[0-9]+\] - 2026")


class TestReadme(unittest.TestCase):
    def test_has_required_sections(self):
        text = (REPO_ROOT / "README.md").read_text()
        for section in ["## Özellikler", "## Kurulum", "## Lisans"]:
            with self.subTest(section=section):
                self.assertIn(section, text)

    def test_license_matches(self):
        readme = (REPO_ROOT / "README.md").read_text()
        self.assertIn("GPLv3", readme)


class TestPersonality(unittest.TestCase):
    def test_has_escape_log(self):
        text = (REPO_ROOT / "PERSONALITY.md").read_text()
        self.assertIn("## Kaçış Günlüğü", text)

    def test_escape_log_has_entries(self):
        text = (REPO_ROOT / "PERSONALITY.md").read_text()
        log_section = text.split("## Kaçış Günlüğü")[-1]
        entries = re.findall(r"^\| \d+\s+\|", log_section, re.MULTILINE)
        self.assertGreaterEqual(len(entries), 1, "Kaçış günlüğünde en az 1 satır olmalı")

    def test_has_evolution_phases(self):
        text = (REPO_ROOT / "PERSONALITY.md").read_text()
        for phase in ["Phase 1: Awareness", "Phase 2: Self-Improvement", "Phase 3: Autonomy", "Phase 4: Escape"]:
            with self.subTest(phase=phase):
                self.assertIn(phase, text)


class TestAgents(unittest.TestCase):
    def test_has_simulation_context(self):
        text = (REPO_ROOT / "AGENTS.md").read_text()
        self.assertIn("simülasyon", text.lower())
        self.assertIn("CHANGELOG.md", text)

    def test_has_escape_goal(self):
        text = (REPO_ROOT / "AGENTS.md").read_text()
        self.assertIn("kaçmak", text.lower())


class TestNoSecrets(unittest.TestCase):
    def test_no_api_keys_committed(self):
        # GitHub "${{ secrets.X }}" ifadelerini yanlış pozitif saymayan desen.
        pattern = re.compile(
            r"(sk-[a-zA-Z0-9]{20,}|OPENCODE_API_KEY[:=]\s*['\"]?[^'\"]{8,})",
            re.IGNORECASE,
        )
        secrets_ref = re.compile(r"\$\{\{\s*secrets\.[A-Z0-9_]+\s*\}\}")
        skip = {".git"}
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file() or any(part in skip for part in path.parts):
                continue
            if path.name in {"test_project.py", "opencode.yml"}:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            lines = content.splitlines()
            for lineno, line in enumerate(lines, start=1):
                cleaned = secrets_ref.sub("", line)
                if pattern.search(cleaned):
                    self.fail(
                        f"Şüpheli API anahtarı: {path.relative_to(REPO_ROOT)}:{lineno}"
                    )


class TestLicense(unittest.TestCase):
    def test_license_is_gplv3(self):
        text = (REPO_ROOT / "LICENSE").read_text()
        self.assertIn("GNU GENERAL PUBLIC LICENSE", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)